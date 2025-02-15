import math

def degree_to_radian(d):
    return math.radians(d)

a = float(input("Input degree: "))

print(f"Output radian: {degree_to_radian(a):.6f}")