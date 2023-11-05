import math
import sympy

class Math:
    def __init__(self, command, tokens) -> None:
        self.command = command
        self.tokens = tokens

    def run(self):
        try:
            if self.command == "sin":
                return math.sin(self.tokens[1])
            elif self.command == "cos":
                return math.cos(self.tokens[1])
            elif self.command == "tan":
                return math.tan(self.tokens[1])
            elif self.command == "ctg":
                return 1 / math.tan(self.tokens[1])
            elif self.command == "arctan":
                return math.atan(self.tokens[1])
            elif self.command == "arcctg":
                return math.pi/2 - math.atan(self.tokens[1])
            elif self.command == "pi":
                return math.pi
            elif self.command == "integral":
                x = sympy.symbols('x')
                expression = self.tokens[1] 
                integral = sympy.integrate(expression, x)
                return integral
            elif self.command == "double_integral":
                x, y = sympy.symbols('x y')
                expression = self.tokens[0]  
                double_integral = sympy.integrate(expression, (x, self.tokens[1], self.tokens[2]), (y, self.tokens[3], self.tokens[4]))
                return integral
            elif self.command == "factorial":
                if self.tokens[1] < 0:
                    print("Error! Factorial is undefined for negative numbers.")
                    exit()
                result = 1
                for i in range(1, self.tokens[1] + 1):
                    result *= i
                return result
            elif self.command == "log":
                if self.tokens[1] <= 0:
                    print("Error! Logarithm is undefined for non-positive numbers.")
                    exit()
                return math.log(self.tokens[1], self.tokens[2])
            elif self.command == "exp":
                return math.exp(self.tokens[1])
            elif self.command == "hypot":
                return math.hypot(self.tokens[1], self.tokens[2])
            elif self.command == "round":
                return round(self.tokens[1])
            else:
                print("Error! Command in MATH module is undefined!")
                exit()
        except:
            print("Error! (MATH module) - Invalid syntax!")
            return