# TPI_LFA - 2025.1 - João, Lorenzo e Marcela                TiposToken.py
from src.imports.CarregarTokens import carregarTokens

nomesToken, simboloToken= carregarTokens('tokens.txt')
definicoesToken = {}

class TipoToken:
    pass

# preenche a classe com os tokens do arquivo
for nome, codigo in nomesToken.items():
    setattr(TipoToken, nome, codigo)
    definicoesToken[nome] = codigo


def obterNomeSimbolico(codigo):
    """
    Entrada: código do token.
    Saída: nome simbólico do token.
    """
    for nome, cod in nomesToken.items():
        if cod == codigo:
            return nome
    return None


class SimboloToken:
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        nomeEncontrado = None
        for nome, cod in definicoesToken.items():
            if cod == self.tipo:
                nomeEncontrado = nome
                break

        if nomeEncontrado is None:
            nomeEncontrado = self.Tipo

        return (
            f"SimboloToken(tipo={nomeEncontrado}, "
            f"lexema='{self.lexema}', "
            f"linha={self.linha}, "
            f"coluna={self.coluna})"
        )