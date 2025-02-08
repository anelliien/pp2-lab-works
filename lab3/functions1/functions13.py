import random
x = random.randrange(1, 21)

name = input("Hello! What is your name?\n")
print(f"Well, {name}, I am thinking of a number between 1 and 20.")
cnt =1
def rightInput(x,cnt):
    num = int(input("Take a guess.\n"))
    if num != x:
        if num < x:
            print("Your guess is too low.")
            return rightInput(x,cnt+1)
        elif num > x:
            print("Your guess is too high.")
            return rightInput(x,cnt+1)
    else:
        print(f"Good job, KBTU! You guessed my number in {cnt} guesses!")

rightInput(x,cnt)
