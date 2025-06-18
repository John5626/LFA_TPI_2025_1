# TPI_LFA - 2025.1 - João, Lorenzo e Marcela                AFD.py

from src.TiposToken import TipoToken

class AFD:
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    digitos = "0123456789"

    def __init__(self):
        self.estQ0 = 0
        self.estPalavraChave = 1
        self.estNumInteiro = 2
        self.estNumFlutuante = 3
        self.estEspaco = 4
        self.estInicioDivisao = 5       # '/'
        self.estComentario = 6          # // ... até \n
        self.estInicioGT = 7            # '>'
        self.estInicioLT = 8            # '<'
        self.estInicioEQ = 9            # '='
        self.estInicioNegacao = 10      # '!'
        self.estInicioAnd = 11          # '&'
        self.estInicioOr = 12           # '|'

        self.mapAceitacao = {
            "ACCEPT_LPAREN": TipoToken.LParenteses,
            "ACCEPT_RPAREN": TipoToken.RParenteses,
            "ACCEPT_LBRACE": TipoToken.LChave,
            "ACCEPT_RBRACE": TipoToken.RChave,
            "ACCEPT_LBRACKET": TipoToken.LColchete,
            "ACCEPT_RBRACKET": TipoToken.RColchete,
            "ACCEPT_SEMICOLON": TipoToken.PVirgula,
            "ACCEPT_COMMA": TipoToken.Virgula,
            "ACCEPT_EQ": TipoToken.EQ,
            "ACCEPT_ASSIGN": TipoToken.Atribuicao,
            "ACCEPT_GEQ": TipoToken.GEQ,
            "ACCEPT_LEQ": TipoToken.LEQ,
            "ACCEPT_GT": TipoToken.GT,
            "ACCEPT_LT": TipoToken.LT,
            "ACCEPT_NEG": TipoToken.NEG,
            "ACCEPT_DIF": TipoToken.DIF,
            "ACCEPT_AND": TipoToken.AND,
            "ACCEPT_OR": TipoToken.OR,
            "ACCEPT_SUM": TipoToken.SUM,
            "ACCEPT_SUB": TipoToken.SUB,
            "ACCEPT_MULT": TipoToken.MULT,
            "ACCEPT_DIV": TipoToken.DIV,
            "ACCEPT_RESTO": TipoToken.RESTO,
            "ACCEPT_NUM_INT": TipoToken.NUM_INT,
            "ACCEPT_NUM_FLOAT": TipoToken.NUM_FLOAT,
            "ACCEPT_VAR": TipoToken.VAR,
            "ACCEPT_IF": TipoToken.IF,
            "ACCEPT_INTDEF": TipoToken.INTDEF,
            "ACCEPT_FLOATDEF": TipoToken.FLOATDEF,
            "ACCEPT_CHAR_TYPE": TipoToken.CHAR_TYPE,
            "ACCEPT_BOOL_TYPE": TipoToken.BOLL_TYPE,
            "ACCEPT_RETURN": TipoToken.RETURN,
            "ACCEPT_WS": TipoToken.WHITESPACE,
            "ACCEPT_COMMENT": TipoToken.COMMENT,
        }

        self.estAtual = self.estQ0

    def processar(self, c):
        if self.estAtual == self.estQ0:
            if c is None:
                return None
            if c.isspace():
                return self.estEspaco
            if self.ehLetra(c):
                return self.estPalavraChave
            if self.ehDigito(c):
                return self.estNumInteiro
            if c == ";":
                return "ACCEPT_SEMICOLON"

            tokensUnico = {
                "(": "ACCEPT_LPAREN",
                ")": "ACCEPT_RPAREN",
                "{": "ACCEPT_LBRACE",
                "}": "ACCEPT_RBRACE",
                "[": "ACCEPT_LBRACKET",
                "]": "ACCEPT_RBRACKET",
                ",": "ACCEPT_COMMA",
                "+": "ACCEPT_SUM",
                "-": "ACCEPT_SUB",
                "*": "ACCEPT_MULT",
                "%": "ACCEPT_RESTO",
            }
            
            if c in tokensUnico:
                return tokensUnico[c]
            if c == "/":
                return self.estInicioDivisao
            if c == "=":
                return self.estInicioEQ
            if c == ">":
                return self.estInicioGT
            if c == "<":
                return self.estInicioLT
            if c == "!":
                return self.estInicioNegacao
            if c == "&":
                return self.estInicioAnd
            if c == "|":
                return self.estInicioOr
            return "ERROR_UNKNOWN_CHAR"

        if self.estAtual == self.estPalavraChave:
            if c is not None and (self.ehLetra(c) or self.ehDigito(c)):
                return self.estPalavraChave
            return "ACCEPT_VAR"

        if self.estAtual == self.estNumInteiro:
            if c is not None and self.ehDigito(c):
                return self.estNumInteiro
            if c == ".":
                return self.estNumFlutuante
            return "ACCEPT_NUM_INT"

        if self.estAtual == self.estNumFlutuante:
            if c is not None and self.ehDigito(c):
                return self.estNumFlutuante
            return "ACCEPT_NUM_FLOAT"

        if self.estAtual == self.estEspaco:
            if c is not None and c.isspace():
                return self.estEspaco
            return "ACCEPT_WS"

        if self.estAtual == self.estInicioDivisao:
            if c == "/":
                return self.estComentario
            return "ACCEPT_DIV"

        if self.estAtual == self.estComentario:
            if c is None or c == "\n":
                return "ACCEPT_WS"
            return self.estComentario

        if self.estAtual == self.estInicioEQ:
            if c == "=":
                return "ACCEPT_EQ"
            return "ACCEPT_ASSIGN"

        if self.estAtual == self.estInicioGT:
            if c == "=":
                return "ACCEPT_GEQ"
            return "ACCEPT_GT"

        if self.estAtual == self.estInicioLT:
            if c == "=":
                return "ACCEPT_LEQ"
            return "ACCEPT_LT"

        if self.estAtual == self.estInicioNegacao:
            if c == "=":
                return "ACCEPT_DIF"
            return "ACCEPT_NEG"

        if self.estAtual == self.estInicioAnd:
            if c == "&":
                return "ACCEPT_AND"
            return "ERROR_EXPECTED_AND"

        if self.estAtual == self.estInicioOr:
            if c == "|":
                return "ACCEPT_OR"
            return "ERROR_EXPECTED_OR"

        return f"ERROR_STATE_{self.estAtual}"

    @staticmethod
    def ehLetra(c: str) -> bool:
        return c in AFD.letras

    @staticmethod
    def ehDigito(c: str) -> bool:
        return c in AFD.digitos

    def reset(self):
        self.estAtual = self.estQ0

    @staticmethod
    def aceita(acao):
        return isinstance(acao, str) and acao.startswith("ACCEPT_")

    @staticmethod
    def ehErro(acao):
        return isinstance(acao, str) and acao.startswith("ERROR_")