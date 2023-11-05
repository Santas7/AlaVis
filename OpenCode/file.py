import math
import sympy

class File:
    def __init__(self, command, tokens, filename) -> None:
        self.command = command
        self.tokens = tokens
        self.file_name = filename

    def run(self):
        try:
            if self.command == "open":
                return True
            elif self.command == "read":
                try:
                    with open(f"{self.file_name}", "r") as file:
                        res = file.readline()
                    return res
                except:
                    print("Error! No file is opened for reading.")
                    exit()
            elif self.command == "write":
                try:
                    with open(f"{self.file_name}", "w") as file:
                        file.write(str(self.tokens[1]))
                    return None
                except:
                    print("Error! No file is opened for writing.")
                    exit()
            elif self.command == "awrite":
                try:
                    with open(f"{self.file_name}", "a") as file:
                        file.write(str(self.tokens[1]))
                    return None
                except:
                    print("Error! No file is opened for writing.")
                    exit()
            else:
                print("Error! Command in FILE module is undefined!")
                exit()
        except:
            print("Error! (FILE module) - Invalid syntax!")
            return