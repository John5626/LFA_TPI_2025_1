# TPI_LFA               Tokens.py
from src.imports.loadToken import load

token_name, token_literal = load('tokens.txt')
token_defs = {}

class TokenType:
    pass

for name, code_val in token_name.items():
    setattr(TokenType, name, code_val)
    ##print(f"TokenType.{name} = {code_val}")
    token_defs[name] = code_val

class Token:
    def __init__(self, type_code, lexeme, line, column):
        self.type = type_code
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        token_name_found = None

        for name, code in token_defs.items():
            if code == self.type:
                token_name_found = name
                break

        if token_name_found is None:
            token_name_found = self.type

        string = (
            f"Token(type={token_name_found}, "
            f"lexeme='{self.lexeme}', "
            f"line={self.line}, "
            f"column={self.column})"
        )

        return string