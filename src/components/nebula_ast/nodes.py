"""
Definição dos Nós da Árvore de Sintaxe Abstrata (AST) para Nebula.
"""

from dataclasses import dataclass
from typing import List, Optional, Union
from src.components.lexer.tokens import Token


class ASTNode:
    """Classe base para todos os nós da AST."""
    pass


@dataclass
class Numero(ASTNode):
    valor: Union[int, float]
    def __repr__(self):
        return f"Numero({self.valor})"


@dataclass
class String(ASTNode):
    valor: str
    def __repr__(self):
        return f"String('{self.valor}')"

@dataclass
class Ler(ASTNode):
    mensagem: Optional['String'] = None
    def __repr__(self):
        if self.mensagem:
            return f"Ler('{self.mensagem.valor}')"
        return "Ler()"

@dataclass
class Booleano(ASTNode):
    valor: bool
    def __repr__(self):
        return f"Booleano({self.valor})"


@dataclass
class Variavel(ASTNode):
    nome: str
    def __repr__(self):
        return f"Variavel({self.nome})"


@dataclass
class BinOp(ASTNode):
    esquerda: ASTNode
    operador: Token
    direita: ASTNode
    def __repr__(self):
        return f"BinOp({self.esquerda}, {self.operador.tipo.name}, {self.direita})"


@dataclass
class UnaryOp(ASTNode):
    operador: Token
    operando: ASTNode
    def __repr__(self):
        return f"UnaryOp({self.operador.tipo.name}, {self.operando})"


@dataclass
class Atribuicao(ASTNode):
    nome: str
    valor: ASTNode
    def __repr__(self):
        return f"Atribuicao({self.nome}, {self.valor})"


@dataclass
class Declaracao(ASTNode):
    nome: str
    valor: Optional[ASTNode] = None
    def __repr__(self):
        return f"Declaracao({self.nome}, {self.valor})"

@dataclass
class Se(ASTNode):
    condicao: ASTNode
    entao: List[ASTNode]
    senao: Optional[List[ASTNode]] = None
    def __repr__(self):
        return f"Se(cond={self.condicao}, entao={len(self.entao)} stmts)"


@dataclass
class Enquanto(ASTNode):
    condicao: ASTNode
    corpo: List[ASTNode]
    def __repr__(self):
        return f"Enquanto(cond={self.condicao}, corpo={len(self.corpo)} stmts)"


@dataclass
class Exibir(ASTNode):
    expressao: ASTNode
    def __repr__(self):
        return f"Exibir({self.expressao})"


@dataclass
class Programa(ASTNode):
    statements: List[ASTNode]
    def __repr__(self):
        return f"Programa({len(self.statements)} stmts)"
    
