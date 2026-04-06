from typing import List, Optional
from dataclasses import dataclass
from src.components.lexer.tokens import TipoToken, Token
from src.components.nebula_ast.nodes import *


class ErroSintatico(Exception):
    """Exceção para erros sintáticos."""
    def __init__(self, mensagem: str, linha: int, coluna: int):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        super().__init__(f"Erro sintático na linha {linha}, coluna {coluna}: {mensagem}")

@dataclass
class ConsultaPlaneta(ASTNode):
    nome: ASTNode
    def __repr__(self):
        return f"ConsultaPlaneta({self.nome})"

class Parser:
    """Analisador sintático recursivo descendente."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.erros: List[str] = []
        self.palavras_chave = {'nebula': TipoToken.NEBULA}
        
    def _parse_nebula(self) -> ConsultaPlaneta:
        self._esperar(TipoToken.NEBULA)
        self._esperar(TipoToken.EXIBIR)
        
        token = self._atual()
        
        if token.tipo == TipoToken.STRING:
            nome_planeta = String(token.valor)
            self._avancar()
        elif token.tipo == TipoToken.IDENTIFICADOR:
            nome_planeta = Variavel(token.valor)
            self._avancar()
        else:
            raise ErroSintatico(
                f"Esperado nome do planeta (string ou variável), encontrado {token.tipo.name}",
                token.linha, token.coluna
            )
        
        self._esperar(TipoToken.PONTO_VIRGULA)
        return ConsultaPlaneta(nome_planeta)

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

        if token.tipo in (TipoToken.FIM, TipoToken.SENAO, TipoToken.EOF):
            return None

        # Comando nebula (consulta a planetas)
        if token.tipo == TipoToken.NEBULA:
            return self._parse_nebula()
        elif token.tipo == TipoToken.CRIAR:
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
        elif token.tipo == TipoToken.LER:
            return self._parse_ler()
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

        # ✅ CORREÇÃO: Adicionar suporte a LER como expressão primária
        if token.tipo == TipoToken.LER:
            return self._parse_ler_como_expressao()

        raise ErroSintatico(
            f"Expressão inesperada: {token.tipo.name}",
            token.linha, token.coluna
        )
    
    def _parse_ler(self) -> Ler:
        self._esperar(TipoToken.LER)
        
        mensagem = None
        if self._atual().tipo == TipoToken.ABRE_PARENTESES:
            self._esperar(TipoToken.ABRE_PARENTESES)
            
            # Se tiver uma string, usa como mensagem
            if self._atual().tipo == TipoToken.STRING:
                mensagem = String(self._atual().valor)
                self._avancar()
            
            self._esperar(TipoToken.FECHA_PARENTESES)
        
        self._esperar(TipoToken.PONTO_VIRGULA)
        return Ler(mensagem)

    def _parse_ler_como_expressao(self) -> Ler:
        self._esperar(TipoToken.LER)
        
        mensagem = None

        if self._atual().tipo == TipoToken.ABRE_PARENTESES:
            self._esperar(TipoToken.ABRE_PARENTESES)
            
            if self._atual().tipo == TipoToken.STRING:
                mensagem = String(self._atual().valor)
                self._avancar()
            
            self._esperar(TipoToken.FECHA_PARENTESES)
        
        return Ler(mensagem)