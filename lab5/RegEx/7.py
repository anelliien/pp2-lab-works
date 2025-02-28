import re
def snake_to_camel(snake_str):
    words = snake_str.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])
snake_str = input("Enter a snake_case string: ")
print(snake_to_camel(snake_str))
