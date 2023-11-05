import os
import math
from datetime import datetime
from file import *
from maths import *
from sys import *
from mem import *

class Interpreter:
    def __init__(self) -> None:
        self.variables = {}
        self.back_res = None
        self.break_loop = None
        self.file_module = False
        self.math_module = False
        self.sys_module = False
        self.mem_module = False
        self.file_info = None
        self.file_status = False
        self.file_name = ""

    def execute(self, code):
        try:
            lines = code.split('\n')
            for line in lines:
                self.execute_line(line)
        except Exception as err:
            print(err)

    def evaluate_condition(self, comp_type, variable1, variable2):
        if comp_type == "equal":
            result = self.variables.get(variable1, None) == self.variables.get(variable2, None)
        elif comp_type == "not_equal":
            result = self.variables.get(variable1, None) != self.variables.get(variable2, None)
        elif comp_type == "less":
            result = self.variables.get(variable1, None) < self.variables.get(variable2, None)
        elif comp_type == "more":
            result = self.variables.get(variable1, None) > self.variables.get(variable2, None)
        elif comp_type == "eless":
            result = self.variables.get(variable1, None) <= self.variables.get(variable2, None)
        elif comp_type == "emore":
            result = self.variables.get(variable1, None) >= self.variables.get(variable2, None)
        else:
            print(f"Unknown comparison type: {comp_type}")
            exit()
        return result
    
    def execute_line(self, line):
        tokens = line.split()
        if tokens:
            command = tokens[0]
            if command == "<<#":
                if (self.back_res == True or self.back_res == None) and (self.break_loop == None or self.break_loop == True):
                    typed = tokens[2]
                    variable_name = tokens[1]
                    if typed != "int" and typed != "string" and typed != "float" and typed != "bool":
                        self.variables[variable_name] = tokens[2]
                    else:
                        if tokens[3] == "[":
                            operand1 = None
                            operand2 = None
                            
                            if typed == "int":
                                operand1 = int(self.variables[tokens[4]])
                                operand2 = int(self.variables[tokens[6]])

                            elif typed == "string":
                                operand1 = self.variables.get(tokens[4], str(tokens[4]))
                                operand2 = self.variables.get(tokens[5], str(tokens[5]))
                            elif typed == "float":
                                operand1 = self.variables.get(tokens[4], float(tokens[4]))
                                operand2 = self.variables.get(tokens[5], float(tokens[5]))
                            elif typed == "bool":
                                operand1 = self.variables.get(tokens[4], bool(tokens[4]))
                                operand2 = self.variables.get(tokens[5], bool(tokens[5]))
                            
                            result = 'NaN'
                            if tokens[5] == '+':
                                result = operand1 + operand2
                            elif tokens[5] == '-':
                                result = operand1 - operand2
                            elif tokens[5] == '*':
                                result = operand1 * operand2
                            elif tokens[5] == '/':
                                result = operand1 / operand2
                            self.variables[variable_name] = result
                        else:
                            if typed == "int":
                                self.variables[variable_name] = int(tokens[3])
                            elif typed == "string":
                                self.variables[variable_name] = str(tokens[3])
                            elif typed == "float":
                                self.variables[variable_name] = float(tokens[3])
                            elif typed == "bool":
                                self.variables[variable_name] = bool(tokens[3])
            elif command == ":.":
                self.break_loop = None  
            elif command == "fi":
                if self.file_module:
                    with open(f"{self.file_name}", "r") as file:
                        self.file_info = file.readline()
                    print(self.file_info)
                else:
                    print("Error! The File module is not connected or connected with an error!")  
                    exit()    
            elif command == "savefi":
                if self.file_module:
                    self.variables[tokens[1]] = self.file_info
                else:
                    print("Error! The File module is not connected or connected with an error!")  
                    exit()    
            elif command in ["open", "read", "write", "awrite"]:
                if self.file_module:
                    if command == "open":
                        self.file_status = True
                    if self.file_status:
                        lst = list()
                        for i in range(len(tokens)):
                            try:
                                lst.append(self.variables[tokens[i]]) 
                            except:
                                lst.append(tokens[i])
                        try:
                            if self.file_name == "" or self.file_name == None:
                                self.file_name = tokens[1]
                        except:
                            if self.file_name == "" or self.file_name == None:
                                self.file_name = ""    

                        file = File(command, lst, str(self.file_name))
                        temp = file.run()
                        if temp != None:
                            self.file_info = temp
                    else:
                        print("Error! You forgot to open the stream files!")
                        exit()
                else:
                    print("Error! The File module is not connected or connected with an error!")  
                    exit()
            elif command in ["sin", "cos", "tan", "ctg", "arctan", "arcctg", "pi", "integral", "double_integral", "factorial", "log", "exp", "hypot", "round"]:
                if self.math_module:
                    lst = list()
                    for i in range(len(tokens)):
                        try:
                            lst.append(self.variables[tokens[i]]) 
                        except:
                            lst.append(tokens[i])
                        
                    math = Math(command, lst)
                    temp = math.run()
                    if temp != None:
                        print(temp)
                else:
                    print("Error! The Math module is not connected or connected with an error!")  
                    exit()
            elif command == "/connect/":
                if tokens[1] == "?":
                    if tokens[2] == "FILE":
                        print("connect module FILE")
                        self.file_module = True
                    elif tokens[2] == "MATH":
                        print("connect module MATH")
                        self.math_module = True
                    elif tokens[2] == "SYSTEM":
                        print("connect module SYSTEM")
                        self.sys_module = True
                    elif tokens[2] == "MEMORY":
                        print("connect module MEMORY")
                        self.mem_module = True
                    else:
                        print("connect error! this module is undefined.")
                        exit()
                else:
                    print("error! module failed..")
                    exit()
            elif command == ".:":
                self.break_loop = True                 
            elif command == "::":
                self.back_res = None
            elif command == "#>>":
                if (self.back_res == True or self.back_res == None) and (self.break_loop == None or self.break_loop == True):
                    variable_name = tokens[1]
                    value = self.variables.get(variable_name, None)
                    if value is not None:
                        print(f"{value}")
                    else:
                        result = ""
                        for i in range(1, len(tokens)):
                            result += tokens[i] + " "
                        print(f"{result}")

            elif command == "typed":
                if (self.back_res == True or self.back_res == None) and (self.break_loop == None or self.break_loop == True):
                    variable_name = tokens[1]
                    value = self.variables.get(variable_name, None)
                    if value is not None:
                        if type(value) == int:
                            print("int")
                        elif type(value) == str:
                            print(f"string")
                        elif type(value) == float:
                            print(f"float")
                        elif type(value) == bool:
                            print(f"bool")
                    else:
                        print("error type variable")
            elif command == "formed":
                if (self.back_res == True or self.back_res == None) and (self.break_loop == None or self.break_loop == True):
                    variable_name = tokens[1]
                    typed = tokens[2]
                    value = self.variables.get(variable_name, None)
                    if value is not None:
                        if typed == "string":
                            self.variables[variable_name] = str(value)
                        elif typed == "float":
                            self.variables[variable_name] = float(value)
                        elif typed == "bool":
                            self.variables[variable_name] = bool(value)
                        elif typed == "int":
                            self.variables[variable_name] = int(value)
                        else:
                            self.variables[variable_name] = None
            
            elif command == 'loop':
                comp_type = tokens[1][5:]
                variable1 = tokens[2]
                variable2 = tokens[3]
                while self.evaluate_condition(comp_type, variable1, variable2):
                    pass

            elif command == 'max':   
                lst = []
                for i in range(2, len(tokens)):  
                    x = self.variables.get(tokens[i], None)
                    if x is None:
                        x = tokens[i]
                    lst.append(x)
                self.variables[tokens[1]] = max(lst)
            elif command == 'gcd':   
                lst = []
                for i in range(2, len(tokens)):  
                    x = self.variables.get(tokens[i], None)
                    if x is None:
                        x = tokens[i]
                    lst.append(x)
                gcd_result = math.gcd(int(lst[0]), int(lst[1]))
                for num in lst[2:]:
                    gcd_result = math.gcd(int(gcd_result), int(num))
                self.variables[tokens[1]] = gcd_result
            elif command == 'lcm':   
                lst = []
                for i in range(2, len(tokens)):  
                    x = self.variables.get(tokens[i], None)
                    if x is None:
                        x = tokens[i]
                    lst.append(x)
                lcm_result = int(lst[0])
                for num in lst[1:]:
                    lcm_result = int(lcm_result) * int(num) // math.gcd(int(lcm_result), int(num))
                self.variables[tokens[1]] = lcm_result
            elif command == 'sqrt':
                self.variables[tokens[1]] = math.sqrt(float(tokens[2]))
            elif command == 'date':
                current_date = datetime.now().strftime("%Y-%m-%d")
                print(f"Date now: {current_date}")

            elif command == 'x10x2':
                variable_name = tokens[1]
                a = self.variables.get(variable_name, None)
                if a is not None:
                    res = format(int(a), 'b')
                    self.variables[variable_name] = res
                else:
                    print("variable is NaN or another problem")
            elif command == 'x10x8':
                variable_name = tokens[1]
                a = self.variables.get(variable_name, None)
                if a is not None:
                    res = format(int(a), 'o')
                    self.variables[variable_name] = res
                else:
                    print("variable is NaN or another problem")
            elif command == 'x10x16':
                variable_name = tokens[1]
                a = self.variables.get(variable_name, None)
                if a is not None:
                    res = format(int(a), 'x')
                    self.variables[variable_name] = res
                else:
                    print("variable is NaN or another problem")
            elif command == 'x2x10':
                variable_name = tokens[1]
                a = self.variables.get(variable_name, None)
                if a is not None:
                    try:
                        res = int(str(a), 16)  # Assuming a is a hexadecimal string
                        self.variables[variable_name] = res
                    except ValueError:
                        print("Invalid hexadecimal string.")
                else:
                    print("Variable is NaN or another problem")

            elif command == 'x2x8':
                variable_name = tokens[1]
                a = self.variables.get(variable_name, None)
                if a is not None:
                    try:
                        res10 = int(str(a), 2)  # Assuming a is a binary string
                        res = format(res10, 'o')
                        self.variables[variable_name] = res
                    except ValueError:
                        print("Invalid binary string.")
                else:
                    print("Variable is NaN or another problem")

            elif command == 'x2x16':
                variable_name = tokens[1]
                a = self.variables.get(variable_name, None)
                if a is not None:
                    try:
                        res10 = int(str(a), 2)  # Assuming a is a binary string
                        res = format(res10, 'x')
                        self.variables[variable_name] = res
                    except ValueError:
                        print("Invalid binary string.")
                else:
                    print("Variable is NaN or another problem")

            elif command == 'time':
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"Time now: {current_time}")
            # Предполагаем, что self.variables - это словарь переменных
            elif command.startswith("del"):
                variable_name = tokens[1]
                try:
                    del self.variables[variable_name]
                    print(f"Variable {variable_name} is deleted.")
                except KeyError:
                    print(f"Variable {variable_name} is not exist.")

            elif command == 'pow':
                self.variables[tokens[1]] = math.pow(float(tokens[2]), float(tokens[3]))

            elif command == 'abs':
                self.variables[tokens[1]] = abs(float(tokens[2]))    
            elif command == 'min':   
                lst = []
                for i in range(2, len(tokens)):  
                    x = self.variables.get(tokens[i], None)
                    if x is None:
                        x = tokens[i]
                    lst.append(x)
                self.variables[tokens[1]] = min(lst)    

            elif command.startswith("comp_"):
                comp_type = command[5:]
                variable1 = tokens[1]
                variable2 = tokens[2]

                if comp_type == "equal":
                    result = self.variables.get(variable1, None) == self.variables.get(variable2, None)
                elif comp_type == "not_equal":
                    result = self.variables.get(variable1, None) != self.variables.get(variable2, None)
                elif comp_type == "less":
                    result = self.variables.get(variable1, None) < self.variables.get(variable2, None)
                elif comp_type == "more":
                    result = self.variables.get(variable1, None) > self.variables.get(variable2, None)
                elif comp_type == "eless":
                    result = self.variables.get(variable1, None) <= self.variables.get(variable2, None)
                elif comp_type == "emore":
                    result = self.variables.get(variable1, None) >= self.variables.get(variable2, None)
                else:
                    print(f"Unknown comparison type: {comp_type}")
                    return
                self.back_res = result
            else:
                print(f"Unknown command: {command}")


interpreter = Interpreter()

with open("py_lang/code.av", "r") as file:
    code = file.read()

interpreter.execute(code)

