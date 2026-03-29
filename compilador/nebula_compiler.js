/**
 * NEBULA LANGUAGE COMPILER
 * Compilador/Interpretador completo em JavaScript
 */

// Token Types
const TipoToken = {
    CRIAR: 'CRIAR', SE: 'SE', SENAO: 'SENAO', ENQUANTO: 'ENQUANTO',
    DEFINIR: 'DEFINIR', RETORNAR: 'RETORNAR', EXIBIR: 'EXIBIR',
    INICIO: 'INICIO', FIM: 'FIM',
    NUMERO_INTEIRO: 'NUMERO_INTEIRO', NUMERO_REAL: 'NUMERO_REAL',
    STRING: 'STRING', BOOLEANO: 'BOOLEANO', IDENTIFICADOR: 'IDENTIFICADOR',
    SOMA: 'SOMA', SUBTRACAO: 'SUBTRACAO', MULTIPLICACAO: 'MULTIPLICACAO',
    DIVISAO: 'DIVISAO', MODULO: 'MODULO', POTENCIA: 'POTENCIA',
    IGUAL: 'IGUAL', DIFERENTE: 'DIFERENTE', MENOR: 'MENOR',
    MENOR_IGUAL: 'MENOR_IGUAL', MAIOR: 'MAIOR', MAIOR_IGUAL: 'MAIOR_IGUAL',
    E_LOGICO: 'E_LOGICO', OU_LOGICO: 'OU_LOGICO', NAO_LOGICO: 'NAO_LOGICO',
    ATRIBUICAO: 'ATRIBUICAO', PONTO_VIRGULA: 'PONTO_VIRGULA',
    VIRGULA: 'VIRGULA', DOIS_PONTOS: 'DOIS_PONTOS',
    ABRE_PARENTESES: 'ABRE_PARENTESES', FECHA_PARENTESES: 'FECHA_PARENTESES',
    EOF: 'EOF'
};

// Lexer
class AnalisadorLexico {
    constructor(codigo) {
        this.codigo = codigo;
        this.pos = 0;
        this.linha = 1;
        this.coluna = 1;
        this.tokens = [];
        this.palavrasChave = {
            'criar': TipoToken.CRIAR, 'se': TipoToken.SE, 'senao': TipoToken.SENAO,
            'enquanto': TipoToken.ENQUANTO, 'definir': TipoToken.DEFINIR,
            'retornar': TipoToken.RETORNAR, 'exibir': TipoToken.EXIBIR,
            'inicio': TipoToken.INICIO, 'fim': TipoToken.FIM,
            'verdadeiro': { tipo: TipoToken.BOOLEANO, valor: true },
            'falso': { tipo: TipoToken.BOOLEANO, valor: false }
        };
    }

    caractereAtual() {
        if (this.pos >= this.codigo.length) return null;
        return this.codigo[this.pos];
    }

    proximoCaractere() {
        if (this.pos + 1 >= this.codigo.length) return null;
        return this.codigo[this.pos + 1];
    }

    avancar() {
        if (this.pos < this.codigo.length && this.codigo[this.pos] === '\n') {
            this.linha++;
            this.coluna = 1;
        } else {
            this.coluna++;
        }
        this.pos++;
    }

    pularEspacos() {
        while (this.caractereAtual() && /\s/.test(this.caractereAtual())) {
            this.avancar();
        }
    }

    pularComentarioLinha() {
        while (this.caractereAtual() && this.caractereAtual() !== '\n') {
            this.avancar();
        }
    }

    pularComentarioBloco() {
        this.avancar(); this.avancar();
        while (this.caractereAtual()) {
            if (this.caractereAtual() === '*' && this.proximoCaractere() === '/') {
                this.avancar(); this.avancar();
                return;
            }
            this.avancar();
        }
        throw new Error(`Comentário de bloco não fechado na linha ${this.linha}`);
    }

    lerString() {
        let valor = "";
        this.avancar();
        while (this.caractereAtual() && this.caractereAtual() !== '"') {
            if (this.caractereAtual() === '\\') {
                this.avancar();
                const escape = this.caractereAtual();
                if (escape === 'n') valor += '\n';
                else if (escape === 't') valor += '\t';
                else if (escape === '\\') valor += '\\';
                else if (escape === '"') valor += '"';
                else valor += escape;
            } else {
                valor += this.caractereAtual();
            }
            this.avancar();
        }
        if (this.caractereAtual() !== '"') {
            throw new Error(`String não fechada na linha ${this.linha}`);
        }
        this.avancar();
        return valor;
    }

