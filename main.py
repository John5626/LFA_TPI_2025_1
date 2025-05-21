from src.imports.loadToken import load
from src.Tokens import TokenType, token_literal, token_name, token_defs, Token

def main():
    print("TokenType.LPAREN =", TokenType.LPAREN)
    assert TokenType.LPAREN == token_defs['LPAREN']

    code_lp = token_literal['if']
    print("Código para 'IF' =", code_lp)
    assert code_lp == TokenType.IF

    tok = Token(TokenType.SUM, '+', line=1, column=5)
    print("Token:", tok)
    assert "SUM" in repr(tok) and "'+'" in repr(tok)

if __name__ == "__main__":
    main()