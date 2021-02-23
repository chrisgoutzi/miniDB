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
        self.skipComment()
        self.skipWhitespace()

        token = None

        # Check the first character of this token to see if we can decide what it is.
        # If it is a multiple character operator (e.g, >=), number, identifier, or keyword then we will process the rest.
        if self.curChar == '*':
            token =  Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '\n':
            token = Token (self.curChar, TokenType.NEWLINE)
        elif self.curChar == ';':
            token = Token(self.curChar, TokenType.SEMICOLON)
        elif self.curChar == '.':
            token = Token(self.curChar, TokenType.DOT)
        elif self.curChar == '(':
            token = Token(self.curChar, TokenType.LPARENS)
        elif self.curChar == ')':
            token = Token(self.curChar, TokenType.RPARENS)
        elif self.curChar == ',':
            token =  Token(self.curChar, TokenType.COMMA)
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)
        elif self.curChar == '>':
            token = Token('>', TokenType.GT)
        elif self.curChar == '<':
            token = Token('<', TokenType.LT)
        elif self.curChar == '=':
            token = Token('=', TokenType.EQ)
        # Detect if it's a string.
        elif self.curChar == '\'':
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\'':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos]  # Get the substring.
            token = Token(tokText, TokenType.STRING)
        # Detect if it's a number.
        elif self.curChar.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':  # Decimal!
                self.nextChar()

                # Must have at least one digit after decimal.
                if not self.peek().isdigit():
                    # Error!
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alpha numeric characters.
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            # Check if the token is in the list of keywords.
            tokText = self.source[startPos : self.curPos + 1]  # Get the substring.
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None:  # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:   # Keyword
                token = Token(tokText, keyword)
        else:
            # Unknown token!
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token


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
    NEWLINE = 9
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
