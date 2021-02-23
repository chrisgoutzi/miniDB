import sys
import enum

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


# Token contains the original text and the type of token.
class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind   # The TokenType that this token is classified as.

    def __str__(self):
        return 'Text: ' + self.text + '\n Kind: ' + str(self.kind) + '\n\n'

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None

# TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
    EOF = -1
    NUMBER = 1
    IDENT = 2
    STRING = 3
    SEMICOLON = 4
    COMMA = 5
    LPARENS = 6
    RPARENS = 7
    DOT = 8
    # Keywords.
    SELECT = 101
    FROM = 102
    WHERE = 103
    UPDATE = 104
    SET = 105
    INSERT = 106
    VALUES = 107
    DROP = 108
    DELETE = 109
    DATABASE = 110
    TABLE = 111
    CREATE = 112
    INT = 113
    TEXT = 114
    INTO = 115
    INDEX = 116
    ON = 117
    PRIMARY = 118
    KEY = 119
    INNER = 120
    JOIN = 121
    # Operators.
    EQ = 201
    ASTERISK = 202
    LT = 203
    GT = 204
