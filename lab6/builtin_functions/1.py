import math

def multiply_list(numbers):
    return math.prod(numbers)

nums = list(map(int, input("Enter numbers separated by spaces: ").split()))
result = multiply_list(nums)

print("Product of the list:", result)
