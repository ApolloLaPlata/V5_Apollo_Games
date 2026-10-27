/**
 * V5 LIVE GAME SDK — Protocolo Unificado de Eventos para Jogos de Transmissão 9:16
 * Holding V5 Apollo — Divisão de Transmissão & Jogos
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
      
      this.callbacks = {
        comment: [],
        gift: [],
        like: [],
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
    }

    initBroadcastChannel() {
      try {
        if (typeof BroadcastChannel !== 'undefined') {
          this.channel = new BroadcastChannel('v5_broadcaster_games');
          this.channel.onmessage = (event) => {
            if (event.data) {
              this.dispatch(event.data);
            }
          };
        }
      } catch (err) {
        console.warn('[V5LiveSDK] BroadcastChannel nao suportado:', err);
      }
    }

    initWindowListener() {
      window.addEventListener('v5_event', (event) => {
        if (event.detail) {
          this.dispatch(event.detail);
        }
      });

      window.addEventListener('message', (event) => {
        if (event.data && (event.data.type || event.data.action)) {
          this.dispatch(event.data);
        }
      });
    }

    initAutoBot() {
      const mockUsers = ['@lucas_gamer', '@mari_live', '@pedro_stream', '@ana_pro', '@bruno_tk', '@clara_v5', '@diego_br'];
      const mockGifts = [
        { name: 'Rosa', coins: 1, weight: 5 },
        { name: 'Moeda V5', coins: 5, weight: 15 },
        { name: 'Coração', coins: 10, weight: 25 },
        { name: 'Leão Dourado', coins: 100, weight: 100 }
      ];

      this.botTimer = setInterval(() => {
        // Se houve evento real nos ultimos 4 segundos, nao gera bot
        if (Date.now() - this.lastEventTime < 3500) {
          return;
        }

        const isGift = Math.random() < 0.25;
        const randomUser = mockUsers[Math.floor(Math.random() * mockUsers.length)];
        const team = Math.random() < 0.5 ? 'A' : 'B';

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
            comment: team === 'A' ? '1' : '2',
            weight: 1,
            isBot: true
          });
        }
      }, this.autoBotInterval);
    }

    dispatch(data) {
      this.lastEventTime = Date.now();
      
      const type = data.type || (data.giftName ? 'gift' : 'comment');

      if (this.callbacks[type]) {
        this.callbacks[type].forEach(fn => fn(data));
      }
      this.callbacks.any.forEach(fn => fn(data));
    }

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

    // Dispara manualmente um evento para simulação local
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
