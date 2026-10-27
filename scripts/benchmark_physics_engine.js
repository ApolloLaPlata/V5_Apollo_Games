const fs = require('fs');
const V5PhysicsEngine = require('../src/core/v5_physics_engine.js');

console.log('='.repeat(70));
console.log(' BENCHMARK DE PERFORMANCE DO MOTOR DE FÍSICA V5 (ETAPA 021)');
console.log(' Holding V5 Apollo — Capitania V5 Games');
console.log('='.repeat(70));

const engine = new V5PhysicsEngine({
  width: 1080,
  height: 1920,
  gravityY: 0.35,
  poolSize: 400
});

// 1. Criar grade clássica de Plinko com 10 fileiras
engine.createPlinkoGrid(540, 300, 10, 48, 56, 330);
console.log(`[SETUP] Pinos gerados: ${engine.pegs.length}`);

// 2. Adicionar caçapas inferiores (Slots)
const slotWidth = 1080 / 7;
for (let i = 0; i < 7; i++) {
  const mult = [10, 5, 2, 50, 2, 5, 10][i];
  engine.addSlot(i * slotWidth, 1650, slotWidth, 100, mult, 'neutral', `${mult}x`);
}
console.log(`[SETUP] Caçapas geradas: ${engine.slots.length}`);

// 3. Adicionar paredes funil
engine.addSegment(50, 150, 200, 320, 0.7);
engine.addSegment(1030, 150, 880, 320, 0.7);
console.log(`[SETUP] Segmentos defletores: ${engine.segments.length}`);

// 4. Teste de Stress: Injetar 350 esferas simultâneas
const TOTAL_BALLS = 350;
for (let i = 0; i < TOTAL_BALLS; i++) {
  const x = 540 + (Math.random() - 0.5) * 200;
  const y = 80 + Math.random() * 120;
  const vx = (Math.random() - 0.5) * 4;
  const vy = Math.random() * 2;
  const isVIP = (i % 25 === 0);
  engine.spawnBall(x, y, vx, vy, 8, isVIP ? '#fbbf24' : '#38bdf8', 'A', isVIP);
}
console.log(`[SETUP] Esferas ativas: ${engine.activeBalls.length}`);

// 5. Executar 500 passos de simulação e medir tempo
let totalCollisions = 0;
let totalCaptures = 0;

engine.onPegCollision = () => { totalCollisions++; };
engine.onSlotCapture = () => { totalCaptures++; };

const STEPS = 500;
const startTime = process.hrtime.bigint();

for (let s = 0; s < STEPS; s++) {
  engine.step(1.0);
}

const endTime = process.hrtime.bigint();
const totalTimeMs = Number(endTime - startTime) / 1_000_000;
const avgTimePerStepMs = totalTimeMs / STEPS;
const estimatedFps = 1000 / avgTimePerStepMs;

console.log('\n' + '-'.repeat(70));
console.log(`[BENCHMARK] Total de passos: ${STEPS}`);
console.log(`[BENCHMARK] Tempo total de execução: ${totalTimeMs.toFixed(2)} ms`);
console.log(`[BENCHMARK] Tempo médio por passo: ${avgTimePerStepMs.toFixed(3)} ms (Limite para 60 FPS: 16.6 ms)`);
console.log(`[BENCHMARK] Capacidade teórica de FPS: ${Math.round(estimatedFps)} FPS`);
console.log(`[BENCHMARK] Colisões com pinos processadas: ${totalCollisions}`);
console.log(`[BENCHMARK] Capturas em caçapas: ${totalCaptures}`);
console.log('-'.repeat(70));

if (avgTimePerStepMs < 4.0) {
  console.log('\n[PASS 100%] O motor de física atinge padrões de alta performance com Folga de CPU > 75%!');
  process.exit(0);
} else {
  console.error('\n[FAIL] Performance abaixo da margem de segurança para 60 FPS.');
  process.exit(1);
}
