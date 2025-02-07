

def PrimeNum(num):
    num  = int(num)
    if num < 2: 
        return False
    
    if num in (2,3): return True
    if num % 2 == 0: 
        return False
    for i in range(3,num ** 0.5 + 1, 2):
        if num % i == 0:
            return False
    return True

thislist = list(input().split())

for num in thislist:
    if PrimeNum(num):
        print(num, end = " ")