/**
 * NEBULA IDE - Application Logic
 * Interface e interatividade do compilador online
 */

// Instância do compilador
const compiler = new NebulaCompiler();

// Elementos DOM
const codeEditor = document.getElementById('codeEditor');
const lineNumbers = document.getElementById('lineNumbers');
const consoleOutput = document.getElementById('consoleOutput');
const tokensOutput = document.getElementById('tokensOutput');
const astOutput = document.getElementById('astOutput');
const tokenCount = document.getElementById('tokenCount');

// Exemplos de código
const examples = {
    hello: `// Olá Mundo em Nebula
criar mensagem = "Olá, Mundo!";
exibir(mensagem);

// Também funciona com números
criar numero = 42;
exibir(numero);`,

    math: `// Operações matemáticas
criar a = 10;
criar b = 3;

exibir("Soma:");
exibir(a + b);

exibir("Subtração:");
exibir(a - b);

exibir("Multiplicação:");
exibir(a * b);

exibir("Divisão:");
exibir(a / b);

exibir("Potência (2^10):");
criar pot = 2 ^ 10;
exibir(pot);

exibir("Resto da divisão:");
exibir(a % b);`,

    loop: `// Loop enquanto (while)
criar contador = 1;

exibir("Contando de 1 a 5:");

enquanto (contador <= 5) inicio
    exibir(contador);
    contador = contador + 1;
fim

exibir("Fim do loop!");`,

    conditional: `// Condicionais
criar idade = 18;

se (idade >= 18) inicio
    exibir("Maior de idade");
fim
senao inicio
    exibir("Menor de idade");
fim

// Condicional com operadores lógicos
criar nota = 75;

se (nota >= 60 && nota < 80) inicio
    exibir("Aprovado com nota B");
fim`,

    complex: `/*
 * Programa completo Nebula
 * Demonstra variáveis, operações, condicionais e loops
 */

// Declarações
criar nome = "Nebula";
criar versao = 1.0;
criar ativo = verdadeiro;

// String concatenation
criar apresentacao = "Bem-vindo ao " + nome + " v" + versao;
exibir(apresentacao);

// Operações matemáticas complexas
criar resultado = (10 + 5) * 2 - 3;
exibir("Resultado: " + resultado);

// Condicional aninhada
criar x = 15;

se (x > 10) inicio
    se (x < 20) inicio
        exibir("x está entre 10 e 20");
    fim
fim

// Loop com condição
criar i = 0;
enquanto (i < 3) inicio
    exibir("Iteração: " + i);
    i = i + 1;
fim

exibir("Programa finalizado!");`
};

// Documentação
const documentation = {
    variables: {
        title: 'Variáveis',
        content: `
            <div class="doc-section">
                <h3>Declaração de Variáveis</h3>
                <p>Use a palavra-chave <code>criar</code> para declarar variáveis:</p>
                <pre><code>criar nome = "João";
criar idade = 25;
criar preco = 19.99;
criar ativo = verdadeiro;</code></pre>

                <h3>Tipos Suportados</h3>
                <p><span class="keyword-tag">string</span> <span class="keyword-tag">inteiro</span> <span class="keyword-tag">real</span> <span class="keyword-tag">booleano</span></p>

                <h3>Atribuição</h3>
                <pre><code>criar x = 10;
x = 20;  // Reatribuição</code></pre>
            </div>
        `
    },
    operators: {
        title: 'Operadores',
        content: `
            <div class="doc-section">
                <h3>Aritméticos</h3>
                <p><span class="keyword-tag">+</span> <span class="keyword-tag">-</span> <span class="keyword-tag">*</span> <span class="keyword-tag">/</span> <span class="keyword-tag">%</span> <span class="keyword-tag">^</span></p>
                <pre><code>criar soma = 10 + 5;
criar potencia = 2 ^ 8;</code></pre>

                <h3>Relacionais</h3>
                <p><span class="keyword-tag">==</span> <span class="keyword-tag">!=</span> <span class="keyword-tag"><</span> <span class="keyword-tag"><=</span> <span class="keyword-tag">></span> <span class="keyword-tag">>=</span></p>

                <h3>Lógicos</h3>
                <p><span class="keyword-tag">&&</span> (E) <span class="keyword-tag">||</span> (OU) <span class="keyword-tag">!</span> (NÃO)</p>
            </div>
        `
    },
    control: {
        title: 'Estruturas de Controle',
        content: `
            <div class="doc-section">
                <h3>Condicional (if/else)</h3>
                <pre><code>se (condicao) inicio
    // código
fim
senao inicio
    // código alternativo
fim</code></pre>

                <h3>Loop (while)</h3>
                <pre><code>enquanto (condicao) inicio
    // código repetido
fim</code></pre>

                <h3>Blocos</h3>
                <p>Todos os blocos usam <code>inicio</code> ... <code>fim</code></p>
            </div>
        `
    },
    io: {
        title: 'Entrada e Saída',
        content: `
            <div class="doc-section">
                <h3>Saída (exibir)</h3>
                <pre><code>exibir("Hello World");
exibir(variavel);
exibir(10 + 20);</code></pre>

                <h3>Concatenação</h3>
                <pre><code>criar msg = "Valor: " + 42;
exibir(msg);</code></pre>
            </div>
        `
    }
};

