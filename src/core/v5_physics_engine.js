/**
 * V5 PHYSICS ENGINE — Motor de Física 2D, Gravidade Vertical & Colisões Elásticas
 * Holding V5 Apollo — Divisão de Jogos & Transmissão 9:16
 * Versão: 1.0.0
 * 
 * Especialmente arquitetado para transmissões ao vivo 9:16 (1080x1920 responsivo):
 * - Gravidade vertical determinística e arrasto aerodinâmico
 * - Colisões elásticas esfera-pino, esfera-esfera e esfera-segmento
 * - Spatial Hash Grid para detecção O(N) permitindo 300+ esferas simultâneas a 60 FPS
 * - Object Pooling de partículas para zero sobrecarga de Garbage Collection
 * - Resposta de impulsos para bumpers, flippers, molas e caçapas
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5PhysicsEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  // =========================================================================
  // 1. SPATIAL HASH GRID (Otimização O(N) para Colisões em Massa)
  // =========================================================================
  class SpatialGrid {
    constructor(cellSize = 48) {
      this.cellSize = cellSize;
      this.grid = new Map();
    }

    clear() {
      this.grid.clear();
    }

    getKey(x, y) {
      const cx = Math.floor(x / this.cellSize);
      const cy = Math.floor(y / this.cellSize);
      return `${cx},${cy}`;
    }

    insert(ball) {
      const key = this.getKey(ball.x, ball.y);
      if (!this.grid.has(key)) {
        this.grid.set(key, []);
      }
      this.grid.get(key).push(ball);
    }

    getNeighbors(ball) {
      const neighbors = [];
      const cx = Math.floor(ball.x / this.cellSize);
      const cy = Math.floor(ball.y / this.cellSize);

      for (let ox = -1; ox <= 1; ox++) {
        for (let oy = -1; oy <= 1; oy++) {
          const key = `${cx + ox},${cy + oy}`;
          const bucket = this.grid.get(key);
          if (bucket) {
            for (let i = 0; i < bucket.length; i++) {
              if (bucket[i].id !== ball.id) {
                neighbors.push(bucket[i]);
              }
            }
          }
        }
      }
      return neighbors;
    }
  }

  // =========================================================================
  // 2. CORPOS FÍSICOS (Esferas, Pinos, Segmentos, Zonas de Força)
  // =========================================================================

  let nextBallId = 1;

  class Ball {
    constructor() {
      this.id = nextBallId++;
      this.active = false;
      this.x = 0;
      this.y = 0;
      this.vx = 0;
      this.vy = 0;
      this.radius = 8;
      this.mass = 1.0;
      this.restitution = 0.75;
      this.friction = 0.985;
      this.color = '#38bdf8';
      this.team = 'A';
      this.scoreMultiplier = 1;
      this.isVIP = false;
      this.trail = [];
      this.bounces = 0;
    }

    init(x, y, vx, vy, radius = 8, color = '#38bdf8', team = 'A', isVIP = false) {
      this.active = true;
      this.x = x;
      this.y = y;
      this.vx = vx;
      this.vy = vy;
      this.radius = radius;
      this.mass = Math.PI * radius * radius * 0.01;
      this.color = color;
      this.team = team;
      this.isVIP = isVIP;
      this.trail = [];
      this.bounces = 0;
      this.restitution = isVIP ? 0.85 : 0.72;
    }
  }

  class Peg {
    constructor(x, y, radius = 5, noteFreq = 440, isBumper = false) {
      this.x = x;
      this.y = y;
      this.radius = radius;
      this.restitution = isBumper ? 1.4 : 0.82;
      this.noteFreq = noteFreq;
      this.isBumper = isBumper;
      this.hitTime = 0;
      this.scoreValue = isBumper ? 50 : 10;
    }
  }

  class Segment {
    constructor(x1, y1, x2, y2, restitution = 0.7, friction = 0.95) {
      this.x1 = x1;
      this.y1 = y1;
      this.x2 = x2;
      this.y2 = y2;
      this.restitution = restitution;
      this.friction = friction;
      this.dx = x2 - x1;
      this.dy = y2 - y1;
      this.length = Math.hypot(this.dx, this.dy);
      this.nx = -this.dy / (this.length || 1);
      this.ny = this.dx / (this.length || 1);
    }
  }

  class Slot {
    constructor(x, y, width, height, multiplier = 1, team = 'neutral', label = '1x') {
      this.x = x;
      this.y = y;
      this.width = width;
      this.height = height;
      this.multiplier = multiplier;
      this.team = team;
      this.label = label;
      this.pulseTime = 0;
      this.captureCount = 0;
    }

    contains(ball) {
      return (
        ball.x >= this.x &&
        ball.x <= this.x + this.width &&
        ball.y >= this.y &&
        ball.y <= this.y + this.height
      );
    }
  }

  class VortexZone {
    constructor(cx, cy, radius = 90, strength = 1.2) {
      this.cx = cx;
      this.cy = cy;
      this.radius = radius;
      this.strength = strength;
    }

    applyForce(ball) {
      const dx = this.cx - ball.x;
      const dy = this.cy - ball.y;
      const dist = Math.hypot(dx, dy);

      if (dist < this.radius && dist > 4) {
        const force = (1 - dist / this.radius) * this.strength;
        // Atração radial
        ball.vx += (dx / dist) * force;
        ball.vy += (dy / dist) * force;
        // Força tangencial / vortex swirl
        ball.vx += (-dy / dist) * (force * 0.7);
        ball.vy += (dx / dist) * (force * 0.7);
      }
    }
  }

  // =========================================================================
  // 3. MOTOR FÍSICO CENTRAL (V5PhysicsEngine)
  // =========================================================================
  class V5PhysicsEngine {
    constructor(options = {}) {
      this.width = options.width || 1080;
      this.height = options.height || 1920;
      this.gravityX = options.gravityX || 0.0;
      this.gravityY = options.gravityY !== undefined ? options.gravityY : 0.32;
      this.drag = options.drag || 0.996;
      this.maxVelocity = options.maxVelocity || 22.0;

      // Limites do Viewport / Paredes
      this.bounds = {
        left: options.left || 0,
        right: options.right || this.width,
        top: options.top || 0,
        bottom: options.bottom || this.height
      };

      // Coleções
      this.pegs = [];
      this.segments = [];
      this.slots = [];
      this.vortexZones = [];

      // Object Pool de Esferas (Pre-allocated para GC zero)
      this.poolSize = options.poolSize || 350;
      this.ballPool = [];
      for (let i = 0; i < this.poolSize; i++) {
        this.ballPool.push(new Ball());
      }

      this.activeBalls = [];
      this.spatialGrid = new SpatialGrid(44);

      // Callbacks
      this.onPegCollision = options.onPegCollision || null;
      this.onSlotCapture = options.onSlotCapture || null;
      this.onBallCollision = options.onBallCollision || null;
    }

    resize(w, h, bounds = null) {
      this.width = w;
      this.height = h;
      if (bounds) {
        this.bounds = bounds;
      } else {
        this.bounds = { left: 0, right: w, top: 0, bottom: h };
      }
    }

    // --- GERENCIAMENTO DE PINOS E OBSTÁCULOS ---
    addPeg(x, y, radius = 5, noteFreq = 440, isBumper = false) {
      const peg = new Peg(x, y, radius, noteFreq, isBumper);
      this.pegs.push(peg);
      return peg;
    }

    clearPegs() {
      this.pegs = [];
    }

    // Gera matriz triangular clássica de Plinko / Galton Board
    createPlinkoGrid(startX, startY, rows = 10, spacingX = 42, spacingY = 48, baseFreq = 330) {
      this.clearPegs();
      const pentatonic = [1.0, 1.125, 1.25, 1.5, 1.667, 2.0, 2.25, 2.5, 3.0];

      for (let r = 0; r < rows; r++) {
        const count = r + 3;
        const rowWidth = (count - 1) * spacingX;
        const rowStartX = startX - (rowWidth / 2);
        const y = startY + (r * spacingY);

        for (let c = 0; c < count; c++) {
          const x = rowStartX + (c * spacingX);
          const isBumper = (r === Math.floor(rows / 2) && (c === 1 || c === count - 2));
          const freq = baseFreq * pentatonic[(r + c) % pentatonic.length];
          this.addPeg(x, y, isBumper ? 8 : 5, freq, isBumper);
        }
      }
    }

    // --- GERENCIAMENTO DE SEGMENTOS E PAREDES ---
    addSegment(x1, y1, x2, y2, restitution = 0.7) {
      const seg = new Segment(x1, y1, x2, y2, restitution);
      this.segments.push(seg);
      return seg;
    }

    clearSegments() {
      this.segments = [];
    }

    // --- GERENCIAMENTO DE CAÇAPAS / SLOTS ---
    addSlot(x, y, width, height, multiplier = 1, team = 'neutral', label = '1x') {
      const slot = new Slot(x, y, width, height, multiplier, team, label);
      this.slots.push(slot);
      return slot;
    }

    clearSlots() {
      this.slots = [];
    }

    // --- ZONAS DE FORÇA (VORTEX / MAGNÉTICA) ---
    addVortex(cx, cy, radius = 90, strength = 1.2) {
      const v = new VortexZone(cx, cy, radius, strength);
      this.vortexZones.push(v);
      return v;
    }

    clearVortexZones() {
      this.vortexZones = [];
    }

    // --- EMISSÃO E RECOLHIMENTO DE ESFERAS ---
    spawnBall(x, y, vx = 0, vy = 0, radius = 8, color = '#38bdf8', team = 'A', isVIP = false) {
      let ball = null;
      for (let i = 0; i < this.ballPool.length; i++) {
        if (!this.ballPool[i].active) {
          ball = this.ballPool[i];
          break;
        }
      }

      if (!ball) {
        // Pool esgotado: recicla o mais antigo
        ball = this.activeBalls.shift();
      }

      ball.init(x, y, vx, vy, radius, color, team, isVIP);
      this.activeBalls.push(ball);
      return ball;
    }

    removeBall(ball) {
      ball.active = false;
      const idx = this.activeBalls.indexOf(ball);
      if (idx !== -1) {
        this.activeBalls.splice(idx, 1);
      }
    }

    clearBalls() {
      for (let i = 0; i < this.activeBalls.length; i++) {
        this.activeBalls[i].active = false;
      }
      this.activeBalls = [];
    }

    // =========================================================================
    // 4. PASSO DE SIMULAÇÃO (UPDATE DO MOTOR)
    // =========================================================================
    step(dt = 1.0) {
      const now = performance.now();
      this.spatialGrid.clear();

      // 1. Inserção na Grade Espacial
      for (let i = 0; i < this.activeBalls.length; i++) {
        this.spatialGrid.insert(this.activeBalls[i]);
      }

      // 2. Atualização Dinâmica das Esferas
      for (let i = this.activeBalls.length - 1; i >= 0; i--) {
        const b = this.activeBalls[i];

        // Aplicação de Gravidade e Arrasto
        b.vx += this.gravityX * dt;
        b.vy += this.gravityY * dt;
        b.vx *= this.drag;
        b.vy *= this.drag;

        // Limitação de Velocidade Terminal (Evita Tunneling através de pinos)
        const speed = Math.hypot(b.vx, b.vy);
        if (speed > this.maxVelocity) {
          const ratio = this.maxVelocity / speed;
          b.vx *= ratio;
          b.vy *= ratio;
        }

        // Zonas de Vórtice / Força Magnética
        for (let v = 0; v < this.vortexZones.length; v++) {
          this.vortexZones[v].applyForce(b);
        }

        // Integração de Posição (Euler)
        b.x += b.vx * dt;
        b.y += b.vy * dt;

        // Rastro de Partículas (Trail para VIPs e bolas rápidas)
        if (b.isVIP || speed > 10.0) {
          b.trail.push({ x: b.x, y: b.y, alpha: 0.8 });
          if (b.trail.length > 8) b.trail.shift();
        }

        // Colisões com Paredes Laterais do Viewport
        if (b.x - b.radius < this.bounds.left) {
          b.x = this.bounds.left + b.radius;
          b.vx = -b.vx * b.restitution;
        } else if (b.x + b.radius > this.bounds.right) {
          b.x = this.bounds.right - b.radius;
          b.vx = -b.vx * b.restitution;
        }

        if (b.y - b.radius < this.bounds.top) {
          b.y = this.bounds.top + b.radius;
          b.vy = -b.vy * b.restitution;
        }

        // 3. Colisão com Segmentos / Defletores Lineares
        for (let s = 0; s < this.segments.length; s++) {
          this.resolveSegmentCollision(b, this.segments[s]);
        }

        // 4. Colisão com Pinos e Bumpers
        for (let p = 0; p < this.pegs.length; p++) {
          this.resolvePegCollision(b, this.pegs[p], now);
        }

        // 5. Colisão Esfera vs Esfera (via Spatial Grid O(N))
        const neighbors = this.spatialGrid.getNeighbors(b);
        for (let n = 0; n < neighbors.length; n++) {
          this.resolveBallBallCollision(b, neighbors[n]);
        }

        // 6. Detecção de Captura em Caçapas / Slots
        let captured = false;
        for (let s = 0; s < this.slots.length; s++) {
          const slot = this.slots[s];
          if (slot.contains(b)) {
            slot.pulseTime = now;
            slot.captureCount++;
            if (this.onSlotCapture) {
              this.onSlotCapture(slot, b);
            }
            this.removeBall(b);
            captured = true;
            break;
          }
        }

        // 7. Remoção por Queda Livre além do limite inferior
        if (!captured && b.y - b.radius > this.bounds.bottom + 50) {
          this.removeBall(b);
        }
      }
    }

    // =========================================================================
    // 5. RESOLUÇÃO DE COLISÕES
    // =========================================================================

    /**
     * Colisão Esfera vs Pino (Ponto Círculo Fixo)
     */
    resolvePegCollision(ball, peg, now) {
      const dx = ball.x - peg.x;
      const dy = ball.y - peg.y;
      const dist = Math.hypot(dx, dy);
      const minDist = ball.radius + peg.radius;

      if (dist < minDist && dist > 0.001) {
        // Separação de penetração
        const overlap = minDist - dist;
        const nx = dx / dist;
        const ny = dy / dist;

        ball.x += nx * overlap;
        ball.y += ny * overlap;

        // Reflexão de velocidade com restituição combinada
        const dot = ball.vx * nx + ball.vy * ny;
        if (dot < 0) {
          const rest = Math.max(ball.restitution, peg.restitution);
          ball.vx -= (1 + rest) * dot * nx;
          ball.vy -= (1 + rest) * dot * ny;

          // Se for Bumper, adiciona impulso radial extra
          if (peg.isBumper) {
            ball.vx += nx * 6.0;
            ball.vy += ny * 6.0;
          }

          ball.bounces++;
          peg.hitTime = now;

          if (this.onPegCollision) {
            this.onPegCollision(peg, ball);
          }
        }
      }
    }

    /**
     * Colisão Esfera vs Segmento de Linha
     */
    resolveSegmentCollision(ball, seg) {
      const vx1 = ball.x - seg.x1;
      const vy1 = ball.y - seg.y1;
      const t = Math.max(0, Math.min(1, (vx1 * seg.dx + vy1 * seg.dy) / (seg.length * seg.length || 1)));

      const closestX = seg.x1 + t * seg.dx;
      const closestY = seg.y1 + t * seg.dy;

      const dx = ball.x - closestX;
      const dy = ball.y - closestY;
      const dist = Math.hypot(dx, dy);

      if (dist < ball.radius && dist > 0.001) {
        const overlap = ball.radius - dist;
        const nx = dx / dist;
        const ny = dy / dist;

        ball.x += nx * overlap;
        ball.y += ny * overlap;

        const dot = ball.vx * nx + ball.vy * ny;
        if (dot < 0) {
          ball.vx -= (1 + seg.restitution) * dot * nx;
          ball.vy -= (1 + seg.restitution) * dot * ny;
          ball.vx *= seg.friction;
          ball.vy *= seg.friction;
        }
      }
    }

    /**
     * Colisão Elástica Esfera vs Esfera (Conservação de Momento 2D)
     */
    resolveBallBallCollision(b1, b2) {
      const dx = b2.x - b1.x;
      const dy = b2.y - b1.y;
      const dist = Math.hypot(dx, dy);
      const minDist = b1.radius + b2.radius;

      if (dist < minDist && dist > 0.001) {
        const overlap = (minDist - dist) * 0.5;
        const nx = dx / dist;
        const ny = dy / dist;

        // Separação de penetração
        b1.x -= nx * overlap;
        b1.y -= ny * overlap;
        b2.x += nx * overlap;
        b2.y += ny * overlap;

        // Velocidades relativas normais
        const kx = b1.vx - b2.vx;
        const ky = b1.vy - b2.vy;
        const p = 2 * (nx * kx + ny * ky) / (b1.mass + b2.mass);

        const rest = (b1.restitution + b2.restitution) * 0.5;

        b1.vx -= p * b2.mass * nx * (1 + rest) * 0.5;
        b1.vy -= p * b2.mass * ny * (1 + rest) * 0.5;
        b2.vx += p * b1.mass * nx * (1 + rest) * 0.5;
        b2.vy += p * b1.mass * ny * (1 + rest) * 0.5;

        if (this.onBallCollision) {
          this.onBallCollision(b1, b2);
        }
      }
    }

    // =========================================================================
    // 6. RENDERIZADOR 2D PADRONIZADO (CANVAS 60 FPS)
    // =========================================================================
    render(ctx) {
      const now = performance.now();

      // 1. Zonas de Vórtice
      for (let i = 0; i < this.vortexZones.length; i++) {
        const v = this.vortexZones[i];
        ctx.save();
        ctx.beginPath();
        ctx.arc(v.cx, v.cy, v.radius, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(168, 85, 247, 0.35)';
        ctx.lineWidth = 2;
        ctx.setLineDash([6, 6]);
        ctx.stroke();
        ctx.restore();
      }

      // 2. Segmentos e Defletores
      for (let i = 0; i < this.segments.length; i++) {
        const seg = this.segments[i];
        ctx.beginPath();
        ctx.moveTo(seg.x1, seg.y1);
        ctx.lineTo(seg.x2, seg.y2);
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 4;
        ctx.lineCap = 'round';
        ctx.stroke();
      }

      // 3. Pinos e Bumpers
      for (let i = 0; i < this.pegs.length; i++) {
        const peg = this.pegs[i];
        const isHit = (now - peg.hitTime < 180);

        ctx.beginPath();
        ctx.arc(peg.x, peg.y, peg.radius + (isHit ? 2 : 0), 0, Math.PI * 2);

        if (peg.isBumper) {
          ctx.fillStyle = isHit ? '#ffffff' : '#fbbf24';
          ctx.shadowColor = '#fbbf24';
          ctx.shadowBlur = isHit ? 20 : 10;
        } else {
          ctx.fillStyle = isHit ? '#38bdf8' : '#e2e8f0';
          ctx.shadowColor = isHit ? '#38bdf8' : 'transparent';
          ctx.shadowBlur = isHit ? 14 : 0;
        }

        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // 4. Caçapas / Slots
      for (let i = 0; i < this.slots.length; i++) {
        const slot = this.slots[i];
        const isPulsing = (now - slot.pulseTime < 250);

        ctx.save();
        ctx.fillStyle = isPulsing ? 'rgba(251, 191, 36, 0.4)' : 'rgba(30, 41, 59, 0.7)';
        ctx.strokeStyle = isPulsing ? '#fbbf24' : 'rgba(255, 255, 255, 0.15)';
        ctx.lineWidth = 2;
        ctx.fillRect(slot.x, slot.y, slot.width, slot.height);
        ctx.strokeRect(slot.x, slot.y, slot.width, slot.height);

        ctx.font = '900 11px monospace';
        ctx.textAlign = 'center';
        ctx.fillStyle = isPulsing ? '#fbbf24' : '#f1f5f9';
        ctx.fillText(slot.label, slot.x + slot.width / 2, slot.y + slot.height * 0.6);
        ctx.restore();
      }

      // 5. Esferas e Rastros
      for (let i = 0; i < this.activeBalls.length; i++) {
        const b = this.activeBalls[i];

        // Rastro (Trail)
        for (let t = 0; t < b.trail.length; t++) {
          const tr = b.trail[t];
          ctx.beginPath();
          ctx.arc(tr.x, tr.y, b.radius * (0.3 + (t / b.trail.length) * 0.5), 0, Math.PI * 2);
          ctx.fillStyle = b.color;
          ctx.globalAlpha = tr.alpha * (t / b.trail.length) * 0.4;
          ctx.fill();
          ctx.globalAlpha = 1.0;
        }

        // Esfera
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
        ctx.fillStyle = b.color;
        if (b.isVIP) {
          ctx.shadowColor = b.color;
          ctx.shadowBlur = 15;
        }
        ctx.fill();
        ctx.shadowBlur = 0;

        // Ponto de brilho especular
        ctx.beginPath();
        ctx.arc(b.x - b.radius * 0.3, b.y - b.radius * 0.3, b.radius * 0.35, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
        ctx.fill();
      }
    }
  }

  return V5PhysicsEngine;
}));
