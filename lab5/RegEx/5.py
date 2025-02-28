import re
pattern = r'^a.*b$'
string = input("Enter a string: ")
print(bool(re.match(pattern, string)))
