/**
 * scripts/test_highway_engine.js
 * ============================================================================
 * TESTE UNITÁRIO E BENCHMARK DO V5 HIGHWAY ENGINE (ETAPA 031)
 * Holding V5 Apollo — Capitania V5 Games & Broadcaster
 * ============================================================================
 */

const V5HighwayEngine = require('../src/core/v5_highway_engine.js');

console.log('='.repeat(75));
console.log(' TESTE & BENCHMARK DO MOTOR DE CORRIDA VERTICAL PSEUDO-3D (ETAPA 031)');
console.log(' Holding V5 Apollo — Capitania V5 Games');
console.log('='.repeat(75));

// 1. Instanciação do Motor 9:16
const engine = new V5HighwayEngine({
  width: 1080,
  height: 1920,
  lanes: 3,
  roadWidth: 1800,
  cameraHeight: 900,
  cameraDepth: 0.84,
  drawDistance: 200,
  horizonY: 1920 * 0.32
});

console.log(`[SETUP] Motor instanciado: ${engine.width}x${engine.height} com ${engine.lanes} faixas`);
console.log(`[SETUP] Segmentos de asfalto gerados: ${engine.segments.length} (${engine.trackLength}m de pista)`);

// 2. Registro dos 3 Avatares Pilotos da Holding
const roxingo = engine.addRacer('roxingo', 'Roxingo Neon', '#a855f7', 0);
const baiano = engine.addRacer('baiano', 'Baiano Turbo', '#f97316', 1);
const macaco = engine.addRacer('macaco', 'Macaco Driver', '#22c55e', 2);

console.log(`[SETUP] 3 Pilotos posicionados nas faixas 0, 1 e 2`);

// 3. Monitor de Ultrapassagens e Troca de Liderança
let leadChangeCount = 0;
engine.onLeadChange = (newLeader, oldLeaderId) => {
  leadChangeCount++;
  console.log(`  [EVENTO] Troca de Liderança #${leadChangeCount}: ${newLeader.name} assumiu a ponta! (superou ${oldLeaderId})`);
};

// 4. Teste de Boosts Interativos
engine.applyBoost('roxingo', 60, 2.5, 1.6);
engine.applyBoost('baiano', 30, 1.5, 1.3);

// 5. Benchmark de Simulação de 600 frames (10 segundos a 60 FPS)
const STEPS = 600;
const hrStart = process.hrtime.bigint();

for (let s = 0; s < STEPS; s++) {
  // Disparar boosts periódicos simulando chat
  if (s === 120) engine.applyBoost('macaco', 80, 3.0, 1.8);
  if (s === 240) engine.applyBoost('baiano', 70, 2.5, 1.7);
  if (s === 360) engine.applyBoost('roxingo', 75, 2.8, 1.75);

  engine.step(1 / 60);
}

const hrEnd = process.hrtime.bigint();
const totalMs = Number(hrEnd - hrStart) / 1_000_000;
const avgStepMs = totalMs / STEPS;
const estFps = 1000 / avgStepMs;
const cpuHeadroom = ((16.666 - avgStepMs) / 16.666) * 100;

console.log('\n' + '-'.repeat(75));
console.log(`[RESULTADOS DE DESEMPENHO]`);
console.log(`  - Passos executados: ${STEPS} frames`);
console.log(`  - Tempo total de simulação física: ${totalMs.toFixed(2)} ms`);
console.log(`  - Tempo médio por frame: ${avgStepMs.toFixed(4)} ms (Orçamento 60fps: 16.666 ms)`);
console.log(`  - Taxa teórica máxima: ${Math.round(estFps)} FPS`);
console.log(`  - Folga de CPU em 60 FPS: ${cpuHeadroom.toFixed(2)}%`);
console.log(`  - Trocas de liderança registradas: ${leadChangeCount}`);
console.log('-'.repeat(75));

// 6. Tabela Final de Telemetria
console.log('\n[CLASSIFICAÇÃO FINAL DA PROVA]');
const standings = engine.getStandings();
standings.forEach(s => {
  console.log(`  #${s.rank} | ${s.name.padEnd(16)} | Vel: ${s.speedKmH} km/h | Dist: ${s.distanceM}m | Gap: +${s.gapM}m | Turbos: ${s.boosts}`);
});

// 7. Validações Assertivas
const asserts = [
  { desc: 'Segmentos criados corretamente', pass: engine.segments.length === 400 },
  { desc: 'Pilotos registrados', pass: engine.racers.length === 3 },
  { desc: 'Líder definido', pass: engine.leader !== null },
  { desc: 'Velocidade física responsiva', pass: engine.leader.speed > 100 },
  { desc: 'Tempo de frame abaixo de 1.0 ms', pass: avgStepMs < 1.0 },
  { desc: 'Trocas de liderança computadas', pass: leadChangeCount > 0 }
];

console.log('\n' + '='.repeat(75));
console.log(' CHECKS DE CONFORMIDADE:');
let allOk = true;
asserts.forEach(a => {
  const mark = a.pass ? '✓ PASS' : '✗ FAIL';
  console.log(`  [${mark}] ${a.desc}`);
  if (!a.pass) allOk = false;
});
console.log('='.repeat(75));

if (allOk) {
  console.log('[ETAPA 031 CONCLUÍDA COM EXCELÊNCIA] Motor Pseudo-3D Highway 100% Operacional!');
  process.exit(0);
} else {
  console.error('[ERRO] Falha em um dos checks de conformidade.');
  process.exit(1);
}
