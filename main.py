import sys
from pathlib import Path
from src.Tokens import TokenType, get_nome_simbolico, Token
from src.AFD import AFD

OP_COMP_2 = {
    "==": TokenType.EQ,
    ">=": TokenType.GEQ,
    "<=": TokenType.LEQ,
    "!=": TokenType.DIF,
    "&&": TokenType.AND,
    "||": TokenType.OR,
}

def classificar_lexema(afd: AFD, lexema: str) -> TokenType:
    afd.reset()

    if lexema in OP_COMP_2:
        return OP_COMP_2[lexema]

    afd.reset()

    if len(lexema) == 1:
        ch = lexema[0]
        action = afd.processa(ch)

        if isinstance(action, int):
            afd.state = action
            action = afd.processa(" ")

        if isinstance(action, str) and action.startswith("ACCEPT_"):
            tok_type = afd.ACCEPT_MAP[action]
            if tok_type == TokenType.VAR:
                if lexema == "int":
                    return TokenType.INTDEF
                if lexema == "if":
                    return TokenType.IF
                if lexema == "float":
                    return TokenType.FLOATDEF
                if lexema == "char":
                    return TokenType.CHAR_TYPE
                if lexema == "bool":
                    return TokenType.BOLL_TYPE
                if lexema == "return":
                    return TokenType.RETURN
                return TokenType.VAR
            return tok_type

        raise SyntaxError(f"Erro léxico: lexema inválido '{lexema}'")

    buffer = ""
    action = None

    for ch in lexema:
        action = afd.processa(ch)

        if isinstance(action, int):
            afd.state = action
            buffer += ch
            continue

        if isinstance(action, str) and action.startswith("ACCEPT_"):
            raise SyntaxError(f"Erro léxico: lexema incompleto ou inválido '{lexema}'")
        if isinstance(action, str) and action.startswith("ERROR_"):
            raise SyntaxError(f"Erro léxico: {action} ao processar '{lexema}'")

    action = afd.processa(" ")
    if isinstance(action, str) and action.startswith("ACCEPT_"):
        tok_type = afd.ACCEPT_MAP[action]

        # Se for VAR, converter keyword
        if tok_type == TokenType.VAR:
            if lexema == "int":
                return TokenType.INTDEF
            if lexema == "if":
                return TokenType.IF
            if lexema == "float":
                return TokenType.FLOATDEF
            if lexema == "char":
                return TokenType.CHAR_TYPE
            if lexema == "bool":
                return TokenType.BOLL_TYPE
            if lexema == "return":
                return TokenType.RETURN
            return TokenType.VAR

        return tok_type

    raise SyntaxError(f"Erro ao classificar lexema '{lexema}'")


def main():
    if len(sys.argv) != 2:
        print("Uso: python main_tokens.py <arquivo_fonte.c>")
        sys.exit(1)

    fonte_path = Path(sys.argv[1])
    if not fonte_path.exists():
        print(f"Arquivo '{fonte_path}' não encontrado.")
        sys.exit(1)

    # Lê todas as linhas do arquivo de entrada
    linhas = fonte_path.read_text(encoding="utf-8").splitlines()

    afd = AFD()
    saida_linhas = []

    for linha in linhas:
        lexemas = linha.strip().split()
        tokens_na_linha = []

        for lex in lexemas:
            if lex == "":
                continue
            try:
                tok_type = classificar_lexema(afd, lex)
            except SyntaxError as e:
                print(f"[Erro léxico] {e}")
                sys.exit(1)

            if tok_type == TokenType.PVIRGULA:
                continue

            nome = get_nome_simbolico(tok_type)
            tokens_na_linha.append(nome)

        saida_linhas.append(" ".join(tokens_na_linha))

    saida_path = fonte_path.with_name("saida.txt")
    with open(saida_path, "w") as fw:
        for l in saida_linhas:
            fw.write(l + "\n")

    print(f"Processamento concluído. Tokens escritos em '{saida_path}'.")
    print("Tokens encontrados:")
    for linha in saida_linhas:
        print(linha)




if __name__ == "__main__":
    main()