    lerNumero() {
        const linha = this.linha, coluna = this.coluna;
        let valor = "";
        while (this.caractereAtual() && (/\d/.test(this.caractereAtual()) || this.caractereAtual() === '.')) {
            valor += this.caractereAtual();
            this.avancar();
        }
        if (valor.includes('.')) {
            return { tipo: TipoToken.NUMERO_REAL, valor: parseFloat(valor), linha, coluna };
        }
        return { tipo: TipoToken.NUMERO_INTEIRO, valor: parseInt(valor), linha, coluna };
    }

    lerIdentificador() {
        const linha = this.linha, coluna = this.coluna;
        let valor = "";
        while (this.caractereAtual() && (/[a-zA-Z0-9_]/.test(this.caractereAtual()))) {
            valor += this.caractereAtual();
            this.avancar();
        }
        if (this.palavrasChave[valor]) {
            const info = this.palavrasChave[valor];
            if (info.tipo) return { tipo: info.tipo, valor: info.valor, linha, coluna };
            return { tipo: info, valor, linha, coluna };
        }
        return { tipo: TipoToken.IDENTIFICADOR, valor, linha, coluna };
    }

    analisar() {
        while (this.caractereAtual()) {
            this.pularEspacos();
            if (!this.caractereAtual()) break;

            const linha = this.linha, coluna = this.coluna, char = this.caractereAtual();

            if (char === '/' && this.proximoCaractere() === '/') {
                this.avancar(); this.avancar();
                this.pularComentarioLinha();
                continue;
            }

            if (char === '/' && this.proximoCaractere() === '*') {
                this.pularComentarioBloco();
                continue;
            }

            if (char === '"') {
                this.tokens.push({ tipo: TipoToken.STRING, valor: this.lerString(), linha, coluna });
                continue;
            }

            if (/\d/.test(char)) {
                this.tokens.push(this.lerNumero());
                continue;
            }

            if (/[a-zA-Z_]/.test(char)) {
                this.tokens.push(this.lerIdentificador());
                continue;
            }

            const doisChars = char + (this.proximoCaractere() || '');
            const ops2 = { '==': TipoToken.IGUAL, '!=': TipoToken.DIFERENTE, '<=': TipoToken.MENOR_IGUAL,
                '>=': TipoToken.MAIOR_IGUAL, '&&': TipoToken.E_LOGICO, '||': TipoToken.OU_LOGICO };

            if (ops2[doisChars]) {
                this.tokens.push({ tipo: ops2[doisChars], valor: doisChars, linha, coluna });
                this.avancar(); this.avancar();
                continue;
            }

            const ops1 = { '+': TipoToken.SOMA, '-': TipoToken.SUBTRACAO, '*': TipoToken.MULTIPLICACAO,
                '/': TipoToken.DIVISAO, '%': TipoToken.MODULO, '^': TipoToken.POTENCIA,
                '<': TipoToken.MENOR, '>': TipoToken.MAIOR, '!': TipoToken.NAO_LOGICO,
                '=': TipoToken.ATRIBUICAO, ';': TipoToken.PONTO_VIRGULA, ',': TipoToken.VIRGULA,
                ':': TipoToken.DOIS_PONTOS, '(': TipoToken.ABRE_PARENTESES, ')': TipoToken.FECHA_PARENTESES };

            if (ops1[char]) {
                this.tokens.push({ tipo: ops1[char], valor: char, linha, coluna });
                this.avancar();
                continue;
            }

            throw new Error(`Caractere inválido '${char}' na linha ${linha}, coluna ${coluna}`);
        }

        this.tokens.push({ tipo: TipoToken.EOF, valor: null, linha: this.linha, coluna: this.coluna });
        return this.tokens;
    }
}

// AST Node
class ASTNode {
    constructor(tipo, props = {}) {
        this.tipo = tipo;
        Object.assign(this, props);
    }
}

// Parser
class Parser {
    constructor(tokens) {
        this.tokens = tokens;
        this.pos = 0;
        this.erros = [];
    }

