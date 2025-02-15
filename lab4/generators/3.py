def is_divisible(n):
    for x in range(0,n+1,12):
        yield x

n = int(input("Input a range of nums: "))
print(", ".join(str(x) for x in is_divisible(n)))