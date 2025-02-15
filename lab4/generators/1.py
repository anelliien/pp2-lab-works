def square_upto_n(N):
    for x in range(N+1):
        yield x **2

N=int(input("Input a range of nums: "))
gen = square_upto_n(N)
for x in gen:
    print(x)

