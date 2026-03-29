#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEBULA LANGUAGE INTERPRETER
===========================
Linguagem de programação didática para a disciplina de 
Construção de Interpretadores e Compiladores.

Características:
- Palavras-chave em português: criar, se, senao, enquanto, exibir
- Blocos delimitados por 'inicio' ... 'fim'
- Statements terminados por ';'
- Operadores lógicos: &&, ||, !
- Comentários: // e /* */

Autor: [João Victor Rocha Santos, Denis Filho Cunha Godoi]
Disciplina: N477 - Construção de Interpretadores e Compiladores
Instituição: Unitri
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Any
import sys

# ==============================
# ENUM DE TIPOS DE TOKEN
# ==============================

class TipoToken(Enum):
    # Palavras-chave
    CRIAR = auto()      # declaração de variável
    SE = auto()         # if
    SENAO = auto()      # else
    ENQUANTO = auto()   # while
    DEFINIR = auto()    # def/função
    RETORNAR = auto()   # return
    EXIBIR = auto()     # print/output
    
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
    
    # Fim de arquivo
    EOF = auto()
    
    def __repr__(self):
        return f"{self.name}"


# ==============================
# CLASSE TOKEN
# ==============================

@dataclass
class Token:
    tipo: TipoToken
    valor: Any = None
    linha: int = 0
    coluna: int = 0
    
    def __repr__(self):
        if self.valor is not None:
            return f"Token({self.tipo}, '{self.valor}', linha={self.linha}, col={self.coluna})"
        return f"Token({self.tipo}, linha={self.linha}, col={self.coluna})"


# ==============================
# ANÁLISADOR LÉXICO (LEXER)
# ==============================

