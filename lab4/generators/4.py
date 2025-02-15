def square_nums(a,b):
    for x in range(a, b+1):
        yield x**2

a = int(input("Start: "))
b = int(input("End: "))
print(", ".join(str(x) for x in square_nums(a,b)))