    atual() { return this.tokens[this.pos] || this.tokens[this.tokens.length - 1]; }
    avancar() { if (this.pos < this.tokens.length - 1) this.pos++; }

    esperar(tipo) {
        const token = this.atual();
        if (token.tipo !== tipo) {
            throw new Error(`Esperado ${tipo}, encontrado ${token.tipo} na linha ${token.linha}`);
        }
        this.avancar();
        return token;
    }

    parse() {
        const statements = [];
        while (this.atual().tipo !== TipoToken.EOF) {
            try {
                const stmt = this.parseStatement();
                if (stmt) statements.push(stmt);
            } catch (e) {
                this.erros.push(e.message);
                while (this.atual().tipo !== TipoToken.PONTO_VIRGULA && this.atual().tipo !== TipoToken.EOF) {
                    this.avancar();
                }
                if (this.atual().tipo === TipoToken.PONTO_VIRGULA) this.avancar();
            }
        }
        return new ASTNode('Programa', { statements });
    }

    parseStatement() {
        const token = this.atual();
        switch (token.tipo) {
            case TipoToken.CRIAR: return this.parseDeclaracao();
            case TipoToken.SE: return this.parseSe();
            case TipoToken.ENQUANTO: return this.parseEnquanto();
            case TipoToken.EXIBIR: return this.parseExibir();
            case TipoToken.IDENTIFICADOR: return this.parseAtribuicaoOuChamada();
            case TipoToken.INICIO: return this.parseBloco();
            case TipoToken.PONTO_VIRGULA: this.avancar(); return null;
            default:
                const expr = this.parseExpressao();
                this.esperar(TipoToken.PONTO_VIRGULA);
                return expr;
        }
    }

    parseDeclaracao() {
        this.esperar(TipoToken.CRIAR);
        const nome = this.esperar(TipoToken.IDENTIFICADOR).valor;
        let valor = null;
        if (this.atual().tipo === TipoToken.ATRIBUICAO) {
            this.avancar();
            valor = this.parseExpressao();
        }
        this.esperar(TipoToken.PONTO_VIRGULA);
        return new ASTNode('Declaracao', { nome, valor });
    }

    parseAtribuicaoOuChamada() {
        const nome = this.esperar(TipoToken.IDENTIFICADOR).valor;
        if (this.atual().tipo === TipoToken.ATRIBUICAO) {
            this.avancar();
            const valor = this.parseExpressao();
            this.esperar(TipoToken.PONTO_VIRGULA);
            return new ASTNode('Atribuicao', { nome, valor });
        }
        return new ASTNode('Variavel', { nome });
    }

    parseSe() {
        this.esperar(TipoToken.SE);
        this.esperar(TipoToken.ABRE_PARENTESES);
        const condicao = this.parseExpressao();
        this.esperar(TipoToken.FECHA_PARENTESES);
        const entao = this.parseBloco().statements;
        let senao = null;
        if (this.atual().tipo === TipoToken.SENAO) {
            this.avancar();
            senao = this.parseBloco().statements;
        }
        return new ASTNode('Se', { condicao, entao, senao });
    }

    parseEnquanto() {
        this.esperar(TipoToken.ENQUANTO);
        this.esperar(TipoToken.ABRE_PARENTESES);
        const condicao = this.parseExpressao();
        this.esperar(TipoToken.FECHA_PARENTESES);
        const corpo = this.parseBloco().statements;
        return new ASTNode('Enquanto', { condicao, corpo });
    }

    parseExibir() {
        this.esperar(TipoToken.EXIBIR);
        this.esperar(TipoToken.ABRE_PARENTESES);
        const expressao = this.parseExpressao();
        this.esperar(TipoToken.FECHA_PARENTESES);
        this.esperar(TipoToken.PONTO_VIRGULA);
        return new ASTNode('Exibir', { expressao });
    }

    parseBloco() {
        this.esperar(TipoToken.INICIO);
        const statements = [];
        while (this.atual().tipo !== TipoToken.FIM && this.atual().tipo !== TipoToken.EOF) {
            const stmt = this.parseStatement();
            if (stmt) statements.push(stmt);
        }
        this.esperar(TipoToken.FIM);
        return new ASTNode('Programa', { statements });
    }

