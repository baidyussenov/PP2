class string():
    def __init__(self):
        self.str = ""

    def getString(self):
        self.str = input()

    def printString(self):
        print(self.str.upper())


A = string()
A.getString()
A.printString()