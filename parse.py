# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer):
        pass

    # Return true if the current token matches.
    def checkToken(self, kind):
        pass

    # Return true if the next token matches.
    def checkPeek(self, kind):
        pass

    # Try to match current token. If not, error.
    def match(self, kind):
        pass

    # Advances the current token.
    def nextToken(self):
        pass

    def abort(self, message):
        pass
    
    def program(self):
        pass

    def query(self):
        # Check the first token to see what kind of query this is.
        pass
    
    # Require one semicolon to end a query.
    def semicolon(self):
        pass
    
    # Identifier + Comparison Operator + Number
    def comparison(self):
        pass

    def isComparisonOperator(self):
        pass

    # Identifier + Equals + Identifier
    def condition(self):
        pass