    parseExpressao() { return this.parseOuLogico(); }

    parseOuLogico() {
        let node = this.parseELogico();
        while (this.atual().tipo === TipoToken.OU_LOGICO) {
            const op = this.atual(); this.avancar();
            node = new ASTNode('BinOp', { esquerda: node, operador: op, direita: this.parseELogico() });
        }
        return node;
    }

    parseELogico() {
        let node = this.parseIgualdade();
        while (this.atual().tipo === TipoToken.E_LOGICO) {
            const op = this.atual(); this.avancar();
            node = new ASTNode('BinOp', { esquerda: node, operador: op, direita: this.parseIgualdade() });
        }
        return node;
    }

    parseIgualdade() {
        let node = this.parseComparacao();
        while ([TipoToken.IGUAL, TipoToken.DIFERENTE].includes(this.atual().tipo)) {
            const op = this.atual(); this.avancar();
            node = new ASTNode('BinOp', { esquerda: node, operador: op, direita: this.parseComparacao() });
        }
        return node;
    }

    parseComparacao() {
        let node = this.parseAdicao();
        const comps = [TipoToken.MENOR, TipoToken.MENOR_IGUAL, TipoToken.MAIOR, TipoToken.MAIOR_IGUAL];
        while (comps.includes(this.atual().tipo)) {
            const op = this.atual(); this.avancar();
            node = new ASTNode('BinOp', { esquerda: node, operador: op, direita: this.parseAdicao() });
        }
        return node;
    }

    parseAdicao() {
        let node = this.parseMultiplicacao();
        while ([TipoToken.SOMA, TipoToken.SUBTRACAO].includes(this.atual().tipo)) {
            const op = this.atual(); this.avancar();
            node = new ASTNode('BinOp', { esquerda: node, operador: op, direita: this.parseMultiplicacao() });
        }
        return node;
    }

    parseMultiplicacao() {
        let node = this.parsePotencia();
        while ([TipoToken.MULTIPLICACAO, TipoToken.DIVISAO, TipoToken.MODULO].includes(this.atual().tipo)) {
            const op = this.atual(); this.avancar();
            node = new ASTNode('BinOp', { esquerda: node, operador: op, direita: this.parsePotencia() });
        }
        return node;
    }

    parsePotencia() {
        let node = this.parseUnario();
        if (this.atual().tipo === TipoToken.POTENCIA) {
            const op = this.atual(); this.avancar();
            return new ASTNode('BinOp', { esquerda: node, operador: op, direita: this.parsePotencia() });
        }
        return node;
    }

    parseUnario() {
        if ([TipoToken.NAO_LOGICO, TipoToken.SUBTRACAO].includes(this.atual().tipo)) {
            const op = this.atual(); this.avancar();
            return new ASTNode('UnaryOp', { operador: op, operando: this.parseUnario() });
        }
        return this.parsePrimario();
    }

    parsePrimario() {
        const token = this.atual();
        switch (token.tipo) {
            case TipoToken.NUMERO_INTEIRO:
            case TipoToken.NUMERO_REAL: this.avancar(); return new ASTNode('Numero', { valor: token.valor });
            case TipoToken.STRING: this.avancar(); return new ASTNode('String', { valor: token.valor });
            case TipoToken.BOOLEANO: this.avancar(); return new ASTNode('Booleano', { valor: token.valor });
            case TipoToken.IDENTIFICADOR: this.avancar(); return new ASTNode('Variavel', { nome: token.valor });
            case TipoToken.ABRE_PARENTESES:
                this.avancar();
                const node = this.parseExpressao();
                this.esperar(TipoToken.FECHA_PARENTESES);
                return node;
            default:
                throw new Error(`Expressão inesperada: ${token.tipo} na linha ${token.linha}`);
        }
    }
}

// Interpreter
class Interpretador {
    constructor(outputCallback) {
        this.variaveis = {};
        this.escopos = [this.variaveis];
        this.output = outputCallback || console.log;
    }

    executar(node) {
        const method = `executar${node.tipo}`;
        if (this[method]) return this[method](node);
        throw new Error(`Tipo não suportado: ${node.tipo}`);
    }

    executarPrograma(node) {
        let resultado;
        for (const stmt of node.statements) resultado = this.executar(stmt);
        return resultado;
    }

