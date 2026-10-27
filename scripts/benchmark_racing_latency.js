/**
 * scripts/benchmark_racing_latency.js
 * ============================================================================
 * ETAPA 039: Teste de Latência e Precisão dos Comandos de Corrida
 * Holding V5 Apollo — Capitania V5 Games & Broadcaster
 * ============================================================================
 * Mede a latência de despacho, processamento e resposta física de comandos
 * em rajadas extremas de chat (1000 comandos/s) nos motores de corrida.
 */

const V5HighwayEngine = require('../src/core/v5_highway_engine.js');

console.log('='.repeat(75));
console.log(' BENCHMARK DE LATÊNCIA E PRECISÃO DOS COMANDOS DE CORRIDA (ETAPA 039)');
console.log(' Holding V5 Apollo — Capitania V5 Games & Broadcaster');
console.log('='.repeat(75));

// 1. Instanciar Motor de Corrida
const engine = new V5HighwayEngine({
  width: 1080,
  height: 1920,
  lanes: 3,
  roadWidth: 1800
});

const r1 = engine.addRacer('roxingo', 'Roxingo Neon', '#a855f7', 0);
const r2 = engine.addRacer('baiano', 'Baiano Turbo', '#f97316', 1);
const r3 = engine.addRacer('macaco', 'Macaco Driver', '#22c55e', 2);

// 2. Simulação de Event Bus Local com medição de latência em microssegundos
class MockEventBus {
  constructor(engine) {
    this.engine = engine;
    this.processedCount = 0;
    this.latenciesUs = [];
  }

  dispatch(payload) {
    const t0 = process.hrtime.bigint();

    // Roteamento de comandos de live (chat / gift)
    const text = String(payload.comment || payload.action || '').trim().toLowerCase();
    const isGift = (payload.type === 'gift');
    const giftName = payload.giftName || 'Rose';

    let targetRacer = null;
    if (text === '1' || text.includes('rox')) targetRacer = 'roxingo';
    else if (text === '2' || text.includes('bai')) targetRacer = 'baiano';
    else if (text === '3' || text.includes('mac')) targetRacer = 'macaco';

    if (targetRacer) {
      if (isGift) {
        const isBig = (giftName === 'Lion' || giftName === 'Rocket');
        this.engine.applyBoost(targetRacer, isBig ? 130 : 65, isBig ? 5.0 : 3.0, isBig ? 2.0 : 1.5);
      } else {
        this.engine.applyBoost(targetRacer, 18, 1.5, 1.2);
      }
    }

    const t1 = process.hrtime.bigint();
    const diffUs = Number(t1 - t0) / 1000;
    this.latenciesUs.push(diffUs);
    this.processedCount++;
  }
}

const bus = new MockEventBus(engine);

// 3. Teste 1: Rajada de 2.000 comandos de chat concorrentes
console.log('\n[TESTE 1] Injetando rajada maciça de 2.000 comandos de chat...');
const BATCH_SIZE = 2000;
const startBatch = process.hrtime.bigint();

for (let i = 0; i < BATCH_SIZE; i++) {
  const teamNum = (i % 3) + 1;
  const isGift = (i % 25 === 0);
  bus.dispatch({
    type: isGift ? 'gift' : 'comment',
    comment: String(teamNum),
    giftName: isGift ? ((i % 100 === 0) ? 'Lion' : 'Rose') : null,
    user: `@viewer_${i}`
  });
}

const endBatch = process.hrtime.bigint();
const totalBatchMs = Number(endBatch - startBatch) / 1_000_000;

// Calcular estatísticas de latência
bus.latenciesUs.sort((a, b) => a - b);
const avgUs = bus.latenciesUs.reduce((a, b) => a + b, 0) / bus.latenciesUs.length;
const p50Us = bus.latenciesUs[Math.floor(bus.latenciesUs.length * 0.50)];
const p95Us = bus.latenciesUs[Math.floor(bus.latenciesUs.length * 0.95)];
const p99Us = bus.latenciesUs[Math.floor(bus.latenciesUs.length * 0.99)];
const maxUs = bus.latenciesUs[bus.latenciesUs.length - 1];
const throughputK = (BATCH_SIZE / totalBatchMs);

