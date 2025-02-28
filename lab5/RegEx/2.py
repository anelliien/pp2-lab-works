import re
pattern = r'^abb{2,3}$'
string = input("Enter a string: ")
print(bool(re.match(pattern, string)))
