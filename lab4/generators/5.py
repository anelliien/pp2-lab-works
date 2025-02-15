def decreasing_nums(n):
    for x in range(n, -1, -1):
        yield x
        
n = int(input("Enter a number: "))
print(", ".join(str(x) for x in decreasing_nums(n)))