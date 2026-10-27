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
     * Enchimento Hiper-Realista de Balão com Sopro Pneumático e Tensão Harmônica
     * @param {number} pressureRatio 0.0 a 1.0
     */
    playBalloonInflate(pressureRatio = 0.5) {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      // 1. Sopro de ar pressurizado (ruído com filtro passa-faixa)
      const noise = ctx.createBufferSource();
      noise.buffer = this.createNoiseBuffer();
      const noiseFilter = ctx.createBiquadFilter();
      noiseFilter.type = 'bandpass';
      noiseFilter.frequency.setValueAtTime(900 + (pressureRatio * 1600), now);
      noiseFilter.Q.setValueAtTime(2.5, now);

      const noiseGain = ctx.createGain();
      noiseGain.gain.setValueAtTime(0.16, now);
      noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.11);

      noise.connect(noiseFilter);
      noiseFilter.connect(noiseGain);
      noiseGain.connect(this.masterGain);
      noise.start(now);
      noise.stop(now + 0.11);

      // 2. Tensão harmônica da borracha (chirp ascendente)
      const osc = ctx.createOscillator();
      const oscGain = ctx.createGain();
      osc.type = 'triangle';
      const baseFreq = 160 + (pressureRatio * 240);
      osc.frequency.setValueAtTime(baseFreq, now);
      osc.frequency.exponentialRampToValueAtTime(baseFreq * 1.5, now + 0.09);

      oscGain.gain.setValueAtTime(0.14, now);
      oscGain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);

      osc.connect(oscGain);
      oscGain.connect(this.masterGain);
      osc.start(now);
      osc.stop(now + 0.09);
    }

    /**
     * Estouro de Balão Hiper-Realista em 3 Estágios (Snap + Shockwave + Sub-Bass Boom)
     */
    playBalloonPop() {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      // 1. Snap de alta frequência
      const snapNoise = ctx.createBufferSource();
      snapNoise.buffer = this.createNoiseBuffer();
      const snapFilter = ctx.createBiquadFilter();
      snapFilter.type = 'highpass';
      snapFilter.frequency.setValueAtTime(1800, now);

      const snapGain = ctx.createGain();
      snapGain.gain.setValueAtTime(0.45, now);
      snapGain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);

      snapNoise.connect(snapFilter);
      snapFilter.connect(snapGain);
      snapGain.connect(this.masterGain);
      snapNoise.start(now);
      snapNoise.stop(now + 0.15);

      // 2. Shockwave do deslocamento de ar
      const shock = ctx.createOscillator();
      const shockGain = ctx.createGain();
      shock.type = 'sawtooth';
      shock.frequency.setValueAtTime(450, now);
      shock.frequency.exponentialRampToValueAtTime(45, now + 0.25);

      shockGain.gain.setValueAtTime(0.4, now);
      shockGain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);

      shock.connect(shockGain);
      shockGain.connect(this.masterGain);
      shock.start(now);
      shock.stop(now + 0.25);

      // 3. Sub-bass boom acústico (55Hz)
      const boom = ctx.createOscillator();
      const boomGain = ctx.createGain();
      boom.type = 'sine';
      boom.frequency.setValueAtTime(65, now);
      boom.frequency.exponentialRampToValueAtTime(30, now + 0.55);

      boomGain.gain.setValueAtTime(0.5, now);
      boomGain.gain.exponentialRampToValueAtTime(0.001, now + 0.55);

      boom.connect(boomGain);
      boomGain.connect(this.masterGain);
      boom.start(now);
      boom.stop(now + 0.55);
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

    /**
     * Micro-Onda de Choque Subaquática (Underwater Shockwave)
     * Combina implosão por cavitação hidrostática, sub-bass rumble abafado e varredura ressonante.
     * @param {number} intensity Intensidade do impacto (0.5 a 2.0)
     */
    playUnderwaterShockwave(intensity = 1.0) {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;
      const clampedIntensity = Math.max(0.5, Math.min(2.0, intensity));

      // 1. Cavitação Hidráulica (Ruído branco abafado sob alta pressão com filtro passa-baixa ressonante)
      const noise = ctx.createBufferSource();
      noise.buffer = this.createNoiseBuffer();
      const filter = ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(450 * clampedIntensity, now);
      filter.frequency.exponentialRampToValueAtTime(40, now + 0.6);
      filter.Q.setValueAtTime(3.5, now);

      const noiseGain = ctx.createGain();
      noiseGain.gain.setValueAtTime(0.35 * clampedIntensity, now);
      noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);

      noise.connect(filter);
      filter.connect(noiseGain);
      noiseGain.connect(this.masterGain);
      noise.start(now);
      noise.stop(now + 0.6);

      // 2. Sub-Bass Hydro Rumble (Estrondo profundo de deslocamento de massa d'água)
      const subOsc = ctx.createOscillator();
      const subGain = ctx.createGain();
      subOsc.type = 'sine';
      subOsc.frequency.setValueAtTime(95, now);
      subOsc.frequency.exponentialRampToValueAtTime(28, now + 0.7);

      subGain.gain.setValueAtTime(0.45 * clampedIntensity, now);
      subGain.gain.exponentialRampToValueAtTime(0.001, now + 0.7);

      subOsc.connect(subGain);
      subGain.connect(this.masterGain);
      subOsc.start(now);
      subOsc.stop(now + 0.7);

      // 3. Pulso de Eco Aquático Ressonante (Sonar Ripple)
      const echoOsc = ctx.createOscillator();
      const echoGain = ctx.createGain();
      echoOsc.type = 'triangle';
      echoOsc.frequency.setValueAtTime(180, now + 0.05);
      echoOsc.frequency.exponentialRampToValueAtTime(60, now + 0.35);

      echoGain.gain.setValueAtTime(0.2 * clampedIntensity, now + 0.05);
      echoGain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

      echoOsc.connect(echoGain);
      echoGain.connect(this.masterGain);
      echoOsc.start(now + 0.05);
      echoOsc.stop(now + 0.35);
    }

    /**
     * Alarme Sonoro de Inundação / Sonar Hydro-Pulse
     * Pulso sonoro de emergência subaquático avisando que a maré passou do limite crítico (>80%).
     * @param {boolean} isUrgent Se true, frequência mais aguda e compasso mais rápido
     */
    playFloodAlert(isUrgent = false) {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      const freq1 = isUrgent ? 880 : 587.33; // A5 ou D5
      const freq2 = isUrgent ? 659.25 : 440;    // E5 ou A4

      [ { f: freq1, t: 0.0 }, { f: freq2, t: 0.14 } ].forEach((tone) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(tone.f, now + tone.t);
        osc.frequency.linearRampToValueAtTime(tone.f * 0.95, now + tone.t + 0.12);

        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(1400, now + tone.t);

        gain.gain.setValueAtTime(0.18, now + tone.t);
        gain.gain.exponentialRampToValueAtTime(0.001, now + tone.t + 0.12);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.masterGain);

        osc.start(now + tone.t);
        osc.stop(now + tone.t + 0.12);
      });
    }

    /**
     * Estouro de Bolha de Alta Tensão / Micro-Respingo
     */
    playBubblePop() {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      const startF = 350 + Math.random() * 200;
      osc.frequency.setValueAtTime(startF, now);
      osc.frequency.exponentialRampToValueAtTime(startF * 2.2, now + 0.06);

      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + 0.06);
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

    // =========================================================================
    // 5. BIBLIOTECA PROCEDURAL DE JINGLES E FANFARRAS DE VITÓRIA (5 SEGUNDOS)
    // =========================================================================

    /**
     * Marcha Comemorativa Épica (Exatos 5 Segundos para a tela de vitória)
     * Estrutura: Fanfarra Triunfal -> Arpejo Dinâmico -> Acorde Sustentado -> Confete Pop
     */
    playEpicVictoryJingle() {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      // Padrão melódico da fanfarra: Sol4, Sol4, Sol4, Dó5, Mi5, Sol5, Dó6
      const score = [
        { f: 392.00, t: 0.00, d: 0.18, type: 'triangle' }, // G4
        { f: 392.00, t: 0.22, d: 0.18, type: 'triangle' }, // G4
        { f: 392.00, t: 0.44, d: 0.18, type: 'triangle' }, // G4
        { f: 523.25, t: 0.68, d: 0.65, type: 'sawtooth' }, // C5 (Longo)
        { f: 659.25, t: 1.35, d: 0.40, type: 'triangle' }, // E5
        { f: 783.99, t: 1.80, d: 0.70, type: 'sawtooth' }, // G5
        { f: 1046.50, t: 2.55, d: 1.80, type: 'triangle' } // C6 (Clímax sustentado)
      ];

      score.forEach(note => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        const startT = now + note.t;

        osc.type = note.type;
        osc.frequency.setValueAtTime(note.f, startT);

        // Micro-harmônico metálico
        gain.gain.setValueAtTime(0.22, startT);
        gain.gain.exponentialRampToValueAtTime(0.001, startT + note.d);

        osc.connect(gain);
        gain.connect(this.masterGain);

        osc.start(startT);
        osc.stop(startT + note.d);
      });

      // Acorde polifônico final glorioso no segundo 2.55
      setTimeout(() => {
        this.playChord('glory', 523.25, 2.0);
      }, 2550);

      // Estouro de confete procedural no clímax
      setTimeout(() => {
        this.playConfettiPop();
      }, 2600);

      setTimeout(() => {
        this.playConfettiPop();
      }, 3200);
    }

    /**
     * Jingle Frenesi do Jackpot Dourado (5 Segundos de arpejos e moedas)
     */
    playJackpotFrenzyJingle() {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      // Arpejo cintilante acelerado
      const arpeggio = [523.25, 659.25, 783.99, 1046.50, 1318.51, 1567.98, 2093.00];
      for (let cycle = 0; cycle < 3; cycle++) {
        arpeggio.forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          const startT = now + (cycle * 0.8) + (idx * 0.08);

          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, startT);

          gain.gain.setValueAtTime(0.18, startT);
          gain.gain.exponentialRampToValueAtTime(0.001, startT + 0.25);

          osc.connect(gain);
          gain.connect(this.masterGain);

          osc.start(startT);
          osc.stop(startT + 0.25);
        });
      }

      // Cascata de moedas tilintando
      this.playCoinShower(8);
      setTimeout(() => this.playCoinShower(8), 1200);
      setTimeout(() => this.playChord('glory', 659.25, 1.5), 2600);
    }

    /**
     * Jingle de Início de Partida ("Round Start" - 2 Segundos de contagem e energia)
     */
    playRoundStartJingle() {
      if (this.isMuted) return;
      this.playCountdownTick(false);
      setTimeout(() => this.playCountdownTick(false), 500);
      setTimeout(() => this.playCountdownTick(true), 1000);
      setTimeout(() => {
        this.playWhistle();
        this.playChord('power', 440, 0.7);
      }, 1500);
    }

    /**
     * Stinger de Mudança de Liderança (1.5 Segundos de tensão dramática)
     */
    playLeadChangeJingle() {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.linearRampToValueAtTime(880, now + 0.35);

      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + 0.6);

      setTimeout(() => this.playChord('power', 523.25, 0.6), 350);
    }

    /**
     * Trombone Triste / Derrota Cômica (3.5 Segundos de "Wah-Wah-Wah-Waaah")
     */
    playSadTromboneJingle() {
      if (this.isMuted) return;
      const ctx = this.getAudioContext();
      const now = ctx.currentTime;

      const notes = [
        { f: 293.66, t: 0.0, d: 0.4 }, // D4
        { f: 277.18, t: 0.5, d: 0.4 }, // C#4
        { f: 261.63, t: 1.0, d: 0.4 }, // C4
        { f: 246.94, t: 1.5, d: 1.2 }  // B3 com queda
      ];

      notes.forEach((n, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        const startT = now + n.t;

        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(n.f, startT);

        // Queda de tom na última nota
        if (idx === 3) {
          osc.frequency.exponentialRampToValueAtTime(n.f * 0.75, startT + n.d);
        }

        gain.gain.setValueAtTime(0.22, startT);
        gain.gain.exponentialRampToValueAtTime(0.001, startT + n.d);

        osc.connect(gain);
        gain.connect(this.masterGain);

        osc.start(startT);
        osc.stop(startT + n.d);
      });
    }

    // Fanfarra de vitória clássica (Retrocompatibilidade)
    playVictory() {
      this.playEpicVictoryJingle();
    }
  }

  return V5SynthAudio;
}));