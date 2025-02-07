import random
x = random.randrange(1, 21)
name = input("Hello! What is your name?\n")
print(f"Well, {name}, I am thinking of a number between 1 and 20.")

cnt = 0
num = -1

while num != x:
    num = int(input("\nTake a guess.\n"))
    cnt+=1
    if num < x:
        print("Your guess is too low.")
    elif num > x:
        print("Your guess is too high.")
    
print(f"Good job, KBTU! You guessed my number in {cnt} guesses!")
        
