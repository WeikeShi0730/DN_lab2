#!/usr/bin/python3

"""
Echo Client and Server Classes

T. D. Todd
McMaster University

to create a Client: "python EchoClientServer.py -r client" 
to create a Server: "python EchoClientServer.py -r server" 

or you can import the module into another file, e.g., 
import EchoClientServer

"""

########################################################################

import socket
import argparse
import sys
import getpass
import hashlib

from company import *

########################################################################
# Echo Server class
########################################################################


class Server:

    # Set the server hostname used to define the server socket address
    # binding. Note that 0.0.0.0 or "" serves as INADDR_ANY. i.e.,
    # bind to all local network interface addresses.
    HOSTNAME = "0.0.0.0"

    # Set the server port to bind the listen socket to.
    PORT = 50000

    RECV_BUFFER_SIZE = 1024
    MAX_CONNECTION_BACKLOG = 10

    MSG_ENCODING = "utf-8"

    # Create server socket address. It is a tuple containing
    # address/hostname and port.
    SOCKET_ADDRESS = (HOSTNAME, PORT)

    students_file = "./course_grades_2021.csv"

    def __init__(self):
        self.create_database()
        self.create_listen_socket()
        self.process_connections_forever()

    def create_database(self):
        self.students = Company("some course", Server.students_file)
        self.students_database = self.students.get_database()
        self.students.calculate_averages()

    def create_listen_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Set socket layer socket options. This allows us to reuse
            # the socket without waiting for any timeouts.
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind socket to socket address, i.e., IP address and port.
            self.socket.bind(Server.SOCKET_ADDRESS)

            # Set socket to listen state.
            self.socket.listen(Server.MAX_CONNECTION_BACKLOG)
            print("Listening on port {} ...".format(Server.PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def process_connections_forever(self):
        try:
            while True:
                # Block while waiting for accepting incoming
                # connections. When one is accepted, pass the new
                # (cloned) socket reference to the connection handler
                # function.
                self.connection_handler(self.socket.accept())
        except Exception as msg:
            print(msg)
        except KeyboardInterrupt:
            print()
        finally:
            self.socket.close()
            sys.exit(1)

    def connection_handler(self, client):
        connection, address_port = client
        print("-" * 72)
        print("Connection received from {}.".format(address_port))

        while True:
            try:
                # Receive bytes over the TCP connection. This will block
                # until "at least 1 byte or more" is available.
                recvd_bytes = connection.recv(Server.RECV_BUFFER_SIZE)

                # If recv returns with zero bytes, the other end of the
                # TCP connection has closed (The other end is probably in
                # FIN WAIT 2 and we are in CLOSE WAIT.). If so, close the
                # server end of the connection and get the next client
                # connection.
                if len(recvd_bytes) == 0:
                    print("Closing client connection ... ")
                    connection.close()
                    break

                # Decode the received bytes back into strings. Then output
                # them.
                recvd_str = recvd_bytes.decode(Server.MSG_ENCODING)
                

                if recvd_str.startswith('b'): # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    print("Received ID/password hash", recvd_str, "from client.")
                    msg = self.server_login(recvd_str)
                else:
                    msg = self.students.get_averages(recvd_str)
                    print("Received", recvd_str, "command from client.")

                # Send the received bytes back to the client.
                connection.sendall(str(msg).encode(Server.MSG_ENCODING))
                print("Sent: ", msg, "\n")

            except KeyboardInterrupt:
                print()
                print("Closing client connection ... ")
                connection.close()
                break

    def server_login(self, recvd_str):
        # student_id = int(recvd_str[1])
        # password = recvd_str[2]
        # print(password)
        for id in self.students_database:
            student = self.students_database[id]
            m = hashlib.sha256()
            m.update(str(student.id).encode(Server.MSG_ENCODING))
            m.update(student.pwd.encode(Server.MSG_ENCODING))
            hashed_info = str(m.digest())

            if hashed_info == recvd_str:
                msg = "Correct password, record found.\n" + "Last Name:" + student.last_name + " First Name:" + student.first_name + " Midterm:" + \
                    str(student.mt) + " Lab 1:" + str(student.l1) + " Lab 2:" + str(student.l2) + \
                    " Lab 3:" + str(student.l3) + \
                    " Lab 4:" + str(student.l4)
                return msg
        msg = "Password failure"
        return msg

########################################################################
# Echo Client class
########################################################################


class Client:

    # Set the server hostname to connect to. If the server and client
    # are running on the same machine, we can use the current
    # hostname.
    #    SERVER_HOSTNAME = socket.gethostbyname('localhost')
    SERVER_HOSTNAME = socket.gethostbyname('')
#    SERVER_HOSTNAME = 'localhost'

    RECV_BUFFER_SIZE = 1024

    def __init__(self):
        self.get_socket()
        self.connect_to_server()
        self.send_console_input_forever()

    def get_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connect_to_server(self):
        try:
            # Connect to the server using its socket address tuple.
            self.socket.connect((Client.SERVER_HOSTNAME, Server.PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def get_console_input(self):
        # In this version we keep prompting the user until a non-blank
        # line is entered.
        while True:
            self.input_text = input("Command: ")
            print("Command entered:", self.input_text)

            if self.input_text == Company.GET_MIDTERM_AVG_CMD:
                print("Fetching midterm average...")
            elif self.input_text == Company.GET_LAB_1_AVG_CMD:
                print("Fetching lab 1 average...")
            elif self.input_text == Company.GET_LAB_2_AVG_CMD:
                print("Fetching lab 2 average...")
            elif self.input_text == Company.GET_LAB_3_AVG_CMD:
                print("Fetching lab 3 average...")
            elif self.input_text == Company.GET_LAB_4_AVG_CMD:
                print("Fetching lab 4 average...")
            elif self.input_text == Company.GET_GRADES:
                self.client_login()

            if self.input_text != "":
                break

    def send_console_input_forever(self):
        while True:
            try:
                self.get_console_input()
                self.connection_send()
                self.connection_receive()
            except (KeyboardInterrupt, EOFError):
                print()
                print("Closing server connection ...")
                self.socket.close()
                sys.exit(1)

    def connection_send(self):
        try:
            # Send string objects over the connection. The string must
            # be encoded into bytes objects first.
            self.socket.sendall(self.input_text.encode(Server.MSG_ENCODING))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connection_receive(self):
        try:
            # Receive and print out text. The received bytes objects
            # must be decoded into string objects.
            recvd_bytes = self.socket.recv(Client.RECV_BUFFER_SIZE)

            # recv will block if nothing is available. If we receive
            # zero bytes, the connection has been closed from the
            # other end. In that case, close the connection on this
            # end and exit.
            if len(recvd_bytes) == 0:
                print("Closing server connection ... ")
                self.socket.close()
                sys.exit(1)

            print("Received: ", recvd_bytes.decode(Server.MSG_ENCODING), "\n")

        except Exception as msg:
            print(msg)
            sys.exit(1)

    def client_login(self):
        student_id = input("Student number: ")
        password = getpass.getpass()
        if student_id and password:
            m = hashlib.sha256()
            m.update(student_id.encode(Server.MSG_ENCODING))
            m.update(password.encode(Server.MSG_ENCODING))
            self.input_text = str(m.digest()) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            print("ID number:", student_id, "password:", password, "recerived.")
            print("ID/password hash", self.input_text, "sent to server.")
        return


########################################################################
# Process command line arguments if this module is run directly.
########################################################################
# When the python interpreter runs this module directly (rather than
# importing it into another file) it sets the __name__ variable to a
# value of "__main__". If this file is imported from another module,
# then __name__ will be set to that module's name.
if __name__ == '__main__':
    roles = {'client': Client, 'server': Server}
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--role',
                        choices=roles,
                        help='server or client role',
                        required=True, type=str)

    args = parser.parse_args()
    roles[args.role]()

########################################################################