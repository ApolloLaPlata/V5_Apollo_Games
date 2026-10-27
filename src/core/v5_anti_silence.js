/**
 * V5 ANTI-SILENCE ENGINE — Motor Autônomo de Simulação de Live 9:16
 * Holding V5 Apollo — Capitania V5 Games
 * Versão: 2.0.0
 * 
 * Garante que nenhuma live fique com tela estática ou áudio em silêncio.
 * Se o chat ficar ocioso por 2.5s, injeta micro-ações orgânicas e balanceadas,
 * silenciando instantaneamente assim que um espectador real interage.
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5AntiSilence = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  class V5AntiSilence {
    constructor(options = {}) {
      this.enabled = options.enabled !== undefined ? options.enabled : true;
      this.silenceThreshold = options.silenceThreshold || 2500; // 2.5s de tolerância
      this.minInterval = options.minInterval || 1800; // 1.8s
      this.maxInterval = options.maxInterval || 3200; // 3.2s
      this.intensity = options.intensity || 'normal'; // 'light', 'normal', 'frenzy'

      this.lastRealEventTime = Date.now();
      this.timerId = null;
      this.onInject = options.onInject || null;

      // Banco Orgânico de Usuários Simulados
      this.userPool = [
        '@carlos_gamer', '@mari_tiktok', '@lucas_stream', '@renata_pro',
        '@thiago_live', '@ana_clara99', '@bruno_sp', '@danilo_play',
        '@julia_v5', '@pedro_fps', '@camila_br', '@felipe_yt',
        '@rodrigo_king', '@bia_streamer', '@vitor_speed'
      ];

      // Catálogo de Presentes Simulados
      this.giftCatalog = [
        { name: 'Rosa Virtual', coins: 1, weight: 5 },
        { name: 'Moeda V5', coins: 5, weight: 15 },
        { name: 'Coração', coins: 10, weight: 25 }
      ];

      // Tendência de Equilíbrio (Bias para aproximar placares)
      this.currentScoreA = 0;
      this.currentScoreB = 0;

      if (this.enabled) {
        this.scheduleNextAction();
      }
    }

    /**
     * Registra que houve um evento real de espectador na live.
     * Silencia imediatamente a simulação para dar palco total ao usuário real.
     */
    notifyRealInteraction() {
      this.lastRealEventTime = Date.now();
      if (this.timerId) {
        clearTimeout(this.timerId);
        this.scheduleNextAction(this.silenceThreshold + 1000); // Aguarda pelo menos 3.5s
      }
    }

    /**
     * Atualiza o placar atual para que o motor ajude o time que estiver perdendo,
     * mantendo a disputa empolgante e acirrada.
     */
    updateScores(scoreA, scoreB) {
      this.currentScoreA = scoreA;
      this.currentScoreB = scoreB;
    }

    /**
     * Agenda a próxima microação autônoma com intervalo estocástico
     */
    scheduleNextAction(customDelay = null) {
      if (!this.enabled) return;

      let delay = customDelay;
      if (delay === null) {
        const span = this.maxInterval - this.minInterval;
        delay = this.minInterval + Math.floor(Math.random() * span);
        if (this.intensity === 'frenzy') delay = Math.floor(delay * 0.6);
        if (this.intensity === 'light') delay = Math.floor(delay * 1.5);
      }

      this.timerId = setTimeout(() => {
        this.executeMicroAction();
      }, delay);
    }

    /**
     * Executa a injeção determinística de ação autônoma
     */
    executeMicroAction() {
      if (!this.enabled) return;

      const idleDuration = Date.now() - this.lastRealEventTime;

      // Se a live estiver ativa com humanos reais dentro do threshold, não dispara
      if (idleDuration >= this.silenceThreshold) {
        const actionPayload = this.generateOrganicAction();
        if (this.onInject) {
          this.onInject(actionPayload);
        }
      }

      // Reagenda próxima ação
      this.scheduleNextAction();
    }

    /**
     * Gera um payload orgânico balanceado
     */
    generateOrganicAction() {
      const user = this.userPool[Math.floor(Math.random() * this.userPool.length)];

      // Inteligência de Balanceamento Elástico:
      // Se o Time A estiver ganhando muito, dá 65% de chance de votar no Time B e vice-versa
      let team = 'A';
      const diff = this.currentScoreA - this.currentScoreB;
      if (diff > 50) {
        team = Math.random() < 0.65 ? 'B' : 'A';
      } else if (diff < -50) {
        team = Math.random() < 0.65 ? 'A' : 'B';
      } else {
        team = Math.random() < 0.5 ? 'A' : 'B';
      }

      // 15% de chance de ser um micro-presente que agita o visual da tela
      const isGift = Math.random() < 0.15;

      if (isGift) {
        const gift = this.giftCatalog[Math.floor(Math.random() * this.giftCatalog.length)];
        return {
          type: 'gift',
          action: 'boost',
          team: team,
          user: user,
          giftName: gift.name,
          coins: gift.coins,
          weight: gift.weight,
          isBot: true,
          timestamp: Date.now()
        };
      }

      // Comentário padrão de votação
      return {
        type: 'comment',
        action: 'vote',
        team: team,
        user: user,
        comment: team === 'A' ? '1' : '2',
        weight: 1,
        isBot: true,
        timestamp: Date.now()
      };
    }

    setIntensity(level) {
      if (['light', 'normal', 'frenzy'].includes(level)) {
        this.intensity = level;
      }
    }

    pause() {
      this.enabled = false;
      if (this.timerId) {
        clearTimeout(this.timerId);
        this.timerId = null;
      }
    }

    resume() {
      if (!this.enabled) {
        this.enabled = true;
        this.lastRealEventTime = Date.now();
        this.scheduleNextAction();
      }
    }

    destroy() {
      this.pause();
    }
  }

  return V5AntiSilence;
}));