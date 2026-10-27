/**
 * scripts/stress_test_physics_particles.js
 * ============================================================================
 * ETAPA 029: Bateria de Testes de Sobrecarga de Partículas (300+ Esferas a 60 FPS)
 * Holding V5 Apollo — Capitania V5 Games & Broadcaster
 * ============================================================================
 * Executa simulações sob estresse extremo em 4 cenários de física distintos:
 *   1. Plinko Pegboard Cascade (350 esferas, 10 fileiras de pinos, 7 caçapas)
 *   2. Pinball Neon Magnetics (350 esferas, 6 bumpers elásticos, defletores)
 *   3. Coin Pusher Friction & Stacking (250 moedas 2.5D com pá oscilante)
 *   4. Cosmic Gravitational Vortex (350 esferas em órbita caótica e sucção não-linear)
 */

const V5PhysicsEngine = require('../src/core/v5_physics_engine.js');

console.log('='.repeat(75));
console.log(' BATERIA DE TESTES DE SOBRECARGA DE PARTÍCULAS — 60 FPS STRESS (ETAPA 029)');
console.log(' Holding V5 Apollo — Capitania V5 Games');
console.log('='.repeat(75));

const results = [];

function runBenchmarkScenario(name, setupFn, totalBalls = 350, steps = 600) {
  const engine = new V5PhysicsEngine({
    width: 1080,
    height: 1920,
    gravityY: 0.35,
    poolSize: 500
  });

  setupFn(engine);

  // Spawn balls
  for (let i = 0; i < totalBalls; i++) {
    const x = 540 + (Math.random() - 0.5) * 360;
    const y = 80 + Math.random() * 200;
    const vx = (Math.random() - 0.5) * 6;
    const vy = Math.random() * 4;
    const isVIP = (i % 20 === 0);
    engine.spawnBall(x, y, vx, vy, 8, isVIP ? '#fbbf24' : '#38bdf8', 'A', isVIP);
  }

  const times = [];
  const startTotal = process.hrtime.bigint();

  for (let s = 0; s < steps; s++) {
    const sStart = process.hrtime.bigint();
    engine.step(1.0);
    const sEnd = process.hrtime.bigint();
    times.push(Number(sEnd - sStart) / 1_000_000);
  }

  const endTotal = process.hrtime.bigint();
  const totalMs = Number(endTotal - startTotal) / 1_000_000;
  const avgMs = totalMs / steps;
  
  // Calcular percentil 95 e desvio
  times.sort((a, b) => a - b);
  const p95Ms = times[Math.floor(times.length * 0.95)];
  const maxMs = times[times.length - 1];
  const estFps = 1000 / avgMs;
  const headroomPct = ((16.666 - avgMs) / 16.666) * 100;

  const passed = (avgMs < 4.0) && (p95Ms < 8.0);
  results.push({ name, totalBalls, steps, avgMs, p95Ms, maxMs, estFps, headroomPct, passed });

  console.log(`\n[CENÁRIO] ${name}`);
  console.log(`  - Partículas ativas simuladas: ${totalBalls}`);
  console.log(`  - Passos executados: ${steps} (~${(steps / 60).toFixed(1)}s em 60fps)`);
  console.log(`  - Tempo médio por frame: ${avgMs.toFixed(3)} ms`);
  console.log(`  - P95 Frametime: ${p95Ms.toFixed(3)} ms | Max: ${maxMs.toFixed(3)} ms`);
  console.log(`  - Taxa teórica máxima: ${Math.round(estFps)} FPS`);
  console.log(`  - Folga de CPU em 60 FPS: ${headroomPct.toFixed(1)}%`);
  console.log(`  - Status: ${passed ? 'APROVADO (ALTA PERFORMANCE)' : 'REPROVADO'}`);
}

// ----------------------------------------------------------------------------
// Cenário 1: Plinko Pegboard Cascade
// ----------------------------------------------------------------------------
runBenchmarkScenario('1. Plinko Pegboard Cascade (10 fileiras, 7 slots)', (engine) => {
  engine.createPlinkoGrid(540, 300, 10, 48, 56, 330);
  const slotW = 1080 / 7;
  for (let i = 0; i < 7; i++) {
    const mult = [10, 5, 2, 50, 2, 5, 10][i];
    engine.addSlot(i * slotW, 1650, slotW, 100, mult, 'neutral', `${mult}x`);
  }
  engine.addSegment(50, 150, 200, 320, 0.7);
  engine.addSegment(1030, 150, 880, 320, 0.7);
}, 350, 600);

// ----------------------------------------------------------------------------
// Cenário 2: Pinball Neon Magnetics & Bumpers
// ----------------------------------------------------------------------------
runBenchmarkScenario('2. Pinball Neon Magnetics (Bumpers elásticos + rails)', (engine) => {
  engine.addPeg(340, 550, 45, 523.25, true);
  engine.addPeg(740, 550, 45, 587.33, true);
  engine.addPeg(540, 720, 55, 659.25, true);
  engine.addPeg(380, 920, 40, 783.99, true);
  engine.addPeg(700, 920, 40, 880.00, true);

  // Guias angulares
  engine.addSegment(120, 1100, 320, 1300, 0.9);
  engine.addSegment(960, 1100, 760, 1300, 0.9);
}, 350, 600);

// ----------------------------------------------------------------------------
// Cenário 3: Coin Pusher 2.5D Friction & Contact Simulation
// ----------------------------------------------------------------------------
runBenchmarkScenario('3. Coin Pusher 2.5D Stacking & Friction', (engine) => {
  engine.gravityY = 0.20;
  engine.drag = 0.97; // Atrito elevado de moedas sobrepostas
  // Paredes laterais estreitas de gabinete de moeda
  engine.addSegment(100, 200, 100, 1600, 0.4);
  engine.addSegment(980, 200, 980, 1600, 0.4);
  // Borda de queda
  engine.addSlot(100, 1600, 880, 80, 10, 'A', 'COIN_DROP');
}, 250, 600);

// ----------------------------------------------------------------------------
// Cenário 4: Cosmic Gravitational Vortex (Inverse-Square Singularity)
// ----------------------------------------------------------------------------
runBenchmarkScenario('4. Cosmic Gravitational Vortex (Órbitas caóticas e sucção)', (engine) => {
  engine.gravityY = 0.0; // Espaço sideral com gravidade central
  engine.addVortex(540, 850, 480, 2.8);
}, 350, 600);

// ----------------------------------------------------------------------------
// Relatório Consolidado de Homologação
// ----------------------------------------------------------------------------
console.log('\n' + '='.repeat(75));
console.log(' SUMÁRIO EXECUTIVO DA BATERIA DE SOBRECARGA:');
console.log('='.repeat(75));
let allPassed = true;
results.forEach((r) => {
  const statusStr = r.passed ? '✓ APROVADO' : '✗ REPROVADO';
  console.log(`[${statusStr}] ${r.name.padEnd(52)}: ${r.avgMs.toFixed(3)} ms/step (${Math.round(r.estFps)} FPS | Folga: ${r.headroomPct.toFixed(1)}%)`);
  if (!r.passed) allPassed = false;
});
console.log('='.repeat(75));

if (allPassed) {
  console.log('[RESULTADO FINAL] 100% DOS CENÁRIOS HOMOLOGADOS COM EXCELÊNCIA A 60 FPS!');
  process.exit(0);
} else {
  console.error('[RESULTADO FINAL] Falha na homologação de sobrecarga.');
  process.exit(1);
}
