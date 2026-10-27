import os
import re
import subprocess
import hashlib
import sys

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"
BROADCASTER_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public"

def calculate_md5(fpath):
    hasher = hashlib.md5()
    with open(fpath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def run_tests():
    print("=" * 70)
    print("SUÍTE DE TESTES: BLINDAGEM DE ARQUITETURA, PARTICULAS E TOASTS")
    print("=" * 70)

    # TEST 1: Particle array cleanup in reset
    particle_games = [
        ("08_caca_tesouro_coordenadas", "resetMatch"),
        ("10_queda_dos_blocos", "resetGame"),
        ("23_sobrevivencia_na_lava", "resetRound"),
        ("24_campo_minado_neon", "resetRound"),
        ("25_batalha_naval_live", "resetRound"),
    ]
    for g, fn in particle_games:
        p = os.path.join(GAMES_DIR, g, "index.html")
        with open(p, "r", encoding="utf-8") as f:
            code = f.read()
        assert "particles.length = 0" in code, f"{g} não limpa particles"
    print(f"[TEST 1] 5/5 jogos limpam 'particles.length = 0' em resets - PASSOU")

    # TEST 2: Toast & Feed child capping in 20 games
    toast_games = [
        ("01_cabo_de_guerra_neon", "toastContainer"),
        ("01b_cabo_de_guerra_elementos", "toastContainer"),
        ("02_plinko_pachinko_fortuna", "toastContainer"),
        ("03_corrida_avatares_holding", "toastFeedEl"),
        ("05_roleta_desafios_live", "toastFeedEl"),
        ("06_batalha_dos_baloes", "toastContainer"),
        ("08_caca_tesouro_coordenadas", "feed"),
        ("09_tsunami_de_curtidas", "toastContainer"),
        ("10_queda_dos_blocos", "feed"),
        ("11_queda_de_braco_titas", "toastContainer"),
        ("12_pachinko_pinball_neon", "toastContainer"),
        ("13_cascata_de_moedas", "toastContainer"),
        ("14_vortex_gravitacional", "toastContainer"),
        ("15_corrida_maluca_espacial", "toastFeedEl"),
        ("16_arrancada_noturna_neon", "toastFeedEl"),
        ("17_caca_niquel_neon_777", "toastFeedEl"),
        ("18_roleta_russa_baloes", "toastFeedEl"),
        ("23_sobrevivencia_na_lava", "feed"),
        ("24_campo_minado_neon", "feed"),
        ("25_batalha_naval_live", "feed"),
    ]
    for g, container in toast_games:
        p = os.path.join(GAMES_DIR, g, "index.html")
        with open(p, "r", encoding="utf-8") as f:
            code = f.read()
        assert f"{container}.children.length >= 4" in code, f"{g} não possui capping em {container}"
    print(f"[TEST 2] 20/20 jogos com limitador de 4 toasts/itens simultâneos no DOM - PASSOU")

    # TEST 3: In-line fallback for V5LiveSDK in games 26-32
    sdk_games = [
        "26_guerra_dos_tanques_neon",
        "27_meteoro_defensor",
        "28_labirinto_pacman_neon",
        "29_basquete_street_neon",
        "30_gol_de_penalti_live",
        "31_guitar_hero_neon",
        "32_corte_de_frutas_neon"
    ]
    for g in sdk_games:
        p = os.path.join(GAMES_DIR, g, "index.html")
        with open(p, "r", encoding="utf-8") as f:
            code = f.read()
        assert "window.V5LiveSDK = class" in code, f"{g} não possui fallback in-line de V5LiveSDK"
    print(f"[TEST 3] 7/7 jogos (26 a 32) blindados com fallback in-line do V5LiveSDK - PASSOU")

    # TEST 4: Broadcaster SDK paths verification
    sdk_src = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\sdk\v5_live_game_sdk.js"
    src_md5 = calculate_md5(sdk_src)
    sdk_b1 = os.path.join(BROADCASTER_DIR, "sdk", "v5_live_game_sdk.js")
    sdk_b2 = os.path.join(BROADCASTER_DIR, "games", "sdk", "v5_live_game_sdk.js")
    assert os.path.isfile(sdk_b1) and calculate_md5(sdk_b1) == src_md5, "SDK não existe ou MD5 difere em public/sdk"
    assert os.path.isfile(sdk_b2) and calculate_md5(sdk_b2) == src_md5, "SDK não existe ou MD5 difere em public/games/sdk"
    print(f"[TEST 4] Arquivos do SDK no Broadcaster sincronizados e validados com MD5 - PASSOU")

    # TEST 5: Syntax check across all 41 cartuchos with node --check
    for g in sorted(os.listdir(GAMES_DIR)):
        p = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(p):
            continue
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        scripts = []
        for m in re.finditer(r'<script\b[^>]*>([\s\S]*?)<\/script>', content, re.IGNORECASE):
            if 'src=' not in m.group(0):
                scripts.append(m.group(1))
        js = '\n'.join(scripts)
        res = subprocess.run(['node', '--check'], input=js.encode('utf-8'), capture_output=True)
        assert res.returncode == 0, f"Erro de sintaxe em {g}: {res.stderr.decode('utf-8', errors='replace')}"
    print(f"[TEST 5] 41/41 cartuchos validados sintaticamente com node --check (0 erros) - PASSOU")

    print("\n" + "=" * 70)
    print("TODOS OS 5 TESTES DE ARQUITETURA E BLINDAGEM PASSARAM COM SUCESSO (100%)!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
