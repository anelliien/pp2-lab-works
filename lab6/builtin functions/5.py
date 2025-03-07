def all_true(t):
    return all(t)

tup = tuple(map(int, input("Enter tuple elements separated by spaces (0 for False, 1 for True): ").split()))

print(all_true(tup))
