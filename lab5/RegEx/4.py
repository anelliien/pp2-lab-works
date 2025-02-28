import re
pattern = r'[A-Z][a-z]+'
string = input("Enter a string: ")
print(re.findall(pattern, string))
