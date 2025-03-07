def count_case(s):
    upper_count = sum(1 for char in s if char.isupper())
    lower_count = sum(1 for char in s if char.islower())
    return upper_count, lower_count

text = input("Enter a string: ")
upper, lower = count_case(text)

print("Uppercase letters:", upper)
print("Lowercase letters:", lower)
