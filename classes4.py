import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def show(self):
        print(f"Point coordinates: ({self.x}, {self.y})")
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def dist(self, other_x, other_y):
        return math.sqrt((self.x - other_x) ** 2 + (self.y - other_y) ** 2)

x1 = float(input("x-coordinate: "))
y1 = float(input("y-coordinate: "))
point1 = Point(x1, y1)
point1.show()

new_x = float(input("new x-coordinate: "))
new_y = float(input("y-coordinate: "))

distance = point1.dist(new_x, new_y)
print(f"Distance between points: {distance:.2f}")
point1.move(new_x, new_y)
point1.show()
