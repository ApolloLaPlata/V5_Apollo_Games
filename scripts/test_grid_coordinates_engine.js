/**
 * scripts/test_grid_coordinates_engine.js
 * ============================================================================
 * ETAPA 071: Teste e Benchmark do Motor de Grids Interativos e Coordenadas
 * Holding V5 Apollo — Capitania V5 Games & Broadcaster
 * ============================================================================
 */

const V5GridCoordinatesEngine = require('../src/core/v5_grid_coordinates_engine.js');

console.log("=".repeat(75));
console.log(" SUÍTE DE TESTES E BENCHMARK: V5 GRID COORDINATES ENGINE (ETAPA 071)");
console.log(" Holding V5 Apollo — Capitania V5 Games");
console.log("=".repeat(75));

let totalChecks = 0;
let passedChecks = 0;

function assert(condition, message) {
  totalChecks++;
  if (condition) {
    console.log(`  [PASS] ${message}`);
    passedChecks++;
  } else {
    console.error(`  [FAIL] ${message}`);
  }
}

// ----------------------------------------------------------------------------
// TESTE 1: Grid 4x4 (16 Células) — Inicialização e Nomenclatura
// ----------------------------------------------------------------------------
console.log("\n[TESTE 1] Inicialização de Grid 4x4 (A1 a D4)");
const grid4x4 = new V5GridCoordinatesEngine({ rows: 4, cols: 4 });
assert(grid4x4.totalCells === 16, "Grid 4x4 possui exatamente 16 células");
assert(grid4x4.cells[0].label === "A1", "Célula 0 mapeada para A1");
assert(grid4x4.cells[3].label === "A4", "Célula 3 mapeada para A4");
assert(grid4x4.cells[12].label === "D1", "Célula 12 mapeada para D1");
assert(grid4x4.cells[15].label === "D4", "Célula 15 mapeada para D4");

// ----------------------------------------------------------------------------
// TESTE 2: Parsing Tolerante de Mensagens de Chat de Celular
// ----------------------------------------------------------------------------
console.log("\n[TESTE 2] Parsing Tolerante de Coordenadas de Chat");
const validInputs = [
  { text: "A1", expected: "A1", row: 0, col: 0 },
  { text: "a1", expected: "A1", row: 0, col: 0 },
  { text: "A 2", expected: "A2", row: 0, col: 1 },
  { text: "b-3", expected: "B3", row: 1, col: 2 },
  { text: "C.4", expected: "C4", row: 2, col: 3 },
  { text: "d1", expected: "D1", row: 3, col: 0 },
  { text: "D4", expected: "D4", row: 3, col: 3 },
  { text: "1A", expected: "A1", row: 0, col: 0 }, // Invertido
  { text: "3B", expected: "B3", row: 1, col: 2 }, // Invertido
  { text: "Voto na b2 galera", expected: "B2", row: 1, col: 1 }, // Frase com coordenada
  { text: "abre a C1!", expected: "C1", row: 2, col: 0 }
];

let allParseValid = true;
validInputs.forEach(item => {
  const parsed = grid4x4.parseCoordinate(item.text);
  if (!parsed.valid || parsed.label !== item.expected || parsed.row !== item.row || parsed.col !== item.col) {
    allParseValid = false;
    console.error(`  Falha no parse de '${item.text}': obtido ${JSON.stringify(parsed)}`);
  }
});
assert(allParseValid, `11/11 formatos reais de chat móvel convertidos com 100% de precisão`);

// Teste de rejeição de coordenadas fora da grade 4x4
const invalidInputs = ["E1", "A5", "Z9", "99", "olá mundo", "123", "", null];
let allInvalidRejected = true;
invalidInputs.forEach(item => {
  const parsed = grid4x4.parseCoordinate(item);
  if (parsed.valid) {
    allInvalidRejected = false;
    console.error(`  Falso positivo no parse inválido de '${item}'`);
  }
});
assert(allInvalidRejected, "Rejeição estrita de entradas fora dos limites (ex: E1, A5 na 4x4)");

// ----------------------------------------------------------------------------
// TESTE 3: Grid 6x6 (36 Células) — Suporte Dinâmico (A1 a F6)
// ----------------------------------------------------------------------------
console.log("\n[TESTE 3] Grid Dinâmico 6x6 (A1 a F6)");
const grid6x6 = new V5GridCoordinatesEngine({ rows: 6, cols: 6 });
assert(grid6x6.totalCells === 36, "Grid 6x6 possui exatamente 36 células");
assert(grid6x6.cells[35].label === "F6", "Última célula da 6x6 é F6");
const parseF6 = grid6x6.parseCoordinate("f6");
assert(parseF6.valid && parseF6.label === "F6" && parseF6.index === 35, "Coordenada F6 validada na grade 6x6");

// ----------------------------------------------------------------------------
// TESTE 4: Votação Ponderada, Gifts e Tracking O(1) de Célula Líder
// ----------------------------------------------------------------------------
console.log("\n[TESTE 4] Votação Ponderada & Tracking O(1) de Líder");
grid4x4.resetFullGrid();

// 2 votos em B2
grid4x4.processEvent({ type: "comment", comment: "B2", user: "@user1" });
grid4x4.processEvent({ type: "comment", comment: "b 2", user: "@user2" });
assert(grid4x4.leadingCellIndex === 5, "Célula líder é B2 (índice 5) com 2 votos");
assert(grid4x4.highestVotes === 2, "Contagem máxima de votos é 2");

