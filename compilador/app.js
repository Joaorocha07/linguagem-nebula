/**
 * NEBULA IDE - Application Logic com Input Embutido no Console
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

// Fila de inputs pendentes
let inputQueue = [];
let inputResolve = null;
let isWaitingInput = false;

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

    input: `// Entrada de dados com ler()
exibir("=== Cadastro ===");

criar nome = ler("Digite seu nome: ");
criar idade = ler("Digite sua idade: ");

exibir("");
exibir("Dados cadastrados:");
exibir("Nome: " + nome);
exibir("Idade: " + idade);`,

    planetas: `// ============================================
// SISTEMA DE CONSULTA ASTRONOMICA NEBULA
// ============================================

exibir("");
exibir("╔════════════════════════════════════════════════════════════╗");
exibir("║     🌌  SISTEMA DE CONSULTA ASTRONOMICA NEBULA  🌌       ║");
exibir("╚════════════════════════════════════════════════════════════╝");
exibir("");

// Exibe o menu
exibir(">>> PLANETAS DISPONIVEIS:");
exibir("   Mercurio, Venus, Terra, Marte, Jupiter, Saturno, Urano, Netuno");
exibir("");

// Loop principal do menu
criar continuar = verdadeiro;

enquanto (continuar) inicio
    exibir("");
    criar planeta = ler("Digite o nome do planeta (ou 'sair' para encerrar): ");
    
    se (planeta == "sair") inicio
        continuar = falso;
        exibir("Encerrando sistema...");
    fim
    senao inicio
        exibir("");
        exibir(">>> Consultando informacoes sobre " + planeta + "...");
        nebula exibir planeta;
    fim
fim

exibir("");
exibir("Obrigado por usar o Sistema Nebula!");`,

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

                <h3>Entrada (ler)</h3>
                <pre><code>criar nome = ler("Digite seu nome: ");
exibir("Olá, " + nome);</code></pre>
                <p>O input aparece diretamente no console!</p>

                <h3>Consulta Planetas (nebula)</h3>
                <pre><code>// Consulta direta
nebula exibir "Terra";

// Com variável
criar planeta = ler("Qual planeta? ");
nebula exibir planeta;</code></pre>
                <p>Planetas disponíveis: Mercurio, Venus, Terra, Marte, Jupiter, Saturno, Urano, Netuno</p>
            </div>
        `
    },
    database: {
        title: 'Banco de Dados Nebula',
        content: `
            <div class="doc-section">
                <h3>🌌 Comando nebula</h3>
                <p>O comando <code>nebula</code> permite consultar informações astronômicas do banco de dados SQLite integrado.</p>
                
                <h3>Sintaxe</h3>
                <pre><code>// Consultar planeta específico
nebula exibir "NomeDoPlaneta";

// Usando variável
criar planeta = "Terra";
nebula exibir planeta;</code></pre>

                <h3>🪐 Planetas Disponíveis</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 12px 0;">
                    <div style="background: var(--bg-tertiary); padding: 8px; border-radius: 4px;">
                        <strong style="color: var(--accent-orange);">Mercurio</strong><br>
                        <small>Planeta Rochoso • 57.9 milhões km</small>
                    </div>
                    <div style="background: var(--bg-tertiary); padding: 8px; border-radius: 4px;">
                        <strong style="color: var(--accent-yellow);">Venus</strong><br>
                        <small>Planeta Rochoso • 108.2 milhões km</small>
                    </div>
                    <div style="background: var(--bg-tertiary); padding: 8px; border-radius: 4px;">
                        <strong style="color: var(--accent-blue);">Terra</strong><br>
                        <small>Planeta Rochoso • 149.6 milhões km</small>
                    </div>
                    <div style="background: var(--bg-tertiary); padding: 8px; border-radius: 4px;">
                        <strong style="color: var(--accent-red);">Marte</strong><br>
                        <small>Planeta Rochoso • 227.9 milhões km</small>
                    </div>
                    <div style="background: var(--bg-tertiary); padding: 8px; border-radius: 4px;">
                        <strong style="color: var(--accent-orange);">Jupiter</strong><br>
                        <small>Planeta Gasoso • 778.5 milhões km</small>
                    </div>
                    <div style="background: var(--bg-tertiary); padding: 8px; border-radius: 4px;">
                        <strong style="color: var(--accent-yellow);">Saturno</strong><br>
                        <small>Planeta Gasoso • 1.434 milhões km</small>
                    </div>
                    <div style="background: var(--bg-tertiary); padding: 8px; border-radius: 4px;">
                        <strong style="color: var(--accent-cyan);">Urano</strong><br>
                        <small>Planeta Gasoso • 2.871 milhões km</small>
                    </div>
                    <div style="background: var(--bg-tertiary); padding: 8px; border-radius: 4px;">
                        <strong style="color: var(--accent-blue);">Netuno</strong><br>
                        <small>Planeta Gasoso • 4.495 milhões km</small>
                    </div>
                </div>

                <h3>📊 Dados Retornados</h3>
                <p>Para cada planeta, o sistema exibe:</p>
                <ul style="margin-left: 20px; line-height: 1.8;">
                    <li><strong>Nome</strong> - Nome do planeta</li>
                    <li><strong>Tipo</strong> - Rochoso ou Gasoso</li>
                    <li><strong>Distância do Sol</strong> - Em milhões de km</li>
                    <li><strong>Diâmetro</strong> - Em km</li>
                    <li><strong>Massa</strong> - Em kg (notação científica)</li>
                    <li><strong>Luas</strong> - Quantidade de luas naturais</li>
                    <li><strong>Ano orbital</strong> - Dias terrestres</li>
                    <li><strong>Temperatura média</strong> - Em °C</li>
                    <li><strong>Observação</strong> - Curiosidade especial</li>
                </ul>

                <h3>💡 Exemplo Completo</h3>
                <pre><code>// Sistema de consulta interativo
exibir("=== SISTEMA NEBULA ===");

// Consulta direta
nebula exibir "Terra";

// Usando variável com input
criar planeta = ler("Digite um planeta: ");
nebula exibir planeta;</code></pre>

                <h3>⚠️ Dicas</h3>
                <p>• A busca é <strong>case-insensitive</strong> ("terra", "Terra", "TERRA" funcionam)</p>
                <p>• Se o planeta não for encontrado, o sistema lista os disponíveis</p>
                <p>• Use com loops e condicionais para criar menus interativos</p>
            </div>
        `
    },
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

// ============================================
// INPUT EMBUTIDO NO CONSOLE
// ============================================

// Criar elemento de input no console
function createConsoleInput(mensagem) {
    const container = document.createElement('div');
    container.className = 'console-input-container';
    container.style.cssText = `
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 0;
        border-bottom: 1px solid var(--border-color);
        animation: fadeIn 0.3s ease;
    `;

    // Prompt
    const prompt = document.createElement('span');
    prompt.className = 'console-prompt';
    prompt.style.cssText = `
        color: var(--accent-green);
        font-family: 'Fira Code', monospace;
        white-space: nowrap;
    `;
    prompt.textContent = mensagem ? `? ${mensagem}` : '> ';

    // Input
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'console-input';
    input.style.cssText = `
        background: transparent;
        border: none;
        border-bottom: 2px solid var(--accent-blue);
        color: var(--text-bright);
        font-family: 'Fira Code', monospace;
        font-size: 13px;
        outline: none;
        flex: 1;
        padding: 4px 8px;
        min-width: 100px;
    `;
    input.autocomplete = 'off';
    input.spellcheck = false;

    container.appendChild(prompt);
    container.appendChild(input);

    return { container, input };
}

// Callback de input que retorna Promise
function inputCallback(mensagem) {
    return new Promise((resolve) => {
        isWaitingInput = true;
        inputResolve = resolve;

        // Criar input no console
        const { container, input } = createConsoleInput(mensagem);
        consoleOutput.appendChild(container);

        // Focar no input
        input.focus();
        consoleOutput.scrollTop = consoleOutput.scrollHeight;

        // Handler de submit
        function handleSubmit() {
            const valor = input.value;
            
            // Desabilitar input
            input.disabled = true;
            input.style.borderBottomColor = 'var(--success)';
            input.style.opacity = '0.7';
            
            // Mostrar o valor digitado como linha de output
            const valueLine = document.createElement('div');
            valueLine.className = 'console-line output';
            valueLine.innerHTML = `<span style="color: var(--text-muted)">➜ ${escapeHtml(valor)}</span>`;
            consoleOutput.appendChild(valueLine);
            
            isWaitingInput = false;
            inputResolve = null;
            
            resolve(valor);
        }

        // Event listeners
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                handleSubmit();
            }
        });

        // Se perder foco, voltar foco (exceto se clicar em outro lugar da IDE)
        input.addEventListener('blur', () => {
            if (isWaitingInput && document.activeElement !== codeEditor) {
                setTimeout(() => input.focus(), 10);
            }
        });
    });
}

// ============================================
// EXECUÇÃO DO CÓDIGO
// ============================================

async function runCode() {
    const code = codeEditor.value;
    if (!code.trim()) {
        showConsoleMessage('Digite algum código para executar!', 'error');
        return;
    }

    // Se já estiver esperando input, não executar
    if (isWaitingInput) {
        showStatus('Aguardando input...', 'warning');
        return;
    }

    // Limpar console
    consoleOutput.innerHTML = '';
    showStatus('Executando...', 'info');

    // Callback de output
    const outputCallback = (value) => {
        addConsoleLine(value, 'output');
    };

    try {
        const result = await compiler.execute(code, outputCallback, inputCallback);

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
    } catch (e) {
        addConsoleLine(`Erro inesperado: ${e.message}`, 'error');
        showStatus('Erro fatal', 'error');
        isWaitingInput = false;
        inputResolve = null;
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
    } else if (node.tipo === 'Ler') {
        content = `<div class="ast-node" style="margin-left: ${level * 20}px">
            <span class="ast-node-type">Ler</span>
            <span class="ast-node-value">${node.mensagem ? formatNodeValue(node.mensagem) : ''}</span>
        </div>`;
    } else if (node.tipo === 'ConsultaPlaneta') {
        content = `<div class="ast-node" style="margin-left: ${level * 20}px">
            <span class="ast-node-type">ConsultaPlaneta</span>
            <span class="ast-node-value">${formatNodeValue(node.nome)}</span>
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
    if (node.tipo === 'Ler') return node.mensagem ? `ler(${formatNodeValue(node.mensagem)})` : 'ler()';
    if (node.tipo === 'ConsultaPlaneta') return `nebula exibir ${formatNodeValue(node.nome)}`;
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
    // Cancelar input pendente se houver
    if (isWaitingInput && inputResolve) {
        inputResolve('');
        isWaitingInput = false;
        inputResolve = null;
    }

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
    const statusLeft = document.querySelector('.status-left');

    const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'clock' : 'info-circle';
    const color = type === 'success' ? '#89d185' : type === 'error' ? '#f14c4c' : type === 'warning' ? '#cca700' : '#3794ff';

    statusLeft.innerHTML = `
        <span class="status-item" style="color: ${color}">
            <i class="fas fa-${icon}"></i> ${message}
        </span>
    `;

    if (type !== 'warning') {
        setTimeout(() => {
            statusLeft.innerHTML = `
                <span class="status-item"><i class="fas fa-check-circle"></i> Pronto</span>
                <span class="status-item" id="tokenCount"><i class="fas fa-coins"></i> 0 tokens</span>
            `;
        }, 3000);
    }
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
