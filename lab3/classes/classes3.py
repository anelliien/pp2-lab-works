
class Shape:
    def __init__(self):
        pass
    def area(self):
        return 0
    
class Square(Shape):
    def __init__(self, length):
        self.length = int(length)
    def area(self):
        return self.length **2

class Rectangle(Shape):
    
    def __init__(self, length, width):
        self.length = int(length)
        self.width = int(width)
    
    def area(self):
        return self.length * self.width


shape = Shape()
print("Shape area:", shape.area())
length = input("Square length: ")
square = Square(length)
print("Square area:", square.area())

rect_length = input("Length of rectangle: ")
rect_width = input("Width of rectangle: ")
rectangle = Rectangle(rect_length, rect_width)
print("Rectangle area:", rectangle.area())