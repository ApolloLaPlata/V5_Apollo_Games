/**
 * V5 LIVE GAME SDK — Protocolo Unificado de Eventos para Jogos de Transmissão 9:16
 * Holding V5 Apollo — Divisão de Transmissão & Jogos
 * Versão: 2.0.0 (Auto-detecção de Ambiente: OBS vs Test Lab vs Standalone)
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.V5LiveSDK = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  class V5LiveGameSDK {
    constructor(options = {}) {
      this.gameId = options.gameId || 'v5_game';
      this.autoBotEnabled = options.autoBotEnabled !== undefined ? options.autoBotEnabled : true;
      this.autoBotInterval = options.autoBotInterval || 2500;
      this.autoBotSilenceThreshold = options.autoBotSilenceThreshold || 3000;
      
      // Auto-detecção de Ambiente de Execução
      this.env = this.detectEnvironment();
      this.isOBS = this.env === 'obs';
      this.isIframe = this.env === 'test_lab';
      this.isStandalone = this.env === 'standalone';

      this.callbacks = {
        comment: [],
        gift: [],
        like: [],
        round_start: [],
        round_end: [],
        any: []
      };

      this.channel = null;
      this.botTimer = null;
      this.lastEventTime = Date.now();

      this.initBroadcastChannel();
      this.initWindowListener();

      if (this.autoBotEnabled) {
        this.initAutoBot();
      }

      // Notifica o ambiente sobre prontidão
      this.notifyReady();
    }

    /**
     * Auto-detecta se o jogo está rodando no OBS Studio,
     * dentro do Test Lab (Iframe) ou como aba Standalone no navegador.
     */
    detectEnvironment() {
      // 1. OBS Browser Source
      const isOBS = (
        typeof window.obsstudio !== 'undefined' ||
        window.location.search.includes('obs=1') ||
        (navigator.userAgent && navigator.userAgent.toLowerCase().includes('obs'))
      );
      if (isOBS) return 'obs';

      // 2. Test Lab Iframe
      const isIframe = window.self !== window.top || window.location.search.includes('testlab=1');
      if (isIframe) return 'test_lab';

      // 3. Standalone Browser
      return 'standalone';
    }

    notifyReady() {
      const readyPayload = {
        type: 'SDK_READY',
        gameId: this.gameId,
        env: this.env,
        timestamp: Date.now()
      };

      // Notifica o Test Lab se estiver em iframe
      if (this.isIframe && window.parent) {
        window.parent.postMessage(readyPayload, '*');
      }

      // Notifica via BroadcastChannel
      if (this.channel) {
        try {
          this.channel.postMessage(readyPayload);
        } catch (e) {}
      }

      // Emite evento DOM local
      window.dispatchEvent(new CustomEvent('v5_sdk_ready', { detail: readyPayload }));
    }

    initBroadcastChannel() {
      try {
        if (typeof BroadcastChannel !== 'undefined') {
          this.channel = new BroadcastChannel('v5_broadcaster_games');
          this.channel.onmessage = (event) => {
            if (event.data && event.data.type !== 'SDK_READY') {
              this.dispatch(event.data);
            }
          };
        }
      } catch (err) {
        console.warn('[V5LiveSDK] BroadcastChannel indisponível:', err);
      }
    }

    initWindowListener() {
      // Escuta CustomEvent da janela
      window.addEventListener('v5_event', (event) => {
        if (event.detail) {
          this.dispatch(event.detail);
        }
      });

      // Escuta postMessage (Iframe Test Lab ou Broadcaster Cockpit)
      window.addEventListener('message', (event) => {
        if (event.data && (event.data.type || event.data.action || event.data.comment)) {
          if (event.data.type === 'SDK_READY') return;
          this.dispatch(event.data);
        }
      });
    }

    /**
     * Normalizador padronizado de payloads de eventos de live
     */
    normalizePayload(raw) {
      if (!raw) return null;

      let type = raw.type || 'comment';
      const comment = (raw.comment || raw.action || '').toString().trim();
      const giftName = raw.giftName || null;
      let weight = Number(raw.weight) || Number(raw.coins) || 1;
      let team = raw.team || null;

      // Normalização de Time (1 -> A, 2 -> B, 3 -> C)
      if (!team) {
        const lower = comment.toLowerCase();
        if (comment === '1' || lower.includes('azul') || lower.includes('blue')) team = 'A';
        else if (comment === '2' || lower.includes('vermelho') || lower.includes('red') || lower.includes('laranja')) team = 'B';
        else if (comment === '3' || lower.includes('ouro') || lower.includes('jackpot') || lower.includes('gold')) team = 'C';
      }

      // Se possui nome de presente, forçar type = gift
      if (giftName || raw.coins) {
        type = 'gift';
      } else if (raw.type === 'like' || raw.action === 'tap') {
        type = 'like';
      }

      return {
        type: type,
        action: raw.action || (type === 'gift' ? 'boost' : (type === 'like' ? 'tap' : 'vote')),
        comment: comment,
        team: team,
        user: raw.user || '@espectador',
        giftName: giftName,
        coins: Number(raw.coins) || (type === 'gift' ? weight : 0),
        weight: weight,
        count: Number(raw.count) || 1,
        isBot: Boolean(raw.isBot),
        isManual: Boolean(raw.isManual),
        timestamp: raw.timestamp || Date.now()
      };
    }

    dispatch(rawData) {
      const data = this.normalizePayload(rawData);
      if (!data) return;

      this.lastEventTime = Date.now();

      if (this.callbacks[data.type]) {
        this.callbacks[data.type].forEach(fn => fn(data));
      }
      this.callbacks.any.forEach(fn => fn(data));
    }

    /**
     * Motor Anti-Silêncio Universal Embutido
     * Se a live ficar sem interação real pelo tempo limite, gera microações autônomas.
     */
    initAutoBot() {
      const mockUsers = [
        '@lucas_gamer', '@mari_live', '@pedro_stream', '@ana_pro', 
        '@bruno_tk', '@clara_v5', '@diego_br', '@bia_tok', '@felipe_yt'
      ];
      
      const mockGifts = [
        { name: 'Rosa', coins: 1, weight: 5 },
        { name: 'Moeda V5', coins: 5, weight: 15 },
        { name: 'Coração', coins: 10, weight: 25 },
        { name: 'Leão Dourado', coins: 100, weight: 100 }
      ];

      this.botTimer = setInterval(() => {
        // Se houve evento real recente, aborta bot
        if (Date.now() - this.lastEventTime < this.autoBotSilenceThreshold) {
          return;
        }

        const isGift = Math.random() < 0.20;
        const randomUser = mockUsers[Math.floor(Math.random() * mockUsers.length)];
        const team = Math.random() < 0.45 ? 'A' : (Math.random() < 0.8 ? 'B' : 'C');

        if (isGift) {
          const gift = mockGifts[Math.floor(Math.random() * mockGifts.length)];
          this.dispatch({
            type: 'gift',
            action: 'boost',
            team: team,
            user: randomUser,
            giftName: gift.name,
            coins: gift.coins,
            weight: gift.weight,
            isBot: true
          });
        } else {
          this.dispatch({
            type: 'comment',
            action: 'vote',
            team: team,
            user: randomUser,
            comment: team === 'A' ? '1' : (team === 'B' ? '2' : '3'),
            weight: 1,
            isBot: true
          });
        }
      }, this.autoBotInterval);
    }

    // Assinatura de Eventos
    on(type, callback) {
      if (this.callbacks[type]) {
        this.callbacks[type].push(callback);
      }
      return this;
    }

    onComment(callback) {
      return this.on('comment', callback);
    }

    onGift(callback) {
      return this.on('gift', callback);
    }

    onLike(callback) {
      return this.on('like', callback);
    }

    onAny(callback) {
      return this.on('any', callback);
    }

    /**
     * Emite eventos de volta para o ecossistema (Broadcaster / Test Lab)
     */
    emit(type, payload = {}) {
      const fullData = {
        type: type,
        gameId: this.gameId,
        env: this.env,
        ...payload,
        timestamp: Date.now()
      };

      if (this.channel) {
        try {
          this.channel.postMessage(fullData);
        } catch (e) {}
      }

      if (this.isIframe && window.parent) {
        window.parent.postMessage(fullData, '*');
      }

      window.dispatchEvent(new CustomEvent(`v5_${type}`, { detail: fullData }));
    }

    // Dispara manualmente um evento
    triggerManual(data) {
      this.dispatch({
        ...data,
        isManual: true
      });
    }

    destroy() {
      if (this.botTimer) clearInterval(this.botTimer);
      if (this.channel) this.channel.close();
    }
  }

  return V5LiveGameSDK;
}));