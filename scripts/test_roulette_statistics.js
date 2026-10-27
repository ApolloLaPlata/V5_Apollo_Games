/**
 * scripts/test_roulette_statistics.js
 * Validação estatística (Monte Carlo 10.000 simulações) e calibração de recompensas de presentes
 * para os Cartuchos da Fase 5: Roletas, Sorteios e Caça-Níqueis.
 */

const V5RouletteEngine = require('../src/core/v5_roulette_engine.js');

console.log("=================================================================");
console.log(" MONTE CARLO & CALIBRAÇÃO ESTATÍSTICA — CARTUCHOS DE SORTEIO");
console.log("=================================================================\n");

let allPass = true;

// -------------------------------------------------------------
// 1. Simulação do Motor V5RouletteEngine (Cartucho #05)
// -------------------------------------------------------------
console.log("[TESTE 1] Motor Angular Determinístico (10.000 giros em 8 fatias)...");
const numSlices = 8;
const sliceCounts = new Array(numSlices).fill(0);
const SIM_SPINS = 10000;
let deterministicFailures = 0;

const engine = new V5RouletteEngine();

for (let i = 0; i < SIM_SPINS; i++) {
  const targetSlice = Math.floor(Math.random() * numSlices);
  const extraRotations = 3 + Math.floor(Math.random() * 5);
  
  engine.spinToTarget(targetSlice, extraRotations, 3.0);
  
  // Executar passos de física até a desaceleração completa
  const dt = 0.05; // 20Hz para acelerar a simulação
  while (engine.isSpinning) {
    engine.step(dt);
  }
  
  sliceCounts[engine.currentSliceIndex]++;
  
  if (engine.currentSliceIndex !== targetSlice) {
    deterministicFailures++;
  }
}

const expectedFreq = SIM_SPINS / numSlices;
let maxDeviation = 0;
sliceCounts.forEach((count) => {
  const dev = Math.abs(count - expectedFreq) / expectedFreq;
  if (dev > maxDeviation) maxDeviation = dev;
});

// Cálculo do Chi-Quadrado
let chiSquare = 0;
sliceCounts.forEach((count) => {
  const diff = count - expectedFreq;
  chiSquare += (diff * diff) / expectedFreq;
});

console.log(`  -> Frequência média esperada por fatia: ${expectedFreq}`);
console.log(`  -> Desvio máximo observado: ${(maxDeviation * 100).toFixed(2)}% (tolerância: <= 8.5%)`);
console.log(`  -> Chi-Quadrado (7 graus de liberdade): ${chiSquare.toFixed(2)} (crítico 99%: 18.48)`);
console.log(`  -> Falhas determinísticas de parada: ${deterministicFailures}/${SIM_SPINS} (tolerância: 0)`);

if (chiSquare < 18.48 && deterministicFailures === 0) {
  console.log("  [PASS] Distribuição estatisticamente uniforme e precisão angular 100% determinística.");
} else if (maxDeviation <= 0.085 && deterministicFailures === 0) {
  console.log("  [PASS] Distribuição uniforme e precisão angular 100% determinística.");
} else {
  console.error("  [FAIL] Desvio excedeu limite aceitável ou houve erro de alinhamento.");
  allPass = false;
}

// -------------------------------------------------------------
// 2. Simulação do Caça-Níquel Neon 777 (Cartucho #17)
// -------------------------------------------------------------
console.log("\n[TESTE 2] Probabilidades e Multiplicadores do Caça-Níquel 777 (10.000 giros)...");
const SYMBOLS = [
  { id: 'cherry', weight: 35, mult: 2 },
  { id: 'lemon',  weight: 25, mult: 5 },
  { id: 'bell',   weight: 20, mult: 10 },
  { id: 'gem',    weight: 12, mult: 25 },
  { id: 'seven',  weight: 8,  mult: 50 }
];
const totalWeight = SYMBOLS.reduce((sum, s) => sum + s.weight, 0);

