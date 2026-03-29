"""
Core Runner - Orquestra a execução do interpretador Nebula.
"""

import sys
from pathlib import Path

# Adiciona src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.components.lexer import AnalisadorLexico
from src.components.parser import Parser
from src.components.interpreter import Interpretador, ErroExecucao


class NebulaRunner:
    """Orquestra a execução completa: lexer -> parser -> interpreter."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.tokens = []
        self.ast = None
        self.erros = []

    def executar_arquivo(self, caminho: str) -> bool:
        """Executa um arquivo Nebula completo."""
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                codigo = f.read()
        except FileNotFoundError:
            print(f"✗ Erro: Arquivo '{caminho}' não encontrado.")
            return False
        except Exception as e:
            print(f"✗ Erro ao ler arquivo: {e}")
            return False

        return self.executar_codigo(codigo)

    def executar_codigo(self, codigo: str) -> bool:
        """Executa código Nebula diretamente."""

        # Análise Léxica
        print("\n[1] ANÁLISE LÉXICA")
        print("-" * 40)
        try:
            lexer = AnalisadorLexico(codigo)
            self.tokens = lexer.analisar()
            if self.verbose:
                for token in self.tokens:
                    print(f"  {token}")
            print(f"✓ {len(self.tokens)} tokens gerados")
        except SyntaxError as e:
            print(f"✗ Erro léxico: {e}")
            return False

        # Análise Sintática
        print("\n[2] ANÁLISE SINTÁTICA")
        print("-" * 40)
        try:
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            if parser.erros:
                self.erros.extend(parser.erros)
                print(f"! {len(parser.erros)} erro(s) sintático(s) encontrado(s)")
            if self.verbose:
                print(f"  AST: {self.ast}")
            print(f"✓ AST gerada com {len(self.ast.statements)} statement(s)")
        except Exception as e:
            print(f"✗ Erro sintático: {e}")
            return False

        # Execução
        print("\n[3] SAÍDA DO PROGRAMA")
        print("-" * 40)
        try:
            interpretador = Interpretador()
            interpretador.executar(self.ast)
            print("-" * 40)
            print("✓ Execução finalizada")
        except ErroExecucao as e:
            print(f"✗ Erro em tempo de execução: {e}")
            return False
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")
            return False

        print("\n" + "=" * 60)
        return True