class AnalisadorLexico:
    def __init__(self, codigo_fonte: str):
        self.codigo = codigo_fonte
        self.pos = 0
        self.linha = 1
        self.coluna = 1
        self.tokens: List[Token] = []
        
        # Palavras-chave da linguagem Nebula
        self.palavras_chave = {
            'criar': TipoToken.CRIAR,
            'se': TipoToken.SE,
            'senao': TipoToken.SENAO,
            'enquanto': TipoToken.ENQUANTO,
            'definir': TipoToken.DEFINIR,
            'retornar': TipoToken.RETORNAR,
            'exibir': TipoToken.EXIBIR,
            'inicio': TipoToken.INICIO,
            'fim': TipoToken.FIM,
            'verdadeiro': (TipoToken.BOOLEANO, True),
            'falso': (TipoToken.BOOLEANO, False),
        }
    
    def _caractere_atual(self) -> Optional[str]:
        if self.pos >= len(self.codigo):
            return None
        return self.codigo[self.pos]
    
    def _proximo_caractere(self) -> Optional[str]:
        if self.pos + 1 >= len(self.codigo):
            return None
        return self.codigo[self.pos + 1]
    
    def _avancar(self):
        if self.pos < len(self.codigo) and self.codigo[self.pos] == '\n':
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
        self.pos += 1
    
    def _pular_espacos(self):
        while self._caractere_atual() is not None and self._caractere_atual() in ' \t\r\n':
            self._avancar()
    
    def _pular_comentario_linha(self):
        while self._caractere_atual() is not None and self._caractere_atual() != '\n':
            self._avancar()
    
    def _pular_comentario_bloco(self):
        self._avancar()  # pula *
        self._avancar()
        while self._caractere_atual() is not None:
            if self._caractere_atual() == '*' and self._proximo_caractere() == '/':
                self._avancar()
                self._avancar()
                return
            self._avancar()
        raise SyntaxError(f"Comentário de bloco não fechado. Linha {self.linha}, Coluna {self.coluna}")
    
    def _ler_string(self) -> str:
        valor = ""
        self._avancar()  # pula aspas inicial
        while self._caractere_atual() is not None and self._caractere_atual() != '"':
            if self._caractere_atual() == '\\':
                self._avancar()
                escape_char = self._caractere_atual()
                if escape_char == 'n':
                    valor += '\n'
                elif escape_char == 't':
                    valor += '\t'
                elif escape_char == '\\':
                    valor += '\\'
                elif escape_char == '"':
                    valor += '"'
                else:
                    valor += escape_char
            else:
                valor += self._caractere_atual()
            self._avancar()
        
        if self._caractere_atual() != '"':
            raise SyntaxError(f"String não fechada. Linha {self.linha}, Coluna {self.coluna}")
        
        self._avancar()  # pula aspas final
        return valor
    
    def _ler_numero(self) -> Token:
        linha = self.linha
        coluna = self.coluna
        valor = ""
        
        while (self._caractere_atual() is not None and 
               (self._caractere_atual().isdigit() or self._caractere_atual() == '.')):
            valor += self._caractere_atual()
            self._avancar()
        
        if '.' in valor:
            return Token(TipoToken.NUMERO_REAL, float(valor), linha, coluna)
        else:
            return Token(TipoToken.NUMERO_INTEIRO, int(valor), linha, coluna)
    
    def _ler_identificador(self) -> Token:
        linha = self.linha
        coluna = self.coluna
        valor = ""
        
        while (self._caractere_atual() is not None and 
               (self._caractere_atual().isalnum() or self._caractere_atual() == '_')):
            valor += self._caractere_atual()
            self._avancar()
        
        if valor in self.palavras_chave:
            info = self.palavras_chave[valor]
            if isinstance(info, tuple):
                return Token(info[0], info[1], linha, coluna)
            return Token(info, valor, linha, coluna)
        
        return Token(TipoToken.IDENTIFICADOR, valor, linha, coluna)
    
    def analisar(self) -> List[Token]:
        while self._caractere_atual() is not None:
            self._pular_espacos()
            
            if self._caractere_atual() is None:
                break
            
            linha = self.linha
            coluna = self.coluna
            char = self._caractere_atual()
            
            # Comentários
            if char == '/' and self._proximo_caractere() == '/':
                self._avancar()
                self._avancar()
                self._pular_comentario_linha()
                continue
            
            if char == '/' and self._proximo_caractere() == '*':
                self._pular_comentario_bloco()
                continue
            
            # Strings
            if char == '"':
                valor = self._ler_string()
                self.tokens.append(Token(TipoToken.STRING, valor, linha, coluna))
                continue
            
            # Números
            if char.isdigit():
                self.tokens.append(self._ler_numero())
                continue
            
            # Identificadores e palavras-chave
            if char.isalpha() or char == '_':
                self.tokens.append(self._ler_identificador())
                continue
            
            # Operadores de dois caracteres
            dois_chars = char + (self._proximo_caractere() or '')
            
            if dois_chars == '==':
                self.tokens.append(Token(TipoToken.IGUAL, '==', linha, coluna))
                self._avancar()
                self._avancar()
                continue
            
            if dois_chars == '!=':
                self.tokens.append(Token(TipoToken.DIFERENTE, '!=', linha, coluna))
                self._avancar()
                self._avancar()
                continue
            
            if dois_chars == '<=':
                self.tokens.append(Token(TipoToken.MENOR_IGUAL, '<=', linha, coluna))
                self._avancar()
                self._avancar()
                continue
            
            if dois_chars == '>=':
                self.tokens.append(Token(TipoToken.MAIOR_IGUAL, '>=', linha, coluna))
                self._avancar()
                self._avancar()
                continue
            
            if dois_chars == '&&':
                self.tokens.append(Token(TipoToken.E_LOGICO, '&&', linha, coluna))
                self._avancar()
                self._avancar()
                continue
            
            if dois_chars == '||':
                self.tokens.append(Token(TipoToken.OU_LOGICO, '||', linha, coluna))
                self._avancar()
                self._avancar()
                continue
            
            # Operadores e delimitadores de um caractere
            operadores = {
                '+': TipoToken.SOMA,
                '-': TipoToken.SUBTRACAO,
                '*': TipoToken.MULTIPLICACAO,
                '/': TipoToken.DIVISAO,
                '%': TipoToken.MODULO,
                '^': TipoToken.POTENCIA,
                '<': TipoToken.MENOR,
                '>': TipoToken.MAIOR,
                '!': TipoToken.NAO_LOGICO,
                '=': TipoToken.ATRIBUICAO,
                ';': TipoToken.PONTO_VIRGULA,
                ',': TipoToken.VIRGULA,
                ':': TipoToken.DOIS_PONTOS,
                '(': TipoToken.ABRE_PARENTESES,
                ')': TipoToken.FECHA_PARENTESES,
            }
            
            if char in operadores:
                self.tokens.append(Token(operadores[char], char, linha, coluna))
                self._avancar()
                continue
            
            raise SyntaxError(f"Caractere inválido '{char}' na linha {linha}, coluna {coluna}")
        
        self.tokens.append(Token(TipoToken.EOF, None, self.linha, self.coluna))
        return self.tokens