// Atualizar números de linha
function updateLineNumbers() {
    const lines = codeEditor.value.split('\n').length;
    lineNumbers.innerHTML = Array.from({ length: Math.max(lines, 1) }, (_, i) => i + 1).join('<br>');
}

// Scroll sincronizado
codeEditor.addEventListener('scroll', () => {
    lineNumbers.scrollTop = codeEditor.scrollTop;
});

// Atualizar linhas ao digitar
codeEditor.addEventListener('input', () => {
    updateLineNumbers();
    updateCursorPosition();
});

// Atualizar posição do cursor
function updateCursorPosition() {
    const pos = codeEditor.selectionStart;
    const text = codeEditor.value.substring(0, pos);
    const lines = text.split('\n');
    const line = lines.length;
    const col = lines[lines.length - 1].length + 1;
    document.querySelector('.cursor-position').textContent = `Ln ${line}, Col ${col}`;
}

codeEditor.addEventListener('click', updateCursorPosition);
codeEditor.addEventListener('keyup', updateCursorPosition);

// Executar código
function runCode() {
    const code = codeEditor.value;
    if (!code.trim()) {
        showConsoleMessage('Digite algum código para executar!', 'error');
        return;
    }

    // Limpar console
    consoleOutput.innerHTML = '';

    // Executar
    const outputLines = [];
    const outputCallback = (value) => {
        outputLines.push(value);
        addConsoleLine(value, 'output');
    };

    const result = compiler.execute(code, outputCallback);

    if (!result.success) {
        result.errors.forEach(err => addConsoleLine(err, 'error'));
        showStatus('Erro na execução', 'error');
    } else {
        showStatus('Execução concluída', 'success');

        // Atualizar painéis
        updateTokensPanel(result.tokens);
        updateAstPanel(result.ast);

        // Atualizar contador
        tokenCount.innerHTML = `<i class="fas fa-coins"></i> ${result.tokens.length - 1} tokens`;
    }
}

// Adicionar linha ao console
function addConsoleLine(text, type = 'output') {
    const line = document.createElement('div');
    line.className = `console-line ${type}`;

    if (type === 'output') {
        line.innerHTML = `<span class="console-prompt">➜</span> ${escapeHtml(String(text))}`;
    } else {
        line.innerHTML = `<span class="console-prompt" style="color: var(--error)">✗</span> ${escapeHtml(String(text))}`;
    }

    consoleOutput.appendChild(line);
    consoleOutput.scrollTop = consoleOutput.scrollHeight;
}

// Mostrar mensagem no console
function showConsoleMessage(text, type = 'info') {
    consoleOutput.innerHTML = `
        <div class="console-welcome">
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <p>${text}</p>
        </div>
    `;
}

