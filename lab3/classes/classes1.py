class UpperCase:
    def __init__(self):
        self.str=""
    def getString(self):
        self.str = input()
    def printString(self):
        print(self.str.upper())

s = UpperCase()
s.getString()
s.printString()