# ==============================
# NÓS DA AST
# ==============================

class ASTNode:
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


# ==============================
# ANÁLISADOR SINTÁTICO (PARSER)
# ==============================

class ErroSintatico(Exception):
    def __init__(self, mensagem: str, linha: int, coluna: int):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        super().__init__(f"Erro sintático na linha {linha}, coluna {coluna}: {mensagem}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.erros: List[str] = []
    
    def _atual(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]
    
    def _avancar(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
    
    def _esperar(self, tipo: TipoToken) -> Token:
        token = self._atual()
        if token.tipo != tipo:
            raise ErroSintatico(
                f"Esperado {tipo.name}, encontrado {token.tipo.name}",
                token.linha, token.coluna
            )
        self._avancar()
        return token
    
    def _sincronizar(self, tokens_sincronizadores: List[TipoToken]):
        while self._atual().tipo not in tokens_sincronizadores and self._atual().tipo != TipoToken.EOF:
            self._avancar()
    
    def parse(self) -> Programa:
        statements = []
        while self._atual().tipo != TipoToken.EOF:
            try:
                stmt = self._parse_statement()
                if stmt:
                    statements.append(stmt)
            except ErroSintatico as e:
                self.erros.append(str(e))
                print(f"[!] {e}")
                self._sincronizar([TipoToken.PONTO_VIRGULA, TipoToken.INICIO, TipoToken.FIM])
                if self._atual().tipo == TipoToken.PONTO_VIRGULA:
                    self._avancar()
        
        return Programa(statements)
    
    def _parse_statement(self) -> Optional[ASTNode]:
        token = self._atual()
        
        if token.tipo == TipoToken.CRIAR:
            return self._parse_declaracao()
        elif token.tipo == TipoToken.SE:
            return self._parse_se()
        elif token.tipo == TipoToken.ENQUANTO:
            return self._parse_enquanto()
        elif token.tipo == TipoToken.EXIBIR:
            return self._parse_exibir()
        elif token.tipo == TipoToken.IDENTIFICADOR:
            return self._parse_atribuicao_ou_chamada()
        elif token.tipo == TipoToken.INICIO:
            return self._parse_bloco()
        elif token.tipo == TipoToken.PONTO_VIRGULA:
            self._avancar()
            return None
        else:
            expr = self._parse_expressao()
            self._esperar(TipoToken.PONTO_VIRGULA)
            return expr
    
    def _parse_declaracao(self) -> Declaracao:
        self._esperar(TipoToken.CRIAR)
        nome = self._esperar(TipoToken.IDENTIFICADOR).valor
        
        valor = None
        if self._atual().tipo == TipoToken.ATRIBUICAO:
            self._avancar()
            valor = self._parse_expressao()
        
        self._esperar(TipoToken.PONTO_VIRGULA)
        return Declaracao(nome, valor)
    
    def _parse_atribuicao_ou_chamada(self) -> ASTNode:
        nome = self._esperar(TipoToken.IDENTIFICADOR).valor
        
        if self._atual().tipo == TipoToken.ATRIBUICAO:
            self._avancar()
            valor = self._parse_expressao()
            self._esperar(TipoToken.PONTO_VIRGULA)
            return Atribuicao(nome, valor)
        else:
            return Variavel(nome)
    
    def _parse_se(self) -> Se:
        self._esperar(TipoToken.SE)
        self._esperar(TipoToken.ABRE_PARENTESES)
        condicao = self._parse_expressao()
        self._esperar(TipoToken.FECHA_PARENTESES)
        
        entao_bloco = self._parse_bloco()
        entao = entao_bloco.statements if isinstance(entao_bloco, Programa) else [entao_bloco]
        
        senao = None
        if self._atual().tipo == TipoToken.SENAO:
            self._avancar()
            senao_bloco = self._parse_bloco()
            senao = senao_bloco.statements if isinstance(senao_bloco, Programa) else [senao_bloco]
        
        return Se(condicao, entao, senao)
    
    def _parse_enquanto(self) -> Enquanto:
        self._esperar(TipoToken.ENQUANTO)
        self._esperar(TipoToken.ABRE_PARENTESES)
        condicao = self._parse_expressao()
        self._esperar(TipoToken.FECHA_PARENTESES)
        
        corpo_bloco = self._parse_bloco()
        corpo = corpo_bloco.statements if isinstance(corpo_bloco, Programa) else [corpo_bloco]
        return Enquanto(condicao, corpo)
    
    def _parse_exibir(self) -> Exibir:
        self._esperar(TipoToken.EXIBIR)
        self._esperar(TipoToken.ABRE_PARENTESES)
        expr = self._parse_expressao()
        self._esperar(TipoToken.FECHA_PARENTESES)
        self._esperar(TipoToken.PONTO_VIRGULA)
        return Exibir(expr)
    
    def _parse_bloco(self) -> Programa:
        self._esperar(TipoToken.INICIO)
        statements = []
        
        while self._atual().tipo not in (TipoToken.FIM, TipoToken.EOF):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        self._esperar(TipoToken.FIM)
        return Programa(statements)
    
    # Precedência: () > !,- > ^ > *,/,% > +,- > <,<=,>,>= > ==,!= > && > ||
    def _parse_expressao(self) -> ASTNode:
        return self._parse_ou_logico()
    
    def _parse_ou_logico(self) -> ASTNode:
        node = self._parse_e_logico()
        while self._atual().tipo == TipoToken.OU_LOGICO:
            op = self._atual()
            self._avancar()
            direita = self._parse_e_logico()
            node = BinOp(node, op, direita)
        return node
    
    def _parse_e_logico(self) -> ASTNode:
        node = self._parse_igualdade()
        while self._atual().tipo == TipoToken.E_LOGICO:
            op = self._atual()
            self._avancar()
            direita = self._parse_igualdade()
            node = BinOp(node, op, direita)
        return node
    
    def _parse_igualdade(self) -> ASTNode:
        node = self._parse_comparacao()
        while self._atual().tipo in (TipoToken.IGUAL, TipoToken.DIFERENTE):
            op = self._atual()
            self._avancar()
            direita = self._parse_comparacao()
            node = BinOp(node, op, direita)
        return node
    
    def _parse_comparacao(self) -> ASTNode:
        node = self._parse_adicao()
        while self._atual().tipo in (TipoToken.MENOR, TipoToken.MENOR_IGUAL, 
                                      TipoToken.MAIOR, TipoToken.MAIOR_IGUAL):
            op = self._atual()
            self._avancar()
            direita = self._parse_adicao()
            node = BinOp(node, op, direita)
        return node
    
    def _parse_adicao(self) -> ASTNode:
        node = self._parse_multiplicacao()
        while self._atual().tipo in (TipoToken.SOMA, TipoToken.SUBTRACAO):
            op = self._atual()
            self._avancar()
            direita = self._parse_multiplicacao()
            node = BinOp(node, op, direita)
        return node
    
    def _parse_multiplicacao(self) -> ASTNode:
        node = self._parse_potencia()
        while self._atual().tipo in (TipoToken.MULTIPLICACAO, TipoToken.DIVISAO, TipoToken.MODULO):
            op = self._atual()
            self._avancar()
            direita = self._parse_potencia()
            node = BinOp(node, op, direita)
        return node
    
    def _parse_potencia(self) -> ASTNode:
        node = self._parse_unario()
        if self._atual().tipo == TipoToken.POTENCIA:
            op = self._atual()
            self._avancar()
            direita = self._parse_potencia()
            return BinOp(node, op, direita)
        return node
    
    def _parse_unario(self) -> ASTNode:
        if self._atual().tipo == TipoToken.NAO_LOGICO:
            op = self._atual()
            self._avancar()
            operando = self._parse_unario()
            return UnaryOp(op, operando)
        elif self._atual().tipo == TipoToken.SUBTRACAO:
            op = self._atual()
            self._avancar()
            operando = self._parse_unario()
            return UnaryOp(op, operando)
        return self._parse_primario()
    
    def _parse_primario(self) -> ASTNode:
        token = self._atual()
        
        if token.tipo == TipoToken.NUMERO_INTEIRO:
            self._avancar()
            return Numero(token.valor)
        
        if token.tipo == TipoToken.NUMERO_REAL:
            self._avancar()
            return Numero(token.valor)
        
        if token.tipo == TipoToken.STRING:
            self._avancar()
            return String(token.valor)
        
        if token.tipo == TipoToken.BOOLEANO:
            self._avancar()
            return Booleano(token.valor)
        
        if token.tipo == TipoToken.IDENTIFICADOR:
            self._avancar()
            return Variavel(token.valor)
        
        if token.tipo == TipoToken.ABRE_PARENTESES:
            self._avancar()
            node = self._parse_expressao()
            self._esperar(TipoToken.FECHA_PARENTESES)
            return node
        
        raise ErroSintatico(
            f"Expressão inesperada: {token.tipo.name}",
            token.linha, token.coluna
        )


# ==============================
# INTERPRETADOR
# ==============================

class ErroExecucao(Exception):
    pass

class Interpretador:
    def __init__(self):
        self.variaveis: Dict[str, Any] = {}
        self.escopos: List[Dict[str, Any]] = [self.variaveis]
    
    def executar(self, node: ASTNode) -> Any:
        method_name = f'_executar_{type(node).__name__}'
        method = getattr(self, method_name, self._executar_generico)
        return method(node)
    
    def _executar_generico(self, node: ASTNode):
        raise ErroExecucao(f"Tipo de nó não suportado: {type(node)}")
    
    def _executar_Programa(self, node: Programa):
        resultado = None
        for stmt in node.statements:
            resultado = self.executar(stmt)
        return resultado
    
    def _executar_Numero(self, node: Numero):
        return node.valor
    
    def _executar_String(self, node: String):
        return node.valor
    
    def _executar_Booleano(self, node: Booleano):
        return node.valor
    
    def _executar_Variavel(self, node: Variavel):
        for escopo in reversed(self.escopos):
            if node.nome in escopo:
                return escopo[node.nome]
        raise ErroExecucao(f"Variável '{node.nome}' não declarada")
    
    def _executar_Declaracao(self, node: Declaracao):
        valor = None
        if node.valor:
            valor = self.executar(node.valor)
        self.escopos[-1][node.nome] = valor
        return valor
    
    def _executar_Atribuicao(self, node: Atribuicao):
        valor = self.executar(node.valor)
        for escopo in reversed(self.escopos):
            if node.nome in escopo:
                escopo[node.nome] = valor
                return valor
        self.escopos[-1][node.nome] = valor
        return valor
    
    def _executar_BinOp(self, node: BinOp):
        esq = self.executar(node.esquerda)
        dir_val = self.executar(node.direita)
        op = node.operador.tipo
        
        if op == TipoToken.SOMA:
            if isinstance(esq, str) or isinstance(dir_val, str):
                return str(esq) + str(dir_val)
            return esq + dir_val
        elif op == TipoToken.SUBTRACAO:
            return esq - dir_val
        elif op == TipoToken.MULTIPLICACAO:
            return esq * dir_val
        elif op == TipoToken.DIVISAO:
            if dir_val == 0:
                raise ErroExecucao("Divisão por zero")
            return esq / dir_val
        elif op == TipoToken.MODULO:
            return esq % dir_val
        elif op == TipoToken.POTENCIA:
            return esq ** dir_val
        elif op == TipoToken.IGUAL:
            return esq == dir_val
        elif op == TipoToken.DIFERENTE:
            return esq != dir_val
        elif op == TipoToken.MENOR:
            return esq < dir_val
        elif op == TipoToken.MENOR_IGUAL:
            return esq <= dir_val
        elif op == TipoToken.MAIOR:
            return esq > dir_val
        elif op == TipoToken.MAIOR_IGUAL:
            return esq >= dir_val
        elif op == TipoToken.E_LOGICO:
            return esq and dir_val
        elif op == TipoToken.OU_LOGICO:
            return esq or dir_val
        
        raise ErroExecucao(f"Operador desconhecido: {op}")
    
    def _executar_UnaryOp(self, node: UnaryOp):
        operando = self.executar(node.operando)
        op = node.operador.tipo
        
        if op == TipoToken.NAO_LOGICO:
            return not operando
        elif op == TipoToken.SUBTRACAO:
            return -operando
        
        raise ErroExecucao(f"Operador unário desconhecido: {op}")
    
    def _executar_Se(self, node: Se):
        condicao = self.executar(node.condicao)
        
        if condicao:
            self.escopos.append({})
            try:
                resultado = None
                for stmt in node.entao:
                    resultado = self.executar(stmt)
                return resultado
            finally:
                self.escopos.pop()
        elif node.senao:
            self.escopos.append({})
            try:
                resultado = None
                for stmt in node.senao:
                    resultado = self.executar(stmt)
                return resultado
            finally:
                self.escopos.pop()
        
        return None
    
    def _executar_Enquanto(self, node: Enquanto):
        resultado = None
        while self.executar(node.condicao):
            self.escopos.append({})
            try:
                for stmt in node.corpo:
                    resultado = self.executar(stmt)
            finally:
                self.escopos.pop()
        return resultado
    
    def _executar_Exibir(self, node: Exibir):
        valor = self.executar(node.expressao)
        print(valor)
        return valor


# ==============================
# INTERFACE DE LINHA DE COMANDO
# ==============================

def executar_arquivo(caminho: str, verbose: bool = False):
    """Executa um arquivo Nebula"""
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return
    
    # Análise Léxica
    print("\n[1] ANÁLISE LÉXICA")
    print("-" * 40)
    try:
        lexer = AnalisadorLexico(codigo)
        tokens = lexer.analisar()
        if verbose:
            for token in tokens:
                print(f"  {token}")
        print(f"✓ {len(tokens)} tokens gerados")
    except SyntaxError as e:
        print(f"✗ Erro léxico: {e}")
        return
    
    # Análise Sintática
    print("\n[2] ANÁLISE SINTÁTICA")
    print("-" * 40)
    try:
        parser = Parser(tokens)
        ast = parser.parse()
        if parser.erros:
            print(f"! {len(parser.erros)} erro(s) sintático(s) encontrado(s)")
        if verbose:
            print(f"  AST: {ast}")
        print(f"✓ AST gerada com {len(ast.statements)} statement(s)")
    except Exception as e:
        print(f"✗ Erro sintático: {e}")
        return
    
    # Execução
    print("\n[3] SAÍDA DO PROGRAMA")
    print("-" * 40)
    try:
        interpretador = Interpretador()
        interpretador.executar(ast)
        print("-" * 40)
        print("✓ Execução finalizada")
    except ErroExecucao as e:
        print(f"✗ Erro em tempo de execução: {e}")
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
    
    print("\n" + "=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Uso: python src/nebula.py examples/<arquivo.neb> [--verbose]")
        print("     python src/nebula.py --help")
        sys.exit(1)
    
    if sys.argv[1] in ('--help', '-h'):
        print("""
NEBULA LANGUAGE INTERPRETER
===========================

Uso: python src/nebula.py examples/tests/<arquivo.neb> [opções]

Opções:
  --verbose, -v    Mostra tokens e AST detalhados
  --help, -h       Mostra esta ajuda

Exemplos:
  python src/nebula.py examples/tests/programa_exemplo.neb -v
  python src/nebula.py -h
        """)
        sys.exit(0)
    
    arquivo = sys.argv[1]
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    executar_arquivo(arquivo, verbose)

if __name__ == "__main__":
    main()
