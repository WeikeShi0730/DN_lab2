"""a module for creating person class"""

class Person:
    def __init__(self, id, pwd, last_name, first_name, mt, l1, l2, l3, l4):
        """

        :param first_name: fist name
        :param last_name:  last name
        """
        
        self.id = id
        self.pwd = pwd
        self.last_name = last_name
        self.first_name=first_name
        self.mt = mt
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.l4 = l4
        

    def full_name(self):
        """

        :return: full name of the person
        """

        return self.first_name + " " + self.last_name