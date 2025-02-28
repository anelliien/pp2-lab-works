import re
pattern = r'\b[a-z]+_[a-z]+\b'
string = input("Enter a string: ")
print(re.findall(pattern, string))
