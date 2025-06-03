"""
Autômato Finito Determinístico (AFD) para análise léxica.
ENTRADAS:
    * Letras: A-Z, a-z
    * Dígitos: 0-9
    * Símbolos: (, ), {, }, [, ], ;, ,, +, -, *, %, /, =, >, <, !, &, |, espaço em branco
SAÍDAS:
    * Identificadores (VAR)
    * Números inteiros (NUM_INT)
    * Números de ponto flutuante (NUM_FLOAT)
    * Palavras-chave (IF, INTDEF, FLOATDEF, CHAR_TYPE, BOOL_TYPE, RETURN)
    * Símbolos de pontuação e operadores (LPAREN, RPAREN, LCHAVE, RCHAVE, LCOLCHETE, RCOLCHETE, PVIRGULA, VIRGULA, SUM, SUB, MULT, DIV, RESTO, EQ, ATRIBUICAO, GEQ, LEQ, GT, LT, NEG, DIF, AND, OR)

Observações:
    * Palavras‑reservadas são tratadas fora do AFD.
    * Estados de um só caractere (LPAREN, RBRACE etc.) aceitam imediatamente.
"""

from src.Tokens import TokenType

class AFD:
    LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    DIGITOS  = '0123456789'

    def __init__(self):
        self.STATE_Q0 = 0
        self.STATE_KW = 1           # ident / keyword (VAR)
        self.STATE_INT  = 2
        self.STATE_FLOAT = 3
        self.STATE_WS = 4
        self.STATE_DIV_START = 5    # leu '/'
        self.STATE_COMMENT = 6      # // ... até \n
        self.STATE_GT_START = 7     # leu '>'
        self.STATE_LT_START = 8     # leu '<'
        self.STATE_EQ_START = 9     # leu '='
        self.STATE_NEG_START = 10   # leu '!'
        self.STATE_AND_START = 11   # leu '&'
        self.STATE_OR_START = 12    # leu '|'

        self.ACCEPT_MAP = {
            'ACCEPT_LPAREN' : TokenType.LPAREN,
            'ACCEPT_RPAREN' : TokenType.RPAREN,
            'ACCEPT_LBRACE' : TokenType.LCHAVE,
            'ACCEPT_RBRACE' : TokenType.RCHAVE,
            'ACCEPT_LBRACKET' : TokenType.LCOLCHETE,
            'ACCEPT_RBRACKET' : TokenType.RCOLCHETE,
            'ACCEPT_SEMICOLON': TokenType.PVIRGULA,
            'ACCEPT_COMMA' : TokenType.VIRGULA,

            'ACCEPT_EQ' : TokenType.EQ,
            'ACCEPT_ASSIGN' : TokenType.ATRIBUICAO,
            'ACCEPT_GEQ' : TokenType.GEQ,
            'ACCEPT_LEQ' : TokenType.LEQ,
            'ACCEPT_GT'  : TokenType.GT,
            'ACCEPT_LT'  : TokenType.LT,
            'ACCEPT_NEG' : TokenType.NEG,
            'ACCEPT_DIF' : TokenType.DIF,
            'ACCEPT_AND' : TokenType.AND,
            'ACCEPT_OR'  : TokenType.OR,

            'ACCEPT_SUM' : TokenType.SUM,
            'ACCEPT_SUB' : TokenType.SUB,
            'ACCEPT_MULT' : TokenType.MULT,
            'ACCEPT_DIV' : TokenType.DIV,
            'ACCEPT_RESTO' : TokenType.RESTO,

            'ACCEPT_NUM_INT' : TokenType.NUM_INT,
            'ACCEPT_NUM_FLOAT' : TokenType.NUM_FLOAT,
            'ACCEPT_VAR' : TokenType.VAR,

            'ACCEPT_IF' : TokenType.IF,
            'ACCEPT_INTDEF' : TokenType.INTDEF,
            'ACCEPT_FLOATDEF' : TokenType.FLOATDEF,
            'ACCEPT_CHAR_TYPE' : TokenType.CHAR_TYPE,
            'ACCEPT_BOOL_TYPE' : TokenType.BOLL_TYPE,
            'ACCEPT_RETURN' : TokenType.RETURN,

            'ACCEPT_WS' : TokenType.WHITESPACE,
            'ACCEPT_COMMENT' : TokenType.COMMENT
        }

        self.state = self.STATE_Q0 # estado inicial


    def processa(self, ch):
        """Processa um caractere e devolve próximo passo."""

        if self.state == self.STATE_Q0:
            if ch is None:           # EOF
                return None

            if ch.isspace():         # espaço / tab / \n
                return self.STATE_WS

            if self.is_letter(ch):  # identificador / keyword
                return self.STATE_KW

            if self.is_digit(ch):   # número inteiro
                return self.STATE_INT

            if ch == ';':
                return 'ACCEPT_SEMICOLON'

            one_char_tokens = {
                '(': 'ACCEPT_LPAREN',
                ')': 'ACCEPT_RPAREN',
                '{': 'ACCEPT_LBRACE',
                '}': 'ACCEPT_RBRACE',
                '[': 'ACCEPT_LBRACKET',
                ']': 'ACCEPT_RBRACKET',
                ',': 'ACCEPT_COMMA',
                '+': 'ACCEPT_SUM',
                '-': 'ACCEPT_SUB',
                '*': 'ACCEPT_MULT',
                '%': 'ACCEPT_RESTO',
            }

            if ch in one_char_tokens:
                return one_char_tokens[ch]

            if ch == '/':
                return self.STATE_DIV_START

            if ch == '=':
                return self.STATE_EQ_START

            if ch == '>':
                return self.STATE_GT_START

            if ch == '<':
                return self.STATE_LT_START

            if ch == '!':
                return self.STATE_NEG_START

            if ch == '&':
                return self.STATE_AND_START

            if ch == '|':
                return self.STATE_OR_START

            return 'ERROR_UNKNOWN_CHAR'

        elif self.state == self.STATE_KW:
            if ch is not None and (self.is_letter(ch) or self.is_digit(ch)):
                return self.STATE_KW
            return 'ACCEPT_VAR'

        elif self.state == self.STATE_INT:
            if ch is not None and self.is_digit(ch):
                return self.STATE_INT
            if ch == '.':
                return self.STATE_FLOAT
            return 'ACCEPT_NUM_INT'

        elif self.state == self.STATE_FLOAT:
            if ch is not None and self.is_digit(ch):
                return self.STATE_FLOAT
            return 'ACCEPT_NUM_FLOAT'

        elif self.state == self.STATE_WS:
            if ch is not None and ch.isspace():
                return self.STATE_WS
            return 'ACCEPT_WS'

        elif self.state == self.STATE_DIV_START:
            if ch == '/':
                return self.STATE_COMMENT

            if ch == '*':
                return 'ACCEPT_DIV'   # não consome '*', lexer irá reler

            return 'ACCEPT_DIV'

        elif self.state == self.STATE_COMMENT:
            if ch is None or ch == '\n':
                return 'ACCEPT_WS'    # descarta como ws
            return STATE_COMMENT

        elif self.state == self.STATE_EQ_START:
            if ch == '=':
                return 'ACCEPT_EQ'
            return 'ACCEPT_ASSIGN'

        elif self.state == self.STATE_GT_START:
            if ch == '=':
                return 'ACCEPT_GEQ'
            return 'ACCEPT_GT'

        elif self.state == self.STATE_LT_START:
            if ch == '=':
                return 'ACCEPT_LEQ'
            return 'ACCEPT_LT'

        elif self.state == self.STATE_NEG_START:
            if ch == '=':
                return 'ACCEPT_DIF'
            return 'ACCEPT_NEG'

        elif self.state == self.STATE_AND_START:
            if ch == '&':
                return 'ACCEPT_AND'
            return 'ERROR_EXPECTED_AND'

        elif self.state == self.STATE_OR_START:
            if ch == '|':
                return 'ACCEPT_OR'
            return 'ERROR_EXPECTED_OR'

        else:
            return 'ERROR_STATE_{self.state}'

    @staticmethod
    def is_letter(c: str) -> bool:
        return c in AFD.LETRAS

    @staticmethod
    def is_digit(c: str) -> bool:
        return c in AFD.DIGITOS

    def reset(self):
        self.state = self.STATE_Q0

    @staticmethod
    def is_accept(action):
        return isinstance(action, str) and action.startswith('ACCEPT_')

    @staticmethod
    def is_error(action):
        return isinstance(action, str) and action.startswith('ERROR_')





