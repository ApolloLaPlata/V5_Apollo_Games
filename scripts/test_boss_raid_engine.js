/**
 * scripts/test_boss_raid_engine.js
 * Teste unitário e benchmark de performance para o V5BossRaidEngine (Etapa 051).
 */

const V5BossRaidEngine = require('../src/core/v5_boss_raid_engine.js');

console.log("=================================================================");
console.log(" VALIDAÇÃO DO MOTOR DE BOSS RAID COOPERATIVO (ETAPA 051)");
console.log("=================================================================\n");

let allPassed = true;
const engine = new V5BossRaidEngine({ maxHp: 1000000, roundDuration: 45 });

// 1. Inicialização
console.log("[TESTE 1] Parâmetros Iniciais do Boss...");
const check1 = engine.currentHp === 1000000 && engine.timeRemaining === 45 && engine.state === 'IDLE';
console.log(`  HP: ${engine.currentHp} | Tempo: ${engine.timeRemaining}s | Estado: ${engine.state}`);
if (check1) {
  console.log("  [PASS] Configuração inicial perfeita.");
} else {
  console.error("  [FAIL] Parâmetros iniciais divergentes.");
  allPassed = false;
}

// 2. Dano de Comentários e Combo
console.log("\n[TESTE 2] Comentários Normais e Acúmulo de Combo...");
const initialHp = engine.currentHp;
for (let i = 0; i < 10; i++) {
  engine.applyAttack({ user: `@viewer_${i}`, type: 'comment' });
}
const damageDealt = initialHp - engine.currentHp;
console.log(`  -> 10 comentários causaram ${damageDealt} de dano`);
console.log(`  -> Combo Count: ${engine.comboCount} | Multiplicador: ${engine.comboMultiplier.toFixed(2)}x`);
if (damageDealt > 1000 && engine.comboCount === 10 && engine.comboMultiplier > 1.1) {
  console.log("  [PASS] Comentários aplicados com progressão de combo.");
} else {
  console.error("  [FAIL] Erro no cálculo de dano ou combo de comentários.");
  allPassed = false;
}

// 3. Presente Crítico & Meteoro
console.log("\n[TESTE 3] Presentes de Alto Impacto (Meteoro de Leão)...");
const preMeteorHp = engine.currentHp;
engine.applyAttack({ user: '@whale_king', type: 'gift', giftName: 'Lion', value: 1000 });
const meteorDmg = preMeteorHp - engine.currentHp;
console.log(`  -> Golpe Meteoro causou: ${meteorDmg} de dano (Screen Shake: ${engine.screenShake.toFixed(1)})`);
if (meteorDmg >= 100000 && engine.screenShake >= 20) {
  console.log("  [PASS] Ataques de presentes possuem peso massivo e acionam mega-tremor.");
} else {
  console.error("  [FAIL] Dano de presente insuficiente.");
  allPassed = false;
}

// 4. Stagger Mechanic (Atordoamento 2x Dano)
console.log("\n[TESTE 4] Atordoamento (Stagger) e Multiplicador 2x...");
engine.staggerCurrent = engine.staggerMax - 100;
engine.applyAttack({ user: '@striker', type: 'comment' });
console.log(`  -> Estado após encher barra de Stagger: ${engine.state}`);
const preStaggerHit = engine.currentHp;
engine.applyAttack({ user: '@striker', type: 'comment' });
const staggerHitDmg = preStaggerHit - engine.currentHp;
console.log(`  -> Dano causado durante Stagger: ${staggerHitDmg}`);
if (engine.state === 'STAGGERED' && staggerHitDmg > 300) {
  console.log("  [PASS] Stagger ativado com sucesso e dobra de dano verificada.");
} else {
  console.error("  [FAIL] Falha no sistema de atordoamento.");
  allPassed = false;
}

// 5. Ranking MVP em Tempo Real
console.log("\n[TESTE 5] Leaderboard MVP da Rodada...");
const topMvp = engine.topMVP;
console.log(`  -> Top 1 MVP: ${topMvp[0]?.user} com ${topMvp[0]?.damage} de dano`);
if (topMvp.length > 0 && topMvp[0].user === '@whale_king') {
  console.log("  [PASS] Ranking MVP ordenado com precisão.");
} else {
  console.error("  [FAIL] Erro na ordenação do MVP.");
  allPassed = false;
}

// 6. Enrage e Derrota do Boss
console.log("\n[TESTE 6] Transição de Enrage (<30% HP) e Derrota...");
engine.currentHp = 350000;
engine.state = 'IDLE';
engine.applyAttack({ user: '@finisher', type: 'gift', giftName: 'Universe', value: 1000 });
console.log(`  -> HP após grande ataque: ${engine.currentHp} (${(engine.getHpPercent()*100).toFixed(1)}%) | Estado: ${engine.state}`);
const enteredEnrage = engine.state === 'ENRAGED';

// Golpe fatal
engine.applyAttack({ user: '@hero', type: 'gift', giftName: 'Lion', value: 1000 });
engine.applyAttack({ user: '@hero', type: 'gift', giftName: 'Lion', value: 1000 });
engine.applyAttack({ user: '@hero', type: 'gift', giftName: 'Lion', value: 1000 });
console.log(`  -> HP Final: ${engine.currentHp} | Estado: ${engine.state} | Vencedor: ${engine.winner}`);

if (enteredEnrage && engine.state === 'DEFEATED' && engine.winner === 'CHAT') {
  console.log("  [PASS] Transição de Enrage e Derrota concluídas com sucesso.");
} else {
  console.error("  [FAIL] Falha no ciclo de Enrage/Derrota.");
  allPassed = false;
}

// 7. Benchmark de Performance (Zero Latência)
console.log("\n[TESTE 7] Benchmark de Desempenho (10.000 ataques em rajada)...");
engine.reset();
const tStart = performance.now();
for (let i = 0; i < 10000; i++) {
  engine.applyAttack({ user: `@user_${i % 100}`, type: (i % 20 === 0) ? 'gift' : 'comment' });
  if (i % 60 === 0) engine.step(1/60);
}
const elapsedMs = performance.now() - tStart;
console.log(`  -> Tempo para 10.000 ataques e 166 steps de física: ${elapsedMs.toFixed(2)}ms`);
console.log(`  -> Média por ataque: ${(elapsedMs / 10000).toFixed(4)}ms (Vazão: ${(10000 / (elapsedMs / 1000)).toFixed(0)} ops/s)`);

if (elapsedMs < 100) {
  console.log("  [PASS] Alta performance garantida para picos extremos de audiência.");
} else {
  console.error("  [FAIL] Benchmark excedeu limite aceitável de 100ms.");
  allPassed = false;
}

console.log("\n=================================================================");
if (allPassed) {
  console.log(" TODOS OS 7 TESTES DO V5 BOSS RAID ENGINE FORAM APROVADOS!");
  console.log("=================================================================");
  process.exit(0);
} else {
  console.error(" FALHA EM UM OU MAIS TESTES!");
  console.log("=================================================================");
  process.exit(1);
}
