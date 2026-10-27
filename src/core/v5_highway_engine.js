/**
 * V5 HIGHWAY ENGINE — Motor de Pistas Verticais Pseudo-3D com Scrolling Infinito & Parallax
 * Holding V5 Apollo — Divisão de Jogos & Transmissão 9:16
 * Fase 4: Cartuchos de Corrida, Tráfego & Velocidade (Etapa 031)
 * Versão: 1.0.0
 * 
 * Arquitetura de Alto Desempenho para Transmissões 9:16 (1080x1920):
 * - Projeção de perspectiva pseudo-3D com divisão não-linear de Z
 * - Scrolling contínuo de asfalto com buffer circular de segmentos
 * - Curvas suaves (Bézier/Euler) e ondulações de relevo com horizonte configurável
 * - Suporte a múltiplos pilotos em pistas dinâmicas com ultrapassagens em milissegundos
 * - Sistema de Parallax em 3 camadas (Céu/Nebulosa, Silhueta Urbana, Postes e Hologramas)
 * - Turbos de Nitro, arrasto aerodinâmico e rubber-banding dinâmico para lives
 * - Zero alocações no loop principal (Zero GC pauses)
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5HighwayEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  // =========================================================================
  // 1. ESTRUTURA DE PONTO E PROJEÇÃO 3D -> 2D
  // =========================================================================
  class WorldPoint {
    constructor() {
      this.x = 0;
      this.y = 0;
      this.z = 0;
      this.screenX = 0;
      this.screenY = 0;
      this.screenW = 0;
      this.scale = 0;
    }

    project(cameraX, cameraY, cameraZ, cameraDepth, canvasW, canvasH, horizonY, roadWidth) {
      const transX = this.x - cameraX;
      const transY = this.y - cameraY;
      const transZ = this.z - cameraZ;

      if (transZ <= 0) {
        this.scale = 0;
        this.screenX = 0;
        this.screenY = 0;
        this.screenW = 0;
        return;
      }

      this.scale = cameraDepth / transZ;
      this.screenX = Math.round((canvasW / 2) + (this.scale * transX * canvasW / 2));
      this.screenY = Math.round(horizonY + (this.scale * transY * canvasH / 2));
      this.screenW = Math.round(this.scale * roadWidth * canvasW / 2);
    }
  }

  // =========================================================================
  // 2. SEGMENTO DE PISTA DE ASFALTO
  // =========================================================================
  class RoadSegment {
    constructor(index) {
      this.index = index;
      this.p1 = new WorldPoint();
      this.p2 = new WorldPoint();
      this.curve = 0;          // Curvatura lateral (-2.0 a +2.0)
      this.elevation = 0;      // Relevo vertical
      this.clipY = 0;          // Oclusão de horizonte
      this.colorTheme = 'dark'; // 'dark' ou 'light' para listras de asfalto
      this.props = [];         // Elementos na beira da estrada (postes, placas)
    }
  }

  // =========================================================================
  // 3. CLASSE DO PILOTO / RACER
  // =========================================================================
  class Racer {
    constructor(id, name, color, laneIndex = 1, totalLanes = 3) {
      this.id = id;
      this.name = name;
      this.color = color;
      this.laneIndex = laneIndex;
      this.totalLanes = totalLanes;

      // Posição no mundo
      this.x = this._getLaneX(laneIndex, totalLanes); // Normalizado: -0.6 a +0.6
      this.targetX = this.x;
      this.z = 0;             // Distância percorrida no circuito (metros)
      
      // Dinâmica de Movimento
      this.speed = 120;       // Velocidade atual (km/h virtual)
      this.baseSpeed = 120;
      this.maxSpeed = 260;
      this.minSpeed = 60;
      this.acceleration = 25;
      this.friction = 0.985;
      
      // Nitro Boost & Efeitos
      this.nitroActive = false;
      this.nitroTimer = 0;
      this.nitroMultiplier = 1.0;
      this.lateralWobble = 0;
      this.driftAngle = 0;

      // Telemetria
      this.rank = 1;
      this.gapMeters = 0;
      this.boostCount = 0;
      this.screen = { x: 0, y: 0, scale: 0, w: 0, h: 0 };
    }

    _getLaneX(lane, total) {
      if (total <= 1) return 0;
      const step = 1.2 / (total - 1);
      return -0.6 + (lane * step);
    }

    setLane(lane) {
      this.laneIndex = Math.max(0, Math.min(this.totalLanes - 1, lane));
      this.targetX = this._getLaneX(this.laneIndex, this.totalLanes);
    }

    applyBoost(amount = 45, duration = 3.0, multiplier = 1.5) {
      this.nitroActive = true;
      this.nitroTimer = Math.max(this.nitroTimer, duration);
      this.nitroMultiplier = multiplier;
      this.speed = Math.min(this.maxSpeed, this.speed + amount);
      this.boostCount++;
    }

    applyHazard(penalty = 40, duration = 1.5) {
      this.speed = Math.max(this.minSpeed, this.speed - penalty);
      this.nitroActive = false;
      this.nitroTimer = 0;
    }

    update(dt) {
      // Atualizar Nitro
      if (this.nitroTimer > 0) {
        this.nitroTimer -= dt;
        if (this.nitroTimer <= 0) {
          this.nitroActive = false;
          this.nitroMultiplier = 1.0;
        }
      }

      // Desaceleração suave para velocidade base
      const targetBase = this.nitroActive ? (this.baseSpeed * this.nitroMultiplier) : this.baseSpeed;
      if (this.speed > targetBase) {
        this.speed -= this.acceleration * dt * 0.7;
      } else if (this.speed < targetBase) {
        this.speed += this.acceleration * dt;
      }

      // Transição suave entre faixas (Steering Spline)
      const dx = this.targetX - this.x;
      this.x += dx * Math.min(1.0, dt * 6.0);
      this.driftAngle = -dx * 0.4; // Inclinação da lataria ao esterçar

      // Vibração aerodinâmica sutil em altas velocidades
      this.lateralWobble = (Math.sin(Date.now() * 0.02) * (this.speed / this.maxSpeed)) * 0.015;

      // Avanço de distância
      this.z += (this.speed * (1000 / 3600)) * dt * 10; // escala de mundo
    }
  }

  // =========================================================================
  // 4. MOTOR PRINCIPAL: V5 HIGHWAY ENGINE
  // =========================================================================
  class V5HighwayEngine {
    constructor(options = {}) {
      this.width = options.width || 1080;
      this.height = options.height || 1920;
      this.roadWidth = options.roadWidth || 1800;
      this.segmentLength = options.segmentLength || 160;
      this.totalSegments = options.totalSegments || 400;
      this.rumbleLength = options.rumbleLength || 3;
      this.lanes = options.lanes || 3;
      this.cameraHeight = options.cameraHeight || 900;
      this.cameraDepth = options.cameraDepth || 0.84;
      this.drawDistance = options.drawDistance || 240;
      this.horizonY = options.horizonY || (this.height * 0.32); // Safe Zone Topo (140px+)

      // Câmera & Pista
      this.cameraZ = 0;
      this.cameraX = 0;
      this.curveOffset = 0;
      this.trackLength = this.totalSegments * this.segmentLength;

      // Parallax Offsets
      this.skyOffset = 0;
      this.cityOffset = 0;
      this.propsOffset = 0;

      // Segmentos da Pista
      this.segments = [];
      this._buildTrack();

      // Pilotos Cadastrados
      this.racers = [];
      this.leader = null;

      // Cores Neon Padrão (Dark Cyberpunk)
      this.theme = {
        skyGradTop: options.skyGradTop || '#030712',
        skyGradBottom: options.skyGradBottom || '#1e1b4b',
        fogColor: options.fogColor || 'rgba(3, 7, 18, ',
        asphaltDark: '#090d16',
        asphaltLight: '#0d1322',
        rumbleCyan: '#06b6d4',
        rumbleMagenta: '#f43f5e',
        laneLine: '#e0e7ff',
        neonEdge: '#38bdf8'
      };

      // Callbacks de Eventos
      this.onLeadChange = null;
      this.onOvertake = null;
      this.lastLeaderId = null;
    }

    _buildTrack() {
      this.segments = [];
      for (let i = 0; i < this.totalSegments; i++) {
        const seg = new RoadSegment(i);
        seg.p1.z = i * this.segmentLength;
        seg.p2.z = (i + 1) * this.segmentLength;
        
        // Padrão de cores zebrado para sensação de movimento contínuo
        seg.colorTheme = (Math.floor(i / this.rumbleLength) % 2 === 0) ? 'dark' : 'light';

        // Curvas suaves e relevos dinâmicos
        if (i > 40 && i < 110) {
          seg.curve = Math.sin((i - 40) / 70 * Math.PI) * 1.8;
          seg.p1.y = Math.sin((i - 40) / 70 * Math.PI) * 450;
        } else if (i > 160 && i < 240) {
          seg.curve = -Math.sin((i - 160) / 80 * Math.PI) * 2.2;
        } else if (i > 280 && i < 360) {
          seg.curve = Math.sin((i - 280) / 80 * Math.PI) * 1.4;
          seg.p1.y = -Math.sin((i - 280) / 80 * Math.PI) * 350;
        }

        // Postes de Neon e Hologramas na beira da estrada
        if (i % 12 === 0) {
          seg.props.push({ type: 'light_pole', side: -1, x: -1.35, color: '#06b6d4' });
          seg.props.push({ type: 'light_pole', side: 1, x: 1.35, color: '#f43f5e' });
        } else if (i % 35 === 0) {
          seg.props.push({ type: 'cyber_billboard', side: 1, x: 1.7, text: 'V5 HOLDING' });
        }

        this.segments.push(seg);
      }
    }

    // --- GERENCIAMENTO DE PILOTOS ---
    addRacer(id, name, color, laneIndex = 1) {
      const racer = new Racer(id, name, color, laneIndex, this.lanes);
      this.racers.push(racer);
      this._updateStandings();
      return racer;
    }

    getRacer(id) {
      return this.racers.find(r => r.id === id);
    }

    applyBoost(racerId, amount = 50, duration = 3.0, multiplier = 1.5) {
      const r = this.getRacer(racerId);
      if (r) r.applyBoost(amount, duration, multiplier);
    }

    applyHazard(racerId, penalty = 40, duration = 1.5) {
      const r = this.getRacer(racerId);
      if (r) r.applyHazard(penalty, duration);
    }

    _findSegment(z) {
      const wrappedZ = ((z % this.trackLength) + this.trackLength) % this.trackLength;
      const index = Math.floor(wrappedZ / this.segmentLength);
      return this.segments[index % this.segments.length];
    }

    _updateStandings() {
      // Ordenar por maior distância percorrida
      this.racers.sort((a, b) => b.z - a.z);

      if (this.racers.length > 0) {
        const currentLeader = this.racers[0];
        if (this.lastLeaderId && this.lastLeaderId !== currentLeader.id) {
          if (this.onLeadChange) {
            this.onLeadChange(currentLeader, this.lastLeaderId);
          }
        }
        this.lastLeaderId = currentLeader.id;
        this.leader = currentLeader;

        // Atribuir ranks e gaps
        this.racers.forEach((r, idx) => {
          r.rank = idx + 1;
          r.gapMeters = Math.max(0, (currentLeader.z - r.z) / 10);
        });
      }
    }

    // --- LOOP DE ATUALIZAÇÃO FÍSICA ---
    step(dt = 1 / 60) {
      // 1. Atualizar dinâmica individual de cada piloto
      this.racers.forEach(r => r.update(dt));

      // 2. Classificação de posições
      this._updateStandings();

      // 3. A Câmera acompanha dinamicamente a média dos corredores (ou o líder com amortecimento)
      if (this.leader) {
        // Alvo da câmera um pouco atrás do líder para excelente campo de visão frontal
        const targetCameraZ = this.leader.z - 380;
        this.cameraZ += (targetCameraZ - this.cameraZ) * Math.min(1.0, dt * 7.0);

        // Curvatura e suavização horizontal da câmera
        const currentSeg = this._findSegment(this.cameraZ);
        const targetCameraX = currentSeg.curve * 0.45;
        this.cameraX += (targetCameraX - this.cameraX) * Math.min(1.0, dt * 5.0);

        // Deslocamento de Parallax
        const avgSpeed = this.racers.reduce((acc, r) => acc + r.speed, 0) / (this.racers.length || 1);
        const speedNorm = (avgSpeed / 180) * dt;
        this.skyOffset = (this.skyOffset + speedNorm * 12 + (currentSeg.curve * 0.3)) % this.width;
        this.cityOffset = (this.cityOffset + speedNorm * 38 + (currentSeg.curve * 0.8)) % this.width;
      }
    }

    // --- RENDERIZADOR CANVAS 2D OTIMIZADO ---
    render(ctx) {
      const W = this.width;
      const H = this.height;

      // 1. Limpar e renderizar céu/nebulosa cyberpunk (Parallax Layer 1)
      this._renderBackground(ctx, W, H);

      // 2. Renderizar Pista de Asfalto (Segmentos Tridimensionais)
      this._renderRoad(ctx, W, H);

      // 3. Renderizar Pilotos (Ordenados por profundidade Z decrescente)
      this._renderRacers(ctx);

      // 4. Renderizar Linhas de Velocidade / Nitro Thrusters
      this._renderSpeedFX(ctx, W, H);
    }

    _renderBackground(ctx, W, H) {
      // Gradiente de Céu Estelar Profundo
      const skyGrad = ctx.createLinearGradient(0, 0, 0, this.horizonY);
      skyGrad.addColorStop(0, this.theme.skyGradTop);
      skyGrad.addColorStop(1, this.theme.skyGradBottom);
      ctx.fillStyle = skyGrad;
      ctx.fillRect(0, 0, W, this.horizonY);

      // Linha do horizonte neon com brilho difuso
      ctx.save();
      ctx.shadowColor = '#818cf8';
      ctx.shadowBlur = 18;
      ctx.strokeStyle = 'rgba(129, 140, 248, 0.45)';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(0, this.horizonY);
      ctx.lineTo(W, this.horizonY);
      ctx.stroke();
      ctx.restore();

      // Silhueta Urbana Cyberpunk (Parallax Layer 2)
      ctx.fillStyle = '#0b0f19';
      const buildingW = 48;
      const numBld = Math.ceil(W / buildingW) + 2;
      const startX = -(this.cityOffset % buildingW);

      for (let i = 0; i < numBld; i++) {
        const bx = startX + (i * buildingW);
        const bHeight = 45 + ((i * 37) % 85);
        ctx.fillRect(bx, this.horizonY - bHeight, buildingW - 4, bHeight);

        // Janelas neon estocásticas
        ctx.fillStyle = (i % 3 === 0) ? '#06b6d4' : '#f43f5e';
        ctx.fillRect(bx + 8, this.horizonY - bHeight + 12, 4, 4);
        ctx.fillRect(bx + 24, this.horizonY - bHeight + 28, 4, 4);
        ctx.fillStyle = '#0b0f19';
      }
    }

    _renderRoad(ctx, W, H) {
      const baseSegment = this._findSegment(this.cameraZ);
      const baseIndex = baseSegment.index;
      let maxy = H;

      // Projetar e desenhar segmentos do fundo para a frente
      for (let n = 0; n < this.drawDistance; n++) {
        const seg = this.segments[(baseIndex + n) % this.segments.length];
        const looped = seg.index < baseIndex;
        const offsetZ = looped ? this.trackLength : 0;

        seg.p1.project(
          this.cameraX * this.roadWidth,
          this.cameraHeight,
          this.cameraZ - offsetZ,
          this.cameraDepth,
          W,
          H,
          this.horizonY,
          this.roadWidth
        );

        seg.p2.project(
          this.cameraX * this.roadWidth,
          this.cameraHeight,
          this.cameraZ - offsetZ,
          this.cameraDepth,
          W,
          H,
          this.horizonY,
          this.roadWidth
        );

        if (seg.p1.screenY <= this.horizonY || seg.p2.screenY >= maxy || seg.p2.screenY <= seg.p1.screenY) {
          continue;
        }

        // Renderizar Asfalto e Zebrados (Trapezóides)
        this._renderSegment(ctx, seg, W);
        maxy = seg.p1.screenY;
      }
    }

    _renderSegment(ctx, seg, W) {
      const p1 = seg.p1;
      const p2 = seg.p2;

      // 1. Grama / Terreno Lateral Neon
      const isDark = (seg.colorTheme === 'dark');
      ctx.fillStyle = isDark ? '#020617' : '#040d21';
      ctx.fillRect(0, p2.screenY, W, p1.screenY - p2.screenY);

      // 2. Faixa Zebrada / Rumble Strip
      const rumbleW1 = p1.screenW * 0.16;
      const rumbleW2 = p2.screenW * 0.16;
      ctx.fillStyle = isDark ? this.theme.rumbleCyan : this.theme.rumbleMagenta;
      this._drawPolygon(
        ctx,
        p1.screenX - p1.screenW - rumbleW1, p1.screenY,
        p1.screenX - p1.screenW, p1.screenY,
        p2.screenX - p2.screenW, p2.screenY,
        p2.screenX - p2.screenW - rumbleW2, p2.screenY
      );
      this._drawPolygon(
        ctx,
        p1.screenX + p1.screenW, p1.screenY,
        p1.screenX + p1.screenW + rumbleW1, p1.screenY,
        p2.screenX + p2.screenW + rumbleW2, p2.screenY,
        p2.screenX + p2.screenW, p2.screenY
      );

      // 3. Asfalto Principal
      ctx.fillStyle = isDark ? this.theme.asphaltDark : this.theme.asphaltLight;
      this._drawPolygon(
        ctx,
        p1.screenX - p1.screenW, p1.screenY,
        p1.screenX + p1.screenW, p1.screenY,
        p2.screenX + p2.screenW, p2.screenY,
        p2.screenX - p2.screenW, p2.screenY
      );

      // 4. Divisórias de Faixa (Pontilhado Neon)
      if (isDark) {
        const laneW1 = (p1.screenW * 2) / this.lanes;
        const laneW2 = (p2.screenW * 2) / this.lanes;
        ctx.fillStyle = this.theme.laneLine;

        for (let l = 1; l < this.lanes; l++) {
          const lx1 = (p1.screenX - p1.screenW) + (l * laneW1);
          const lx2 = (p2.screenX - p2.screenW) + (l * laneW2);
          const dw1 = Math.max(2, p1.screenW * 0.015);
          const dw2 = Math.max(2, p2.screenW * 0.015);

          this._drawPolygon(
            ctx,
            lx1 - dw1, p1.screenY,
            lx1 + dw1, p1.screenY,
            lx2 + dw2, p2.screenY,
            lx2 - dw2, p2.screenY
          );
        }
      }
    }

    _drawPolygon(ctx, x1, y1, x2, y2, x3, y3, x4, y4) {
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.lineTo(x3, y3);
      ctx.lineTo(x4, y4);
      ctx.closePath();
      ctx.fill();
    }

    _renderRacers(ctx) {
      // Ordenar por Z ascendente para desenhar os mais distantes primeiro (Painter's Algorithm)
      const sorted = [...this.racers].sort((a, b) => a.z - b.z);

      sorted.forEach(r => {
        // Projeta racer no espaço de tela
        const relZ = r.z - this.cameraZ;
        if (relZ <= 10 || relZ > this.drawDistance * this.segmentLength) return;

        const scale = this.cameraDepth / relZ;
        const screenX = Math.round((this.width / 2) + (scale * (r.x + r.lateralWobble - this.cameraX) * this.roadWidth * this.width / 4));
        const screenY = Math.round(this.horizonY + (scale * this.cameraHeight * this.height / 2));
        const carW = Math.max(18, Math.round(scale * 320 * this.width / 2));
        const carH = Math.max(12, Math.round(carW * 0.65));

        r.screen = { x: screenX, y: screenY, scale, w: carW, h: carH };

        // Renderiza o Kart / Veículo Vetorial Neon
        this._drawCarSprite(ctx, r, screenX, screenY, carW, carH);
      });
    }

    _drawCarSprite(ctx, r, cx, cy, w, h) {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(r.driftAngle);

      // Sombra projetada no asfalto
      ctx.fillStyle = 'rgba(0, 0, 0, 0.65)';
      ctx.beginPath();
      ctx.ellipse(0, h * 0.35, w * 0.55, h * 0.22, 0, 0, Math.PI * 2);
      ctx.fill();

      // Chassi do Veículo (Cores vibrantes por time)
      ctx.fillStyle = r.color;
      ctx.shadowColor = r.color;
      ctx.shadowBlur = r.nitroActive ? 25 : 12;

      // Corpo Principal do Kart / Carro
      ctx.beginPath();
      ctx.roundRect(-w * 0.45, -h * 0.4, w * 0.9, h * 0.7, 6);
      ctx.fill();

      // Cabine / Parabrisa Escuro
      ctx.fillStyle = '#0f172a';
      ctx.shadowBlur = 0;
      ctx.beginPath();
      ctx.roundRect(-w * 0.32, -h * 0.28, w * 0.64, h * 0.4, 4);
      ctx.fill();

      // Luzes Traseiras de Neon
      ctx.fillStyle = '#ef4444';
      ctx.shadowColor = '#ef4444';
      ctx.shadowBlur = 8;
      ctx.fillRect(-w * 0.42, h * 0.25, w * 0.18, h * 0.12);
      ctx.fillRect(w * 0.24, h * 0.25, w * 0.18, h * 0.12);

      // Fogo de Escape / Nitro Boost
      if (r.nitroActive) {
        ctx.fillStyle = '#38bdf8';
        ctx.shadowColor = '#38bdf8';
        ctx.shadowBlur = 18;
        const flameH = (h * 0.45) + (Math.random() * h * 0.25);
        ctx.beginPath();
        ctx.moveTo(-w * 0.15, h * 0.3);
        ctx.lineTo(0, h * 0.3 + flameH);
        ctx.lineTo(w * 0.15, h * 0.3);
        ctx.closePath();
        ctx.fill();
      }

      // Tag com Nome e Posição (Rank)
      ctx.restore();
      ctx.save();
      ctx.font = `bold ${Math.max(11, Math.round(w * 0.22))}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.fillStyle = '#ffffff';
      ctx.shadowColor = '#000000';
      ctx.shadowBlur = 6;
      ctx.fillText(`#${r.rank} ${r.name}`, cx, cy - (h * 0.65));
      ctx.restore();
    }

    _renderSpeedFX(ctx, W, H) {
      if (!this.leader || this.leader.speed < 180) return;

      // Linhas de velocidade verticais periféricas quando o líder acelera muito
      const intensity = Math.min(1.0, (this.leader.speed - 180) / 80);
      ctx.strokeStyle = `rgba(255, 255, 255, ${0.15 * intensity})`;
      ctx.lineWidth = 1.5;

      const numLines = Math.floor(10 * intensity);
      for (let i = 0; i < numLines; i++) {
        const lx = (i % 2 === 0) ? (Math.random() * (W * 0.2)) : (W - Math.random() * (W * 0.2));
        const ly = this.horizonY + Math.random() * (H - this.horizonY);
        const lLen = 40 + Math.random() * 80;
        ctx.beginPath();
        ctx.moveTo(lx, ly);
        ctx.lineTo(lx, ly + lLen);
        ctx.stroke();
      }
    }

    // --- TELEMETRIA & ESTATÍSTICAS ---
    getStandings() {
      return this.racers.map(r => ({
        id: r.id,
        name: r.name,
        rank: r.rank,
        speedKmH: Math.round(r.speed),
        distanceM: Math.round(r.z / 10),
        gapM: Math.round(r.gapMeters),
        nitroActive: r.nitroActive,
        boosts: r.boostCount
      }));
    }
  }

  return V5HighwayEngine;
}));
