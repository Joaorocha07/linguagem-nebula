"""
Analisador Léxico (Lexer) para a linguagem Nebula.
Converte código fonte em uma lista de tokens.
"""

from typing import List, Optional
from .tokens import TipoToken, Token


class AnalisadorLexico:
    """Analisador léxico que converte código fonte em tokens."""

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
            'ler': TipoToken.LER,
            'inicio': TipoToken.INICIO,
            'fim': TipoToken.FIM,
            'verdadeiro': (TipoToken.BOOLEANO, True),
            'falso': (TipoToken.BOOLEANO, False),
        }

        self.palavras_chave['nebula'] = TipoToken.NEBULA

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
        """Executa a análise léxica e retorna a lista de tokens."""
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