    executarNumero(node) { return node.valor; }
    executarString(node) { return node.valor; }
    executarBooleano(node) { return node.valor; }

    executarVariavel(node) {
        for (let i = this.escopos.length - 1; i >= 0; i--) {
            if (node.nome in this.escopos[i]) return this.escopos[i][node.nome];
        }
        throw new Error(`Variável '${node.nome}' não declarada`);
    }

    executarDeclaracao(node) {
        const valor = node.valor ? this.executar(node.valor) : null;
        this.escopos[this.escopos.length - 1][node.nome] = valor;
        return valor;
    }

    executarAtribuicao(node) {
        const valor = this.executar(node.valor);
        for (let i = this.escopos.length - 1; i >= 0; i--) {
            if (node.nome in this.escopos[i]) {
                this.escopos[i][node.nome] = valor;
                return valor;
            }
        }
        this.escopos[this.escopos.length - 1][node.nome] = valor;
        return valor;
    }

    executarBinOp(node) {
        const esq = this.executar(node.esquerda);
        const dir = this.executar(node.direita);
        const op = node.operador.tipo;

        switch (op) {
            case TipoToken.SOMA: return (typeof esq === 'string' || typeof dir === 'string') ? String(esq) + String(dir) : esq + dir;
            case TipoToken.SUBTRACAO: return esq - dir;
            case TipoToken.MULTIPLICACAO: return esq * dir;
            case TipoToken.DIVISAO: if (dir === 0) throw new Error('Divisão por zero'); return esq / dir;
            case TipoToken.MODULO: return esq % dir;
            case TipoToken.POTENCIA: return Math.pow(esq, dir);
            case TipoToken.IGUAL: return esq === dir;
            case TipoToken.DIFERENTE: return esq !== dir;
            case TipoToken.MENOR: return esq < dir;
            case TipoToken.MENOR_IGUAL: return esq <= dir;
            case TipoToken.MAIOR: return esq > dir;
            case TipoToken.MAIOR_IGUAL: return esq >= dir;
            case TipoToken.E_LOGICO: return esq && dir;
            case TipoToken.OU_LOGICO: return esq || dir;
            default: throw new Error(`Operador desconhecido: ${op}`);
        }
    }

    executarUnaryOp(node) {
        const operando = this.executar(node.operando);
        const op = node.operador.tipo;
        if (op === TipoToken.NAO_LOGICO) return !operando;
        if (op === TipoToken.SUBTRACAO) return -operando;
        throw new Error(`Operador unário desconhecido: ${op}`);
    }

    executarSe(node) {
        if (this.executar(node.condicao)) {
            this.escopos.push({});
            try { for (const stmt of node.entao) this.executar(stmt); }
            finally { this.escopos.pop(); }
        } else if (node.senao) {
            this.escopos.push({});
            try { for (const stmt of node.senao) this.executar(stmt); }
            finally { this.escopos.pop(); }
        }
    }

    executarEnquanto(node) {
        while (this.executar(node.condicao)) {
            this.escopos.push({});
            try { for (const stmt of node.corpo) this.executar(stmt); }
            finally { this.escopos.pop(); }
        }
    }

    executarExibir(node) {
        const valor = this.executar(node.expressao);
        this.output(valor);
        return valor;
    }
}

// Main Compiler Class
class NebulaCompiler {
    constructor() {
        this.tokens = [];
        this.ast = null;
    }

    compile(codigo) {
        const lexer = new AnalisadorLexico(codigo);
        this.tokens = lexer.analisar();

        const parser = new Parser(this.tokens);
        this.ast = parser.parse();

        if (parser.erros.length > 0) {
            return { success: false, errors: parser.erros, stage: 'parser' };
        }
        return { success: true, tokens: this.tokens, ast: this.ast };
    }

    execute(codigo, outputCallback) {
        const result = this.compile(codigo);
        if (!result.success) return result;

        try {
            const interpreter = new Interpretador(outputCallback);
            interpreter.executar(this.ast);
            return { success: true, tokens: this.tokens, ast: this.ast };
        } catch (e) {
            return { success: false, errors: [e.message], stage: 'runtime' };
        }
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { NebulaCompiler, AnalisadorLexico, Parser, Interpretador, TipoToken };
}
