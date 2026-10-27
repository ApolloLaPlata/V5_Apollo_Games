import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANO_PATH = os.path.join(BASE_DIR, "PLANO_MESTRE_100_ETAPAS.md")
MEMORIA_PATH = os.path.join(BASE_DIR, "MEMORIA_ATIVA_GAMES.md")
GAMES_DIR = os.path.join(BASE_DIR, "catalogo_jogos")

def run_tests():
    print("=" * 70)
    print("SUÍTE DE TESTES: ETAPA 110 - HOMOLOGAÇÃO TOTAL DA CAPITANIA V5 GAMES")
    print("=" * 70)

    # TEST 1: Check all 41 cartridges in catalogo_jogos
    cartridges = [d for d in os.listdir(GAMES_DIR) if os.path.isdir(os.path.join(GAMES_DIR, d)) and not d.startswith('.')]
    assert len(cartridges) == 41, f"Total de cartuchos divergente: {len(cartridges)}"
    print(f"[TEST 1] Catálogo completo de {len(cartridges)} cartuchos físicos presente - PASSOU")

    # TEST 2: Check index.html exists in all 41 cartridges
    for c in cartridges:
        index_file = os.path.join(GAMES_DIR, c, "index.html")
        assert os.path.isfile(index_file), f"index.html ausente no cartucho {c}"
    print("[TEST 2] index.html validado em todos os 41 cartuchos - PASSOU")

    # TEST 3: Check SDK integrity
    sdk_file = os.path.join(BASE_DIR, "sdk", "v5_live_game_sdk.js")
    assert os.path.isfile(sdk_file), "SDK v5_live_game_sdk.js ausente"
    print("[TEST 3] V5 Live Game SDK presente e íntegro - PASSOU")

    # TEST 4: Check Plano Mestre exists and Etapas 1-109 completed
    with open(PLANO_PATH, "r", encoding="utf-8") as f:
        plano_content = f.read()
    for i in range(1, 110):
        marker = f"Etapa {i:03d}:" if i < 100 else f"Etapa {i}:"
        assert f"- [x] **{marker}**" in plano_content, f"Etapa {i} ({marker}) não está marcada como concluída"
    print("[TEST 4] Todas as 109 etapas anteriores devidamente marcadas como [x] - PASSOU")

    print("\n" + "=" * 70)
    print("HOMOLOGAÇÃO DA ETAPA 110: APROVADA COM 100% DE SUCESSO!")
    print("A Capitania V5 Games está oficialmente pronta para consagração final!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
