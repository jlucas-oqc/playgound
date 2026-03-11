from dataclasses import dataclass

@dataclass
class Vehicle:
    make: str
    year: int

@dataclass
class Car(Vehicle):
    colour: str

def demo_type_checking(value):
    match value:
        case list():
            return "list"
        case Vehicle():
            return "Vehicle"
    return "Unknown type"

if __name__ == "__main__":
    print(demo_type_checking([1, 2, 3]))  # Output: "list"
    print(demo_type_checking(Vehicle(make="Toyota", year=2020)))  # Output: "Vehicle"
    print(demo_type_checking(Car(make="Ford", year=2022, colour="blue")))  # Output: "Vehicle"
    print(demo_type_checking("Hello"))  # Output: "Unknown type"