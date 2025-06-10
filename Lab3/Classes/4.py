class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        return self.x, self.y

    def move(self, delta_a, delta_b):
        self.x += delta_a
        self.y += delta_b
        return self.x, self.y

    def dist(self, x1, y1):
        dx = self.x - x1
        dy = self.y - y1
        s = (dx ** 2 + dy ** 2)
        return s ** 0.5


x = int(input())
y = int(input())
p = Point(x, y)
print(p.show())
print(p.move(int(input()), int(input())))
print(p.dist(int(input()), int(input())))
