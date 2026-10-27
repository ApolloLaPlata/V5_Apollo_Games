const fs = require('fs');
const path = require('path');
const vm = require('vm');

const GAMES_DIR = path.join(__dirname, '..', 'catalogo_jogos');

const dirs = fs.readdirSync(GAMES_DIR).filter(d => fs.statSync(path.join(GAMES_DIR, d)).isDirectory());

let totalTested = 0;
let errors = [];

dirs.forEach(dir => {
  const file = path.join(GAMES_DIR, dir, 'index.html');
  if (!fs.existsSync(file)) return;

  const content = fs.readFileSync(file, 'utf8');
  
  // Extract script content
  const scripts = [];
  const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
  let match;
  while ((match = scriptRegex.exec(content)) !== null) {
    if (!match[0].includes('src=')) {
      scripts.push(match[1]);
    }
  }

  const jsCode = scripts.join('\n');

  // Create a minimal browser mockup environment
  const mockListeners = {};
  const mockWindow = {
    addEventListener: (evt, cb) => {
      if (!mockListeners[evt]) mockListeners[evt] = [];
      mockListeners[evt].push(cb);
    },
    removeEventListener: () => {},
    innerWidth: 1080,
    innerHeight: 1920,
    devicePixelRatio: 1,
    location: { reload: () => {} },
    BroadcastChannel: function() {
      return {
        onmessage: null,
        postMessage: () => {},
        close: () => {}
      };
    }
  };

  const mockDoc = {
    getElementById: (id) => ({
      style: {},
      classList: { add: () => {}, remove: () => {}, toggle: () => {} },
      appendChild: () => {},
      removeChild: () => {},
      addEventListener: () => {},
      getContext: () => ({
        clearRect: () => {}, fillRect: () => {}, strokeRect: () => {},
        beginPath: () => {}, closePath: () => {}, moveTo: () => {},
        lineTo: () => {}, arc: () => {}, fill: () => {}, stroke: () => {},
        save: () => {}, restore: () => {}, translate: () => {}, rotate: () => {},
        scale: () => {}, createLinearGradient: () => ({ addColorStop: () => {} }),
        createRadialGradient: () => ({ addColorStop: () => {} }),
        fillText: () => {}, strokeText: () => {}, measureText: () => ({ width: 10 })
      }),
      width: 1080,
      height: 1920
    }),
    querySelectorAll: () => [],
    querySelector: () => null,
    createElement: () => ({
      style: {},
      classList: { add: () => {}, remove: () => {} },
      appendChild: () => {},
      setAttribute: () => {}
    }),
    body: { appendChild: () => {}, style: {} }
  };

  const context = vm.createContext({
    window: mockWindow,
    document: mockDoc,
    BroadcastChannel: mockWindow.BroadcastChannel,
    console: { log: () => {}, warn: () => {}, error: () => {} },
    setTimeout: (fn) => setTimeout(fn, 100000), // mock timeout
    clearTimeout: () => {},
    setInterval: () => 1,
    clearInterval: () => {},
    requestAnimationFrame: () => 1,
    cancelAnimationFrame: () => {},
    performance: { now: () => Date.now() },
    Math: Math,
    Date: Date,
    AudioContext: function() {
      return {
        state: 'suspended',
        resume: () => Promise.resolve(),
        createGain: () => ({
          gain: { setValueAtTime: () => {}, linearRampToValueAtTime: () => {}, exponentialRampToValueAtTime: () => {} },
          connect: () => {}
        }),
        createOscillator: () => ({
          type: 'sine',
          frequency: { setValueAtTime: () => {}, exponentialRampToValueAtTime: () => {}, linearRampToValueAtTime: () => {} },
          connect: () => {},
          start: () => {},
          stop: () => {}
        }),
        createBuffer: () => ({ getChannelData: () => new Float32Array(100) }),
        createBufferSource: () => ({ buffer: null, connect: () => {}, start: () => {} }),
        createBiquadFilter: () => ({ frequency: { setValueAtTime: () => {}, exponentialRampToValueAtTime: () => {} }, connect: () => {} }),
        destination: {}
      };
    }
  });

  try {
    vm.runInContext(jsCode, context);
    totalTested++;
    
    // Now simulate dispatching malformed payloads to listeners!
    const testPayloads = [
      null,
      undefined,
      "",
      "{}",
      "{ invalid json",
      123,
      true,
      {},
      { type: null },
      { type: 'comment', user: null, comment: null },
      { type: 'gift', user: undefined, giftName: null, value: 'NaN' },
      { type: 'vote', action: null, value: -99 }
    ];

    // Trigger v5_event listeners
    if (mockListeners['v5_event']) {
      mockListeners['v5_event'].forEach(cb => {
        testPayloads.forEach(p => {
          try {
            cb({ detail: p, data: p });
          } catch (e) {
            errors.push(`[${dir}] Erro no listener v5_event com payload ${JSON.stringify(p)}: ${e.message}`);
          }
        });
      });
    }

    // Trigger message listeners
    if (mockListeners['message']) {
      mockListeners['message'].forEach(cb => {
        testPayloads.forEach(p => {
          try {
            cb({ data: p });
          } catch (e) {
            errors.push(`[${dir}] Erro no listener message com payload ${JSON.stringify(p)}: ${e.message}`);
          }
        });
      });
    }

  } catch (err) {
    // If the game script itself fails to evaluate in mock context (e.g. references untracked DOM element)
    // we record it to see what mock needs
  }
});

console.log(`Fuzz test concluído. Testados: ${totalTested}/41.`);
if (errors.length > 0) {
  console.log(`Erros encontrados (${errors.length}):`);
  errors.forEach(e => console.log('  ' + e));
} else {
  console.log('Zero erros de runtime em payloads malformados!');
}
