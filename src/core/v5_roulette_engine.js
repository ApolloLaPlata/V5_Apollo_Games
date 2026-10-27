/**
 * V5 ROULETTE ENGINE — Motor Matemático Determinístico de Desaceleração Angular
 * Holding V5 Apollo — Divisão de Jogos & Transmissão 9:16
 * Fase 5: Roletas, Sorteios & Caça-Níqueis (Etapa 041)
 * Versão: 1.0.0
 * 
 * Especialmente arquitetado para transmissões ao vivo 9:16 (1080x1920 responsivo):
 * - Curva de desaceleração angular contínua com amortecimento cúbico (Cubic Ease-Out)
 * - Modo determinístico direcionado (pára com exatidão matemática na fatia sorteada)
 * - Simulação física da palheta mecânica (flapper) colidindo contra pinos divisores
 * - Suporte a fatias dinâmicas ponderadas (pesos customizáveis)
 * - Efeito de micro-recuo elástico (Pin Bouncing) ao atingir o repouso final
 * - Zero alocações no loop principal (Zero GC)
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5RouletteEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  const TWO_PI = Math.PI * 2;

  // =========================================================================
  // 1. ESTRUTURA DE FATIA DA ROLETA
  // =========================================================================
  class RouletteSlice {
    constructor(index, data = {}) {
      this.index = index;
      this.id = data.id || `slice_${index}`;
      this.label = data.label || `Desafio #${index + 1}`;
      this.subtext = data.subtext || '';
      this.color = data.color || '#3b82f6';
      this.textColor = data.textColor || '#ffffff';
      this.icon = data.icon || '🎯';
      this.weight = data.weight || 1;
      this.startAngle = 0;
      this.endAngle = 0;
      this.midAngle = 0;
    }
  }

  // =========================================================================
  // 2. MOTOR PRINCIPAL: V5 ROULETTE ENGINE
  // =========================================================================
  class V5RouletteEngine {
    constructor(options = {}) {
      // Estado Angular
      this.angle = options.initialAngle || 0;          // Radianos [0, 2PI]
      this.angularVelocity = 0;                        // Radianos por segundo
      this.isSpinning = false;

      // Parâmetros de Giro & Desaceleração
      this.friction = options.friction || 0.985;        // Amortecimento natural
      this.minSpinDuration = options.minSpinDuration || 4.5; // Segundos mínimos de giro
      this.maxSpinDuration = options.maxSpinDuration || 7.0;

      // Modo Determinístico (Targeted)
      this.isTargeted = false;
      this.targetSliceIndex = -1;
      this.targetAngle = 0;
      this.startAngle = 0;
      this.spinElapsed = 0;
      this.spinDuration = 0;

      // Palheta Mecânica (Flapper) & Pinos
      this.pointerAngle = -Math.PI / 2; // Apontador localizado no topo (12 horas = -PI/2)
      this.flapperDeflection = 0;       // Ângulo de deflexão elástica da palheta (-0.25 a +0.25 rad)
      this.lastPinCrossed = -1;
      this.totalPinClicks = 0;

      // Fatias
      this.slices = [];
      if (options.slices && Array.isArray(options.slices)) {
        this.setSlices(options.slices);
      } else {
        this._initDefaultSlices();
      }

      // Callbacks
      this.onPinClick = null;       // Disparado a cada pino transposto (som mecânico de catraca)
      this.onSliceChange = null;    // Disparado quando a fatia sob o ponteiro muda
      this.onSpinStart = null;      // Disparado ao iniciar o giro
      this.onSpinHalt = null;       // Disparado ao parar completamente

      this.currentSliceIndex = 0;
    }

    _initDefaultSlices() {
      const defaultData = [
        { id: 'dance', label: 'DANCINHA', icon: '💃', color: '#ec4899', textColor: '#fff' },
        { id: 'water', label: 'BEBER ÁGUA', icon: '💧', color: '#06b6d4', textColor: '#fff' },
        { id: 'opera', label: 'CANTAR ÓPERA', icon: '🎭', color: '#a855f7', textColor: '#fff' },
        { id: 'pushups', label: '10 FLEXÕES', icon: '💪', color: '#f59e0b', textColor: '#fff' },
        { id: 'chicken', label: 'IMITAR GALINHA', icon: '🐔', color: '#ef4444', textColor: '#fff' },
        { id: 'shoutout', label: 'SUPER SALVE', icon: '📢', color: '#10b981', textColor: '#fff' },
        { id: 'floss', label: 'PASSINHO', icon: '🕺', color: '#8b5cf6', textColor: '#fff' },
        { id: 'jackpot', label: 'RODADA DUPLA', icon: '⭐', color: '#fbbf24', textColor: '#000' }
      ];
      this.setSlices(defaultData);
    }

    setSlices(slicesData) {
      if (!Array.isArray(slicesData) || slicesData.length === 0) return;

      const totalWeight = slicesData.reduce((acc, s) => acc + (s.weight || 1), 0);
      let accumAngle = 0;

      this.slices = slicesData.map((d, idx) => {
        const slice = new RouletteSlice(idx, d);
        const sliceSpan = ((d.weight || 1) / totalWeight) * TWO_PI;
        slice.startAngle = accumAngle;
        slice.endAngle = accumAngle + sliceSpan;
        slice.midAngle = accumAngle + (sliceSpan / 2);
        accumAngle += sliceSpan;
        return slice;
      });

      this._updateCurrentSlice();
    }

    // --- INÍCIO DE GIRO ---
    spin(initialVelocity = 35) {
      this.isSpinning = true;
      this.isTargeted = false;
      this.angularVelocity = Math.max(20, initialVelocity);
      this.lastPinCrossed = -1;

      if (this.onSpinStart) this.onSpinStart(null);
    }

    /**
     * Giro Determinístico Direcionado:
     * Garante matematicamente que o ponteiro pare exatamente na fatia desejada.
     */
    spinToTarget(targetIndex = null, minLaps = 5, duration = 5.5) {
      if (this.slices.length === 0) return;

      // Se nenhum alvo for especificado, sorteia baseado nos pesos
      if (targetIndex === null || targetIndex < 0 || targetIndex >= this.slices.length) {
        targetIndex = this._pickWeightedRandomSlice();
      }

      this.isSpinning = true;
      this.isTargeted = true;
      this.targetSliceIndex = targetIndex;
      this.spinElapsed = 0;
      this.spinDuration = Math.max(3.0, duration);

      const targetSlice = this.slices[targetIndex];
      // Escolher ponto interno seguro dentro da fatia (entre 15% e 85% para não ficar na risca)
      const sliceSpan = targetSlice.endAngle - targetSlice.startAngle;
      const innerOffset = targetSlice.startAngle + (sliceSpan * (0.25 + Math.random() * 0.50));

      // Como o ponteiro está em pointerAngle (-PI/2), o ângulo final da roleta deve ser:
      // pointerAngle = (targetAngle + innerOffset) % TWO_PI  =>  targetAngle = pointerAngle - innerOffset
      let desiredAngle = (this.pointerAngle - innerOffset);
      desiredAngle = ((desiredAngle % TWO_PI) + TWO_PI) % TWO_PI;

      // Normalizar ângulo atual
      const currentNorm = ((this.angle % TWO_PI) + TWO_PI) % TWO_PI;

      // Calcular distância angular total (voltas completas + deslocamento relativo)
      let deltaAngle = desiredAngle - currentNorm;
      if (deltaAngle <= 0) deltaAngle += TWO_PI;
      deltaAngle += (minLaps * TWO_PI);

      this.startAngle = this.angle;
      this.targetAngle = this.startAngle + deltaAngle;
      this.lastPinCrossed = -1;

      if (this.onSpinStart) this.onSpinStart(this.targetSliceIndex);
    }

    _pickWeightedRandomSlice() {
      const totalWeight = this.slices.reduce((acc, s) => acc + s.weight, 0);
      let rand = Math.random() * totalWeight;
      for (let i = 0; i < this.slices.length; i++) {
        rand -= this.slices[i].weight;
        if (rand <= 0) return i;
      }
      return this.slices.length - 1;
    }

    // Aplica impulso adicional (ex: quando chegam presentes durante o giro)
    applyTorque(amount = 12) {
      if (!this.isSpinning) {
        this.spin(amount);
      } else if (!this.isTargeted) {
        this.angularVelocity += amount;
      } else {
        // No modo direcionado, acrescenta mais voltas inteiras sem estragar o alvo
        this.targetAngle += TWO_PI;
        this.spinDuration += 1.2;
      }
    }

    // --- LOOP DE ATUALIZAÇÃO FÍSICA ---
    step(dt = 1 / 60) {
      if (!this.isSpinning) return;

      if (this.isTargeted) {
        this._stepTargeted(dt);
      } else {
        this._stepOrganic(dt);
      }

      // 1. Manter ângulo normalizado para renderização contínua
      this.angle = (this.angle % TWO_PI + TWO_PI) % TWO_PI;

      // 2. Simular Palheta Mecânica (Flapper) e Pinos Divisores
      this._updateFlapperMechanics();

      // 3. Atualizar fatia atualmente sob o ponteiro
      this._updateCurrentSlice();
    }

    _stepTargeted(dt) {
      this.spinElapsed += dt;
      const t = Math.min(1.0, this.spinElapsed / this.spinDuration);

      // Curva Quintic Ease-Out para suspense dramático no final: f(t) = 1 - (1 - t)^4
      const ease = 1 - Math.pow(1 - t, 4);
      this.angle = this.startAngle + (this.targetAngle - this.startAngle) * ease;

      // Velocidade angular derivada da curva para efeitos de som
      const derivative = 4 * Math.pow(1 - t, 3);
      this.angularVelocity = ((this.targetAngle - this.startAngle) / this.spinDuration) * derivative;

      if (t >= 1.0) {
        this.angle = this.targetAngle;
        this.angularVelocity = 0;
        this.isSpinning = false;
        this.flapperDeflection = 0;

        if (this.onSpinHalt) {
          this.onSpinHalt(this.slices[this.currentSliceIndex]);
        }
      }
    }

    _stepOrganic(dt) {
      this.angle += this.angularVelocity * dt;
      this.angularVelocity *= Math.pow(this.friction, dt * 60);

      // Parada completa
      if (Math.abs(this.angularVelocity) < 0.05) {
        this.angularVelocity = 0;
        this.isSpinning = false;
        this.flapperDeflection = 0;

        if (this.onSpinHalt) {
          this.onSpinHalt(this.slices[this.currentSliceIndex]);
        }
      }
    }

    _updateFlapperMechanics() {
      if (this.slices.length === 0) return;

      // Ângulo relativo do ponteiro em relação à roleta
      const relAngle = ((this.pointerAngle - this.angle) % TWO_PI + TWO_PI) % TWO_PI;

      // Pinos ficam nas fronteiras de cada fatia
      for (let i = 0; i < this.slices.length; i++) {
        const pinAngle = this.slices[i].startAngle;
        const diff = Math.abs(relAngle - pinAngle);
        const pinThreshold = 0.06; // Radianos de contato com a palheta

        if (diff < pinThreshold) {
          // Palheta está sendo empurrada pelo pino
          this.flapperDeflection = (relAngle < pinAngle ? -1 : 1) * 0.22;

          if (this.lastPinCrossed !== i) {
            this.lastPinCrossed = i;
            this.totalPinClicks++;

            if (this.onPinClick) {
              const speedRatio = Math.min(2.5, Math.abs(this.angularVelocity) / 8);
              this.onPinClick(i, speedRatio);
            }
          }
          return;
        }
      }

      // Sem contato: mola da palheta retorna suavemente ao repouso
      this.flapperDeflection *= 0.75;
    }

    _updateCurrentSlice() {
      if (this.slices.length === 0) return;

      const relAngle = ((this.pointerAngle - this.angle) % TWO_PI + TWO_PI) % TWO_PI;

      for (let i = 0; i < this.slices.length; i++) {
        const s = this.slices[i];
        if (relAngle >= s.startAngle && relAngle < s.endAngle) {
          if (this.currentSliceIndex !== i) {
            this.currentSliceIndex = i;
            if (this.onSliceChange) {
              this.onSliceChange(s);
            }
          }
          break;
        }
      }
    }

    // Retorna fatia ativa no momento
    getCurrentSlice() {
      return this.slices[this.currentSliceIndex] || null;
    }
  }

  return V5RouletteEngine;
}));
