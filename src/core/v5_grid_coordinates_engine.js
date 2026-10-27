/**
 * V5 GRID COORDINATES ENGINE — Motor de Grids Interativos e Mapeamento de Coordenadas de Chat
 * Holding V5 Apollo — Divisão de Jogos & Transmissão 9:16
 * Fase 8: Cartuchos de Tabuleiro & Coordenadas (Etapa 071)
 * Versão: 1.0.0
 * 
 * Especialmente arquitetado para transmissões verticais 9:16 (1080x1920 responsivo):
 * - Parsing ultra-tolerante de coordenadas digitadas em teclado de celular ("A1", "b3", "1a", "c-4", "d 2")
 * - Suporte a grids dinâmicos: 4x4 (16 células: A1..D4) e 6x6 (36 células: A1..F6)
 * - Agregação ponderada de votos em tempo real com tracking O(1) de célula líder
 * - Multiplicador de presentes (Gifts) com disparo de sensores de Raio-X e revelação em área
 * - State Machine de células: HIDDEN (0), REVEALED (1), EXPLODED (2), LOCKED (3), FLAGGED (4)
 * - Tipos de conteúdo: EMPTY (0), TREASURE (1), TRAP (2), MINE (3), KEY (4), SHIP (5)
 * - Utilitário geométrico de layout vertical 9:16 com respeito a Safe Zones (Topo 140px / Base 180px)
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5GridCoordinatesEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  // Constantes de Estado das Células
  const CELL_STATE = {
    HIDDEN: 0,
    REVEALED: 1,
    EXPLODED: 2,
    LOCKED: 3,
    FLAGGED: 4
  };

  // Constantes de Conteúdo das Células
  const CELL_CONTENT = {
    EMPTY: 0,
    TREASURE: 1,
    TRAP: 2,
    MINE: 3,
    KEY: 4,
    SHIP: 5
  };

  // Nomes de linhas padrão (A até H)
  const ROW_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];

  class V5GridCoordinatesEngine {
    constructor(options = {}) {
      this.rows = options.rows || 4;
      this.cols = options.cols || 4;
      this.totalCells = this.rows * this.cols;

      // Configuração de Pesos de Voto
      this.commentWeight = options.commentWeight || 1;
      this.giftMultiplier = options.giftMultiplier || 15;
      this.superGiftMultiplier = options.superGiftMultiplier || 50;

      // Callbacks
      this.onCellRevealed = options.onCellRevealed || null;
      this.onLeadingCellChanged = options.onLeadingCellChanged || null;
      this.onTreasureFound = options.onTreasureFound || null;
      this.onTrapTriggered = options.onTrapTriggered || null;
      this.onRoundResolved = options.onRoundResolved || null;

      // Estado do Grid
      this.cells = [];
      this.leadingCellIndex = -1;
      this.highestVotes = 0;
      this.totalVotesRound = 0;
      this.isRoundLocked = false;

      // Ranking de Participantes da Rodada
      this.participants = new Map();

      // Inicialização da Grade
      this._initGrid();
    }

    /**
     * Inicializa as estruturas de dados das células
     */
    _initGrid() {
      this.cells = new Array(this.totalCells);
      this.leadingCellIndex = -1;
      this.highestVotes = 0;
      this.totalVotesRound = 0;
      this.isRoundLocked = false;
      this.participants.clear();

      for (let r = 0; r < this.rows; r++) {
        const letter = ROW_LETTERS[r] || String.fromCharCode(65 + r);
        for (let c = 0; c < this.cols; c++) {
          const index = r * this.cols + c;
          const colNumber = c + 1;
          const label = `${letter}${colNumber}`;

          this.cells[index] = {
            index: index,
            row: r,
            col: c,
            rowLetter: letter,
            colNumber: colNumber,
            label: label,
            state: CELL_STATE.HIDDEN,
            content: CELL_CONTENT.EMPTY,
            contentValue: 0,
            votes: 0,
            voters: {},
            lastVoter: null,
            xRayGlow: 0.0,
            discoverer: null,
            // Coordenadas calculadas no layout
            rect: { x: 0, y: 0, width: 0, height: 0 }
          };
        }
      }
    }

    /**
     * Parser ultra tolerante para coordenadas digitadas em live de celular.
     * Suporta formatos:
     * - "A1", "a1", "B3", "d4", "f6"
     * - "1A", "3b", "4d" (ordem invertida comum)
     * - "A-1", "a 1", "c.3", "b,2", "quadrante a1"
     * 
     * @param {string} text - Mensagem bruta do chat
     * @returns {Object} { valid: boolean, row: number, col: number, index: number, label: string }
     */
    parseCoordinate(text) {
      if (!text || typeof text !== 'string') {
        return { valid: false };
      }

      const str = text.trim().toUpperCase();

      // Regex 1: Letra primeiro, depois número (ex: "A1", "A 1", "A-1", "A:1")
      // Limita as letras até a última linha configurada (ex: A-D para 4 linhas, A-F para 6)
      const maxLetter = ROW_LETTERS[this.rows - 1];
      const letterPattern = `[A-${maxLetter}]`;
      const numPattern = `[1-${this.cols}]`;

      const standardMatch = str.match(new RegExp(`(?:^|[^A-Z0-9])(${letterPattern})[\\s\\-\\.,_:]*(${numPattern})(?:[^A-Z0-9]|$)`));
      if (standardMatch) {
        const row = standardMatch[1].charCodeAt(0) - 65;
        const col = parseInt(standardMatch[2], 10) - 1;
        if (row >= 0 && row < this.rows && col >= 0 && col < this.cols) {
          const index = row * this.cols + col;
          return {
            valid: true,
            row: row,
            col: col,
            index: index,
            label: `${ROW_LETTERS[row]}${col + 1}`
          };
        }
      }

      // Regex 2: Número primeiro, depois letra (ex: "1A", "1-A", "3 b")
      const invertedMatch = str.match(new RegExp(`(?:^|[^A-Z0-9])(${numPattern})[\\s\\-\\.,_:]*(${letterPattern})(?:[^A-Z0-9]|$)`));
      if (invertedMatch) {
        const col = parseInt(invertedMatch[1], 10) - 1;
        const row = invertedMatch[2].charCodeAt(0) - 65;
        if (row >= 0 && row < this.rows && col >= 0 && col < this.cols) {
          const index = row * this.cols + col;
          return {
            valid: true,
            row: row,
            col: col,
            index: index,
            label: `${ROW_LETTERS[row]}${col + 1}`
          };
        }
      }

      return { valid: false };
    }

    /**
     * Processa um evento padronizado do V5 Live Event Bus
     * 
     * @param {Object} eventPayload { type, comment, giftName, value, user }
     * @returns {Object|null} Resumo da ação executada ou null se sem efeito
     */
    processEvent(eventPayload) {
      if (!eventPayload || this.isRoundLocked) return null;

      const user = eventPayload.user || '@espectador';
      const type = eventPayload.type || 'comment';
      const comment = (eventPayload.comment || '').trim();
      const giftName = eventPayload.giftName || null;
      const value = eventPayload.value || 1;

      // 1. Verificar se é presente com ação direta
      if (type === 'gift') {
        const isSuper = (giftName && giftName.toLowerCase().includes('lion')) || value >= 500;
        const weight = isSuper ? this.superGiftMultiplier : this.giftMultiplier;

        // Se o payload contiver coordenada no comment
        let targetIndex = -1;
        const coord = this.parseCoordinate(comment);
        if (coord.valid && this.cells[coord.index].state === CELL_STATE.HIDDEN) {
          targetIndex = coord.index;
        } else {
          // Se não especificou coordenada, aplica na célula líder atual ou na com maior potencial
          targetIndex = this.leadingCellIndex >= 0 ? this.leadingCellIndex : this._getRandomHiddenCellIndex();
        }

        if (targetIndex >= 0) {
          this._applyVote(targetIndex, user, weight, true, isSuper);
          // Efeito de Raio-X na célula
          this.cells[targetIndex].xRayGlow = 1.0;

          // Se for super presente, ativa raio-X em cruz (vizinhos imediatos)
          if (isSuper) {
            this._applyCrossXRay(targetIndex);
          }

          return {
            action: 'gift_boost',
            user: user,
            cellIndex: targetIndex,
            label: this.cells[targetIndex].label,
            weight: weight,
            isSuper: isSuper
          };
        }
      }

      // 2. Comentário normal do chat
      const coord = this.parseCoordinate(comment);
      if (coord.valid) {
        const cell = this.cells[coord.index];
        // Votos só contam para células que ainda estão cobertas
        if (cell.state === CELL_STATE.HIDDEN) {
          this._applyVote(coord.index, user, this.commentWeight, false, false);
          return {
            action: 'vote',
            user: user,
            cellIndex: coord.index,
            label: coord.label,
            weight: this.commentWeight
          };
        }
      }

      return null;
    }

    /**
     * Aplica o voto na célula e recalcula o líder
     */
    _applyVote(index, user, weight, isGift = false, isSuper = false) {
      const cell = this.cells[index];
      cell.votes += weight;
      cell.voters[user] = (cell.voters[user] || 0) + weight;
      cell.lastVoter = user;

      // Tracking de participantes globais
      const currentPts = this.participants.get(user) || 0;
      this.participants.set(user, currentPts + weight);

      this.totalVotesRound += weight;

      // Atualiza célula líder em O(1)
      const prevLeader = this.leadingCellIndex;
      if (cell.votes > this.highestVotes) {
        this.highestVotes = cell.votes;
        this.leadingCellIndex = index;

        if (this.leadingCellIndex !== prevLeader && this.onLeadingCellChanged) {
          this.onLeadingCellChanged(this.cells[this.leadingCellIndex]);
        }
      }
    }

    /**
     * Efeito de Raio-X em cruz para Super Gifts
     */
    _applyCrossXRay(centerIndex) {
      const center = this.cells[centerIndex];
      const neighbors = [
        { r: center.row - 1, c: center.col },
        { r: center.row + 1, c: center.col },
        { r: center.row, c: center.col - 1 },
        { r: center.row, c: center.col + 1 }
      ];

      neighbors.forEach(n => {
        if (n.r >= 0 && n.r < this.rows && n.c >= 0 && n.c < this.cols) {
          const idx = n.r * this.cols + n.c;
          if (this.cells[idx].state === CELL_STATE.HIDDEN) {
            this.cells[idx].xRayGlow = Math.max(this.cells[idx].xRayGlow, 0.65);
          }
        }
      });
    }

    /**
     * Revela a célula (acionada quando o timer da rodada fecha ou por ação direta)
     */
    revealCell(index, discovererUser = null) {
      if (index < 0 || index >= this.totalCells) return null;
      const cell = this.cells[index];

      if (cell.state !== CELL_STATE.HIDDEN) return cell;

      cell.state = (cell.content === CELL_CONTENT.TRAP || cell.content === CELL_CONTENT.MINE)
        ? CELL_STATE.EXPLODED
        : CELL_STATE.REVEALED;

      cell.discoverer = discovererUser || cell.lastVoter || '@chat';

      // Notificações de callback
      if (this.onCellRevealed) {
        this.onCellRevealed(cell);
      }

      if (cell.content === CELL_CONTENT.TREASURE && this.onTreasureFound) {
        this.onTreasureFound(cell);
      } else if ((cell.content === CELL_CONTENT.TRAP || cell.content === CELL_CONTENT.MINE) && this.onTrapTriggered) {
        this.onTrapTriggered(cell);
      }

      return cell;
    }

    /**
     * Resolve a rodada abrindo a célula mais votada pelo chat
     */
    resolveLeadingCell() {
      if (this.leadingCellIndex < 0) {
        // Se ninguém votou, abre uma aleatória coberta
        this.leadingCellIndex = this._getRandomHiddenCellIndex();
      }

      if (this.leadingCellIndex >= 0) {
        const topVoter = this._getTopVoterForCell(this.leadingCellIndex);
        const revealed = this.revealCell(this.leadingCellIndex, topVoter);

        // Reset de contadores de voto para a próxima rodada
        this.resetVotesOnly();

        if (this.onRoundResolved) {
          this.onRoundResolved(revealed);
        }

        return revealed;
      }

      return null;
    }

    /**
     * Reseta apenas os votos sem fechar as células já abertas (próximo turno)
     */
    resetVotesOnly() {
      this.leadingCellIndex = -1;
      this.highestVotes = 0;
      this.totalVotesRound = 0;

      for (let i = 0; i < this.totalCells; i++) {
        this.cells[i].votes = 0;
        this.cells[i].voters = {};
        this.cells[i].lastVoter = null;
        this.cells[i].xRayGlow = Math.max(0, this.cells[i].xRayGlow - 0.4);
      }
    }

    /**
     * Reseta todo o tabuleiro (nova partida completa)
     */
    resetFullGrid() {
      this._initGrid();
    }

    /**
     * Popula o grid com tesouros e armadilhas aleatórias
     * @param {Object} config { treasures: 3, traps: 4, keys: 2 }
     */
    populateContent(config = {}) {
      const treasuresCount = config.treasures || 2;
      const trapsCount = config.traps || 3;
      const keysCount = config.keys || 1;

      // Limpar conteúdos
      for (let i = 0; i < this.totalCells; i++) {
        this.cells[i].content = CELL_CONTENT.EMPTY;
        this.cells[i].contentValue = 0;
      }

      // Embaralhar índices disponíveis
      const indices = Array.from({ length: this.totalCells }, (_, i) => i);
      for (let i = indices.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [indices[i], indices[j]] = [indices[j], indices[i]];
      }

      let ptr = 0;
      // Posicionar Tesouros
      for (let t = 0; t < treasuresCount && ptr < indices.length; t++) {
        this.cells[indices[ptr]].content = CELL_CONTENT.TREASURE;
        this.cells[indices[ptr]].contentValue = 1000;
        ptr++;
      }
      // Posicionar Chaves
      for (let k = 0; k < keysCount && ptr < indices.length; k++) {
        this.cells[indices[ptr]].content = CELL_CONTENT.KEY;
        this.cells[indices[ptr]].contentValue = 500;
        ptr++;
      }
      // Posicionar Armadilhas / Minas
      for (let tr = 0; tr < trapsCount && ptr < indices.length; tr++) {
        this.cells[indices[ptr]].content = CELL_CONTENT.TRAP;
        this.cells[indices[ptr]].contentValue = -300;
        ptr++;
      }
    }

    /**
     * Calcula o layout geométrico responsivo das células para a proporção 9:16.
     * Garante células perfeitamente legíveis entre Safe Zone Top (140px) e Bottom (180px).
     * 
     * @param {number} width - Largura atual da tela
     * @param {number} height - Altura atual da tela
     * @param {number} safeTop - Margem de topo (ex: 140)
     * @param {number} safeBottom - Margem de base (ex: 180)
     * @param {number} gap - Espaçamento entre células (ex: 8)
     */
    computeLayout(width, height, safeTop = 140, safeBottom = 180, gap = 8) {
      const availWidth = width * 0.90; // 90% da largura útil
      const availHeight = height - safeTop - safeBottom;

      // Dimensões de cada célula preservando aspecto quadrado
      const maxCellWidth = (availWidth - (this.cols - 1) * gap) / this.cols;
      const maxCellHeight = (availHeight - (this.rows - 1) * gap) / this.rows;
      const cellSize = Math.min(maxCellWidth, maxCellHeight);

      const totalGridW = this.cols * cellSize + (this.cols - 1) * gap;
      const totalGridH = this.rows * cellSize + (this.rows - 1) * gap;

      const startX = (width - totalGridW) / 2;
      const startY = safeTop + (availHeight - totalGridH) / 2;

      for (let r = 0; r < this.rows; r++) {
        for (let c = 0; c < this.cols; c++) {
          const index = r * this.cols + c;
          const x = startX + c * (cellSize + gap);
          const y = startY + r * (cellSize + gap);

          this.cells[index].rect = {
            x: x,
            y: y,
            width: cellSize,
            height: cellSize,
            radius: Math.max(6, Math.floor(cellSize * 0.12))
          };
        }
      }

      return {
        startX: startX,
        startY: startY,
        cellSize: cellSize,
        totalWidth: totalGridW,
        totalHeight: totalGridH
      };
    }

    /**
     * Retorna um índice aleatório de célula que ainda esteja coberta (HIDDEN)
     */
    _getRandomHiddenCellIndex() {
      const hidden = [];
      for (let i = 0; i < this.totalCells; i++) {
        if (this.cells[i].state === CELL_STATE.HIDDEN) {
          hidden.push(i);
        }
      }
      if (hidden.length === 0) return -1;
      return hidden[Math.floor(Math.random() * hidden.length)];
    }

    /**
     * Retorna o usuário com mais votos em uma célula específica
     */
    _getTopVoterForCell(index) {
      const cell = this.cells[index];
      let topUser = '@chat';
      let maxPts = 0;

      for (const [user, pts] of Object.entries(cell.voters)) {
        if (pts > maxPts) {
          maxPts = pts;
          topUser = user;
        }
      }
      return topUser;
    }

    /**
     * Retorna os N maiores contribuidores da partida
     */
    getTopParticipants(n = 3) {
      const list = Array.from(this.participants.entries()).map(([user, pts]) => ({
        user: user,
        score: pts
      }));
      list.sort((a, b) => b.score - a.score);
      return list.slice(0, n);
    }
  }

  // Exportação das constantes estáticas
  V5GridCoordinatesEngine.CELL_STATE = CELL_STATE;
  V5GridCoordinatesEngine.CELL_CONTENT = CELL_CONTENT;
  V5GridCoordinatesEngine.ROW_LETTERS = ROW_LETTERS;

  return V5GridCoordinatesEngine;
}));
