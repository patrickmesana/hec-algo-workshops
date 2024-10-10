#%%

def addition(a, b):
    return a + b


def subtraction(a, b):
    return a - b




#%%

class Calculator:
    
        def addition(self, a, b):
            return a + b
    
        

calc = Calculator()
print(calc.addition(2, 3))


#%%

class Calculator:
    
        @staticmethod
        def addition(a, b):
            return a + b
    
        

print(Calculator.addition(2, 3))

# %%


class Number:
    def __init__(self, value):
        """Initialize with a value"""
        self.value = value

    def add(self, other):
        """Add another Number object"""
        if isinstance(other, Number):
            return Number(self.value + other.value)
        else:
            raise TypeError("Operand must be of type Number")
        

    def __str__(self):
        return str(self.value)
    

n1 = Number(2)
n2 = Number(3)
n3 = n1.add(n2)
print(n3)
        

#%% 



class Number:
    def __init__(self, value):
        """Initialize with a value"""
        self.value = value

    def __add__(self, other):
        """Add another Number object"""
        if isinstance(other, Number):
            return Number(self.value + other.value)
        else:
            raise TypeError("Operand must be of type Number")
        

    def __str__(self):
        return str(self.value)
    

n1 = Number(2)
n2 = Number(3)
n3 = n1 + n2
print(n3)
# %%


class Number:
    def __init__(self, value):
        """Initialize with a value"""
        self.value = value

    def __add__(self, other):
        """Add another Number object"""
        if isinstance(other, Number):
            return Number(self.value + other.value)
        else:
            raise TypeError("Operand must be of type Number")
        

    def __str__(self):
        return str(self.value)
    

n1 = Number(2)
n2 = Number(3)
n3 = n1 + n2
print(n3)


#%%

from abc import ABC, abstractmethod

class Number(ABC):
    def __init__(self, value):
        """Initialize with a value"""
        self.value = value

    @abstractmethod
    def __add__(self, other):
        """Overload the + operator for Number objects"""
        pass

    @abstractmethod
    def __sub__(self, other):
        """Overload the - operator for Number objects"""
        pass

    @abstractmethod
    def __mul__(self, other):
        """Overload the * operator for Number objects"""
        pass

    @abstractmethod
    def __truediv__(self, other):
        """Overload the / operator for Number objects"""
        pass

    def __str__(self):
        """String representation of the Number object"""
        return str(self.value)
    

class IntegerNumber(Number):
    def __init__(self, value):
        """Initialize with an integer value"""
        if not isinstance(value, int):
            raise TypeError("Value must be of type int")
        super().__init__(value)

    def __add__(self, other):
        """Overload the + operator for IntegerNumber objects"""
        if isinstance(other, IntegerNumber):
            return IntegerNumber(self.value + other.value)
        else:
            raise TypeError("Operand must be of type IntegerNumber")

    def __sub__(self, other):
        """Overload the - operator for IntegerNumber objects"""
        if isinstance(other, IntegerNumber):
            return IntegerNumber(self.value - other.value)
        else:
            raise TypeError("Operand must be of type IntegerNumber")

    def __mul__(self, other):
        """Overload the * operator for IntegerNumber objects"""
        if isinstance(other, IntegerNumber):
            return IntegerNumber(self.value * other.value)
        else:
            raise TypeError("Operand must be of type IntegerNumber")

    def __truediv__(self, other):
        """Overload the / operator for IntegerNumber objects, with zero division check"""
        if isinstance(other, IntegerNumber):
            if other.value == 0:
                raise ValueError("Cannot divide by zero")
            return IntegerNumber(self.value // other.value)  # Integer division for integers
        else:
            raise TypeError("Operand must be of type IntegerNumber")

    def __str__(self):
        """String representation of the IntegerNumber"""
        return str(self.value)