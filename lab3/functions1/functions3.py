def solve(numheads, numlegs):
    rabbits = 1 / 2 * numlegs - numheads
    chickens = numheads - rabbits
    print("Rabbits: " , int(rabbits), "Chickens: ", int(chickens))

numheads = int(input())
numlegs = int(input())
solve(numheads, numlegs)