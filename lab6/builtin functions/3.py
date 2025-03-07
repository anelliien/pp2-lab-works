def is_palindrome(s):
    cleaned = ''.join(filter(str.isalnum, s)).lower() 
    return cleaned == cleaned[::-1]

text = input("Enter a string: ")
if is_palindrome(text):
    print("The string is a palindrome.")
else:
    print("The string is not a palindrome.")
