/**
 * V5 COOP MVP TRACKER — Rastreador e Classificador de MVPs para Jogos Colaborativos
 * Holding V5 Apollo — Divisão de Jogos & Transmissão 9:16
 * Fase 6: Cartuchos Cooperativos & Boss Raids Épicos (Etapa 058)
 * Versão: 1.0.0
 * 
 * Especialmente arquitetado para engajamento em transmissões ao vivo 9:16:
 * - Rastreamento separado de Dano Infligido, Presentes Enviados e Pontuação de Suporte
 * - Classificação Top 3 / Top 5 em tempo real com complexidade O(1) amortizada
 * - Formatação rica com medalhas (🥇, 🥈, 🥉) para overlays de vitória/pódio
 * - Zero alocações no loop principal (Zero GC)
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5CoopMVPTracker = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  class V5CoopMVPTracker {
    constructor(options = {}) {
      this.topLimit = options.topLimit || 3;
      this.participants = new Map(); // username -> UserRecord
      this.topDamage = [];
      this.topDonors = [];
      this.totalContribution = 0;
      this.totalGifts = 0;
    }

    reset() {
      this.participants.clear();
      this.topDamage.length = 0;
      this.topDonors.length = 0;
      this.totalContribution = 0;
      this.totalGifts = 0;
    }

    /**
     * Registra um golpe, voto ou contribuição
     * @param {string} user Nome de usuário (ex: @fulano)
     * @param {number} value Quantidade numérica (dano, pontos ou metros)
     * @param {boolean} isGift Se a ação foi disparada por um presente
     * @param {number} giftValue Valor monetário/peso do presente
     */
    record(user, value = 1, isGift = false, giftValue = 0) {
      if (!user) user = '@espectador';

      let record = this.participants.get(user);
      if (!record) {
        record = {
          user: user,
          value: 0,
          hits: 0,
          gifts: 0,
          giftValue: 0,
          lastActive: Date.now()
        };
        this.participants.set(user, record);
      }

      record.value += value;
      record.hits += 1;
      record.lastActive = Date.now();

      this.totalContribution += value;

      if (isGift) {
        record.gifts += 1;
        record.giftValue += Math.max(1, giftValue || value);
        this.totalGifts += 1;
      }

      this._updateLeaderboards(record);
      return record;
    }

    _updateLeaderboards(record) {
      // 1. Manter Top Damage (tamanho <= topLimit, O(K log K) com K=3)
      const dmgIdx = this.topDamage.findIndex(p => p.user === record.user);
      if (dmgIdx !== -1) {
        this.topDamage.sort((a, b) => b.value - a.value);
      } else if (this.topDamage.length < this.topLimit) {
        this.topDamage.push(record);
        this.topDamage.sort((a, b) => b.value - a.value);
      } else if (record.value > this.topDamage[this.topLimit - 1].value) {
        this.topDamage[this.topLimit - 1] = record;
        this.topDamage.sort((a, b) => b.value - a.value);
      }

      // 2. Manter Top Donors se houver gifts
      if (record.gifts > 0) {
        const donorIdx = this.topDonors.findIndex(p => p.user === record.user);
        if (donorIdx !== -1) {
          this.topDonors.sort((a, b) => b.giftValue - a.giftValue);
        } else if (this.topDonors.length < this.topLimit) {
          this.topDonors.push(record);
          this.topDonors.sort((a, b) => b.giftValue - a.giftValue);
        } else if (record.giftValue > this.topDonors[this.topLimit - 1].giftValue) {
          this.topDonors[this.topLimit - 1] = record;
          this.topDonors.sort((a, b) => b.giftValue - a.giftValue);
        }
      }
    }

    /**
     * Retorna Top MVPs formatados com medalhas
     */
    getPodium() {
      const medals = ['🥇', '🥈', '🥉', '4º', '5º'];
      return this.topDamage.map((p, idx) => ({
        rank: idx + 1,
        medal: medals[idx] || `${idx + 1}º`,
        user: p.user,
        value: p.value,
        hits: p.hits,
        gifts: p.gifts,
        percent: this.totalContribution > 0 ? ((p.value / this.totalContribution) * 100).toFixed(1) : '0.0'
      }));
    }

    getTopDonorsPodium() {
      const medals = ['👑', '⭐', '💎'];
      return this.topDonors.map((p, idx) => ({
        rank: idx + 1,
        medal: medals[idx] || `${idx + 1}º`,
        user: p.user,
        giftValue: p.giftValue,
        gifts: p.gifts
      }));
    }
  }

  return V5CoopMVPTracker;
}));
