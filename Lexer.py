import enum
import sys

# Token contains the original text and the type of token.
class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText  # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind  # The TokenType that this token is classified as.

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being above 20
            if kind.name == tokenText and kind.value >= 20 and kind.value < 35:
                return kind
        return None


# TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
    # Used to signal the end of file data
    EOF = -1
    # Indicates the end of a line of text
    NEWLINE = 0
    # Used to recognize any number (real_literal and natural_literal)
    NUMS = 1
    # Used for and ID
    IDENT = 2
    # Used for a series of characters
    STRING = 3
    # Keyword that allows for the labeling of an ID to be called by GOTO
    LABEL = 21
    # Keyword the allows for the execution of another line of code instead of the current one
    GOTO = 22
    # Keyword that allows the execution of a string or expression within my language
    PRINT = 23
    # Keyword that allows for a varible to be inserted and checks if it already exists
    INPUT = 24
    # Keyword that allows for a variable to be set as an expression or number
    LET = 25
    # Keyword that initiates an if statement taking in a boolean expression
    IF = 26
    # Keyword that is needed within the if statement for my language to take in a statement right after
    THEN = 27
    # Keyword to end the if statement in my language
    ENDIF = 28
    # Keyword that initiates a while loop taking in a boolean expression
    WHILE = 29
    # Keyword that is needed within the while loop for my language to take in a statement right after
    REPEAT = 30
    # Keyword to end the while loop in my language
    ENDWHILE = 31
    # Operator equal sign: =
    EQL = 41
    # Operator addition sign: +
    ADDI_SGN = 42
    # Operator subtraction sign: -
    SUB_SGN = 43
    # Operator multiplication sign: *
    MULT_SGN = 44
    # Operator division sign: /
    DIV_SGN = 45
    # Operator modulo sign: %
    MOD_OP = 52
    # Operator exponent sign: ^
    EXPONENT = 54
    # Operator equal-to sign: ==
    EQLTO = 46
    # Operator not equal-to sign: !==
    NTEQLTO = 47
    # Operator less than sign: <
    LESTHN = 48
    # Operator less than equal-to sign: <==
    LESEQLTO = 49
    # Operator greater than sign: >
    GRTHN = 50
    # Operator greater than equal-to sign: >==
    GREQLTO = 51
    # The token symbol to represent left parenthesis: (
    L_PAREN = 52
    # The token symbol to represent right parenthesis: )
    R_PAREN = 53
    # The token symbol to represent a left bracket: {
    L_BRAC = 55
    # The token symbol to represent a right bracket: }
    R_BRAC = 56
    # The token symbol to represent a semicolon: ;
    SEMI = 57