// Atualizar painel de tokens
function updateTokensPanel(tokens) {
    if (!tokens || tokens.length === 0) {
        tokensOutput.innerHTML = '<p class="empty-state">Nenhum token gerado</p>';
        return;
    }

    const html = tokens.filter(t => t.tipo !== 'EOF').map(token => `
        <div class="token-item">
            <span class="token-type">${token.tipo}</span>
            <span class="token-value">${token.valor !== null ? escapeHtml(String(token.valor)) : 'null'}</span>
            <span class="token-pos">Ln ${token.linha}, Col ${token.coluna}</span>
        </div>
    `).join('');

    tokensOutput.innerHTML = html;
}

// Atualizar painel AST
function updateAstPanel(ast) {
    if (!ast) {
        astOutput.innerHTML = '<p class="empty-state">AST não disponível</p>';
        return;
    }

    astOutput.innerHTML = renderAstNode(ast);
}

function renderAstNode(node, level = 0) {
    if (!node) return '';

    const indent = '  '.repeat(level);
    let content = '';

    if (node.tipo === 'Programa') {
        content = `<div class="ast-node">
            <div class="ast-node-header" onclick="toggleNode(this)">
                <i class="fas fa-chevron-down"></i>
                <span class="ast-node-type">Programa</span>
                <span class="ast-node-value">(${node.statements.length} statements)</span>
            </div>
            <div class="ast-children">
                ${node.statements.map(s => renderAstNode(s, level + 1)).join('')}
            </div>
        </div>`;
    } else if (node.tipo === 'Declaracao') {
        content = `<div class="ast-node" style="margin-left: ${level * 20}px">
            <span class="ast-node-type">Declaracao</span>
            <span class="ast-node-value">${node.nome}${node.valor ? ' = ' + formatNodeValue(node.valor) : ''}</span>
        </div>`;
    } else if (node.tipo === 'Atribuicao') {
        content = `<div class="ast-node" style="margin-left: ${level * 20}px">
            <span class="ast-node-type">Atribuicao</span>
            <span class="ast-node-value">${node.nome} = ${formatNodeValue(node.valor)}</span>
        </div>`;
    } else if (node.tipo === 'Exibir') {
        content = `<div class="ast-node" style="margin-left: ${level * 20}px">
            <span class="ast-node-type">Exibir</span>
            <span class="ast-node-value">${formatNodeValue(node.expressao)}</span>
        </div>`;
    } else if (node.tipo === 'Se') {
        content = `<div class="ast-node">
            <div class="ast-node-header" onclick="toggleNode(this)">
                <i class="fas fa-chevron-down"></i>
                <span class="ast-node-type">Se</span>
            </div>
            <div class="ast-children">
                <div style="margin-left: ${(level + 1) * 20}px">cond: ${formatNodeValue(node.condicao)}</div>
                ${node.entao.map(s => renderAstNode(s, level + 1)).join('')}
                ${node.senao ? '<div style="margin-left: ' + (level + 1) * 20 + 'px">senao:</div>' + node.senao.map(s => renderAstNode(s, level + 1)).join('') : ''}
            </div>
        </div>`;
    } else if (node.tipo === 'Enquanto') {
        content = `<div class="ast-node">
            <div class="ast-node-header" onclick="toggleNode(this)">
                <i class="fas fa-chevron-down"></i>
                <span class="ast-node-type">Enquanto</span>
            </div>
            <div class="ast-children">
                <div style="margin-left: ${(level + 1) * 20}px">cond: ${formatNodeValue(node.condicao)}</div>
                ${node.corpo.map(s => renderAstNode(s, level + 1)).join('')}
            </div>
        </div>`;
    } else if (node.tipo === 'BinOp') {
        content = `<div class="ast-node" style="margin-left: ${level * 20}px">
            <span class="ast-node-type">BinOp</span>
            <span class="ast-node-value">${node.operador.valor || node.operador.tipo}</span>
        </div>`;
    } else if (node.tipo === 'Numero' || node.tipo === 'String' || node.tipo === 'Booleano') {
        content = `<div class="ast-node" style="margin-left: ${level * 20}px">
            <span class="ast-node-type">${node.tipo}</span>
            <span class="ast-node-value">${escapeHtml(String(node.valor))}</span>
        </div>`;
    } else if (node.tipo === 'Variavel') {
        content = `<div class="ast-node" style="margin-left: ${level * 20}px">
            <span class="ast-node-type">Variavel</span>
            <span class="ast-node-value">${node.nome}</span>
        </div>`;
    } else {
        content = `<div class="ast-node" style="margin-left: ${level * 20}px">
            <span class="ast-node-type">${node.tipo}</span>
        </div>`;
    }

    return content;
}

