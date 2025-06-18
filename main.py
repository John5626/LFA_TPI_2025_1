# TPI_LFA - 2025.1 - João, Lorenzo e Marcela                main.py
import sys
from pathlib import Path
from src.TiposToken import TipoToken, obterNomeSimbolico
from src.AFD import AFD

def mapearPalavraReservada(lexema: str, tipo: TipoToken) -> TipoToken:
    """
    Entrada: lexema, tipo
    Saída: TipoToken mapeado dadp a palavra
    """
    mapPalavrasReservadas = {
        "int": TipoToken.INTDEF,
        "if": TipoToken.IF,
        "float": TipoToken.FLOATDEF,
        "char": TipoToken.CHAR_TYPE,
        "bool": TipoToken.BOLL_TYPE,
        "return": TipoToken.RETURN,
    }

    reservado = mapPalavrasReservadas.get(lexema)
    if reservado is not None:
        return reservado

    if tipo == TipoToken.VAR:
         if not lexema.startswith("VAR") or len(lexema) == 3:
            raise SyntaxError(f"Variáveis devem começar por 'VAR'")

         return TipoToken.VAR


    return tipo


def classificaUnicoCaractere(afd: AFD, lexema: str) -> TipoToken:
    """
    Entrada: AFD, lexema unico
    Saída: TipoToken correspondente ao lexema
    """
    acao = afd.processar(lexema)
    if isinstance(acao, int):
        afd.estAtual = acao
        acao = afd.processar(" ")
    if isinstance(acao, str) and acao.startswith("ACCEPT_"):
        return afd.mapAceitacao[acao]
    raise SyntaxError(f"Lexema inválido '{lexema}'")


def classificarMultiplosCaracteres(afd: AFD, lexema: str) -> TipoToken:
    """
    Entrada: AFD, lexema mult
    Saída: TipoToken correspondente ao lexema
    """
    for ch in lexema:
        acao = afd.processar(ch)
        if isinstance(acao, int):
            afd.estAtual = acao
            continue

        if isinstance(acao, str) and acao.startswith("ACCEPT_"):
            raise SyntaxError(f"Lexema incompleto ou inválido '{lexema}'")

        if isinstance(acao, str) and acao.startswith("ERROR_"):
            raise SyntaxError(f"Erro: {acao} ao processar '{lexema}'")

    acao = afd.processar(" ")
    if isinstance(acao, str) and acao.startswith("ACCEPT_"):
        return afd.mapAceitacao[acao]
    raise SyntaxError(f"Erro ao classificar lexema '{lexema}'")


def classificarLexema(afd: AFD, lexema: str) -> TipoToken:
    opCompDoisCarac = {
        "==": TipoToken.EQ,
        ">=": TipoToken.GEQ,
        "<=": TipoToken.LEQ,
        "!=": TipoToken.DIF,
        "&&": TipoToken.AND,
        "||": TipoToken.OR,
        "//": TipoToken.COMMENT,
    }

    afd.reset()

    if lexema.startswith("//"):
            print(f"[Comentário] {lexema}")
            return TipoToken.COMMENT

    if lexema in opCompDoisCarac:
        return opCompDoisCarac[lexema]

    if len(lexema) == 1:
        tipo = classificaUnicoCaractere(afd, lexema)
    else:
        tipo = classificarMultiplosCaracteres(afd, lexema)

    return mapearPalavraReservada(lexema, tipo)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Insira o argumento")
        sys.exit(1)

    f = Path(sys.argv[1])
    if not f.exists():
        print(f"Arquivo '{f}' não encontrado.")
        sys.exit(1)

    linhas = f.read_text().splitlines()
    afd = AFD()
    linhasSaida = []

    for linha in linhas:
        lexemas = linha.strip().split()
        tokensNaLinha = []

        for lexema in lexemas:
            if lexema == "":
                continue

            try:
                tipoToken = classificarLexema(afd, lexema)
            except SyntaxError as e:
                print(f"[Erro léxico] {e}")
                sys.exit(1)

            #if tipoToken == TipoToken.PVIRGULA:
            #    continue

            nomeSimbolico = obterNomeSimbolico(tipoToken)
            tokensNaLinha.append(nomeSimbolico)

        linhasSaida.append(" ".join(tokensNaLinha))

    f = f.with_name("saida.txt")
    with open(f, "w") as arquivoSaida:
        for linha in linhasSaida:
            arquivoSaida.write(linha + "\n")

    print(f"Processamento concluído. Tokens escritos em '{f}'.")
    print("Tokens encontrados:")
    for linha in linhasSaida:
        print(linha)

