import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def fix_all_discovered_bugs():
    # 1. Fix 02_plinko_pachinko_fortuna
    p02 = os.path.join(GAMES_DIR, "02_plinko_pachinko_fortuna", "index.html")
    with open(p02, "r", encoding="utf-8") as f:
        c02 = f.read()

    # Fix giftName null check in 02
    target02 = "if (weight >= 50 || giftName.toLowerCase().includes('leão') || giftName.toLowerCase().includes('lion')) {"
    # Also check if it might be encoded differently
    pattern02 = r"if\s*\(\s*weight\s*>=\s*50\s*\|\|\s*giftName\.toLowerCase\(\)\.includes\(['\"]le[ã\?]o['\"]\)\s*\|\|\s*giftName\.toLowerCase\(\)\.includes\(['\"]lion['\"]\)\s*\)\s*\{"
    replacement02 = "const gStr = (giftName || '').toLowerCase();\n      if (weight >= 50 || gStr.includes('leão') || gStr.includes('lion')) {"
    c02_fixed = re.sub(pattern02, replacement02, c02)

    # Also ensure giftName has a default fallback so toasts don't say 'enviou null'
    c02_fixed = c02_fixed.replace("const giftName = payload.giftName || null;", "const giftName = payload.giftName || 'Presente';")

    if c02_fixed != c02:
        with open(p02, "w", encoding="utf-8") as f:
            f.write(c02_fixed)
        print("[FIXED] 02_plinko_pachinko_fortuna: blindado contra giftName nulo e toLowerCase()")
    else:
        print("[WARN] 02_plinko_pachinko_fortuna: padrão não encontrado ou já aplicado")

    # 2. Fix 23_sobrevivencia_na_lava
    p23 = os.path.join(GAMES_DIR, "23_sobrevivencia_na_lava", "index.html")
    with open(p23, "r", encoding="utf-8") as f:
        c23 = f.read()

    pattern23 = r'const\s+boostVal\s*=\s*\(\s*giftName\.toLowerCase\(\)\.includes\(["\']lion["\']\)\s*\|\|\s*value\s*>=\s*500\s*\)\s*\?\s*50\s*:\s*25;'
    replacement23 = 'const gName = (giftName || "").toLowerCase();\n        const boostVal = (gName.includes("lion") || value >= 500) ? 50 : 25;'
    c23_fixed = re.sub(pattern23, replacement23, c23)

    if c23_fixed != c23:
        with open(p23, "w", encoding="utf-8") as f:
            f.write(c23_fixed)
        print("[FIXED] 23_sobrevivencia_na_lava: blindado contra giftName nulo e toLowerCase()")
    else:
        print("[WARN] 23_sobrevivencia_na_lava: padrão não encontrado ou já aplicado")

    # 3. Fix 15_corrida_maluca_espacial meteor spawner
    p15 = os.path.join(GAMES_DIR, "15_corrida_maluca_espacial", "index.html")
    with open(p15, "r", encoding="utf-8") as f:
        c15 = f.read()

    pattern15 = r'setInterval\s*\(\s*\(\)\s*=>\s*\{\s*if\s*\(\s*Math\.random\(\)\s*<\s*0\.65\s*\)\s*spawnMeteor\(\);\s*\}\s*,\s*1200\s*\);'
    replacement15 = 'setInterval(() => {\n      if (isGameOver) return;\n      if (Math.random() < 0.65) spawnMeteor();\n    }, 1200);'
    c15_fixed = re.sub(pattern15, replacement15, c15)

    if c15_fixed != c15:
        with open(p15, "w", encoding="utf-8") as f:
            f.write(c15_fixed)
        print("[FIXED] 15_corrida_maluca_espacial: spawnMeteor() agora pausa durante isGameOver")
    else:
        print("[WARN] 15_corrida_maluca_espacial: padrão não encontrado ou já aplicado")

    # 4. Fix defensive entry guard in handleGameEvent for 08, 10, 23, 24, 25
    guarded_games = [
        "08_caca_tesouro_coordenadas",
        "10_queda_dos_blocos",
        "23_sobrevivencia_na_lava",
        "24_campo_minado_neon",
        "25_batalha_naval_live"
    ]

    for g in guarded_games:
        pg = os.path.join(GAMES_DIR, g, "index.html")
        with open(pg, "r", encoding="utf-8") as f:
            cg = f.read()

        # Check function handleGameEvent(data) {
        pattern_handler = r'(function\s+handleGameEvent\s*\(\s*data\s*\)\s*\{\s*)(if\s*\(\s*isGameOver\s*\)\s*return;)'
        replacement_handler = r'\1if (!data || typeof data !== "object") return;\n      \2'
        cg_fixed = re.sub(pattern_handler, replacement_handler, cg)

        if cg_fixed != cg:
            with open(pg, "w", encoding="utf-8") as f:
                f.write(cg_fixed)
            print(f"[FIXED] {g}: adicionada guarda defensiva contra data nulo/inválido em handleGameEvent")
        else:
            print(f"[INFO] {g}: guarda defensiva já presente ou padrão diferente")

if __name__ == "__main__":
    fix_all_discovered_bugs()