function formatNodeValue(node) {
    if (!node) return 'null';
    if (node.tipo === 'Numero' || node.tipo === 'String' || node.tipo === 'Booleano') {
        return escapeHtml(String(node.valor));
    }
    if (node.tipo === 'Variavel') return node.nome;
    if (node.tipo === 'BinOp') return `(${formatNodeValue(node.esquerda)} ${node.operador.valor || node.operador.tipo} ${formatNodeValue(node.direita)})`;
    return node.tipo;
}

function toggleNode(header) {
    const children = header.nextElementSibling;
    if (children) {
        children.style.display = children.style.display === 'none' ? 'block' : 'none';
        header.querySelector('i').classList.toggle('fa-chevron-right');
        header.querySelector('i').classList.toggle('fa-chevron-down');
    }
}

// Carregar exemplo
function loadExampleCode(example) {
    if (examples[example]) {
        codeEditor.value = examples[example];
        updateLineNumbers();
        showConsoleMessage(`Exemplo "${example}" carregado. Clique em Executar!`, 'info');
    }
}

// Mostrar documentação
function showDoc(topic) {
    const doc = documentation[topic];
    if (doc) {
        document.getElementById('docTitle').textContent = doc.title;
        document.getElementById('docContent').innerHTML = doc.content;
        document.getElementById('docModal').classList.add('active');
    }
}

function closeDoc() {
    document.getElementById('docModal').classList.remove('active');
}

// Alternar painéis
function switchPanel(panel) {
    document.querySelectorAll('.panel-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));

    event.target.classList.add('active');
    document.getElementById(panel + 'Panel').classList.add('active');
}

// Limpar tudo
function clearAll() {
    codeEditor.value = '';
    consoleOutput.innerHTML = `
        <div class="console-welcome">
            <i class="fas fa-rocket"></i>
            <p>Bem-vindo ao Nebula IDE!</p>
            <p class="hint">Escreva seu código e clique em "Executar" para começar.</p>
        </div>
    `;
    tokensOutput.innerHTML = '<p class="empty-state">Execute o código para ver os tokens gerados.</p>';
    astOutput.innerHTML = '<p class="empty-state">Execute o código para ver a AST.</p>';
    tokenCount.innerHTML = '<i class="fas fa-coins"></i> 0 tokens';
    updateLineNumbers();
}

// Copiar código
function copyCode() {
    codeEditor.select();
    document.execCommand('copy');

    const btn = event.target.closest('.icon-btn');
    const original = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-check"></i>';
    setTimeout(() => btn.innerHTML = original, 1000);
}

// Mostrar status
function showStatus(message, type) {
    const statusBar = document.querySelector('.status-bar');
    const statusLeft = document.querySelector('.status-left');

    const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle';
    const color = type === 'success' ? '#89d185' : type === 'error' ? '#f14c4c' : '#3794ff';

    statusLeft.innerHTML = `
        <span class="status-item" style="color: ${color}">
            <i class="fas fa-${icon}"></i> ${message}
        </span>
    `;

    setTimeout(() => {
        statusLeft.innerHTML = `
            <span class="status-item"><i class="fas fa-check-circle"></i> Pronto</span>
            <span class="status-item" id="tokenCount"><i class="fas fa-coins"></i> 0 tokens</span>
        `;
    }, 3000);
}

// Utilitários
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Fechar modal ao clicar fora
document.getElementById('docModal').addEventListener('click', (e) => {
    if (e.target.id === 'docModal') closeDoc();
});

// Atalhos de teclado
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        runCode();
    }
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        clearAll();
    }
});

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    updateLineNumbers();
    loadExampleCode('hello');
});
