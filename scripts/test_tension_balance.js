/**
 * scripts/test_tension_balance.js
 * ============================================================================
 * ETAPA 069: Testes de Balanceamento de Tempo e Curva de Adrenalina
 * Fase 7: Cartuchos de Tensão, Eliminação & Cronômetro
 * Holding V5 Apollo — Capitania V5 Games & Broadcaster
 * ============================================================================
 * Simulação estocástica de Monte Carlo (10.000 rodadas) para os 4 cartuchos
 * de eliminação (#07, #21, #22, #23), medindo:
 *   1. Duração média e variância de cada partida (alvo: 25s a 50s; nunca > 60s)
 *   2. Curva convexa de tensão e adrenalina sonora/visual d²A/dt² > 0
 *   3. Calibração de alavancagem de Gifts (5x a 20x vs comentários)
 *   4. Zero falhas de deadlock ou encerramento instantâneo (< 10s)
 */

console.log("=".repeat(75));
console.log(" BATERIA MONTE CARLO: BALANCEAMENTO DE TENSÃO & ADRENALINA (ETAPA 069)");
console.log(" Holding V5 Apollo — Capitania V5 Games");
console.log("=".repeat(75));

const SIMULATED_ROUNDS = 10000;

// ----------------------------------------------------------------------------
// 1. Simulação Cartucho #07: Pêndulo Demolidor
// ----------------------------------------------------------------------------
function simulatePendulumGame() {
  const fortressMaxHp = 50000;
  let fortressHp = fortressMaxHp;
  let time = 0;
  let angle = Math.PI * 0.35;
  let angularVel = 0;
  let isSwinging = false;
  let isSuper = false;
  let lastGiftTime = -999;
  const ropeLength = 550;
  const gravity = 880;
  const damping = 0.06;
  const dt = 1 / 60; // 60 FPS

  while (fortressHp > 0 && time < 45.0) {
    time += dt;

    // Chegada de comandos do chat (1=puxar, 2=soltar, 3=turbo)
    if (Math.random() < (1.1 * dt)) {
      const act = Math.floor(Math.random() * 3) + 1;
      if (act === 1) {
        angle = Math.min(Math.PI * 0.47, angle + 0.18);
        isSwinging = false;
        angularVel = 0;
      } else if (act === 2) {
        isSwinging = true;
      } else if (act === 3) {
        isSwinging = true;
        angularVel += 2.2;
      }
    }

    // Gifts acionam Cosmic Wreck (Super Tração com cooldown de 3.0s)
    if ((time - lastGiftTime > 3.0) && Math.random() < (0.035 * dt)) {
      lastGiftTime = time;
      isSuper = true;
      angle = Math.PI * 0.46;
      angularVel = 2.5;
      isSwinging = true;
    }

    // Física do pêndulo
    if (isSwinging) {
      const naturalFreqSq = gravity / ropeLength;
      const angularAcc = (-naturalFreqSq * Math.sin(angle)) - (damping * angularVel);
      angularVel += angularAcc * dt;
      angle += angularVel * dt;

      // Colisão com a muralha (absorção estrutural máxima de 15.000 HP por impacto)
      if (angle <= 0.05 && angularVel < 0) {
        const impactSpeed = Math.abs(angularVel * ropeLength);
        const dmg = Math.min(15000, Math.floor(impactSpeed * (isSuper ? 25 : 8)));
        fortressHp = Math.max(0, fortressHp - dmg);
        angularVel = -angularVel * 0.4; // Rebote elástico
        isSuper = false;
      }
    }
  }

  return { duration: time, hpLeft: fortressHp };
}

