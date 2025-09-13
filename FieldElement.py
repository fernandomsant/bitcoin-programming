class FieldElement:

    def __init__(self, num, prime):
        if num >= prime or num < 0:
            raise ValueError("The field element should be between 0 and its order minus one, inclusive")
        self.num = num
        self.prime = prime
    
    def __repr__(self):
        return f'FieldElement_{self.prime}({self.num})'
    
    def __eq__(self, other):
        if not isinstance(other, FieldElement):
            return False
        self.check_fields_order(other)
        return self.num == other.num

    def check_fields_order(self, other):
        if not isinstance(other, FieldElement):
            raise ValueError("The operand is not a FieldElement instance")
        if self.prime == other.prime:
            return
        else:
            raise ValueError("Different field order elements")

    def __neg__(self):
        inverse = -1 * self
        return inverse

    def __add__(self, other):
        self.check_fields_order(other)
        num = (self.num + other.num) % self.prime
        return FieldElement(num, self.prime)
    
    def __sub__(self, other):
        self.check_fields_order(other)
        num = (self.num - other.num) % self.prime
        return FieldElement(num, self.prime)
    
    def __mul__(self, other):
        if isinstance(other, FieldElement):
            self.check_fields_order(other)
            num = (self.num * other.num) % self.prime
            return FieldElement(num, self.prime)
        if isinstance(other, int):
            num = (self.num * other) % self.prime
            return FieldElement(num, self.prime)
        raise ValueError('Multiply only by the field elements itself or integers')
    
    def __rmul__(self, other):
        return self.__mul__(FieldElement(other % self.prime, self.prime))
    
    def __truediv__(self, other):
        if isinstance(other, FieldElement):
            self.check_fields_order(other)
            other_inverse = pow(other, (self.prime - 2))
        elif isinstance(other, int):
            other_inverse = pow(other, (self.prime - 2), self.prime)    
        else:
            raise ValueError('Divide only by the field elements itself or integers')
        return (self * other_inverse)
    
    def __rtruediv__(self, other):
        return self.__truediv__(FieldElement(other % self.prime, self.prime))
    
    def __pow__(self, other):
        if not isinstance(other, int):
            raise ValueError('Potentiation only defined on integers set')
        num = pow(self.num, other, self.prime)
        return FieldElement(num, self.prime)