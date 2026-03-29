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

Uso:
    python src/nebula.py examples/programa_exemplo.neb
    python src/nebula.py examples/tests/teste_condicional.neb -v
"""

import os
import sys

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.components.core.runner import NebulaRunner


def main():
    if len(sys.argv) < 2:
        print("Uso: python src/nebula.py examples/<arquivo.neb> [--verbose]")
        print("     python src/nebula.py --help")
        sys.exit(1)

    if sys.argv[1] in ('--help', '-h'):
        print("""
NEBULA LANGUAGE INTERPRETER
===========================

Uso: python src/nebula.py <caminho/arquivo.neb> [opções]

Opções:
  --verbose, -v    Mostra tokens e AST detalhados
  --help, -h       Mostra esta ajuda

Exemplos:
  python src/nebula.py examples/programa_exemplo.neb
  python src/nebula.py examples/tests/teste_condicional.neb -v
  python src/nebula.py ../meu_programa.neb
        """)
        sys.exit(0)

    arquivo = sys.argv[1]
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    runner = NebulaRunner(verbose=verbose)
    sucesso = runner.executar_arquivo(arquivo)

    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
