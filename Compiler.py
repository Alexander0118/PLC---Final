from Lexer import *
from Parser import *


class Compiler:
    def compiler():
        print("Compiler Output:")

        # Change the text file here!!!
        with open("TestFile.txt") as inputFile:
            input = inputFile.read()

        lexer = Lexer(input)
        parser = Parser(lexer)

        parser.program()  # Starts the parser
        print("Parsing Complete.")

    compiler()
