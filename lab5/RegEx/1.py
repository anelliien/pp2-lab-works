import re
pattern = r'^ab*$'
string = input("Enter a string: ")
print(bool(re.match(pattern, string)))
