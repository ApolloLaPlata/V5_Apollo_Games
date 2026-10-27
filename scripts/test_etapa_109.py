import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIVE_BUS_PATH = r"C:\Users\v5est\.gemini\antigravity\brain\9270dd65-160e-47e8-aea2-6a92fd50cfc6\antigravity_hive_bus.md"
PLANO_PATH = os.path.join(BASE_DIR, "PLANO_MESTRE_100_ETAPAS.md")
MEMORIA_PATH = os.path.join(BASE_DIR, "MEMORIA_ATIVA_GAMES.md")

def run_tests():
    print("=" * 70)
    print("SUÍTE DE TESTES: ETAPA 109 - ATUALIZAÇÃO DO HIVE BUS & MEMÓRIA")
    print("=" * 70)

    # TEST 1: Check antigravity_hive_bus.md
    assert os.path.isfile(HIVE_BUS_PATH), "antigravity_hive_bus.md não encontrado"
    with open(HIVE_BUS_PATH, "r", encoding="utf-8", errors="replace") as f:
        hive_content = f.read()
    assert "Capitania #04: V5 Games" in hive_content and "Etapa 109 Concluída" in hive_content, "Anúncio da Etapa 109 não encontrado no hive bus"
    print("[TEST 1] Anúncio da Etapa 109 presente no antigravity_hive_bus.md - PASSOU")

    # TEST 2: Check PLANO_MESTRE_100_ETAPAS.md
    with open(PLANO_PATH, "r", encoding="utf-8") as f:
        plano_content = f.read()
    assert "- [x] **Etapa 109:**" in plano_content, "Etapa 109 não está marcada como concluída no Plano Mestre"
    print("[TEST 2] Etapa 109 marcada como [x] no PLANO_MESTRE_100_ETAPAS.md - PASSOU")

    # TEST 3: Check MEMORIA_ATIVA_GAMES.md
    with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
        memoria_content = f.read()
    assert "Etapa 109 Homologada" in memoria_content, "MEMORIA_ATIVA_GAMES.md não reflete homologação da Etapa 109"
    assert "scripts/update_hive_bus_109.py" in memoria_content, "Script da Etapa 109 não registrado na memória ativa"
    print("[TEST 3] MEMORIA_ATIVA_GAMES.md atualizada com Etapa 109 - PASSOU")

    # TEST 4: Integrity of the 41 cartridges in catalogo_jogos
    games_dir = os.path.join(BASE_DIR, "catalogo_jogos")
    cartridges = [d for d in os.listdir(games_dir) if os.path.isdir(os.path.join(games_dir, d)) and not d.startswith('.')]
    assert len(cartridges) == 41, f"Total de cartuchos divergente: esperado 41, encontrado {len(cartridges)}"
    print(f"[TEST 4] Catálogo de 41 cartuchos íntegro no disco - PASSOU")

    print("\n" + "=" * 70)
    print("TODOS OS 4 TESTES DA ETAPA 109 PASSARAM COM SUCESSO ABSOLUTO (100%)!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
