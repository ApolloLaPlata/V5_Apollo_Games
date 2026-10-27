import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"
SDK_FILE = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\sdk\v5_live_game_sdk.js"

def fix_beforeunload_leak():
    print("--- 1. Corrigindo vazamento de event listener beforeunload ---")
    fixed_count = 0
    for g in sorted(os.listdir(GAMES_DIR)):
        idx = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(idx):
            continue
        with open(idx, "r", encoding="utf-8") as f:
            content = f.read()

        changed = False

        # Pattern 1: broadcasterChannel
        pattern1 = r"(broadcasterChannel\.onmessage\s*=\s*\(event\)\s*=>\s*\{[ \t\r\n]*if\s*\(event\s*&&\s*event\.data\)\s*handleLivePayload\(event\.data\);)[ \t\r\n]*(window\.addEventListener\('beforeunload',[^;]+;\s*\}\);)[ \t\r\n]*(\};)"
        if re.search(pattern1, content):
            replacement1 = r"\1\n      };\n      \2"
            content = re.sub(pattern1, replacement1, content)
            changed = True

        # Pattern 2: channel in game 02
        pattern2 = r"(channel\.onmessage\s*=\s*\(e\)\s*=>\s*\{[ \t\r\n]*if\s*\(e\.data\)\s*processLiveEvent\(e\.data\);)[ \t\r\n]*(window\.addEventListener\('beforeunload',[^;]+;\s*\}\);)[ \t\r\n]*(\};)"
        if re.search(pattern2, content):
            replacement2 = r"\1\n      };\n      \2"
            content = re.sub(pattern2, replacement2, content)
            changed = True

        # Pattern 3: channel in games 33-40
        pattern3 = r"(channel\.onmessage\s*=\s*\(event\)\s*=>\s*\{[ \t\r\n]*handleIncomingEvent\(event\.data\);)[ \t\r\n]*(window\.addEventListener\('beforeunload',[^;]+;\s*\}\);)[ \t\r\n]*(\};)"
        if re.search(pattern3, content):
            replacement3 = r"\1\n        };\n        \2"
            content = re.sub(pattern3, replacement3, content)
            changed = True

        if changed:
            with open(idx, "w", encoding="utf-8") as f:
                f.write(content)
            fixed_count += 1
            print(f"  [OK] Corrigido beforeunload em: {g}")

    print(f"Total de jogos corrigidos (beforeunload): {fixed_count}")

def fix_parseint_radix():
    print("--- 2. Corrigindo parseInt sem radix 10 ---")
    # Game 23
    p23 = os.path.join(GAMES_DIR, "23_sobrevivencia_na_lava", "index.html")
    with open(p23, "r", encoding="utf-8") as f:
        c23 = f.read()
    if "parseInt(data.team)" in c23:
        c23 = c23.replace("parseInt(data.team)", "parseInt(data.team, 10)")
        with open(p23, "w", encoding="utf-8") as f:
            f.write(c23)
        print("  [OK] Corrigido parseInt(data.team, 10) no jogo 23")

    # Game 33
    p33 = os.path.join(GAMES_DIR, "33_corrida_de_cavalos_retro", "index.html")
    with open(p33, "r", encoding="utf-8") as f:
        c33 = f.read()
    if "parseInt(targetTeam)" in c33:
        c33 = c33.replace("parseInt(targetTeam)", "parseInt(targetTeam, 10)")
        with open(p33, "w", encoding="utf-8") as f:
            f.write(c33)
        print("  [OK] Corrigido parseInt(targetTeam, 10) no jogo 33")

