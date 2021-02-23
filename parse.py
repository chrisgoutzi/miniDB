import sys
from lex import *
from database import Database

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.

        self.db = None

    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # Try to match current token. If not, error.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected" + kind.name +
                       ", got " + self.curToken.kind.name)
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error. " + message)
    
    def program(self):
        # Parse all the queries in the program.
        while not self.checkToken(TokenType.EOF):
            self.query()

    def query(self):
        # Check the first token to see what kind of query this is.
        if self.checkToken(TokenType.SELECT):
            # self.setUp()
            self.nextToken()

            if self.checkToken(TokenType.ASTERISK):
                table_name = None
                self.nextToken()
                self.match(TokenType.FROM)

                if self.checkToken(TokenType.IDENT):
                    table_name = self.curToken.text
                    self.nextToken()

                if self.checkToken(TokenType.SEMICOLON):
                    self.nextToken()
                    # SELECT * FROM table_name;
                    # TODO(chris): Call the right miniDB function.
                    self.db.select(table_name, '*')

                elif self.checkToken(TokenType.WHERE):
                    self.nextToken()
                    comparisonTokens = self.comparison()
                    comparison = ""
                    for i in range(len(comparisonTokens)):
                        comparison += comparisonTokens[i].text
                    self.match(TokenType.SEMICOLON)

                    # SELECT * FROM table_name WHERE comparison;
                    # TODO(chris): Call the right miniDB function.
                    self.db.select(table_name, '*', comparison)

                elif self.checkToken(TokenType.INNER):
                    self.nextToken()
                    self.match(TokenType.JOIN)
                    other_table_name = None

                    if self.checkToken(TokenType.IDENT):
                        other_table_name = self.curToken.text
                        self.nextToken()

                    self.match(TokenType.ON)
                    conditionTokens = self.condition()
                    condition = ""
                    for i in range(len(conditionTokens)):
                        condition += conditionTokens[i].text
                    self.match(TokenType.SEMICOLON)
                    print(condition)

                    # SELECT * FROM table_name INNER JOIN other_table_name ON condition;
                    # TODO(chris): Call the right miniDB function.
                    self.db.inner_join(table_name, other_table_name, condition)

            elif self.checkToken(TokenType.IDENT):
                
                columns = []
                table_name = None
                columns.append(self.curToken.text)

                self.nextToken()
                

                while not self.checkToken(TokenType.FROM):
                    if self.checkToken(TokenType.IDENT):
                        columns.append(self.curToken.text)
                        self.nextToken()
                    elif self.checkToken(TokenType.COMMA):
                        self.nextToken()
                    else:
                        self.abort("Error with SELECT statement. Expected asterisk or column names.")
                
                self.nextToken()
                if self.checkToken(TokenType.IDENT):
                    table_name = self.curToken.text
                    self.nextToken()
                
                if self.checkToken(TokenType.SEMICOLON):
                    self.nextToken()
                    # SELECT building_name FROM classroom;
                    # OR
                    # SELECT building_name, capacity FROM classroom;
                    # TODO(chris): Link the right miniDB function.
                    self.db.select(table_name, columns)

                elif self.checkToken(TokenType.WHERE):
                    self.nextToken()

                    comparisonTokens = self.comparison()
                    comparison = ""
                    for i in range(len(comparisonTokens)):
                        comparison += comparisonTokens[i].text

                    self.semicolon()

                    # SELECT building_name FROM classroom WHERE capacity < 60;
                    # OR
                    # SELECT building_name, capacity FROM classroom capacity < 60;
                    # TODO(chris): Link the right miniDB function.
                    self.db.select(table_name, columns, comparison)

                elif self.checkToken(TokenType.INNER):
                    other_table_name = None

                    self.nextToken()
                    self.match(TokenType.JOIN)
                    if self.checkToken(TokenType.IDENT):
                        other_table_name = self.curToken.text
                        self.nextToken()

                    self.match(TokenType.ON)
                    conditionTokens = self.condition()
                    condition = ""
                    for i in range(len(conditionTokens)):
                        condition += conditionTokens[i].text
                    
                    if self.checkToken(TokenType.SEMICOLON):
                        self.semicolon()
                        self.db.inner_join(table_name, other_table_name, condition, return_object=True)._select_where(columns)
                    elif self.checkToken(TokenType.WHERE):
                        self.nextToken()
                        comparisonTokens = self.comparison()
                        comparison = ""
                        for i in range(len(comparisonTokens)):
                            comparison += comparisonTokens[i].text
                        self.semicolon()
                        print(columns)
                        self.db.inner_join(table_name, other_table_name, condition, return_object=True)._select_where(columns, comparison)
                        

                    self.semicolon()
                    self.db.inner_join(table_name, other_table_name, condition, return_object=True)._select_where(columns)

        elif self.checkToken(TokenType.CREATE):
            self.match(TokenType.CREATE)

            if self.checkToken(TokenType.TABLE):
                self.match(TokenType.TABLE)

                table_name = None
                keys = []
                values = []
                primaryKey = None
                if self.checkToken(TokenType.IDENT):
                    table_name = self.curToken.text

                self.nextToken()
                self.match(TokenType.LPARENS)
                while not self.checkToken(TokenType.RPARENS):
                    columnNameToken = None
                    columnTypeToken = None
                    if self.checkToken(TokenType.IDENT):
                        columnNameToken = self.curToken
                        self.match(TokenType.IDENT)

                        # NOTE(chris): checkToken() is case-sensitive.
                        # So INT works, but int doesn't.
                        if self.checkToken(TokenType.INT):
                            keys.append(columnNameToken.text)
                            values.append(int)
                            self.match(TokenType.INT)
                        elif self.checkToken(TokenType.TEXT):
                            keys.append(columnNameToken.text)
                            values.append(str)
                            self.match(TokenType.TEXT)
                        else:
                            self.abort("Error")
                    elif self.checkToken(TokenType.COMMA):
                        self.nextToken()
                    elif self.checkToken(TokenType.PRIMARY):
                        self.nextToken()
                        self.match(TokenType.KEY)
                        self.match(TokenType.LPARENS)
                        primaryKey = self.curToken.text
                        self.match(TokenType.IDENT)
                        self.match(TokenType.RPARENS)

                self.match(TokenType.RPARENS)
                self.semicolon()
                self.db.create_table(table_name, keys, values, primaryKey)

            elif self.checkToken(TokenType.DATABASE):
                self.match(TokenType.DATABASE)
                database_name = None
                if self.checkToken(TokenType.IDENT):
                    database_name = self.curToken.text
                self.match(TokenType.IDENT)
                self.semicolon()
                self.db = Database(database_name, load=False)
            elif self.checkToken(TokenType.INDEX):
                index_name = None
                table_name = None

                self.match(TokenType.INDEX)
                index_name = self.curToken.text
                self.match(TokenType.IDENT)

                self.match(TokenType.ON)

                table_name = self.curToken.text
                self.match(TokenType.IDENT)

                self.semicolon()
                self.db.create_index(table_name, index_name)

        elif self.checkToken(TokenType.INSERT):
            # Insert statement
            self.match(TokenType.INSERT)
            self.match(TokenType.INTO)

            table_name = None
            values = []

            if self.checkToken(TokenType.IDENT):
                table_name = self.curToken.text
                self.nextToken()
            else:
                self.abort("Error. Expected table name")

            self.match(TokenType.VALUES)

            self.match(TokenType.LPARENS)

            while not self.checkToken(TokenType.RPARENS):
                if self.checkToken(TokenType.STRING):
                    values.append(self.curToken.text)
                    self.nextToken()
                elif self.checkToken(TokenType.NUMBER):
                    values.append(int(self.curToken.text))
                    self.nextToken()
                elif self.checkToken(TokenType.COMMA):
                    self.nextToken()
            self.match(TokenType.RPARENS)
            self.semicolon()
            self.db.insert(table_name, values)

        elif self.checkToken(TokenType.DROP):
            self.nextToken()

            if self.checkToken(TokenType.TABLE):
                table_name = None
                self.nextToken()
                if self.checkToken(TokenType.IDENT):
                    table_name = self.curToken.text
                self.semicolon()
                self.abort("Table to drop is: " + table_name)
                self.db.drop_table(table_name)

            elif self.checkToken(TokenType.DATABASE):
                database_name = None
                self.nextToken()
                if self.checkToken(TokenType.IDENT):
                    database_name = self.curToken.text
                self.semicolon()
                self.abort("Database to drop is: " + database_name)
                self.db.drop_db()

            elif self.checkToken(TokenType.INDEX):
                pass
        elif self.checkToken(TokenType.UPDATE):
            # Update statement
            table_name = None
            column = None
            value = None
            self.nextToken()
            if self.checkToken(TokenType.IDENT):
                table_name = self.curToken.text
                self.nextToken()

            self.match(TokenType.SET)

            if self.checkToken(TokenType.IDENT):
                column = self.curToken.text
                self.nextToken()

            self.match(TokenType.EQ)

            if self.checkToken(TokenType.NUMBER) or self.checkToken(TokenType.STRING):
                value = self.curToken.text
                self.nextToken()

            self.match(TokenType.WHERE)
            comparisonTokens = self.comparison()
            comparison = ""
            for i in range(len(comparisonTokens)):
                comparison += comparisonTokens[i].text

            self.semicolon()
            self.db.update(table_name, value, column, comparison)
        elif self.checkToken(TokenType.DELETE):
            self.nextToken()
            self.match(TokenType.FROM)

            table_name = None

            if self.checkToken(TokenType.IDENT):
                table_name = self.curToken.text
                self.nextToken()

            self.match(TokenType.WHERE)

            comparisonTokens = self.comparison()
            comparison = ""
            for i in range(len(comparisonTokens)):
                comparison += comparisonTokens[i].text

            self.semicolon()
            self.db.delete(table_name, comparison)
    
    # Require one semicolon to end a query.
    def semicolon(self):
        self.match(TokenType.SEMICOLON)
    
    # Identifier + Comparison Operator + Number or String
    def comparison(self):
        ident = None
        operator = None
        value = None

        if self.checkToken(TokenType.IDENT):
            ident = self.curToken
            self.nextToken()

        if self.isComparisonOperator():
            operator = self.curToken
            self.nextToken()

        if self.checkToken(TokenType.NUMBER):
            value = self.curToken
            self.nextToken()
        elif self.checkToken(TokenType.STRING):
            value = self.curToken
            self.nextToken()

        return [ident, operator, value]

    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.EQ)

    # Identifier + Equals + Identifier
    def condition(self):
        # Identifier + Equals + Identifier
        ident = None
        operator = None
        other_ident = None

        if self.checkToken(TokenType.IDENT):
            ident = self.curToken
            self.nextToken()

        if self.checkToken(TokenType.EQ):
            operator = self.curToken
            operator.text = "=="
            self.nextToken()

        if self.checkToken(TokenType.IDENT):
            other_ident = self.curToken
            self.nextToken()

        return [ident, operator, other_ident]