/**
 * V5 BOSS RAID ENGINE — Motor de Batalhas Coletivas Colaborativas
 * Holding V5 Apollo — Divisão de Jogos & Transmissão 9:16
 * Fase 6: Cartuchos Cooperativos & Boss Raids Épicos (Etapa 051)
 * Versão: 1.0.0
 * 
 * Especialmente arquitetado para transmissões verticais 9:16 (TikTok Live, YouTube Shorts, Twitch):
 * - Boss Titan com 1.000.000 HP enfrentando o chat coletivo em tempo real
 * - Máquina de estados: IDLE, ATTACKING, ENRAGED (< 30% HP), STAGGERED, DEFEATED
 * - Sistema de ataque escalonado: Comentários (Hits normais), Gifts (Críticos & Meteoros)
 * - Multiplicador dinâmico de combo baseado na frequência de mensagens do público
 * - Object Pool de Floating Combat Text (números de dano flutuantes sem alocação/GC)
 * - Leaderboard MVP em tempo real dos Top Atacantes e Top Doadores
 * - Auto-reset em ciclo fechado com contagem regressiva de rodada
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5BossRaidEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  // Estados do Boss
  const BOSS_STATES = {
    IDLE: 'IDLE',
    ATTACKING: 'ATTACKING',
    STAGGERED: 'STAGGERED',
    ENRAGED: 'ENRAGED',
    DEFEATED: 'DEFEATED',
    VICTORIOUS: 'VICTORIOUS'
  };

  // =========================================================================
  // 1. OBJECT POOL DE NÚMEROS DE DANO FLUTUANTES (FLOATING COMBAT TEXT)
  // =========================================================================
  class DamageNumber {
    constructor() {
      this.active = false;
      this.text = '';
      this.x = 0;
      this.y = 0;
      this.vx = 0;
      this.vy = 0;
      this.scale = 1.0;
      this.alpha = 1.0;
      this.color = '#ffffff';
      this.isCritical = false;
      this.life = 0;
      this.maxLife = 1.0;
    }

    init(text, x, y, isCritical = false, color = '#ffffff') {
      this.active = true;
      this.text = text;
      this.x = x;
      this.y = y;
      this.vx = (Math.random() - 0.5) * 60;
      this.vy = isCritical ? -180 - Math.random() * 80 : -90 - Math.random() * 40;
      this.scale = isCritical ? 1.6 : 1.0;
      this.alpha = 1.0;
      this.color = color;
      this.isCritical = isCritical;
      this.life = 0;
      this.maxLife = isCritical ? 1.4 : 0.9;
    }

    step(dt) {
      if (!this.active) return;
      this.life += dt;
      this.x += this.vx * dt;
      this.y += this.vy * dt;
      this.vy += 80 * dt; // Gravidade sutil

      const progress = this.life / this.maxLife;
      if (progress >= 1.0) {
        this.active = false;
      } else {
        this.alpha = Math.max(0, 1.0 - progress);
        if (this.isCritical && progress < 0.2) {
          this.scale = 1.6 + progress * 1.5;
        }
      }
    }
  }

  // =========================================================================
  // 2. MOTOR PRINCIPAL: V5 BOSS RAID ENGINE
  // =========================================================================
  class V5BossRaidEngine {
    constructor(options = {}) {
      // Parâmetros de HP do Titã
      this.maxHp = options.maxHp || 1000000;
      this.currentHp = this.maxHp;
      this.displayHp = this.maxHp; // HP suavizado para barras de vida animadas
      this.staggerMax = options.staggerMax || 50000;
      this.staggerCurrent = 0;

      // Tempo de Partida (Ciclo Fechado de 45 segundos padrão)
      this.roundDuration = options.roundDuration || 45.0;
      this.timeRemaining = this.roundDuration;
      this.isRoundActive = true;
      this.winner = null; // 'CHAT' ou 'BOSS'

      // Máquina de Estados do Boss
      this.state = BOSS_STATES.IDLE;
      this.stateTimer = 0;
      this.enrageThreshold = 0.30; // 30% HP entra em Fúria

      // Sistema de Combo
      this.comboCount = 0;
      this.comboTimer = 0;
      this.comboWindow = 2.0; // 2 segundos sem hits zera o combo
      this.comboMultiplier = 1.0;

      // Tremor de Tela (Screen Shake)
      this.screenShake = 0;

      // Ranking MVP em Tempo Real
      this.contributors = new Map(); // username -> { name, damage, gifts, hits, avatar }
      this.topMVP = [];

      // Object Pool de Números de Dano (120 instâncias)
      this.damagePool = [];
      this.maxDamageNumbers = 120;
      for (let i = 0; i < this.maxDamageNumbers; i++) {
        this.damagePool.push(new DamageNumber());
      }

      // Callbacks para UI & Áudio
      this.onDamageTaken = null;     // (damage, isCritical, attacker, newHp)
      this.onBossStateChange = null; // (oldState, newState)
      this.onBossAttack = null;      // (attackType, intensity)
      this.onStagger = null;         // ()
      this.onEnrage = null;          // ()
      this.onDefeat = null;          // (mvpList)
      this.onVictory = null;         // ()
      this.onComboUpdate = null;     // (comboCount, multiplier)
    }

    // Reinicia partida para ciclo fechado
    reset(options = {}) {
      this.maxHp = options.maxHp || this.maxHp;
      this.currentHp = this.maxHp;
      this.displayHp = this.maxHp;
      this.staggerCurrent = 0;
      this.timeRemaining = this.roundDuration;
      this.isRoundActive = true;
      this.winner = null;
      this.state = BOSS_STATES.IDLE;
      this.stateTimer = 0;
      this.comboCount = 0;
      this.comboTimer = 0;
      this.comboMultiplier = 1.0;
      this.screenShake = 0;
      this.contributors.clear();
      this.topMVP = [];

      // Desativar números do pool
      for (let i = 0; i < this.damagePool.length; i++) {
        this.damagePool[i].active = false;
      }

      if (this.onBossStateChange) this.onBossStateChange(null, BOSS_STATES.IDLE);
    }

    // --- REGISTRO DE ATAQUES DO CHAT ---
    /**
     * Aplica dano ao Boss disparado por evento do chat ou gift
     * @param {Object} event { user, type: 'comment'|'gift', giftName, value, spawnX, spawnY }
     */
    applyAttack(event = {}) {
      if (!this.isRoundActive || this.currentHp <= 0) return 0;

      const user = event.user || '@espectador';
      const isGift = event.type === 'gift';
      const giftName = event.giftName || null;
      const val = Math.max(1, event.value || 1);

      // 1. Cálculo de Dano Base
      let baseDamage = 150; // Dano de comentário normal (150 HP)
      let isCritical = false;
      let label = '';
      let color = '#38bdf8'; // Azul neon padrão

      if (isGift) {
        isCritical = true;
        // Presentes com peso massivo:
        if (giftName === 'Lion' || giftName === 'Universe' || val >= 1000) {
          baseDamage = 100000; // Golpe Meteoro Quântico
          label = `METEORO! -100K`;
          color = '#f59e0b'; // Ouro cósmico
          this.screenShake = Math.max(this.screenShake, 25);
        } else if (giftName === 'Capivara' || giftName === 'Doughnut' || val >= 100) {
          baseDamage = 25000;  // Raio Elemental
          label = `SUPER CRÍTICO! -25K`;
          color = '#ec4899'; // Rosa neon
          this.screenShake = Math.max(this.screenShake, 15);
        } else {
          // Rosa ou presentes padrão (1 a 99)
          baseDamage = 5000 * Math.max(1, Math.min(val, 20));
          label = `CRÍTICO! -${(baseDamage/1000).toFixed(0)}K`;
          color = '#ef4444'; // Vermelho crítico
          this.screenShake = Math.max(this.screenShake, 8);
        }
      } else {
        // Variação orgânica no comentário (+/- 25%)
        baseDamage = Math.floor(baseDamage * (0.85 + Math.random() * 0.35));
        label = `-${baseDamage}`;
        this.screenShake = Math.max(this.screenShake, 2.5);
      }

      // 2. Multiplicador de Combo & Stagger
      let finalMultiplier = this.comboMultiplier;
      if (this.state === BOSS_STATES.STAGGERED) {
        finalMultiplier *= 2.0; // 2x dano durante atordoamento!
        label += ` [2X STAGGER]`;
      }

      const totalDamage = Math.floor(baseDamage * finalMultiplier);

      // 3. Aplicação do Dano no HP
      this.currentHp = Math.max(0, this.currentHp - totalDamage);

      // 4. Incremento de Combo
      this.comboCount++;
      this.comboTimer = this.comboWindow;
      this.comboMultiplier = Math.min(3.0, 1.0 + (this.comboCount * 0.02)); // Até 3.0x combo

      if (this.onComboUpdate) {
        this.onComboUpdate(this.comboCount, this.comboMultiplier);
      }

      // 5. Atualização da Barra de Stagger
      if (this.state !== BOSS_STATES.STAGGERED && this.state !== BOSS_STATES.DEFEATED) {
        this.staggerCurrent += isGift ? 8000 : 800;
        if (this.staggerCurrent >= this.staggerMax) {
          this._triggerStagger();
        }
      }

      // 6. Ranking de Contribuição MVP
      this._recordContribution(user, totalDamage, isGift);

      // 7. Spawn de Floating Combat Text (Object Pool)
      const spawnX = event.spawnX !== undefined ? event.spawnX : (300 + (Math.random() - 0.5) * 200);
      const spawnY = event.spawnY !== undefined ? event.spawnY : (600 + (Math.random() - 0.5) * 150);
      this._spawnDamageText(label, spawnX, spawnY, isCritical, color);

      // 8. Transição para Estado Enrage se HP < 30%
      if (this.state === BOSS_STATES.IDLE && this.currentHp > 0 && (this.currentHp / this.maxHp) <= this.enrageThreshold) {
        this._setBossState(BOSS_STATES.ENRAGED);
        if (this.onEnrage) this.onEnrage();
      }

      // 9. Verificação de Derrota
      if (this.currentHp <= 0) {
        this._triggerDefeat();
      }

      if (this.onDamageTaken) {
        this.onDamageTaken(totalDamage, isCritical, user, this.currentHp);
      }

      return totalDamage;
    }

    _spawnDamageText(text, x, y, isCritical, color) {
      for (let i = 0; i < this.damagePool.length; i++) {
        if (!this.damagePool[i].active) {
          this.damagePool[i].init(text, x, y, isCritical, color);
          break;
        }
      }
    }

    _recordContribution(user, damage, isGift) {
      let data = this.contributors.get(user);
      if (!data) {
        data = { user, damage: 0, gifts: 0, hits: 0 };
        this.contributors.set(user, data);
      }
      data.damage += damage;
      data.hits += 1;
      if (isGift) data.gifts += 1;

      // Atualiza Top 3 MVPs em tempo real
      this.topMVP = Array.from(this.contributors.values())
        .sort((a, b) => b.damage - a.damage)
        .slice(0, 3);
    }

    _setBossState(newState) {
      if (this.state === newState) return;
      const oldState = this.state;
      this.state = newState;
      this.stateTimer = 0;
      if (this.onBossStateChange) {
        this.onBossStateChange(oldState, newState);
      }
    }

    _triggerStagger() {
      this.staggerCurrent = 0;
      this._setBossState(BOSS_STATES.STAGGERED);
      this.screenShake = 18;
      if (this.onStagger) this.onStagger();
    }

    _triggerDefeat() {
      this.isRoundActive = false;
      this.winner = 'CHAT';
      this._setBossState(BOSS_STATES.DEFEATED);
      this.screenShake = 30;
      if (this.onDefeat) {
        this.onDefeat(this.topMVP);
      }
    }

    _triggerBossVictory() {
      this.isRoundActive = false;
      this.winner = 'BOSS';
      this._setBossState(BOSS_STATES.VICTORIOUS);
      this.screenShake = 35;
      if (this.onVictory) {
        this.onVictory();
      }
    }

    // --- LOOP DE ATUALIZAÇÃO FÍSICA & CRONÔMETRO ---
    step(dt = 1 / 60) {
      // 1. Atualizar números de dano no pool
      for (let i = 0; i < this.damagePool.length; i++) {
        if (this.damagePool[i].active) {
          this.damagePool[i].step(dt);
        }
      }

      // 2. Amortecimento da barra de vida visual (lerp suave)
      this.displayHp += (this.currentHp - this.displayHp) * Math.min(1.0, 10.0 * dt);

      // 3. Amortecimento do Screen Shake
      if (this.screenShake > 0) {
        this.screenShake = Math.max(0, this.screenShake - (25 * dt));
      }

      if (!this.isRoundActive) return;

      // 4. Cronômetro da Rodada
      this.timeRemaining -= dt;
      if (this.timeRemaining <= 0) {
        this.timeRemaining = 0;
        // Se o tempo esgotar e o Boss ainda tiver HP, vitória do Boss
        this._triggerBossVictory();
        return;
      }

      // 5. Temporizador de Combo
      if (this.comboTimer > 0) {
        this.comboTimer -= dt;
        if (this.comboTimer <= 0) {
          this.comboCount = 0;
          this.comboMultiplier = 1.0;
          if (this.onComboUpdate) {
            this.onComboUpdate(0, 1.0);
          }
        }
      }

      // 6. Ciclo de Estados do Boss
      this.stateTimer += dt;

      if (this.state === BOSS_STATES.STAGGERED) {
        // Atordoado dura 4.5 segundos antes de voltar
        if (this.stateTimer >= 4.5) {
          const nextState = (this.currentHp / this.maxHp <= this.enrageThreshold) ? BOSS_STATES.ENRAGED : BOSS_STATES.IDLE;
          this._setBossState(nextState);
        }
      } else if (this.state === BOSS_STATES.ATTACKING) {
        // Ataque dura 1.2 segundos
        if (this.stateTimer >= 1.2) {
          const nextState = (this.currentHp / this.maxHp <= this.enrageThreshold) ? BOSS_STATES.ENRAGED : BOSS_STATES.IDLE;
          this._setBossState(nextState);
        }
      } else {
        // No modo IDLE ou ENRAGED, o Boss contra-ataca a cada 6 a 9 segundos
        const attackInterval = this.state === BOSS_STATES.ENRAGED ? 4.5 : 7.0;
        if (this.stateTimer >= attackInterval) {
          this._setBossState(BOSS_STATES.ATTACKING);
          this.screenShake = this.state === BOSS_STATES.ENRAGED ? 20 : 12;
          if (this.onBossAttack) {
            this.onBossAttack('SLAM', this.screenShake);
          }
        }
      }
    }

    // Retorna percentual de vida restante [0.0 a 1.0]
    getHpPercent() {
      return Math.max(0, this.currentHp / this.maxHp);
    }

    // Retorna percentual de vida exibida (suavizada) [0.0 a 1.0]
    getDisplayHpPercent() {
      return Math.max(0, this.displayHp / this.maxHp);
    }
  }

  V5BossRaidEngine.BOSS_STATES = BOSS_STATES;
  return V5BossRaidEngine;
}));
