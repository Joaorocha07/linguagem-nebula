"""
Definição de Tokens e Tipos de Token para a linguagem Nebula.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any


class TipoToken(Enum):
    """Enumeração de todos os tipos de tokens da linguagem Nebula."""

    # Palavras-chave
    CRIAR = auto()      # declaração de variável
    SE = auto()         # if
    SENAO = auto()      # else
    ENQUANTO = auto()   # while
    DEFINIR = auto()    # def/função
    RETORNAR = auto()   # return
    EXIBIR = auto()     # print/output
    LER = auto()        # input/entrada

    # Tipos
    NUMERO_INTEIRO = auto()
    NUMERO_REAL = auto()
    STRING = auto()
    BOOLEANO = auto()
    IDENTIFICADOR = auto()

    # Operadores Aritméticos
    SOMA = auto()           # +
    SUBTRACAO = auto()      # -
    MULTIPLICACAO = auto()  # *
    DIVISAO = auto()        # /
    MODULO = auto()         # %
    POTENCIA = auto()       # ^

    # Operadores Relacionais
    IGUAL = auto()          # ==
    DIFERENTE = auto()      # !=
    MENOR = auto()          # <
    MENOR_IGUAL = auto()    # <=
    MAIOR = auto()          # >
    MAIOR_IGUAL = auto()    # >=

    # Operadores Lógicos
    E_LOGICO = auto()       # &&
    OU_LOGICO = auto()      # ||
    NAO_LOGICO = auto()     # !

    # Delimitadores
    ATRIBUICAO = auto()     # =
    PONTO_VIRGULA = auto()  # ;
    VIRGULA = auto()        # ,
    DOIS_PONTOS = auto()    # :

    # Parênteses e Blocos
    ABRE_PARENTESES = auto()    # (
    FECHA_PARENTESES = auto()   # )
    INICIO = auto()             # inicio
    FIM = auto()                # fim

    NEBULA = auto()      # nebula - comando de consulta ao banco

    # Fim de arquivo
    EOF = auto()

    def __repr__(self):
        return f"{self.name}"


@dataclass
class Token:
    """Representa um token na análise léxica."""
    tipo: TipoToken
    valor: Any = None
    linha: int = 0
    coluna: int = 0

    def __repr__(self):
        if self.valor is not None:
            return f"Token({self.tipo}, '{self.valor}', linha={self.linha}, col={self.coluna})"
        return f"Token({self.tipo}, linha={self.linha}, col={self.coluna})"
