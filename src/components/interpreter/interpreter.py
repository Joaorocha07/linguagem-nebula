"""
Interpretador para a linguagem Nebula.
Executa a AST gerada pelo parser.
"""

from typing import Any, Dict, List
import sqlite3
from pathlib import Path
from src.components.lexer.tokens import TipoToken
from src.components.nebula_ast.nodes import *
from src.components.parser.parser import ConsultaPlaneta


class ErroExecucao(Exception):
    pass

class Interpretador:
    """Interpretador que executa a AST."""

    def __init__(self, banco_db: str = "nebula.db"):
        self.variaveis: Dict[str, Any] = {}
        self.escopos: List[Dict[str, Any]] = [self.variaveis]
        self.banco_db = banco_db
        self.verificar_banco()

    def verificar_banco(self) -> None:
        """Verifica se o banco de dados existe."""
        if not Path(self.banco_db).exists():
            raise ErroExecucao(f"Banco de dados '{self.banco_db}' não encontrado. Execute primeiro o script de criação.")

    def executar(self, node: ASTNode) -> Any:
        """Método principal de execução - dispacha para o método específico."""
        method_name = f'_executar_{type(node).__name__}'
        method = getattr(self, method_name, self._executar_generico)
        return method(node)
    
    def conectar(self) -> sqlite3.Connection:
        return sqlite3.connect(self.banco_db)

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
    
    def _executar_Ler(self, node: Ler) -> str:
        """Executa leitura de entrada do usuário."""
        # Exibe mensagem se houver
        if node.mensagem:
            print(node.mensagem.valor, end="")
        else:
            print("> ", end="")
        
        # Lê entrada do usuário
        try:
            valor = input()
            return valor
        except EOFError:
            return ""

    def _executar_ConsultaPlaneta(self, node: 'ConsultaPlaneta'):
        """Executa consulta ao banco de dados de planetas."""
        valor_nome = self.executar(node.nome)
        nome_planeta = str(valor_nome)
        
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            
            # Busca case-insensitive
            cursor.execute("""
                SELECT nome, tipo, distancia_sol, diametro, massa, 
                       luas, ano_orbital, temperatura_media, observacao
                FROM planetas
                WHERE LOWER(nome) = LOWER(?)
            """, (nome_planeta,))
            
            resultado = cursor.fetchone()
            
            if resultado is None:
                print(f"❌ Planeta '{nome_planeta}' não encontrado no banco de dados Nebula.")
                print("💡 Planetas disponíveis: Mercúrio, Vênus, Terra, Marte, Júpiter, Saturno, Urano, Netuno")
                return None
            
            nome, tipo, distancia, diametro, massa, luas, ano, temp, observacao = resultado
            
            # Formatação bonita da saída
            print("\n" + "=" * 70)
            print(f"  🪐  {nome.upper()}")
            print("=" * 70)
            print(f"  📊 Tipo: {tipo}")
            print(f"  🌞 Distância do Sol: {distancia} milhões de km")
            print(f"  📏 Diâmetro: {diametro:,} km")
            print(f"  ⚖️  Massa: {massa}")
            print(f"  🌙 Luas: {luas}")
            print(f"  🗓️  Ano orbital: {ano} dias terrestres")
            print(f"  🌡️  Temperatura média: {temp}°C")
            print("-" * 70)
            print(f"  💡 Observação:")
            print(f"     {observacao}")
            print("=" * 70 + "\n")
            
            return nome
        