def toCentigrade(F):
    return (5 / 9) * (F - 32)

F = float(input())
C = toCentigrade(F)
print(C)