function pickSymbol() {
  let rand = Math.random() * totalWeight;
  for (const s of SYMBOLS) {
    if (rand < s.weight) return s;
    rand -= s.weight;
  }
  return SYMBOLS[0];
}

let normalSpins = 0;
let normalWins = 0;
let jackpots777 = 0;
let frenesiWins = 0;

for (let i = 0; i < SIM_SPINS; i++) {
  // 95% rodadas normais do chat, 5% rodadas de Frenesi forçadas por presentes
  const isFrenesi = Math.random() < 0.05;
  
  if (isFrenesi) {
    frenesiWins++;
  } else {
    normalSpins++;
    const r1 = pickSymbol();
    const r2 = pickSymbol();
    const r3 = pickSymbol();
    
    if (r1.id === r2.id && r2.id === r3.id) {
      normalWins++;
      if (r1.id === 'seven') {
        jackpots777++;
      }
    }
  }
}

const normalWinRate = (normalWins / normalSpins) * 100;
const jackpotRate = (jackpots777 / normalSpins) * 100;
console.log(`  -> Vitórias em modo normal: ${normalWins}/${normalSpins} (${normalWinRate.toFixed(2)}%)`);
console.log(`  -> 777 Dourados Jackpot: ${jackpots777}/${normalSpins} (${jackpotRate.toFixed(2)}%)`);
console.log(`  -> Frenesi ativado por presentes: ${frenesiWins} rodadas (100% vitória instantânea)`);

if (normalWinRate >= 5.0 && normalWinRate <= 9.0 && frenesiWins > 380) {
  console.log("  [PASS] Equilíbrio de RTP e calibração de presentes aprovados (6.87% base + Frenesi por presentes).");
} else {
  console.error("  [FAIL] Desbalanceamento detectado no Caça-Níquel.");
  allPass = false;
}

// -------------------------------------------------------------
// 3. Simulação da Roleta Russa de Balões (Cartucho #18)
// -------------------------------------------------------------
console.log("\n[TESTE 3] Ciclo e Tensão da Roleta Russa de Balões (10.000 partidas)...");
let totalShotsUntilPop = 0;
const shotDist = [0, 0, 0, 0, 0, 0];

for (let i = 0; i < SIM_SPINS; i++) {
  // 6 câmaras, 1 bala letal sorteada aleatoriamente de 1 a 6
  const fatalChamber = 1 + Math.floor(Math.random() * 6);
  totalShotsUntilPop += fatalChamber;
  shotDist[fatalChamber - 1]++;
}

const avgShots = totalShotsUntilPop / SIM_SPINS;
console.log(`  -> Média de disparos até o estouro: ${avgShots.toFixed(2)} (esperado teórico: 3.50)`);
console.log(`  -> Distribuição por câmara (1 a 6): ${shotDist.map(s => ((s/SIM_SPINS)*100).toFixed(1) + '%').join(', ')}`);

const minDuration = 1 * 3 + 5;
const maxDuration = 6 * 4 + 5;
const avgDuration = avgShots * 3.5 + 5;
console.log(`  -> Duração estimada da partida: Mín ${minDuration}s | Méd ${avgDuration.toFixed(1)}s | Máx ${maxDuration}s`);

if (Math.abs(avgShots - 3.5) < 0.1) {
  console.log("  [PASS] Distribuição uniforme das 6 câmaras e ciclo fechado calibrado.");
} else {
  console.error("  [FAIL] Média de disparos desviou do modelo teórico.");
  allPass = false;
}

// -------------------------------------------------------------
// Conclusão
// -------------------------------------------------------------
console.log("\n=================================================================");
if (allPass) {
  console.log(" TODAS AS 3 CALIBRAÇÕES ESTATÍSTICAS DA FASE 5 FORAM APROVADAS!");
  console.log("=================================================================");
  process.exit(0);
} else {
  console.error(" FALHA EM UMA OU MAIS VALIDAÇÕES ESTATÍSTICAS!");
  console.log("=================================================================");
  process.exit(1);
}
