# NEBULA Language Interpreter

Linguagem de programação didática para a disciplina de Construção de Interpretadores e Compiladores.

## 📁 Estrutura do Projeto

```
LINGUAGEM-NEBULA/
├── compilador/
│   ├── app.js
│   ├── index.html
│   ├── nebula_compiler.js
│   ├── README.md
│   ├── style.css
│   └── test.html
│
├── docs/
│   ├── ESPECIFICACAO_NEBULA.pdf
│   ├── INSTRUCOES_EXECUCAO.pdf
│   └── README.pdf
│
├── examples/
│   └── tests/
│       ├── teste_condicional.neb
│       ├── teste_erros_recuperaveis.neb
│       ├── teste_invalido.neb
│       ├── teste_precedencia.neb
│       └── programa_exemplo.neb
│
├── src/
│   ├── components/
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── runner.py
│   │   │
│   │   ├── interpreter/
│   │   │   ├── __init__.py
│   │   │   └── interpreter.py
│   │   │
│   │   ├── lexer/
│   │   │   ├── __init__.py
│   │   │   ├── lexer.py
│   │   │   └── tokens.py
│   │   │
│   │   ├── nebula_ast/
│   │   │   ├── __init__.py
│   │   │   └── nodes.py
│   │   │
│   │   └── parser/
│   │       ├── __init__.py
│   │       └── parser.py
│   │
│   ├── nebula.py
│   └── run_tests.py
│
├── meu_programa.neb
├── nebula_ler_aqui.pdf
└── README.md
```

## 🚀 Como Usar

### Executar um programa

```bash
# Na raiz do projeto
python src/nebula.py examples/programa_exemplo.neb

# Com modo verbose (mostra tokens e AST)
python src/nebula.py examples/programa_exemplo.neb -v

# Ou usando caminho absoluto/relativo
python src/nebula.py /caminho/para/meu_programa.neb
```

### Executar todos os testes

```bash
python src/run_tests.py
```

## 📝 Características da Linguagem

- **Palavras-chave em português**: `criar`, `se`, `senao`, `enquanto`, `exibir`
- **Blocos**: delimitados por `inicio` ... `fim`
- **Terminador**: statements terminam com `;`
- **Operadores lógicos**: `&&` (E), `||` (OU), `!` (NÃO)
- **Comentários**: `//` linha única, `/* */` bloco
- **Tipos**: números inteiros, reais, strings, booleanos

## 💻 Exemplo de Código

```nebula
// Declaração de variáveis
criar nome = "Mundo";
criar numero = 42;

// Saída
criar mensagem = "Olá, " + nome + "!";
exibir(mensagem);

// Condicional
se (numero > 40) inicio
    exibir("Número é maior que 40!");
fim

// Loop
enquanto (numero < 50) inicio
    exibir(numero);
    numero = numero + 1;
fim
```

## 🧪 Testes

Os testes estão em `examples/tests/`:

- `teste_condicional.neb` - Testa if/else
- `teste_precedencia.neb` - Testa precedência de operadores
- `teste_enquanto.neb` - Testa loops while

## 👥 Autores

- João Victor Rocha Santos
- Denis Filho Cunha Godoi

**Disciplina**: N477 - Construção de Interpretadores e Compiladores  
**Instituição**: Unitri