class Lexer:
    def __init__(self, input):
        self.source = input + "\n"  # Source code to lex as a string
        self.currentChar = ""  # Gets the current character in the string
        self.currentPos = -1  # Gets the current position in the string
        self.nextChar()

    # Processes the next character
    def nextChar(self):
        self.currentPos += 1
        if self.currentPos >= len(self.source):
            self.currentChar = "\0"  # EOF
        else:
            self.currentChar = self.source[self.currentPos]

    # Returns the lookahead character
    def peek(self):
        if self.currentPos + 1 >= len(self.source):
            return "\0"
        return self.source[self.currentPos + 1]

    # Prints the error messages
    def error(self, message):
        sys.exit("Lexing error. " + message)

    # Skips whitespace except the start of a new line. Indicates the end of a statement
    def skipWhitespace(self):
        while (
            self.currentChar == " "
            or self.currentChar == "\t"
            or self.currentChar == "\r"
        ):
            self.nextChar()

    # Skips single line comments
    def skipComment(self):
        if self.currentChar == "#":
            while self.currentChar != "\n":
                self.nextChar()

    # Gets the next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        if self.currentChar == "+":
            token = Token(self.currentChar, TokenType.ADDI_SGN)
        elif self.currentChar == "-":
            token = Token(self.currentChar, TokenType.SUB_SGN)
        elif self.currentChar == "*":
            token = Token(self.currentChar, TokenType.MULT_SGN)
        elif self.currentChar == "%":
            token = Token(self.currentChar, TokenType.MOD_OP)
        elif self.currentChar == "/":
            token = Token(self.currentChar, TokenType.DIV_SGN)
        elif self.currentChar == "^":
            token = Token(self.currentChar, TokenType.EXPONENT)
        elif self.currentChar == "(":
            token = Token(self.currentChar, TokenType.L_PAREN)
        elif self.currentChar == ")":
            token = Token(self.currentChar, TokenType.R_PAREN)
        elif self.currentChar == "{":
            token = Token(self.currentChar, TokenType.L_BRAC)
        elif self.currentChar == "}":
            token = Token(self.currentChar, TokenType.R_BRAC)
        elif self.currentChar == ";":
            token = Token(self.currentChar, TokenType.SEMI)
        elif self.currentChar == "=":
            # Checks whether it's = or ==
            if self.peek() == "=":
                lastChar = self.currentChar
                self.nextChar()
                token = Token(lastChar + self.currentChar, TokenType.EQLTO)
            else:
                token = Token(self.currentChar, TokenType.EQL)
        elif self.currentChar == ">":
            # Checks whether it's > or >==
            if self.peek() == "=":
                lastChar = self.currentChar
                self.nextChar()
                if self.peek() == "=":
                    lastChar = self.currentChar
                    self.nextChar()
                    token = Token(lastChar + self.currentChar, TokenType.GREQLTO)

            else:
                token = Token(self.currentChar, TokenType.GRTHN)
        elif self.currentChar == "<":
            # Checks whether it's < or <==
            if self.peek() == "=":
                lastChar = self.currentChar
                self.nextChar()
                if self.peek() == "=":
                    lastChar = self.currentChar
                    self.nextChar()
                    token = Token(lastChar + self.currentChar, TokenType.LESEQLTO)
            else:
                token = Token(self.currentChar, TokenType.LESTHN)
        elif self.currentChar == "!":
            # Checks if !==
            if self.peek() == "=":
                lastChar = self.currentChar
                self.nextChar()
                if self.peek() == "=":
                    lastChar = self.currentChar
                    self.nextChar()
                    token = Token(lastChar + self.currentChar, TokenType.NTEQLTO)
            else:
                self.error("Expected !=, got !" + self.peek())
        elif self.currentChar == '"':
            # Get characters between quotations.
            self.nextChar()
            startPos = self.currentPos

            while self.currentChar != '"':
                # Don't allow special characters in the string.
                if (
                    self.currentChar == "\r"
                    or self.currentChar == "\n"
                    or self.currentChar == "\t"
                    or self.currentChar == "\\"
                    or self.currentChar == "%"
                ):
                    self.error("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.currentPos]
            token = Token(tokText, TokenType.STRING)
        elif self.currentChar.isdigit():
            # The first character is a digit so recognizes it as a number
            # Get all digits or decimal numbers
            startPos = self.currentPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == ".":  # Classifies it as a decimal number
                self.nextChar()

                # There must be another digit after the decimal
                if not self.peek().isdigit():
                    self.error("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.currentPos + 1]
            token = Token(tokText, TokenType.NUMS)
        elif self.currentChar.isalpha():
            # The first character is a letter so recognizes it as an ID or keyword
            startPos = self.currentPos
            while self.peek().isalnum():
                self.nextChar()

            # Checks if the token is in the list of keywords
            tokText = self.source[startPos : self.currentPos + 1]
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None:
                token = Token(tokText, TokenType.IDENT)
            else:
                token = Token(tokText, keyword)
        elif self.currentChar == "\n":
            token = Token(self.currentChar, TokenType.NEWLINE)
        elif self.currentChar == "\0":
            token = Token("", TokenType.EOF)
        else:
            # Throws error if the token is not known
            self.error("Unknown token: " + self.currentChar)

        self.nextChar()
        return token
