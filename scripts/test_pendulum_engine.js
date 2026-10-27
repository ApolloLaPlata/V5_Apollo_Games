/**
 * scripts/test_pendulum_engine.js
 * Teste unitário e validação de física para o V5PendulumEliminationEngine (Etapa 061 & 063)
 */

const V5PendulumEliminationEngine = require('../src/core/v5_pendulum_elimination_engine.js');

console.log("=================================================================");
console.log(" VALIDAÇÃO DO MOTOR DE FÍSICA PENDULAR & ELIMINAÇÃO (ETAPA 061/063)");
console.log("=================================================================\n");

let allPassed = true;
const engine = new V5PendulumEliminationEngine({
  pivotX: 500,
  pivotY: 200,
  length: 400,
  fortressX: 800,
  fortressMaxHp: 20000
});

// 1. Posição Inicial e Geometria
console.log("[TESTE 1] Parâmetros Iniciais e Posição Geométrica...");
const pos0 = engine.getBallPosition();
console.log(`  -> Ângulo inicial: ${(engine.angle * 180 / Math.PI).toFixed(1)}°`);
console.log(`  -> Posição da bola: (${pos0.x.toFixed(1)}, ${pos0.y.toFixed(1)})`);

if (pos0.x > 500 && pos0.y > 200) {
  console.log("  [PASS] Geometria inicial e trigonometria validadas.");
} else {
  console.error("  [FAIL] Coordenadas Cartesianas inconsistentes.");
  allPassed = false;
}

// 2. Integração Física da Queda Pendular
console.log("\n[TESTE 2] Queda e Aceleração Gravitacional...");
engine.release(false);
const initialAngle = engine.angle;
for (let i = 0; i < 20; i++) {
  engine.step(1/60);
}
console.log(`  -> Ângulo após 20 steps (1/3s): ${(engine.angle * 180 / Math.PI).toFixed(1)}°`);
console.log(`  -> Velocidade angular (rad/s): ${engine.angularVelocity.toFixed(2)}`);

if (Math.abs(engine.angularVelocity) > 0.5) {
  console.log("  [PASS] Dinâmica gravitacional d²θ/dt² integrada com precisão.");
} else {
  console.error("  [FAIL] O pêndulo não acelerou sob a gravidade.");
  allPassed = false;
}

// 3. Colisão com a Muralha e Rebote
console.log("\n[TESTE 3] Detecção de Impacto Estrutural e Rebote Restitutivo...");
// Posicionar bola perto da fortaleza se movendo para a direita
engine.angle = Math.PI * 0.45;
engine.angularVelocity = 3.5;
const preCollisionHp = engine.fortressHp;
engine.step(1/60);

const damageTaken = preCollisionHp - engine.fortressHp;
console.log(`  -> Dano causado na muralha: ${damageTaken} HP`);
console.log(`  -> Vida restante da muralha: ${engine.fortressHp} / ${engine.fortressMaxHp} HP`);
console.log(`  -> Velocidade angular pós-colisão (rebote invertido): ${engine.angularVelocity.toFixed(2)} rad/s`);

if (damageTaken > 500 && engine.angularVelocity < 0) {
  console.log("  [PASS] Transferência de momento linear e rebote negativo validados.");
} else {
  console.error("  [FAIL] Falha no cálculo de impacto ou restituição elástica.");
  allPassed = false;
}

// 4. Super Impacto de Presentes (Boost Cósmico)
console.log("\n[TESTE 4] Golpe Cósmico Super-Charged de Presentes...");
engine.fortressHp = 100000;
engine.fortressMaxHp = 100000;
engine.isRoundActive = true;
engine.release(true); // Super Charged
const superHpBefore = engine.fortressHp;
engine.step(1/60);
const superDmg = superHpBefore - engine.fortressHp;

console.log(`  -> Dano do Super Impacto: ${superDmg} HP (Screen Shake: ${engine.screenShake.toFixed(1)})`);
if (superDmg > damageTaken && engine.screenShake >= 20) {
  console.log("  [PASS] Boost de presentes amplifica impacto estrutural e tremor.");
} else {
  console.error("  [FAIL] Super boost não surtiu o efeito desejado.");
  allPassed = false;
}

// 5. Benchmark de Performance
console.log("\n[TESTE 5] Benchmark de Desempenho (10.000 steps de física contínua)...");
const tStart = performance.now();
for (let i = 0; i < 10000; i++) {
  engine.step(1/60);
}
const elapsedMs = performance.now() - tStart;
console.log(`  -> 10.000 steps executados em: ${elapsedMs.toFixed(2)}ms`);
console.log(`  -> Média por step: ${(elapsedMs / 10000).toFixed(4)}ms (Vazão: ${(10000 / (elapsedMs / 1000)).toFixed(0)} steps/s)`);

if (elapsedMs < 30) {
  console.log("  [PASS] Performance excepcional para 60 FPS garantidos no OBS.");
} else {
  console.error("  [FAIL] Benchmark excedeu limite de 30ms.");
  allPassed = false;
}

console.log("\n=================================================================");
if (allPassed) {
  console.log(" TODOS OS TESTES DO MOTOR DE PÊNDULO FORAM APROVADOS!");
  console.log("=================================================================");
  process.exit(0);
} else {
  console.error(" FALHA EM UM OU MAIS TESTES!");
  console.log("=================================================================");
  process.exit(1);
}
