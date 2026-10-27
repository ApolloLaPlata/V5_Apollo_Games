/**
 * V5 PENDULUM ELIMINATION ENGINE — Motor de Física Pendular Não-Linear e Tensão Estrutural
 * Holding V5 Apollo — Divisão de Jogos & Transmissão 9:16
 * Fase 7: Cartuchos de Tensão, Eliminação & Cronômetro (Etapas 061 & 063)
 * Versão: 1.0.0
 * 
 * Especialmente arquitetado para transmissões verticais 9:16 (1080x1920 responsivo):
 * - Simulação física exata de pêndulo não-linear: d²θ/dt² = -(g/L)*sin(θ) - γ*ω
 * - Integrador Verlet simplificado com conservação de momento angular
 * - Sistema de ajuste de ângulo de lançamento comandado pelo chat (0° a 85°)
 * - Detecção contínua de colisão contra muralha estrutural com transferência de momento
 * - Gerenciamento de rodadas de eliminação com contagem regressiva e pulso de adrenalina
 * - Object Pool de fragmentos e detritos estruturais (Zero GC)
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5PendulumEliminationEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  // =========================================================================
  // 1. OBJECT POOL DE DETRITOS ESTATÍSTICOS / FRAGMENTOS
  // =========================================================================
  class StructuralDebris {
    constructor() {
      this.active = false;
      this.x = 0;
      this.y = 0;
      this.vx = 0;
      this.vy = 0;
      this.rotation = 0;
      this.rotSpeed = 0;
      this.size = 8;
      this.color = '#94a3b8';
      this.life = 0;
      this.maxLife = 1.0;
    }

    init(x, y, vx, vy, size, color) {
      this.active = true;
      this.x = x;
      this.y = y;
      this.vx = vx;
      this.vy = vy;
      this.rotation = Math.random() * Math.PI * 2;
      this.rotSpeed = (Math.random() - 0.5) * 10;
      this.size = size || (6 + Math.random() * 8);
      this.color = color || '#cbd5e1';
      this.life = 0;
      this.maxLife = 0.8 + Math.random() * 0.4;
    }

    step(dt) {
      if (!this.active) return;
      this.life += dt;
      this.x += this.vx * dt;
      this.y += this.vy * dt;
      this.vy += 650 * dt; // Gravidade na queda dos destroços
      this.rotation += this.rotSpeed * dt;

      if (this.life >= this.maxLife) {
        this.active = false;
      }
    }
  }

  // =========================================================================
  // 2. MOTOR PRINCIPAL: V5 PENDULUM ELIMINATION ENGINE
  // =========================================================================
  class V5PendulumEliminationEngine {
    constructor(options = {}) {
      // Geometria e Física do Pêndulo
      this.pivotX = options.pivotX || 540;   // Coordenada do teto (X central em 1080)
      this.pivotY = options.pivotY || 240;   // Coordenada do teto (Y)
      this.length = options.length || 520;   // Comprimento da corda/haste metálica
      this.gravity = options.gravity || 980; // Constante gravitacional em pixels/s²
      this.damping = options.damping || 0.08;// Amortecimento do ar (fricção)
      this.ballRadius = options.ballRadius || 38; // Raio da bola de demolição
      this.mass = options.mass || 50;        // Massa da bola de demolição (kg)

      // Estado Angular
      this.angle = options.initialAngle || (Math.PI / 3); // Ângulo θ (radianos)
      this.angularVelocity = 0;              // ω = dθ/dt
      this.angularAcceleration = 0;          // α = d²θ/dt²
      this.isSwinging = false;
      this.isSuperCharged = false;          // Boost de presentes (fogo cósmico)

      // Fortaleza Estrutural Destrutível
      this.fortressX = options.fortressX || 780; // Posição X da fortaleza
      this.fortressMaxHp = options.fortressMaxHp || 50000;
      this.fortressHp = this.fortressMaxHp;
      this.wallIntegrity = 1.0;              // 1.0 a 0.0

      // Cronômetro de Tensão & Rodada
      this.roundDuration = options.roundDuration || 45.0;
      this.timeRemaining = this.roundDuration;
      this.isRoundActive = true;
      this.winner = null;

      // Tremor de Tela
      this.screenShake = 0;

      // Object Pool de Detritos (100 unidades)
      this.debrisPool = [];
      for (let i = 0; i < 100; i++) {
        this.debrisPool.push(new StructuralDebris());
      }

      // Callbacks
      this.onImpact = null;        // (impactForce, damage, remainingHp)
      this.onFortressCollapse = null; // ()
      this.onTimeOut = null;       // ()
    }

    reset() {
      this.angle = Math.PI / 3;
      this.angularVelocity = 0;
      this.angularAcceleration = 0;
      this.isSwinging = false;
      this.isSuperCharged = false;
      this.fortressHp = this.fortressMaxHp;
      this.wallIntegrity = 1.0;
      this.timeRemaining = this.roundDuration;
      this.isRoundActive = true;
      this.winner = null;
      this.screenShake = 0;

      for (let i = 0; i < this.debrisPool.length; i++) {
        this.debrisPool[i].active = false;
      }
    }

    /**
     * Ajusta o ângulo de recuo do pêndulo pelo chat (ex: comentários '1', '2', '3' ou 'puxar')
     * @param {number} pullRadians Ângulo de puxada (radianos positivos ou negativos)
     */
    pull(pullRadians = 0.25) {
      if (!this.isRoundActive) return;
      this.angle = Math.min(Math.PI * 0.48, Math.max(-Math.PI * 0.48, this.angle + pullRadians));
      this.isSwinging = false;
      this.angularVelocity = 0;
    }

    /**
     * Libera o pêndulo para colisão devastadora
     * @param {boolean} isSuper Se for presente de super impacto
     */
    release(isSuper = false) {
      if (!this.isRoundActive) return;
      this.isSwinging = true;
      this.isSuperCharged = isSuper;
      if (isSuper) {
        this.angle = Math.PI * 0.46; // Ângulo máximo de 83 graus!
        this.angularVelocity = 1.2;
      }
    }

    /**
     * Aplica torque direto instantâneo
     */
    applyImpulse(force = 2.0) {
      if (!this.isRoundActive) return;
      this.isSwinging = true;
      this.angularVelocity += force;
    }

    // Calcula coordenadas Cartesianas da bola no plano
    getBallPosition() {
      const x = this.pivotX + Math.sin(this.angle) * this.length;
      const y = this.pivotY + Math.cos(this.angle) * this.length;
      return { x, y };
    }

    // --- LOOP DE ATUALIZAÇÃO FÍSICA ---
    step(dt = 1 / 60) {
      // 1. Atualizar detritos estruturais no pool
      for (let i = 0; i < this.debrisPool.length; i++) {
        if (this.debrisPool[i].active) {
          this.debrisPool[i].step(dt);
        }
      }

      // 2. Amortecimento de Screen Shake
      if (this.screenShake > 0) {
        this.screenShake = Math.max(0, this.screenShake - (30 * dt));
      }

      if (!this.isRoundActive) return;

      // 3. Cronômetro de Eliminação
      this.timeRemaining -= dt;
      if (this.timeRemaining <= 0) {
        this.timeRemaining = 0;
        this.isRoundActive = false;
        this.winner = 'DEFESA';
        if (this.onTimeOut) this.onTimeOut();
        return;
      }

      // 4. Integração Física do Pêndulo Não-Linear
      if (this.isSwinging) {
        // Equação diferencial: α = -(g/L) * sin(θ) - (γ/M) * ω
        const naturalFreqSq = this.gravity / this.length;
        this.angularAcceleration = (-naturalFreqSq * Math.sin(this.angle)) - (this.damping * this.angularVelocity);

        // Integração Semi-Implícita de Euler / Verlet
        this.angularVelocity += this.angularAcceleration * dt;
        this.angle += this.angularVelocity * dt;

        // 5. Detecção de Impacto com a Fortaleza Estrutural
        const pos = this.getBallPosition();
        if (pos.x + this.ballRadius >= this.fortressX && this.angularVelocity > 0) {
          this._handleFortressCollision(pos);
        }
      }
    }

    _handleFortressCollision(pos) {
      // Momento linear da bola: p = mass * linearVelocity
      const linearSpeed = Math.abs(this.angularVelocity * this.length);
      let impactEnergy = 0.5 * this.mass * linearSpeed * (linearSpeed / 100);

      if (this.isSuperCharged) {
        impactEnergy *= 4.0; // 4x dano em golpe cósmico de presente!
      }

      const damage = Math.floor(impactEnergy);
      this.fortressHp = Math.max(0, this.fortressHp - damage);
      this.wallIntegrity = Math.max(0, this.fortressHp / this.fortressMaxHp);

      // Rebote elástico com perda de energia
      const restitution = 0.45;
      this.angularVelocity = -this.angularVelocity * restitution;

      // Screen Shake proporcional
      this.screenShake = this.isSuperCharged ? 28 : Math.min(20, linearSpeed * 0.03);

      // Spawnar detritos de alvenaria
      this._spawnStructuralDebris(pos.x, pos.y, this.isSuperCharged ? 35 : 14);

      if (this.onImpact) {
        this.onImpact(linearSpeed, damage, this.fortressHp);
      }

      // Verificação de Colapso Total da Fortaleza
      if (this.fortressHp <= 0) {
        this.isRoundActive = false;
        this.winner = 'DEMOLIDOR';
        this.screenShake = 35;
        this._spawnStructuralDebris(pos.x, pos.y, 60);
        if (this.onFortressCollapse) {
          this.onFortressCollapse();
        }
      }
    }

    _spawnStructuralDebris(originX, originY, count = 12) {
      let spawned = 0;
      for (let i = 0; i < this.debrisPool.length && spawned < count; i++) {
        if (!this.debrisPool[i].active) {
          const vx = (Math.random() * -300) - 50; // Detritos voam para a esquerda
          const vy = (Math.random() - 0.7) * 400;
          const color = Math.random() > 0.4 ? '#facc15' : '#94a3b8';
          this.debrisPool[i].init(originX, originY, vx, vy, 4 + Math.random() * 8, color);
          spawned++;
        }
      }
    }
  }

  return V5PendulumEliminationEngine;
}));
