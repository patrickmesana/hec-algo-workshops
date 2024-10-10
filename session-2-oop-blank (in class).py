#%%

def addition(a, b):
    return a + b

addition(1, 2)

# %%

class Calculator:
    @staticmethod
    def addition(a, b):
        return a + b
    @staticmethod
    def substraction(a, b):
        return a - b
    
calc = Calculator()
calc.addition(1, 2)
# %%
calc.substraction(2, 1)