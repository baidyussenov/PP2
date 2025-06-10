class Rectangle():
    def __init__(self, length, width):
        self.length = length
        self.width = width
    def area(self):
        return self.length * self.width

length = int(input())
width = int(input())
Area = Rectangle(length, width)
print(Area.area())