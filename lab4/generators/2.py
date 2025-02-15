def even_num_gen(n):
    for i in range(0,n+1,2):
        yield i
n = int(input("Input a range of nums: "))

print(", ".join(str(x) for x in even_num_gen(n)))