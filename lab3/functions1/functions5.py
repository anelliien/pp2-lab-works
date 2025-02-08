from itertools import permutations


def generator(s):
    for ch in permutations(s):
        print("".join(ch))

s = input()
generator(s)