import sys

class Lexer:
    def __init__(self, input):
        self.source = input
        self.curChar = ''   # Current character in the string.
        self.curPos = -1    # Current position in the string.
        self.nextChar()

    # Process the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'    # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        sys.exit("Lexing error. " + message)

    # Skip whitespace and newlines.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r' or self.curChar == '\n':
            self.nextChar()

    # Skip comments in the code.
    def skipComment(self):
        if self.curChar == '-':
            if self.peek() == '-':
                while self.curChar != '\n':
                    self.nextChar()

    # Return the next token.
    def getToken(self):
        pass