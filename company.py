""" This module is for creating company class
This company class include an employees dictionary that include person object
from database file

"""
##############################################################################

from person import *

##############################################################################


class Company:

    GET_MIDTERM_AVG_CMD = "GMA"
    GET_LAB_1_AVG_CMD = "GL1A"
    GET_LAB_2_AVG_CMD = "GL2A"
    GET_LAB_3_AVG_CMD = "GL3A"
    GET_LAB_4_AVG_CMD = "GL4A"
    GET_GRADES = "GG"

    def __init__(self, name, employee_database_file):
        """

        :param name: company name
        :param employee_database_file: employee database
        """

        # company name
        self.name = name

        # set database file variable
        self.employee_database_file = employee_database_file

        # create an empty dic of employee
        self.employees = {}

        # read database file
        self.import_employee_database()

    def import_employee_database(self):
        """
        Read the employee database, clean each record, parse them and create the employee dic

        :return: none
        """

        # read the database and clean whitespace from rach record
        self.read_and_clean_database_record()

        # read each line and parse the employee id_no, first name, and last name
        self.parse_employee_records()

        # create employee dic
        self.create_employee_dic()

    def read_and_clean_database_record(self):
        """
        read and clean database
        :return: none
        """
        try:
            file = open(self.employee_database_file, 'r')
            lines = file.readlines()[1:-1]
            print("Data read from CSV file:", self.employee_database_file)
            print(
                "ID Number,Password,Last Name,First Name,Midterm,Lab 1,Lab 2,Lab 3,Lab 4")
        except FileNotFoundError:
            print(f"Creating databased {self.employee_database_file}")
            file = open(self.employee_database_file, 'w+')

        self.cleaned_records = [cleaned_line for cleaned_line in [
            line.strip() for line in lines] if cleaned_line != '']

        for cleaned_line in self.cleaned_records:
            print(cleaned_line)

        file.close()

    def parse_employee_records(self):
        """
        split each line into employee if, first name, and last name
        :return: none
        """
        try:
            self.employee_list = [(int(element[0].strip()), element[1].strip(), element[2].strip(), element[3].strip(), float(element[4].strip()), float(element[5].strip(
            )), float(element[6].strip()), float(element[7].strip()), float(element[8].strip())) for element in [line.split(',') for line in self.cleaned_records]]
        except Exception:
            print("Invalid input file")
            exit()

    def create_employee_dic(self):
        """
        add everyone into the company list
        :return:none
        """

        for employee in self.employee_list:
            try:
                id_number, pwd, lname, fname, mt, l1, l2, l3, l4 = employee

                new_person = Person(
                    id=id_number, pwd=pwd, last_name=lname, first_name=fname, mt=mt, l1=l1, l2=l2, l3=l3, l4=l4)

                self.employees[id_number] = new_person

            except Exception:
                print("name is not fully specified")

    def print_employees(self):
        for id, p in self.employees.items():
            print(f"id:{id} first name: {p.first_name} last name: {p.last_name}")
        print()

    def get_database(self):
        return self.employees

    def calculate_averages(self):
        MA = L1A = L2A = L3A = L4A = 0
        for person_id in self.employees:
            person = self.employees[person_id]
            MA += person.mt
            L1A += person.l1
            L2A += person.l2
            L3A += person.l3
            L4A += person.l4
        total_count = len(self.employees)
        self.averages = {"MA": MA/total_count, "L1A": L1A/total_count,
                         "L2A": L2A/total_count, "L3A": L3A/total_count, "L4A": L4A/total_count}
        return

    def get_averages(self, string):
        try:
            if string == Company.GET_MIDTERM_AVG_CMD:
                return self.averages["MA"]
            elif string == Company.GET_LAB_1_AVG_CMD:
                return self.averages["L1A"]
            elif string == Company.GET_LAB_2_AVG_CMD:
                return self.averages["L2A"]
            elif string == Company.GET_LAB_3_AVG_CMD:
                return self.averages["L3A"]
            elif string == Company.GET_LAB_4_AVG_CMD:
                return self.averages["L4A"]
        except Exception:
            print("command not found")

    def login(self):
        return
        # if __name__ == "__main__":
        #     company_name = "good"

        #     employee_file = "./course_grades_2021.csv"

        #     company = Company(company_name, employee_file)

        #     company.print_employees()
