class Shape():
    def __init__(self):
        pass
    def Area(self):
        return 0
class Square(Shape):
    def __init__(self, length):
        Shape.__init__(self)
        self.length = length
    def area(self):
        return self.length * self.length
    
sq = Square(int(input()))
print(sq.area())