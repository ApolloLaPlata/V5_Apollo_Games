import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def apply_particle_resets():
    games_and_fns = [
        ("08_caca_tesouro_coordenadas", "resetMatch"),
        ("10_queda_dos_blocos", "resetGame"),
        ("23_sobrevivencia_na_lava", "resetRound"),
        ("24_campo_minado_neon", "resetRound"),
        ("25_batalha_naval_live", "resetRound"),
    ]
    for g, fn in games_and_fns:
        path = os.path.join(GAMES_DIR, g, "index.html")
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        # Find function definition
        pattern = rf'(function\s+{fn}\s*\([^)]*\)\s*\{{)'
        replacement = r'\1\n      particles.length = 0;'
        if "particles.length = 0" not in code:
            new_code = re.sub(pattern, replacement, code, count=1)
            if new_code != code:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_code)
                print(f"[FIXED PARTICLES] {g}: particles.length = 0 adicionado em {fn}()")
            else:
                print(f"[WARN PARTICLES] {g}: padrão não correspondido")
        else:
            print(f"[INFO PARTICLES] {g}: particles.length = 0 já presente")

def apply_toast_capping():
    games_to_fix = [
        # (game, fn_name, container_var)
        ("01_cabo_de_guerra_neon", "spawnToast", "toastContainer"),
        ("01b_cabo_de_guerra_elementos", "spawnToast", "toastContainer"),
        ("02_plinko_pachinko_fortuna", "spawnToast", "toastContainer"),
        ("03_corrida_avatares_holding", "addToast", "toastFeedEl"),
        ("05_roleta_desafios_live", "addToast", "toastFeedEl"),
        ("06_batalha_dos_baloes", "spawnToast", "toastContainer"),
        ("08_caca_tesouro_coordenadas", "pushActivityFeed", "feed"),
        ("09_tsunami_de_curtidas", "spawnToast", "toastContainer"),
        ("10_queda_dos_blocos", "pushActivityFeed", "feed"),
        ("11_queda_de_braco_titas", "spawnToast", "toastContainer"),
        ("12_pachinko_pinball_neon", "spawnToast", "toastContainer"),
        ("13_cascata_de_moedas", "spawnToast", "toastContainer"),
        ("14_vortex_gravitacional", "spawnToast", "toastContainer"),
        ("15_corrida_maluca_espacial", "addToast", "toastFeedEl"),
        ("16_arrancada_noturna_neon", "addToast", "toastFeedEl"),
        ("17_caca_niquel_neon_777", "addToast", "toastFeedEl"),
        ("18_roleta_russa_baloes", "addToast", "toastFeedEl"),
        ("23_sobrevivencia_na_lava", "pushActivityFeed", "feed"),
        ("24_campo_minado_neon", "pushActivityFeed", "feed"),
        ("25_batalha_naval_live", "pushActivityFeed", "feed"),
    ]

    for g, fn, container in games_to_fix:
        path = os.path.join(GAMES_DIR, g, "index.html")
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        if f"{container}.children.length >= 4" in code or f"{container}.children.length >=" in code:
            print(f"[INFO TOAST] {g}: {container} já possui capping")
            continue

        # Look for function header
        # In pushActivityFeed, `const feed = document.getElementById(...)` comes first
        if fn == "pushActivityFeed":
            pattern = rf'(const\s+{container}\s*=\s*document\.getElementById\([^)]+\);\s*)'
            replacement = rf'\1while ({container} && {container}.children.length >= 4) {{ {container}.removeChild({container}.firstElementChild); }}\n      '
        else:
            pattern = rf'(function\s+{fn}\s*\([^)]*\)\s*\{{\s*)'
            replacement = rf'\1while ({container} && {container}.children.length >= 4) {{ {container}.removeChild({container}.firstElementChild); }}\n      '

        new_code = re.sub(pattern, replacement, code, count=1)
        if new_code != code:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_code)
            print(f"[FIXED TOAST] {g}: limitador de 4 itens simultâneos adicionado a {fn}()")
        else:
            print(f"[WARN TOAST] {g}: padrão não correspondido para {fn}()")

def apply_sdk_fallback_in_26_to_32():
    sdk_games = [
        "26_guerra_dos_tanques_neon",
        "27_meteoro_defensor",
        "28_labirinto_pacman_neon",
        "29_basquete_street_neon",
        "30_gol_de_penalti_live",
        "31_guitar_hero_neon",
        "32_corte_de_frutas_neon"
    ]

    fallback_code = """    // Garantia de Isolamento Autônomo (Fallback In-line caso o script SDK externo não esteja disponível)
    if (typeof window.V5LiveSDK === 'undefined') {
      window.V5LiveSDK = class {
        constructor() {
          this.lastEventTime = Date.now();
          this.callbacks = {};
        }
        on(evt, cb) {
          if (!this.callbacks[evt]) this.callbacks[evt] = [];
          this.callbacks[evt].push(cb);
        }
        emit(evt, data) {
          this.lastEventTime = Date.now();
          if (this.callbacks[evt]) this.callbacks[evt].forEach(cb => cb(data));
        }
      };
    }
"""

    for g in sdk_games:
        path = os.path.join(GAMES_DIR, g, "index.html")
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        if "Fallback In-line caso o script SDK" in code:
            print(f"[INFO SDK] {g}: Fallback já presente")
            continue

        # Insert right before `const sdk = new V5LiveSDK`
        target = "const sdk = new V5LiveSDK"
        if target in code:
            new_code = code.replace(target, fallback_code + "    " + target, 1)
            # Also update handleLiveCommand to update sdk.lastEventTime
            if "sdk.lastEventTime = Date.now();" not in new_code:
                # Add to beginning of handler
                pattern_handler = r'(function\s+(?:handleLiveCommand|handleIncomingCommand|handleGameEvent)\s*\([^)]*\)\s*\{)'
                new_code = re.sub(pattern_handler, r'\1\n      if (typeof sdk !== "undefined" && sdk) sdk.lastEventTime = Date.now();', new_code, count=1)

            with open(path, "w", encoding="utf-8") as f:
                f.write(new_code)
            print(f"[FIXED SDK] {g}: Blindagem de fallback in-line do V5LiveSDK aplicada")
        else:
            print(f"[WARN SDK] {g}: const sdk = new V5LiveSDK não encontrado")

if __name__ == "__main__":
    print("Iniciando aplicação cirúrgica de melhorias de arquitetura e correções de bugs...")
    apply_particle_resets()
    apply_toast_capping()
    apply_sdk_fallback_in_26_to_32()
    print("Concluído!")
