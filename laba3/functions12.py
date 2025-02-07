def histogram(thislist):
    for x in thislist:
        x = int(x)
        print("*"*x)

thislist = input().split()
histogram(thislist)