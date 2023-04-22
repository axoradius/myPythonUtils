"""
excercise on classes from https://realpython.com/python3-object-oriented-programming/
basic excercise create 2 instances of the same class
"""


class Car:
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage

    def __str__(self):
        return f"The {self.color} car has {self.mileage} miles."


class ElectricCar(Car):
    noise = "no noise"

    def __str__(self):
        return f"The {self.color} car with {self.mileage} miles makes {self.noise}"


class SportsCar(Car):
    noise = "high noise"

    def __str__(self):
        return f"The {self.color} car with {self.mileage} miles makes {self.noise}"


if __name__ == "__main__":
    bmw = SportsCar("white", 130000)
    mercedes = ElectricCar("blue", 15000)

    for car in (bmw, mercedes):
        print(car)