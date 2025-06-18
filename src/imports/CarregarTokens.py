# TPI_LFA - 2025.1 - João, Lorenzo e Marcela                    CarregarTokens.py

import os

def carregarTokens(nomeArquivo):
    """
    Entrada: nome do arquivo contendo os tokens.
    Sáida: dicionário contendo os nomes e literais dos tokens
    """

    nomesToken = {}
    literaisToken = {}
    codigo = 1

    caminhoTokens = os.path.join(os.path.dirname(__file__), '..', nomeArquivo)

    with open(caminhoTokens, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue

            partes = linha.split(None, 1)
            if len(partes) != 2:
                continue

            nome, literal = partes
            nomesToken[nome] = codigo
            literaisToken[literal] = codigo
            codigo += 1

    return nomesToken, literaisToken