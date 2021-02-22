import sys

class Lexer:
    def __init__(self, input):
        pass

    # Process the next character.
    def nextChar(self):
        pass

    # Return the lookahead character.
    def peek(self):
        pass

    # Invalid token found, print error message and exit.
    def abort(self, message):
        pass

    # Skip whitespace and newlines.
    def skipWhitespace(self):
        pass

    # Skip comments in the code.
    def skipComment(self):
        pass

    # Return the next token.
    def getToken(self):
        pass