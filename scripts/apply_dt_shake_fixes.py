import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

games_to_fix = [
    ("08_caca_tesouro_coordenadas", "resetMatch", "ox", "oy"),
    ("10_queda_dos_blocos", "resetGame", "ox", "oy"),
    ("23_sobrevivencia_na_lava", "resetRound", "offsetX", "offsetY"),
    ("24_campo_minado_neon", "resetRound", "ox", "oy"),
    ("25_batalha_naval_live", "resetRound", "ox", "oy"),
]

for g, reset_fn, x_var, y_var in games_to_fix:
    path = os.path.join(GAMES_DIR, g, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Fix dt clamping
    code_mod = code.replace("const dt = (now - lastTime) / 1000;", "const dt = Math.min(0.1, (now - lastTime) / 1000);")

    # 2. Fix screenShake transform reset in gameLoop
    old_shake_block = f"""      if (screenShake > 0) {{
        screenShake = Math.max(0, screenShake - dt * 25);
        const stage = document.getElementById('game-stage');
        const {x_var} = (Math.random() - 0.5) * screenShake;
        const {y_var} = (Math.random() - 0.5) * screenShake;
        stage.style.transform = `translate(${{{x_var}}}px, ${{{y_var}}}px)`;
      }}"""

    new_shake_block = f"""      if (screenShake > 0) {{
        screenShake = Math.max(0, screenShake - dt * 25);
        const stage = document.getElementById('game-stage');
        if (stage) {{
          if (screenShake > 0) {{
            const {x_var} = (Math.random() - 0.5) * screenShake;
            const {y_var} = (Math.random() - 0.5) * screenShake;
            stage.style.transform = `translate(${{{x_var}}}px, ${{{y_var}}}px)`;
          }} else {{
            stage.style.transform = 'none';
          }}
        }}
      }}"""

    if old_shake_block in code_mod:
        code_mod = code_mod.replace(old_shake_block, new_shake_block)
        print(f"[FIXED SHAKE LOOP] {g}: stage.style.transform reset adicionado no gameLoop")
    else:
        print(f"[WARN SHAKE LOOP] {g}: padrão de screenShake não correspondeu exatamente")

    # 3. Add transform reset in reset function
    target_reset = f"function {reset_fn}() {{"
    replacement_reset = f"function {reset_fn}() {{\n      const stageEl = document.getElementById('game-stage');\n      if (stageEl) stageEl.style.transform = 'none';"
    if target_reset in code_mod and "stageEl.style.transform = 'none'" not in code_mod:
        code_mod = code_mod.replace(target_reset, replacement_reset, 1)
        print(f"[FIXED RESET TRANSFORM] {g}: stageEl.style.transform = 'none' adicionado em {reset_fn}()")

    if code_mod != code:
        with open(path, "w", encoding="utf-8") as f:
            f.write(code_mod)
        print(f"[SUCCESS] {g}: atualizado com sucesso!")
    else:
        print(f"[INFO] {g}: nenhuma alteração necessária")
