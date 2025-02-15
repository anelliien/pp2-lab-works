import math

def area(n, l):
    if n == 4:
        a = l*l
    else:
        a = n * l * l / 4 * (1/ math.tan(math.pi/n))
    print(f"The area of the polygon is: {a}")

n = int(input("Input number of sides: "))
l = int(input("Input the length of a side: "))
area(n,l)