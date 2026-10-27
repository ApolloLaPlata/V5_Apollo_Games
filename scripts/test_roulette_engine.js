/**
 * scripts/test_roulette_engine.js
 * ============================================================================
 * TESTE UNITÁRIO E BENCHMARK DO MOTOR DE ROLETA DETERMINÍSTICA (ETAPA 041)
 * Holding V5 Apollo — Capitania V5 Games & Broadcaster
 * ============================================================================
 */

const V5RouletteEngine = require('../src/core/v5_roulette_engine.js');

console.log('='.repeat(75));
console.log(' TESTE & BENCHMARK DO MOTOR DE ROLETA DETERMINÍSTICA (ETAPA 041)');
console.log(' Holding V5 Apollo — Capitania V5 Games & Broadcaster');
console.log('='.repeat(75));

// 1. Instanciação do Motor com 8 Fatias
const engine = new V5RouletteEngine();
console.log(`[SETUP] Motor instanciado com ${engine.slices.length} fatias configuradas`);

// 2. Teste de Precisão Determinística em 5 giros direcionados
console.log('\n[TESTE DE PRECISÃO DETERMINÍSTICA]');
const targetsToTest = [0, 2, 4, 6, 7];
let deterministicSuccessCount = 0;

targetsToTest.forEach(targetIdx => {
  let haltSlice = null;
  let pinClicks = 0;

  engine.onPinClick = () => { pinClicks++; };
  engine.onSpinHalt = (slice) => { haltSlice = slice; };

  // Iniciar giro determinístico para o alvo especificado
  engine.spinToTarget(targetIdx, 4, 3.0);

  // Executar simulação por 4 segundos a 60 FPS (240 passos)
  for (let s = 0; s < 240; s++) {
    engine.step(1 / 60);
  }

  const reachedIdx = engine.currentSliceIndex;
  const match = (reachedIdx === targetIdx);
  if (match) deterministicSuccessCount++;

  console.log(`  - Alvo #${targetIdx} (${engine.slices[targetIdx].label}) -> Parou em #${reachedIdx} (${engine.slices[reachedIdx].label}) | Pinos clicados: ${pinClicks} | [${match ? '✓ EXATO' : '✗ ERRO'}]`);
});

// 3. Benchmark de Performance (1.000 passos contínuos)
console.log('\n[BENCHMARK DE PERFORMANCE (1.000 PASSOS)]');
engine.spinToTarget(3, 8, 8.0);

const STEPS = 1000;
const hrStart = process.hrtime.bigint();

for (let s = 0; s < STEPS; s++) {
  engine.step(1 / 60);
}

const hrEnd = process.hrtime.bigint();
const totalMs = Number(hrEnd - hrStart) / 1_000_000;
const avgStepMs = totalMs / STEPS;
const estFps = 1000 / avgStepMs;
const cpuHeadroom = ((16.666 - avgStepMs) / 16.666) * 100;

console.log(`  - Passos executados: ${STEPS}`);
console.log(`  - Tempo total de cálculo angular: ${totalMs.toFixed(3)} ms`);
console.log(`  - Tempo médio por frame: ${avgStepMs.toFixed(5)} ms (Orçamento 60fps: 16.666 ms)`);
console.log(`  - Taxa teórica máxima: ${Math.round(estFps).toLocaleString()} FPS`);
console.log(`  - Folga de CPU em 60 FPS: ${cpuHeadroom.toFixed(2)}%`);

// 4. Checagens de Conformidade
const checks = [
  { desc: 'Fatias geradas e ângulos normalizados', pass: engine.slices.length === 8 },
  { desc: 'Precisão determinística 100% nos 5 alvos testados', pass: deterministicSuccessCount === targetsToTest.length },
  { desc: 'Simulação da palheta gerou cliques de pinos mecânicos', pass: engine.totalPinClicks > 0 },
  { desc: 'Tempo de frame abaixo de 0.05 ms', pass: avgStepMs < 0.05 }
];

console.log('\n' + '='.repeat(75));
console.log(' CHECKS DE CONFORMIDADE:');
let allOk = true;
checks.forEach(c => {
  const mark = c.pass ? '✓ PASS' : '✗ FAIL';
  console.log(`  [${mark}] ${c.desc}`);
  if (!c.pass) allOk = false;
});
console.log('='.repeat(75));

if (allOk) {
  console.log('[ETAPA 041 CONCLUÍDA COM EXCELÊNCIA] Motor de Roleta Determinística 100% Homologado!');
  process.exit(0);
} else {
  console.error('[ERRO] Falha em um dos checks de conformidade.');
  process.exit(1);
}
