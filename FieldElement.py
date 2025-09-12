class FieldElement:

    def __init__(self, num, prime):
        if num >= prime or num < 0:
            raise ValueError("The field element should be between 0 and its order minus one, inclusive")
        self.num = num
        self.prime = prime
    
    def __repr__(self):
        return f'FieldElement_{self.prime}({self.num})'
    
    def __eq__(self, other):
        self.check_fields_order(other)
        return self.num == other.num

    def check_fields_order(self, other):
        if not isinstance(other, FieldElement):
            raise ValueError("The operand is not a FieldElement instance")
        if self.prime == other.prime:
            return
        else:
            raise ValueError("Different field order elements")

    def __add__(self, other):
        self.check_fields_order(other)
        num = (self.num + other.num) % self.prime
        return FieldElement(num, self.prime)
    
    def __sub__(self, other):
        self.check_fields_order(other)
        num = (self.num - other.num) % self.prime
        return FieldElement(num, self.prime)
    
    def __mul__(self, other):
        self.check_fields_order(other)
        num = (self.num * other.num) % self.prime
        return FieldElement(num, self.prime)
    
    def __truediv__(self, other):
        self.check_fields_order(other)
        other_num_inverse = other.num ** (self.prime - 2)
        num = (self.num * other_num_inverse) % self.prime
        return FieldElement(num, self.prime)