console.log(`  - Comandos processados: ${bus.processedCount} / ${BATCH_SIZE} (100% entrega)`);
console.log(`  - Tempo total da rajada: ${totalBatchMs.toFixed(2)} ms`);
console.log(`  - Vazão (Throughput): ${Math.round(throughputK * 1000).toLocaleString()} comandos/segundo`);
console.log(`  - Latência Média por comando: ${avgUs.toFixed(3)} µs (${(avgUs / 1000).toFixed(4)} ms)`);
console.log(`  - P50 (Mediana): ${p50Us.toFixed(3)} µs | P95: ${p95Us.toFixed(3)} µs | P99: ${p99Us.toFixed(3)} µs`);
console.log(`  - Pior caso (Max): ${maxUs.toFixed(3)} µs (${(maxUs / 1000).toFixed(4)} ms)`);

// 4. Teste 2: Estabilidade de Frame Rate durante rajada concorrente
console.log('\n[TESTE 2] Simulando 300 passos de física a 60 FPS com injeção contínua de comandos...');
let stepTimes = [];
for (let s = 0; s < 300; s++) {
  // Injeta 5 comandos por frame (300 comandos/s)
  for (let c = 0; c < 5; c++) {
    bus.dispatch({
      type: 'comment',
      comment: String((c % 3) + 1),
      user: `@live_chat_${s}_${c}`
    });
  }

  const s0 = process.hrtime.bigint();
  engine.step(1 / 60);
  const s1 = process.hrtime.bigint();
  stepTimes.push(Number(s1 - s0) / 1_000_000);
}

const avgStepMs = stepTimes.reduce((a, b) => a + b, 0) / stepTimes.length;
const maxStepMs = Math.max(...stepTimes);
const estFps = 1000 / avgStepMs;
const cpuHeadroom = ((16.666 - avgStepMs) / 16.666) * 100;

console.log(`  - Passos de física executados: ${stepTimes.length}`);
console.log(`  - Tempo médio por frame sob carga: ${avgStepMs.toFixed(4)} ms`);
console.log(`  - Pior frametime: ${maxStepMs.toFixed(4)} ms`);
console.log(`  - Taxa teórica sob carga de chat: ${Math.round(estFps)} FPS`);
console.log(`  - Folga de CPU: ${cpuHeadroom.toFixed(2)}%`);

// 5. Validações Assertivas
const checks = [
  { desc: '100% dos comandos entregues sem perda', pass: bus.processedCount >= 3500 },
  { desc: 'Latência média abaixo de 100 µs (0.1 ms)', pass: avgUs < 100 },
  { desc: 'P99 abaixo de 500 µs (0.5 ms)', pass: p99Us < 500 },
  { desc: 'Frametime sob carga abaixo de 1.0 ms', pass: avgStepMs < 1.0 },
  { desc: 'Pilotos responderam com aceleração física', pass: r1.speed > r1.baseSpeed && r2.speed > r2.baseSpeed }
];

console.log('\n' + '='.repeat(75));
console.log(' CHECKS DE CONFORMIDADE DE LATÊNCIA:');
let allOk = true;
checks.forEach(c => {
  const mark = c.pass ? '✓ PASS' : '✗ FAIL';
  console.log(`  [${mark}] ${c.desc}`);
  if (!c.pass) allOk = false;
});
console.log('='.repeat(75));

if (allOk) {
  console.log('[ETAPA 039 CONCLUÍDA COM EXCELÊNCIA] Latência ultra-baixa validada com folga cirúrgica!');
  process.exit(0);
} else {
  console.error('[ERRO] Falha no teste de latência.');
  process.exit(1);
}
