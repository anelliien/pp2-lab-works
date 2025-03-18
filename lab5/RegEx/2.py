import re
pattern = r'^ab{2,3}$'
string = input("Enter a string: ")
print(bool(re.match(pattern, string)))
