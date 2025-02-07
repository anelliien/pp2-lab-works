import math

def findVolume(r):
    volume = float(4/3 * math.pi * r * r*r)
    print(volume)

r = int(input())
findVolume(r)