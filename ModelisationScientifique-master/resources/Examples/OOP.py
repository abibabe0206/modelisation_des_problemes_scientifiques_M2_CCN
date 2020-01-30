#!/usr/bin/python

class Person:

    # Class Attribute
    species = "Homo sapiens sapiens"

    # Initializer / Instance attributes
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    # instance method
    def printname(self):
        print("My name is", self.firstname, self.lastname + ".")


p1 = Person("John", "Doe")
p1.printname() 


class Student(Person):

    def __init__(self, fname, lname, year): #def __init__(self, fname, lname, year):
        #Person.__init__(self, fname, lname)  
        super().__init__(fname, lname)
        self.graduationyear = year

    # instance method
    def welcome(self):
        print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)

# Child classes inherit attributes and
# behaviors from the parent class
s1 = Student("Jim", "Smith", 2020)
print(s1.printname())

# Child classes have specific attributes
# and behaviors as well
s1.welcome()