def fix_game_39_target_reset():
    print("--- 3. Corrigindo reset de alvos no jogo 39 ---")
    p39 = os.path.join(GAMES_DIR, "39_alvo_movel_snipers", "index.html")
    with open(p39, "r", encoding="utf-8") as f:
        c39 = f.read()

    target_init = """    function initSniperGame() {
      state.roundActive = true;
      state.timeRemaining = ROUND_DURATION_SEC;
      state.score = 0;
      state.bullseyes = 0;
      state.totalShots = 0;
      state.hits = 0;
      state.lockOnTimer = 0;
      state.arrows = [];
      state.particles = [];
      state.confetti = [];
      state.resetCountdown = 5;
      state.donors = {};"""

    replacement_init = """    function initSniperGame() {
      state.roundActive = true;
      state.timeRemaining = ROUND_DURATION_SEC;
      state.score = 0;
      state.bullseyes = 0;
      state.totalShots = 0;
      state.hits = 0;
      state.lockOnTimer = 0;
      state.arrows = [];
      state.particles = [];
      state.confetti = [];
      state.resetCountdown = 5;
      state.donors = {};
      state.targets = [
        {
          x: 540,
          y: 620,
          radius: 90,
          vx: 320,
          minX: 180,
          maxX: 900,
          color: '#ff0055',
          isMain: true
        }
      ];"""

    if target_init in c39:
        c39 = c39.replace(target_init, replacement_init)
        with open(p39, "w", encoding="utf-8") as f:
            f.write(c39)
        print("  [OK] Corrigido reset deterministico de alvos no jogo 39")
    else:
        print("  [WARN] Padrão não encontrado no jogo 39")

def fix_game_28_arrays_reset():
    print("--- 4. Corrigindo limpeza de partículas e textos no jogo 28 ---")
    p28 = os.path.join(GAMES_DIR, "28_labirinto_pacman_neon", "index.html")
    with open(p28, "r", encoding="utf-8") as f:
        c28 = f.read()

    target_reset = """      state.freezeGhostsTime = 0;
      state.speedBoostTime = 0;

      // Restaura o labirinto original"""

    replacement_reset = """      state.freezeGhostsTime = 0;
      state.speedBoostTime = 0;
      state.floatingTexts = [];
      state.particles = [];

      // Restaura o labirinto original"""

    if target_reset in c28:
        c28 = c28.replace(target_reset, replacement_reset)
        with open(p28, "w", encoding="utf-8") as f:
            f.write(c28)
        print("  [OK] Adicionada limpeza de floatingTexts e particles no reset do jogo 28")
    else:
        print("  [WARN] Padrão não encontrado no jogo 28")

def fix_sdk_deduplication():
    print("--- 5. Adicionando desduplicação LRU no SDK ---")
    with open(SDK_FILE, "r", encoding="utf-8") as f:
        sdk_c = f.read()

    # 1. Constructor: seenEventIds
    target_ctor = "this.lastEventTime = Date.now();"
    replacement_ctor = """this.lastEventTime = Date.now();
      this.seenEventIds = new Set();
      this.seenEventList = [];"""

    if target_ctor in sdk_c and "this.seenEventIds = new Set();" not in sdk_c:
        sdk_c = sdk_c.replace(target_ctor, replacement_ctor)
        print("  [OK] Injetado cache seenEventIds no construtor do SDK")

    # 2. normalizePayload: id preservation
    target_norm = "return {\n        type: type,"
    replacement_norm = "return {\n        id: raw.id || raw.eventId || raw.msgId || null,\n        type: type,"

    if target_norm in sdk_c and "id: raw.id || raw.eventId" not in sdk_c:
        sdk_c = sdk_c.replace(target_norm, replacement_norm)
        print("  [OK] Preservação de id adicionada em normalizePayload")

    # 3. dispatch: deduplication check
    target_dispatch = """    dispatch(rawData) {
      const data = this.normalizePayload(rawData);
      if (!data) return;

      this.lastEventTime = Date.now();"""

    replacement_dispatch = """    dispatch(rawData) {
      const data = this.normalizePayload(rawData);
      if (!data) return;

      // Desduplicação LRU (previne duplo processamento em bridges redundantes)
      if (data.id) {
        if (this.seenEventIds.has(data.id)) return;
        this.seenEventIds.add(data.id);
        this.seenEventList.push(data.id);
        if (this.seenEventList.length > 200) {
          this.seenEventIds.delete(this.seenEventList.shift());
        }
      }

      this.lastEventTime = Date.now();"""

    if target_dispatch in sdk_c:
        sdk_c = sdk_c.replace(target_dispatch, replacement_dispatch)
        print("  [OK] Guarda de desduplicação adicionada em dispatch()")

    with open(SDK_FILE, "w", encoding="utf-8") as f:
        f.write(sdk_c)

if __name__ == "__main__":
    fix_beforeunload_leak()
    fix_parseint_radix()
    fix_game_39_target_reset()
    fix_game_28_arrays_reset()
    fix_sdk_deduplication()
