import random
"""
https://realpython.com/python3-object-oriented-programming/
OOP structures a program such that properties and behaviors are bundled into objects
a person with properties (age, gender) and behaviors (walking, talking, breathing)

a class is a user defined structure to hold data. A class is the blueprint, an instance is the object that holds the data
the instance objects are mutable, meaning their attribute values can change
the class defines the instance methods, those methods can only be called from the object that was created from this class

the methods which can be used to configure or customize classes (like __init__ and __str__) are "dunder methods" (as they begin with double _)
"""


def randomNbr():
    rnd = random.randint(1, 99)
    return rnd


class Person:
    # Class attributes: attributes created outside of the init method. every instance get this attribute with same value upon creation
    # also the class attribute value can be changed in the object.
    species = "human"

    # instance attributes: the init method sets the initial values for the object properties.
    # the init method receives the parameters which can be used to set values to the instance attributes
    # when creating an instance, a value for each attribute must be passed on otherwise you get an error
    def __init__(self, name, age):
        self.name = name  # this is an instance attribute, as every object created from this class will have its own value
        self.age = age

    def __str__(self):  # this creates a function used when you print the object
        return (f"{self.name} is a {self.species} and is {self.age} years old")


if __name__ == "__main__":
    print("start")

    benny = Person("benny", randomNbr())
    print("instance attribute age is     : ", benny.age)
    print("instance attribute species is : ", benny.species)

    benny.age = 77  # object instance attribute can be changed
    print(benny)
