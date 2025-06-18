# Implementação de um analisador léxico simplificado

O objetivo do presente trabalho, é desenvolver parte de um **Analisador Léxico Simplificado**, a parte a ser desenvolvida 
é o **reconhecedor de tokens**. Além disso, a entrada do programa deverá ser um arquivo de texto e sua sintaxe limitada 
aos caracteres apresentados a seguir. Cabe ressaltar que, além dos tokens solicitados, também foi incluído o símbolo 
‘//’ para permitir comentários de linha no código de entrada, caso necessário.


---
## Autores
- **João Victor Domingos e Souza** - [John5626]
- **Lorenzo Jordani Bertozzi Luz** - [LorenzoBertozzi]
- **Marcela Gomes Pinheiro** - [marcelagomes1]

---

# Tokens reconhecidos

```
LParenteses (
RParenteses )
LChave {
RChave }
LColchete [
RColchete ]
EQ ==
Atribuicao =
GEQ >=
LEQ <=
GT >
LT <
NEG !
Virgula ,
PVirgula ;
IF if
SUM +
SUB -
MULT *
DIV /
RESTO %
INTDEF int
FLOATDEF float
AND &&
OR ||
NUM_INT [0-9]+
NUM_FLOAT [0-9]*\.[0-9]+
DIF !=
CHAR_TYPE char
BOLL_TYPE bool
RETURN return
VAR VAR\.[A-Za-z0-9]*
COMMENT //.*
WHITESPACE \s+
```
---
## Descrição

No geral, o analisador irá reconhecer categorias de tokens como:
- Identificadores
- Números (inteiros e reais)
- Operadores e delimitadores
- Palavras-reservadas
- Comentários e espaços em branco (descartados)

Mais detalhes acesse a documentação do projeto em `docs/DocumentaçãoLFA.pdf`.

---
## AFD
![AFD](docs/AFD.jpg)
O AFD foi criado utilizando o JFLAP para facilitar a visualização e o entendimento do funcionamento do analisador léxico. O arquivo JFLAP pode ser encontrado na pasta `docs/`.

---
## Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes do Python)
- JFLAP (opcional, para visualizar o AFD)
---

## Estrutura do Projeto
```bash
LFA_TPI_2025_1/
├── readme.md
├── docs/
├── src/
│   ├── imports/
│   │   └── CarregarTokens.py
│   ├── AFD.py
│   ├── TiposToken.py
│   └── tokens.txt
├── tests/
├── .gitignore
```

---

## Como Executar

1. Clone este repositório e entre na pasta:
    ```bash
      git clone <https://github.com/John5626/LFA_TPI_2025_1> && cd LFA_TPI_2025_1

2. (Opcional) Crie e ative um ambiente virtual::
    ```bash
    python -m venv .venv
    source .venv/bin/activate
   
3. Rode o programa:
    ```bash
    python3 main.py tests/teste.txt
    ```
    

## Ferramentas e Referências Utilizadas
- Python 3.10 e documentação
- PyCharm
- Git
- JFLAP (Criação do AFD)
