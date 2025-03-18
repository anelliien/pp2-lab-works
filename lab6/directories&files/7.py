source = input("Enter the source file path: ")
destination = input("Enter the destination file path: ")

with open(source, 'r') as src, open(destination, 'w') as dest:
    dest.write(src.read())

print("File copied successfully.")
