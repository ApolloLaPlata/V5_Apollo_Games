/**
 * scripts/test_board_usability.js
 * ============================================================================
 * ETAPAS 078 & 079: Verificação de Usabilidade, Recompensa Rápida e Leitura
 * de Coordenadas no Feed de Texto do TikTok / YouTube Live
 * Fase 8: Cartuchos de Tabuleiro & Coordenadas
 * Holding V5 Apollo — Capitania V5 Games & Broadcaster
 * ============================================================================
 * Executa 10.000 testes com entradas realistas de espectadores de celular,
 * medindo:
 *   1. Taxa de reconhecimento de coordenadas (Alvo: 100% dos formatos válidos)
 *   2. Rejeição de ruído/falsos positivos (Alvo: 100% das mensagens inválidas)
 *   3. Latência de parsing e feedback háptico/visual (Alvo: < 0.05ms)
 *   4. Mecânica de recompensa rápida e feedback na tela
 */

const V5GridCoordinatesEngine = require('../src/core/v5_grid_coordinates_engine.js');

console.log("=".repeat(75));
console.log(" BATERIA DE USABILIDADE & RECONHECIMENTO DE COORDENADAS (ETAPAS 078 & 079)");
console.log(" Holding V5 Apollo — Capitania V5 Games");
console.log("=".repeat(75));

const engine4x4 = new V5GridCoordinatesEngine({ rows: 4, cols: 4 });
const engine5x5 = new V5GridCoordinatesEngine({ rows: 5, cols: 5 });
const engine6x6 = new V5GridCoordinatesEngine({ rows: 6, cols: 6 });

// ----------------------------------------------------------------------------
// 1. Corpus de Testes Realistas de Chat Móvel (10.000 amostras)
// ----------------------------------------------------------------------------
const VALID_TEMPLATES = [
  // Formato direto maiúsculo / minúsculo
  (r, c) => `${r}${c}`,
  (r, c) => `${r.toLowerCase()}${c}`,
  // Espaçado
  (r, c) => `${r} ${c}`,
  (r, c) => `${r.toLowerCase()} ${c}`,
  // Pontuações comuns
  (r, c) => `${r}-${c}`,
  (r, c) => `${r}.${c}`,
  (r, c) => `${r},${c}`,
  (r, c) => `${r}:${c}`,
  // Invertido (número primeiro)
  (r, c) => `${c}${r}`,
  (r, c) => `${c}${r.toLowerCase()}`,
  (r, c) => `${c} ${r}`,
  (r, c) => `${c}-${r}`,
  // Frases reais com contexto de live
  (r, c) => `voto na ${r}${c}!`,
  (r, c) => `abre a ${r}${c} streamer`,
  (r, c) => `vai na ${r.toLowerCase()}${c} agora`,
  (r, c) => `🔥 ${r}${c} 🔥`,
  (r, c) => `todo mundo no ${r}${c}`,
  (r, c) => `BORA ${r}${c} VENCE`,
  (r, c) => `minha coordenada é ${r} ${c}`,
  (r, c) => `leao na ${r}${c}`
];

const INVALID_TEMPLATES = [
  "boa noite live",
  "kkkkkkkkkk",
  "salve streamer!",
  "onde é?",
  "123456",
  "qual o jogo?",
  "top demais",
  "segura a live",
  "Z9",
  "E9",
  "99",
  "X0",
  "AA",
  "11",
  "!!",
  "🎁",
  "oi",
  "show",
  "vai dar ruim",
  "chat lento"
];

const ROW_LETTERS_4 = ['A', 'B', 'C', 'D'];
const ROW_LETTERS_6 = ['A', 'B', 'C', 'D', 'E', 'F'];

console.log("\nGerando 10.000 amostras simuladas de mensagens de chat do TikTok...");

let validTested = 0;
let validMatched = 0;
let invalidTested = 0;
let invalidRejected = 0;

const startTime = performance.now();

