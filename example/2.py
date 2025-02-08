class Person:
    def __init__(self):
        pass

class Student(Person):
    def __init__(self,):
        self.great = "g"
    
    def print(self):
        print(self.great)
student = input()
person = Student(student)
person.print()