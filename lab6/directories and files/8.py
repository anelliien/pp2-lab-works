import os

path = input("Enter the file path to delete: ")

if os.path.exists(path) and os.access(path, os.W_OK):
    os.remove(path)
    print("File deleted successfully.")
else:
    print("File does not exist or cannot be deleted.")
