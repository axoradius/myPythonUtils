import random
"""
https://realpython.com/python3-object-oriented-programming/

inheritance of class, by including another class

First pass on the parent class parameters, then the child class parameters

"""

def randomNbr():
    rnd = random.randint(1, 99)
    return rnd


class Person:
    species = "person"

    def __init__(self, name, age):
        self.name = name  # this is an instance attribute, as every object created from this class will have its own value
        self.age = age

    def __str__(self):  # this creates a function used when you print the object
        return f"{self.name} is a {self.species} and is {self.age} years old"


class Adult(Person):
    agecategory = "adult"
    def __init__(self, name, age, job):
        super().__init__(name, age) # super() looks up the method from the parent class.
        self.profession = job

    def __str__(self):  # this creates a function used when you print the object
        return f"{self.name} is a {self.agecategory}, is {self.age} years old and has {self.profession} as a job"


class Child(Adult):
    agecategory = "child"
    def __int__(self, name, age, school):
        Person.__init__(name, age)
        self.grade = school

    def __str__(self):
        return f"{self.name} is a {self.agecategory}, is {self.age} years old and is in {self.profession} grade studies"


if __name__ == "__main__":
    print("start")
    #heidi = Adult("heidi", 53, "auditor")
    benny = Adult("benny", 52, "ITconsultant")
    print(benny)
    mariska = Child("Mariska", 21, "university")
    print(mariska)
    #for p in (mariska):
    #    print(p)

