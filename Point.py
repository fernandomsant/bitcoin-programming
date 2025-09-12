class Point:
    
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y