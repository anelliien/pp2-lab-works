import os

path = input("Enter the path: ")

if os.path.exists(path):
    print("Path exists.")
    print("Directory:", os.path.dirname(path))
    print("Filename:", os.path.basename(path))
else:
    print("Path does not exist.")
