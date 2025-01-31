print(6 & 3)
"""
The & operator compares each bit and set it to 1 if both are 1, otherwise it is set to 0:
"""

print(3 << 2)
"""
The << operator inserts the specified number of 0's (in this case 2) from the right and let the same amount of leftmost bits fall off:

If you push 00 in from the left:
 3 = 0000000000000011
becomes
12 = 0000000000001100
"""