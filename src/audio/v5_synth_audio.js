/**
 * V5 SYNTH AUDIO — Gerador Procedural de Efeitos Sonoros para Lives 9:16
 * Holding V5 Apollo — Divisão de Transmissão & Jogos
 * Versão: 2.0.0 (Polifonia, Ruído Branco, Síntese FM e Efeitos Especiais)
 * 100% nativo via Web Audio API — Zero dependência externa (.mp3/.wav).
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5SynthAudio = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  class V5SynthAudio {
    constructor() {
      this.ctx = null;
      this.isMuted = false;
      this.masterVolume = 0.8;
      this.masterGain = null;
    }

    getAudioContext() {
      if (!this.ctx) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioCtx();
        this.masterGain = this.ctx.createGain();
        this.masterGain.gain.setValueAtTime(this.masterVolume, this.ctx.currentTime);
        this.masterGain.connect(this.ctx.destination);
      }
      if (this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      return this.ctx;
    }

    setMasterVolume(val) {
      this.masterVolume = Math.max(0, Math.min(1, val));
      if (this.masterGain && this.ctx) {
        this.masterGain.gain.setValueAtTime(this.masterVolume, this.ctx.currentTime);
      }
    }

    // =========================================================================
    // 1. GERADOR DE RUÍDO BRANCO FILTRADO (Explosões, Confetes, Balões)
    // =========================================================================

    /**
     * Gera buffer estático de ruído branco de 1 segundo
     */
    createNoiseBuffer() {
      const ctx = this.getAudioContext();
      const bufferSize = ctx.sampleRate;
      const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
      }
      return buffer;
    }

    /**
     * Explosão pesada de impacto ou canhão com filtro passa-baixa
     */
    playExplosion(duration = 0.6, cutoffFreq = 400) {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      const noise = ctx.createBufferSource();
      noise.buffer = this.createNoiseBuffer();

      const filter = ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(cutoffFreq, now);
      filter.frequency.exponentialRampToValueAtTime(30, now + duration);

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.4, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + duration);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(this.masterGain);

      noise.start(now);
      noise.stop(now + duration);
    }

    /**
     * Pop rápido de confete ou balão estourando
     */
    playConfettiPop() {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      const noise = ctx.createBufferSource();
      noise.buffer = this.createNoiseBuffer();

      const filter = ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(1400, now);
      filter.Q.setValueAtTime(3, now);

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(this.masterGain);

      noise.start(now);
      noise.stop(now + 0.12);
    }

    // =========================================================================
    // 2. SÍNTESE FM (Frequency Modulation) — Laser, Sinos Metálicos, Bumpers
    // =========================================================================

    /**
     * Sintetizador FM com Carrier e Modulator para timbres ricos
     */
    playFMSynth(carrierFreq = 440, modFreq = 220, modIndex = 150, duration = 0.3) {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      // Carrier (Oscilador Principal)
      const carrier = ctx.createOscillator();
      carrier.type = 'sine';
      carrier.frequency.setValueAtTime(carrierFreq, now);

      // Modulator (Oscilador que modula a frequência do Carrier)
      const modulator = ctx.createOscillator();
      modulator.type = 'sine';
      modulator.frequency.setValueAtTime(modFreq, now);

      // Ganho de Modulação
      const modGain = ctx.createGain();
      modGain.gain.setValueAtTime(modIndex, now);
      modGain.gain.exponentialRampToValueAtTime(0.01, now + duration);

      // Envelope de Volume Principal
      const mainGain = ctx.createGain();
      mainGain.gain.setValueAtTime(0.25, now);
      mainGain.gain.exponentialRampToValueAtTime(0.001, now + duration);

      // Conexões FM
      modulator.connect(modGain);
      modGain.connect(carrier.frequency);

      carrier.connect(mainGain);
      mainGain.connect(this.masterGain);

      modulator.start(now);
      carrier.start(now);

      modulator.stop(now + duration);
      carrier.stop(now + duration);
    }

    /**
     * Bumper Elástico de Pinball (FM com efeito 'boing')
     */
    playBumper() {
      this.playFMSynth(280, 140, 250, 0.22);
    }

    /**
     * Disparo laser arcade retrô
     */
    playLaser() {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(990, now);
      osc.frequency.exponentialRampToValueAtTime(110, now + 0.15);

      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + 0.15);
    }

    // =========================================================================
    // 3. GERADOR DE ACORDES POLIFÔNICOS (Triunfo, Vitória, Mudança de Fase)
    // =========================================================================

    /**
     * Toca um acorde simultâneo com múltiplos osciladores afinados
     */
    playChord(chordType = 'major', rootFreq = 440, duration = 0.5) {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      let ratios = [1, 1.25, 1.5]; // Maior (Tônica, 3ª maior, 5ª justa)
      if (chordType === 'minor') ratios = [1, 1.2, 1.5];
      if (chordType === 'power') ratios = [1, 1.5, 2.0];
      if (chordType === 'glory') ratios = [1, 1.25, 1.5, 2.0]; // Maior com oitava

      ratios.forEach((ratio, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        const freq = rootFreq * ratio;
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, now);

        // Micro-detune estéreo para criar efeito chorus espacial
        osc.detune.setValueAtTime((idx - 1) * 8, now);

        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + duration);

        osc.connect(gain);
        gain.connect(this.masterGain);

        osc.start(now);
        osc.stop(now + duration);
      });
    }

    // =========================================================================
    // 4. EFEITOS CLÁSSICOS DE LIVE (Moeda, Apito, Motor, Tração)
    // =========================================================================

    // Som de Moeda / Presente individual recebido
    playCoin() {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(987.77, now); // B5
      osc.frequency.setValueAtTime(1318.51, now + 0.08); // E6

      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + 0.35);
    }

    // Chuva rápida de moedas
    playCoinShower(count = 5) {
      for (let i = 0; i < count; i++) {
        setTimeout(() => this.playCoin(), i * 65);
      }
    }

    // Som de tração na corda / passo pesado
    playTug() {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(150, now);
      osc.frequency.exponentialRampToValueAtTime(60, now + 0.12);

      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + 0.15);
    }

    // Apito do árbitro
    playWhistle() {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(2600, now);
      osc.frequency.linearRampToValueAtTime(3200, now + 0.06);
      osc.frequency.setValueAtTime(2800, now + 0.12);

      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + 0.25);
    }

    // Tic-tac de contagem regressiva (3, 2, 1...)
    playCountdownTick(isFinal = false) {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      const freq = isFinal ? 880 : 440;
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, now);

      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + (isFinal ? 0.4 : 0.15));

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + (isFinal ? 0.4 : 0.15));
    }

    // Fanfarra de vitória clássica
    playVictory() {
      this.playChord('glory', 523.25, 0.8);
      setTimeout(() => this.playChord('glory', 659.25, 1.2), 300);
      setTimeout(() => this.playConfettiPop(), 600);
    }
  }

  return V5SynthAudio;
}));