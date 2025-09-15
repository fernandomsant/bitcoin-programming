class Point:
    
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b

        if x != None and y != None and (y**2 != x**3 + a*x + b):
            raise ValueError('The point does not correspond the equation')
        return
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def check_equation(self, other):
        if not isinstance(other, Point):
            raise ValueError('The operand is not a Point instance')
        if (self.a == other.a and self.b == other.b):
            return
        else:
            raise ValueError('The points does not correspond the equations')

    def __neg__(self):
        inverse = self.__class__(self.x, -self.y, self.a, self.b)
        return inverse

    def __add__(self, other):
        self.check_equation(other)
        x1, x2, y1, y2 = self.x, other.x, self.y, other.y
        if x1 == None:
            return other
        if x2 == None:
            return self
        if x1 == x2 and y1 != y2:
            return self.__class__(None, None, self.a, self.b)
        if self == other:
            s = (3 * (x1**2) + self.a) / (2 * y1)
            x3 = s**2 - 2 * x1
            y3 = -(s * (x3 - x1) + y1)
            return self.__class__(x3, y3, self.a, self.b)
        s = (y2 - y1) / (x2 - x1)
        x3 = s**2 - x1 - x2
        y3 = -(s * (x3 - x1) + y1)
        return self.__class__(x3, y3, self.a, self.b)
    
    def __sub__(self, other):
        self.check_equation(other)
        return self + (-other)
    
    def __rmul__(self, other):
        if not isinstance(other, int) and other > 0:
            raise ValueError('The factor must be an integer greater than zero')
        result = self.__class__(None, None, self.a, self.b)
        p = self.__class__(self.x, self.y, self.a, self.b)
        while other > 0:
            if other & 1:
                result += p
            p += p
            other >>= 1
        return result