for (let i = 0; i < 10000; i++) {
  const isTargetValid = (i % 2 === 0);

  if (isTargetValid) {
    validTested++;
    const rowIdx = Math.floor(Math.random() * 4);
    const colIdx = Math.floor(Math.random() * 4);
    const letter = ROW_LETTERS_4[rowIdx];
    const num = colIdx + 1;
    const templateFn = VALID_TEMPLATES[Math.floor(Math.random() * VALID_TEMPLATES.length)];
    const text = templateFn(letter, num);

    const parsed = engine4x4.parseCoordinate(text);
    if (parsed.valid && parsed.row === rowIdx && parsed.col === colIdx && parsed.label === `${letter}${num}`) {
      validMatched++;
    } else {
      console.error(`Falha ao reconhecer válido: "${text}" -> resultado:`, parsed);
    }
  } else {
    invalidTested++;
    const text = INVALID_TEMPLATES[Math.floor(Math.random() * INVALID_TEMPLATES.length)];
    const parsed = engine4x4.parseCoordinate(text);
    if (!parsed.valid) {
      invalidRejected++;
    } else {
      console.error(`Falso positivo detectado em: "${text}" -> resultado:`, parsed);
    }
  }
}

const totalTimeMs = performance.now() - startTime;
const avgLatencyMicros = ((totalTimeMs / 10000) * 1000).toFixed(2);
const throughputOps = Math.floor((10000 / totalTimeMs) * 1000);

// ----------------------------------------------------------------------------
// 2. Teste da Mecânica de Recompensa Rápida & Feedback Visual
// ----------------------------------------------------------------------------
console.log("\nValidando Mecânica de Recompensa Rápida e Feedback na Tela...");

let feedbackDispatched = 0;
let scoreAccumulated = 0;

engine4x4.onCellRevealed = (cell) => {
  feedbackDispatched++;
};

engine4x4.onTreasureFound = (cell) => {
  scoreAccumulated += 1000;
};

// Votar e resolver 4 rodadas com tesouro
for (let turn = 0; turn < 4; turn++) {
  engine4x4.cells[turn].content = V5GridCoordinatesEngine.CELL_CONTENT.TREASURE;
  engine4x4.processEvent({ type: "comment", comment: engine4x4.cells[turn].label, user: "@jogador" });
  engine4x4.resolveLeadingCell();
}

const isFeedbackWorking = (feedbackDispatched === 4 && scoreAccumulated === 4000);

// ----------------------------------------------------------------------------
// 3. Verificações de Usabilidade e Conformidade
// ----------------------------------------------------------------------------
const checks = [
  {
    name: "Taxa de Acerto em Coordenadas Válidas (100%)",
    pass: validMatched === validTested,
    val: `${validMatched}/${validTested} (${((validMatched / validTested) * 100).toFixed(2)}%)`
  },
  {
    name: "Rejeição Estrita de Ruído/Mensagens Sem Coordenadas (100%)",
    pass: invalidRejected === invalidTested,
    val: `${invalidRejected}/${invalidTested} (${((invalidRejected / invalidTested) * 100).toFixed(2)}%)`
  },
  {
    name: "Latência de Resposta Ultra-Rápida (< 0.05ms)",
    pass: parseFloat(avgLatencyMicros) < 50.0,
    val: `${avgLatencyMicros} µs (${throughputOps.toLocaleString()} ops/s)`
  },
  {
    name: "Mecânica de Recompensa Rápida e Callbacks de Impacto",
    pass: isFeedbackWorking,
    val: `${feedbackDispatched} revelações, ${scoreAccumulated} pts acumulados`
  }
];

console.log("\n" + "=".repeat(75));
console.log(" RESULTADOS DO TESTE DE USABILIDADE (10.000 MENSAGENS)");
console.log("=".repeat(75));

let allPassed = true;
checks.forEach(c => {
  const status = c.pass ? "[PASS]" : "[FAIL]";
  console.log(`  ${status} ${c.name} -> ${c.val}`);
  if (!c.pass) allPassed = false;
});

console.log("=".repeat(75));
if (allPassed) {
  console.log("USABILIDADE E LEITURA DE CHAT HOMOLOGADAS COM 100% DE SUCESSO!");
  process.exit(0);
} else {
  console.error("FALHA NA VERIFICAÇÃO DE USABILIDADE!");
  process.exit(1);
}
