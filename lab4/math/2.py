import math

def area(h, a, b):
    print(f"Expected Output: {(a+b) / 2 * h:.1f}")

h = float(input("Height: "))
a = float(input("Base, first value: "))
b = float(input("Base, second value: "))

area(h,a,b)