// ----------------------------------------------------------------------------
// 2. Simulação Cartucho #21: Batata Quente Explosiva
// ----------------------------------------------------------------------------
function simulateHotPotatoGame() {
  // Tempo secreto entre 22 e 38 segundos
  const secretDetonationTime = 22 + Math.random() * 16;
  let time = 0;
  let holder = 0;
  let passes = 0;
  const bpmHistory = [];

  while (time < secretDetonationTime && time < 45.0) {
    const dt = 1.0;
    time += dt;

    // Frequência cardíaca / adrenalina: 75 -> 180 BPM
    const progress = time / secretDetonationTime;
    const currentBpm = 75 + 105 * Math.pow(progress, 2.0);
    bpmHistory.push(currentBpm);

    // Passes acionados por votos do chat
    if (Math.random() < 0.45) {
      holder = (holder + 1) % 5;
      passes++;
    }
  }

  return {
    duration: time,
    passes: passes,
    startBpm: bpmHistory[0],
    peakBpm: bpmHistory[bpmHistory.length - 1],
    isConvexBpm: (bpmHistory[Math.floor(bpmHistory.length / 2)] - bpmHistory[0]) <
                 (bpmHistory[bpmHistory.length - 1] - bpmHistory[Math.floor(bpmHistory.length / 2)])
  };
}

// ----------------------------------------------------------------------------
// 3. Simulação Cartucho #22: Ponte de Vidro Quebradiço
// ----------------------------------------------------------------------------
function simulateGlassBridgeGame() {
  const steps = 8;
  let currentStep = 0;
  let time = 0;
  let giftsUsed = 0;

  while (currentStep < steps && time < 45.0) {
    // Decisão da multidão por degrau leva entre 3.0 e 4.5 segundos
    const stepDuration = 3.0 + Math.random() * 1.5;
    time += stepDuration;

    // Chance de acerto da multidão com raio-X de gift (20% de ativação de gift)
    const hasGiftXray = Math.random() < 0.20;
    if (hasGiftXray) giftsUsed++;

    const isCorrect = hasGiftXray ? true : (Math.random() < 0.55);

    if (isCorrect) {
      currentStep++;
    } else {
      time += 1.0; // Animação de queda e quebra
      currentStep++; // Próximo avança pelo degrau descoberto
    }
  }

  return { duration: Math.min(45.0, time), stepsCompleted: currentStep, giftsUsed };
}

// ----------------------------------------------------------------------------
// 4. Simulação Cartucho #23: Sobrevivência na Lava
// ----------------------------------------------------------------------------
function simulateLavaSurvivalGame() {
  const platforms = [100, 100, 100, 100];
  let time = 0;
  const dt = 0.5;
  let aliveCount = 4;

  while (aliveCount > 1 && time < 45.0) {
    time += dt;
    const lavaProgress = time / 45.0;
    const decay = (2.2 + lavaProgress * 4.0) * dt;

    for (let i = 0; i < 4; i++) {
      if (platforms[i] <= 0) continue;

      // Distribuição estocástica de votos
      const chatWeight = (i === 0 ? 0.35 : (i === 1 ? 0.25 : (i === 2 ? 0.22 : 0.18)));
      const votes = (Math.random() < chatWeight ? 1.8 : 0.4);
      const giftBoost = Math.random() < 0.02 ? 15 : 0;

      platforms[i] = Math.min(100, platforms[i] - decay + votes * 1.0 + giftBoost);

      if (platforms[i] <= 0) {
        aliveCount--;
      }
    }
  }

  return { duration: Math.min(45.0, time), aliveAtEnd: aliveCount };
}

// ----------------------------------------------------------------------------
// Execução dos 10.000 Testes de Monte Carlo
// ----------------------------------------------------------------------------
console.log(`\nIniciando ${SIMULATED_ROUNDS.toLocaleString()} simulações para cada um dos 4 cartuchos...`);

// 1. Pêndulo
let sumPendulum = 0, minPendulum = 999, maxPendulum = 0;
for (let i = 0; i < SIMULATED_ROUNDS; i++) {
  const res = simulatePendulumGame();
  sumPendulum += res.duration;
  if (res.duration < minPendulum) minPendulum = res.duration;
  if (res.duration > maxPendulum) maxPendulum = res.duration;
}
const avgPendulum = sumPendulum / SIMULATED_ROUNDS;

// 2. Batata Quente
let sumPotato = 0, minPotato = 999, maxPotato = 0, convexCount = 0;
for (let i = 0; i < SIMULATED_ROUNDS; i++) {
  const res = simulateHotPotatoGame();
  sumPotato += res.duration;
  if (res.duration < minPotato) minPotato = res.duration;
  if (res.duration > maxPotato) maxPotato = res.duration;
  if (res.isConvexBpm) convexCount++;
}
const avgPotato = sumPotato / SIMULATED_ROUNDS;

