/**
 * V5 ROUND MANAGER — Módulo Universal de Auto-Reset e Ciclo Fechado de Partidas
 * Holding V5 Apollo — Capitania V5 Games
 * Versão: 1.0.0
 * 
 * Gerencia partidas de 30 a 60 segundos com transição comemorativa de 5 segundos
 * e reinício 100% automático sem recarregar a página no OBS Studio.
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5RoundManager = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  const ROUND_STATES = {
    IDLE: 'idle',
    COUNTDOWN: 'countdown',
    PLAYING: 'playing',
    CELEBRATING: 'celebrating',
    RESETTING: 'resetting'
  };

  class V5RoundManager {
    constructor(options = {}) {
      this.duration = options.duration || 45; // 30 a 60s
      this.celebrationDuration = options.celebrationDuration || 5000; // 5 segundos
      this.roundNumber = 1;
      this.secondsRemaining = this.duration;
      this.state = ROUND_STATES.IDLE;
      
      this.timerInterval = null;
      this.celebrationTimeout = null;

      // Histórico de Vitórias Acumuladas
      this.wins = {
        A: 0,
        B: 0,
        C: 0,
        draws: 0
      };

      // Callbacks do Ciclo de Vida
      this.callbacks = {
        onStart: options.onStart || null,
        onTick: options.onTick || null,
        onEnd: options.onEnd || null,
        onReset: options.onReset || null
      };

      // Elementos do DOM (se informados)
      this.timerEl = options.timerEl || null;
      this.overlayEl = options.overlayEl || null;
      this.titleEl = options.titleEl || null;
      this.detailEl = options.detailEl || null;
      this.iconEl = options.iconEl || null;
      this.progressFillEl = options.progressFillEl || null;

      // Integração com o Sintetizador de Áudio Procedural
      this.audio = options.audio || null;

      // Auto-iniciar se solicitado
      if (options.autoStart !== false) {
        this.startRound();
      }
    }

    /**
     * Inicia uma nova rodada do cartucho
     */
    startRound() {
      this.clearAllTimers();
      this.state = ROUND_STATES.PLAYING;
      this.secondsRemaining = this.duration;

      // Atualiza interface inicial
      if (this.timerEl) {
        this.timerEl.innerText = this.secondsRemaining;
      }
      if (this.overlayEl) {
        this.overlayEl.classList.remove('active');
      }
      if (this.progressFillEl) {
        this.progressFillEl.style.width = '0%';
        this.progressFillEl.style.transition = 'none';
      }

      // Dispara som de início
      if (this.audio && typeof this.audio.playRoundStartJingle === 'function') {
        this.audio.playRoundStartJingle();
      }

      // Notifica callback onStart
      if (this.callbacks.onStart) {
        this.callbacks.onStart({
          roundNumber: this.roundNumber,
          duration: this.duration
        });
      }

      // Loop do cronômetro de 1 em 1 segundo
      this.timerInterval = setInterval(() => {
        this.secondsRemaining--;

        if (this.timerEl) {
          this.timerEl.innerText = this.secondsRemaining;
        }

        // Tic-tac sonoro nos últimos 3 segundos
        if (this.secondsRemaining <= 3 && this.secondsRemaining > 0) {
          if (this.audio && typeof this.audio.playCountdownTick === 'function') {
            this.audio.playCountdownTick(false);
          }
        }

        if (this.callbacks.onTick) {
          this.callbacks.onTick(this.secondsRemaining);
        }

        if (this.secondsRemaining <= 0) {
          this.endRound();
        }
      }, 1000);
    }

    /**
     * Encerra a rodada atual e ativa o modo celebração
     * Pode ser invocado por tempo limite (0s) ou por meta batida.
     */
    endRound(customResult = null) {
      if (this.state === ROUND_STATES.CELEBRATING) return;
      this.clearAllTimers();
      this.state = ROUND_STATES.CELEBRATING;

      // Determina resultado
      let result = customResult;
      if (!result && this.callbacks.onEnd) {
        result = this.callbacks.onEnd();
      }

      // Valores padrão de resultado
      result = result || {
        winner: 'A',
        winnerTitle: 'TIME AZUL VENCEU!',
        winnerIcon: '👑',
        winnerColor: '#38bdf8',
        detailText: `Rodada #${this.roundNumber} concluída com sucesso!`
      };

      // Atualiza placar histórico de vitórias
      if (result.winner === 'A') this.wins.A++;
      else if (result.winner === 'B') this.wins.B++;
      else if (result.winner === 'C') this.wins.C++;
      else this.wins.draws++;

      // Atualiza DOM do overlay comemorativo
      if (this.titleEl) {
        this.titleEl.innerText = result.winnerTitle;
        if (result.winnerColor) this.titleEl.style.color = result.winnerColor;
      }
      if (this.iconEl) {
        this.iconEl.innerText = result.winnerIcon || '👑';
      }
      if (this.detailEl) {
        this.detailEl.innerText = result.detailText;
      }
      if (this.overlayEl) {
        this.overlayEl.classList.add('active');
      }

      // Animação suave da barra de auto-reset (5 segundos de preenchimento linear)
      if (this.progressFillEl) {
        this.progressFillEl.style.width = '0%';
        setTimeout(() => {
          this.progressFillEl.style.transition = `width ${this.celebrationDuration}ms linear`;
          this.progressFillEl.style.width = '100%';
        }, 50);
      }

      // Toca jingle procedural de vitória de 5 segundos
      if (this.audio) {
        if (typeof this.audio.playEpicVictoryJingle === 'function') {
          this.audio.playEpicVictoryJingle();
        } else if (typeof this.audio.playVictory === 'function') {
          this.audio.playVictory();
        }
      }

      // Auto-reset programado para após a comemoração
      this.celebrationTimeout = setTimeout(() => {
        this.resetRound();
      }, this.celebrationDuration);
    }

    /**
     * Reseta entidades e inicia a próxima rodada
     */
    resetRound() {
      this.state = ROUND_STATES.RESETTING;
      this.roundNumber++;

      if (this.callbacks.onReset) {
        this.callbacks.onReset({
          nextRound: this.roundNumber,
          wins: { ...this.wins }
        });
      }

      // Inicia imediatamente a próxima rodada
      this.startRound();
    }

    clearAllTimers() {
      if (this.timerInterval) {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
      }
      if (this.celebrationTimeout) {
        clearTimeout(this.celebrationTimeout);
        this.celebrationTimeout = null;
      }
    }

    isPlaying() {
      return this.state === ROUND_STATES.PLAYING;
    }

    isCelebrating() {
      return this.state === ROUND_STATES.CELEBRATING;
    }

    destroy() {
      this.clearAllTimers();
      this.state = ROUND_STATES.IDLE;
    }
  }

  return V5RoundManager;
}));