// 3 votos em C3 -> C3 ultrapassa B2
grid4x4.processEvent({ type: "comment", comment: "c3", user: "@user3" });
grid4x4.processEvent({ type: "comment", comment: "C3", user: "@user4" });
grid4x4.processEvent({ type: "comment", comment: "c3", user: "@user5" });
assert(grid4x4.leadingCellIndex === 10, "Célula C3 ultrapassou B2 e virou líder");
assert(grid4x4.highestVotes === 3, "Novo ápice de votos é 3");

// Super Gift (Leão) em A1 -> A1 recebe 50 votos e dispara Raio-X em cruz
const giftResult = grid4x4.processEvent({
  type: "gift",
  giftName: "Lion",
  value: 500,
  comment: "a1",
  user: "@super_whale"
});
assert(giftResult.action === "gift_boost" && giftResult.isSuper, "Super Gift reconhecido");
assert(grid4x4.leadingCellIndex === 0, "A1 virou líder absoluto com 50 votos");
assert(grid4x4.cells[0].xRayGlow === 1.0, "Célula A1 recebeu 100% de brilho Raio-X");
assert(grid4x4.cells[1].xRayGlow >= 0.65, "Vizinho direito (A2) recebeu Raio-X em cruz");
assert(grid4x4.cells[4].xRayGlow >= 0.65, "Vizinho inferior (B1) recebeu Raio-X em cruz");

// ----------------------------------------------------------------------------
// TESTE 5: Resolução de Rodada & Transições de Conteúdo (Tesouro/Mina)
// ----------------------------------------------------------------------------
console.log("\n[TESTE 5] Resolução da Célula Líder & Callbacks");
grid4x4.cells[0].content = V5GridCoordinatesEngine.CELL_CONTENT.TREASURE;
let treasureFound = false;
grid4x4.onTreasureFound = (cell) => {
  treasureFound = true;
};

const resolved = grid4x4.resolveLeadingCell();
assert(resolved.index === 0, "Célula A1 resolvida");
assert(resolved.state === V5GridCoordinatesEngine.CELL_STATE.REVEALED, "Estado transitou para REVEALED");
assert(resolved.discoverer === "@super_whale", "Descobridor registrado como @super_whale");
assert(treasureFound, "Callback onTreasureFound disparado com sucesso");

// Reseta apenas votos e abre a próxima rodada
assert(grid4x4.leadingCellIndex === -1, "Votos resetados para próximo turno");
assert(grid4x4.cells[0].state === V5GridCoordinatesEngine.CELL_STATE.REVEALED, "Célula A1 permanece revelada");

// ----------------------------------------------------------------------------
// TESTE 6: Cálculo de Bounding Boxes 9:16 Responsivo
// ----------------------------------------------------------------------------
console.log("\n[TESTE 6] Mapeamento Geométrico 9:16 com Safe Zones");
const layout = grid4x4.computeLayout(1080, 1920, 140, 180, 10);
assert(layout.cellSize > 180 && layout.cellSize < 260, `Tamanho de célula ideal calculado: ${layout.cellSize.toFixed(1)}px`);
assert(layout.startY >= 140, `Grid posicionado abaixo da Top Safe Zone (140px): ${layout.startY.toFixed(1)}px`);
assert(layout.startY + layout.totalHeight <= 1920 - 180, `Grid posicionado acima da Bottom Safe Zone (180px): ${(layout.startY + layout.totalHeight).toFixed(1)}px`);
assert(grid4x4.cells[15].rect.width === layout.cellSize, "Célula final possui dimensões uniformes");

// ----------------------------------------------------------------------------
// TESTE 7: Benchmark de Alta Frequência (100.000 Eventos de Chat)
// ----------------------------------------------------------------------------
console.log("\n[TESTE 7] Benchmark de Performance (100.000 Eventos)");
const benchmarkGrid = new V5GridCoordinatesEngine({ rows: 4, cols: 4 });
const mockComments = ["A1", "b2", "C3", "d4", "A4", "D1", "c2", "b3"];

const startBench = performance.now();
for (let i = 0; i < 100000; i++) {
  const text = mockComments[i % mockComments.length];
  benchmarkGrid.processEvent({
    type: "comment",
    comment: text,
    user: `@tester_${i % 200}`
  });
}
const elapsedMs = performance.now() - startBench;
const opsPerSec = Math.floor((100000 / elapsedMs) * 1000);
const latencyMicros = ((elapsedMs / 100000) * 1000).toFixed(2);

console.log(`  Processados: 100.000 eventos de chat em ${elapsedMs.toFixed(2)} ms`);
console.log(`  Throughput:  ${opsPerSec.toLocaleString()} ops/segundo`);
console.log(`  Latência:    ${latencyMicros} µs por voto de coordenada`);

assert(opsPerSec > 500000, `Throughput > 500.000 ops/s atingido (${opsPerSec.toLocaleString()} ops/s)`);
assert(latencyMicros < 2.0, `Latência sub-2µs atingida (${latencyMicros} µs)`);

// ----------------------------------------------------------------------------
// Relatório Final
// ----------------------------------------------------------------------------
console.log("\n" + "=".repeat(75));
console.log(` RESULTADO: ${passedChecks}/${totalChecks} CHECKS APROVADOS`);
console.log("=".repeat(75));

if (passedChecks === totalChecks) {
  console.log("HOMOLOGAÇÃO DA ETAPA 071 CONCLUÍDA COM 100% DE SUCESSO!");
  process.exit(0);
} else {
  console.error("FALHA EM UM OU MAIS CHECKS DA ETAPA 071!");
  process.exit(1);
}
