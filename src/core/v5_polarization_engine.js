/**
 * V5 POLARIZATION ENGINE — Motor de Física de Disputa e Torcidas (Tug / Pressão 9:16)
 * Holding V5 Apollo — Capitania V5 Games
 * Versão: 1.0.0
 * 
 * Modela a física inercial de disputa entre 2 lados (Cabo de Guerra, Queda de Braço, Pressômetro):
 * - Centro de equilíbrio elástico (Spring Physics)
 * - Inércia e amortecimento de impactos (Damping / Impulse)
 * - Detecção suave de limites de vitória
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5PolarizationEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  class V5PolarizationEngine {
    constructor(options = {}) {
      this.center = options.center || 50.0;
      this.position = options.center || 50.0; // 0% a 100%
      this.velocity = 0.0;

      // Parâmetros de Física Ajustáveis
      this.springTension = options.springTension !== undefined ? options.springTension : 0.015;
      this.damping = options.damping !== undefined ? options.damping : 0.88;
      this.mass = options.mass || 1.0;
      this.forceMultiplier = options.forceMultiplier || 1.2;

      // Limiares de Vitória
      this.thresholdA = options.thresholdA || 14.0; // Perto do canto esquerdo
      this.thresholdB = options.thresholdB || 86.0; // Perto do canto direito

      // Estatísticas da Partida
      this.totalPullsA = 0;
      this.totalPullsB = 0;
      this.momentumA = 0;
      this.momentumB = 0;

      this.onVictory = options.onVictory || null;
      this.isLocked = false;
    }

    /**
     * Aplica impulso instantâneo gerado por voto ou presente
     * @param {'A'|'B'} team Lado que puxou/empurrou
     * @param {number} weight Peso do voto (1) ou presente (5 a 50)
     */
    applyForce(team, weight = 1) {
      if (this.isLocked) return;

      const impulse = (weight * this.forceMultiplier) / this.mass;

      if (team === 'A') {
        this.velocity -= impulse;
        this.totalPullsA += weight;
        this.momentumA += weight;
      } else {
        this.velocity += impulse;
        this.totalPullsB += weight;
        this.momentumB += weight;
      }
    }

    /**
     * Passo de simulação física (invocar dentro do requestAnimationFrame)
     * @returns {number} Posição normalizada (0.0 a 100.0)
     */
    update() {
      if (this.isLocked) return this.position;

      // 1. Força elástica em direção ao centro (simula resistência mecânica da corda/braço)
      const springForce = (this.center - this.position) * this.springTension;
      this.velocity += springForce;

      // 2. Amortecimento de atrito
      this.velocity *= this.damping;

      // 3. Atualiza posição
      this.position += this.velocity;

      // 4. Limites de colisão estritos
      if (this.position <= this.thresholdA) {
        this.position = this.thresholdA;
        this.velocity = 0;
        this.triggerWin('A');
      } else if (this.position >= this.thresholdB) {
        this.position = this.thresholdB;
        this.velocity = 0;
        this.triggerWin('B');
      }

      return this.position;
    }

    triggerWin(team) {
      if (this.isLocked) return;
      this.isLocked = true;
      if (this.onVictory) {
        this.onVictory({
          winner: team,
          finalPosition: this.position,
          totalA: this.totalPullsA,
          totalB: this.totalPullsB
        });
      }
    }

    reset() {
      this.position = this.center;
      this.velocity = 0;
      this.isLocked = false;
      this.momentumA = 0;
      this.momentumB = 0;
    }

    getProgressRatio() {
      return (this.position - this.thresholdA) / (this.thresholdB - this.thresholdA);
    }
  }

  return V5PolarizationEngine;
}));