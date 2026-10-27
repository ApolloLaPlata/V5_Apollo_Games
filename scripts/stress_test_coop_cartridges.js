/**
 * scripts/stress_test_coop_cartridges.js
 * Teste de stress com simulação de ataques em massa de alta densidade (Etapa 059)
 * Holding V5 Apollo — Capitania V5 Games
 */

const V5BossRaidEngine = require('../src/core/v5_boss_raid_engine.js');
const V5CoopMVPTracker = require('../src/core/v5_coop_mvp_tracker.js');

console.log("=================================================================");
console.log(" STRESS TEST: SIMULAÇÃO DE ATAQUES EM MASSA DE ALTA DENSIDADE");
console.log("=================================================================\n");

let allPassed = true;

// 1. Stress Test no V5BossRaidEngine (50.000 ataques em rajada)
console.log("[CENÁRIO 1] 50.000 Ataques Simultâneos no Titã de 1.000.000 HP...");
const raid = new V5BossRaidEngine({ maxHp: 10000000, roundDuration: 60 });
const numAttackers = 5000;
const attackers = Array.from({ length: numAttackers }, (_, i) => `@viewer_${i}`);

const tStart = performance.now();
for (let i = 0; i < 50000; i++) {
  const user = attackers[i % numAttackers];
  const isGift = (i % 25 === 0);
  raid.applyAttack({
    user: user,
    type: isGift ? 'gift' : 'comment',
    giftName: isGift ? 'Lion' : null,
    value: isGift ? 1000 : 1
  });
  if (i % 60 === 0) {
    raid.step(1/60);
  }
}
const elapsedRaid = performance.now() - tStart;
const opsPerSecRaid = (50000 / (elapsedRaid / 1000));
const avgLatencyUsRaid = (elapsedRaid / 50000) * 1000;

console.log(`  -> 50.000 ataques processados em: ${elapsedRaid.toFixed(2)}ms`);
console.log(`  -> Vazão do motor: ${opsPerSecRaid.toFixed(0)} ataques/segundo`);
console.log(`  -> Latência média por ataque: ${avgLatencyUsRaid.toFixed(2)} µs (microsegundos)`);
console.log(`  -> Folga de CPU em 60 FPS: ${(100 - (elapsedRaid / (50000/60 * 16.6)) * 100).toFixed(2)}%`);

if (opsPerSecRaid > 100000 && elapsedRaid < 500) {
  console.log("  [PASS] Motor suporta com folga picos extremos de viralização ao vivo.");
} else {
  console.error("  [FAIL] Vazão de processamento abaixo do limiar.");
  allPassed = false;
}

// 2. Stress Test no V5CoopMVPTracker (100.000 registros e ordenação contínua)
console.log("\n[CENÁRIO 2] 100.000 Inserções no Rastreador MVP com 10.000 Espectadores Únicos...");
const tracker = new V5CoopMVPTracker({ topLimit: 3 });
const tStartTracker = performance.now();

for (let i = 0; i < 100000; i++) {
  const user = `@player_${i % 10000}`;
  const isGift = (i % 50 === 0);
  tracker.record(user, isGift ? 5000 : 150, isGift, isGift ? 100 : 0);
}

const elapsedTracker = performance.now() - tStartTracker;
const opsPerSecTracker = (100000 / (elapsedTracker / 1000));
const podium = tracker.getPodium();

console.log(`  -> 100.000 registros executados em: ${elapsedTracker.toFixed(2)}ms`);
console.log(`  -> Vazão do Tracker: ${opsPerSecTracker.toFixed(0)} ops/segundo`);
console.log(`  -> Participantes rastreados: ${tracker.participants.size}`);
console.log(`  -> Pódio Top 1: ${podium[0]?.medal} ${podium[0]?.user} com ${podium[0]?.value} pts (${podium[0]?.percent}%)`);

if (opsPerSecTracker > 100000 && tracker.participants.size === 10000) {
  console.log("  [PASS] Sistema de ranking MVP ordenado em tempo real com alta performance.");
} else {
  console.error("  [FAIL] Desempenho do tracker abaixo do esperado.");
  allPassed = false;
}

console.log("\n=================================================================");
if (allPassed) {
  console.log(" TODOS OS TESTES DE STRESS DE ALTA DENSIDADE FORAM APROVADOS!");
  console.log("=================================================================");
  process.exit(0);
} else {
  console.error(" FALHA EM UM OU MAIS TESTES DE STRESS!");
  console.log("=================================================================");
  process.exit(1);
}
