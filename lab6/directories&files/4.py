file_path = input("Enter the file path: ")

with open(file_path, 'r') as file:
    line_count = sum(1 for line in file)

print("Number of lines:", line_count)
