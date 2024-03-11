from math import sqrt, atan2

class PVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def sub(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def mult(self, n):
        self.x *= n
        self.y *= n

    def div(self, n):
        self.x /= n
        self.y /= n

    def mag(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        m = self.mag()
        if m != 0:
            self.div(m)

    def heading(self):
        angle = atan2(self.y, self.x)
        return angle

    def limit(self, max_val):
        magnitude = self.mag()
        if magnitude > max_val:
            self.x = (self.x / magnitude) * max_val
            self.y = (self.y / magnitude) * max_val