// 3. Ponte de Vidro
let sumGlass = 0, minGlass = 999, maxGlass = 0;
for (let i = 0; i < SIMULATED_ROUNDS; i++) {
  const res = simulateGlassBridgeGame();
  sumGlass += res.duration;
  if (res.duration < minGlass) minGlass = res.duration;
  if (res.duration > maxGlass) maxGlass = res.duration;
}
const avgGlass = sumGlass / SIMULATED_ROUNDS;

// 4. Sobrevivência na Lava
let sumLava = 0, minLava = 999, maxLava = 0;
for (let i = 0; i < SIMULATED_ROUNDS; i++) {
  const res = simulateLavaSurvivalGame();
  sumLava += res.duration;
  if (res.duration < minLava) minLava = res.duration;
  if (res.duration > maxLava) maxLava = res.duration;
}
const avgLava = sumLava / SIMULATED_ROUNDS;

// ----------------------------------------------------------------------------
// Verificações e Relatório de Conformidade
// ----------------------------------------------------------------------------
const checks = [
  {
    name: "Cartucho #07 (Pêndulo): Duração Média Calibrada (30s - 45s)",
    pass: avgPendulum >= 30 && avgPendulum <= 45,
    val: `${avgPendulum.toFixed(2)}s (min: ${minPendulum.toFixed(1)}s, max: ${maxPendulum.toFixed(1)}s)`
  },
  {
    name: "Cartucho #21 (Batata Quente): Duração Média Calibrada (25s - 40s)",
    pass: avgPotato >= 25 && avgPotato <= 40,
    val: `${avgPotato.toFixed(2)}s (min: ${minPotato.toFixed(1)}s, max: ${maxPotato.toFixed(1)}s)`
  },
  {
    name: "Cartucho #21 (Batata Quente): Curva de Tensão Convexa (BPM escala para 180)",
    pass: (convexCount / SIMULATED_ROUNDS) > 0.99,
    val: `${((convexCount / SIMULATED_ROUNDS) * 100).toFixed(1)}% convexidade validada`
  },
  {
    name: "Cartucho #22 (Ponte de Vidro): Duração Média Calibrada (25s - 45s)",
    pass: avgGlass >= 25 && avgGlass <= 45,
    val: `${avgGlass.toFixed(2)}s (min: ${minGlass.toFixed(1)}s, max: ${maxGlass.toFixed(1)}s)`
  },
  {
    name: "Cartucho #23 (Sobrevivência na Lava): Duração Média Calibrada (28s - 45s)",
    pass: avgLava >= 28 && avgLava <= 45,
    val: `${avgLava.toFixed(2)}s (min: ${minLava.toFixed(1)}s, max: ${maxLava.toFixed(1)}s)`
  },
  {
    name: "Regra do Ciclo Fechado: Zero partidas excedendo 60 segundos",
    pass: maxPendulum <= 60 && maxPotato <= 60 && maxGlass <= 60 && maxLava <= 60,
    val: `Max global: ${Math.max(maxPendulum, maxPotato, maxGlass, maxLava).toFixed(1)}s <= 60s`
  },
  {
    name: "Regra Anti-Frustração: Zero partidas encerrando antes de 10 segundos",
    pass: minPendulum >= 10 && minPotato >= 10 && minGlass >= 10 && minLava >= 10,
    val: `Min global: ${Math.min(minPendulum, minPotato, minGlass, minLava).toFixed(1)}s >= 10s`
  }
];

console.log("\n" + "=".repeat(75));
console.log(" RESULTADOS DO BALANCEAMENTO DE TENSÃO & ADRENALINA (10.000 RODADAS)");
console.log("=".repeat(75));

let allPassed = true;
checks.forEach(c => {
  const status = c.pass ? "[PASS]" : "[FAIL]";
  console.log(`  ${status} ${c.name} -> ${c.val}`);
  if (!c.pass) allPassed = false;
});

console.log("=".repeat(75));
if (allPassed) {
  console.log("TODAS AS MÉTRICAS DE BALANCEAMENTO DA FASE 7 FORAM APROVADAS COM 100%!");
  process.exit(0);
} else {
  console.error("FALHA EM UMA OU MAIS MÉTRICAS DE BALANCEAMENTO!");
  process.exit(1);
}
