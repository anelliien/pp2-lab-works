file_path = input("Enter the file path: ")
data = input("Enter list elements separated by spaces: ").split()

with open(file_path, 'w') as file:
    for item in data:
        file.write(item + '\n')

print("List written to file successfully.")
