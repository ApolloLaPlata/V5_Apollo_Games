"""
scripts/test_elimination_cartridges.py
============================================================================
ETAPA 070: Homologação e Envio dos Cartuchos de Eliminação (Fase 7)
Holding V5 Apollo — Capitania V5 Games & Broadcaster
============================================================================
Homologa formalmente os 4 cartuchos de eliminação e tensão segundo as 5 Leis Absolutas:
  1. 07_pendulo_destruidor (Pêndulo Demolidor 9:16)
  2. 21_batata_quente_explosiva (Batata Quente Explosiva 9:16)
  3. 22_ponte_de_vidro_quebradico (Ponte de Vidro Quebradiço 9:16)
  4. 23_sobrevivencia_na_lava (Sobrevivência na Lava 9:16)
"""

import os
import re
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_DIR = os.path.join(BASE_DIR, "catalogo_jogos")
BROADCASTER_GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games"
MANIFEST_PATH = os.path.join(BROADCASTER_GAMES_DIR, "v5_games_manifest.json")

ELIMINATION_GAMES = [
    {
        "slug": "07_pendulo_destruidor",
        "name": "Pêndulo Demolidor",
        "commands": ["1", "2", "3"]
    },
    {
        "slug": "21_batata_quente_explosiva",
        "name": "Batata Quente Explosiva",
        "commands": ["1", "2", "3", "passar"]
    },
    {
        "slug": "22_ponte_de_vidro_quebradico",
        "name": "Ponte de Vidro Quebradiço",
        "commands": ["1", "2", "esq", "dir"]
    },
    {
        "slug": "23_sobrevivencia_na_lava",
        "name": "Sobrevivência na Lava",
        "commands": ["1", "2", "3", "4", "ciano", "roxo", "ouro", "verde"]
    }
]

def run_elimination_checks():
    print("=" * 75)
    print(" SUÍTE DE HOMOLOGAÇÃO DE CARTUCHOS DE ELIMINAÇÃO & TENSÃO (ETAPA 070)")
    print(" Holding V5 Apollo — Capitania V5 Games & Broadcaster")
    print("=" * 75)

    total_passed = 0
    total_tests = 0

    for game in ELIMINATION_GAMES:
        slug = game["slug"]
        name = game["name"]
        print(f"\n[TESTANDO] {slug} — {name}")

        src_html_path = os.path.join(CATALOG_DIR, slug, "index.html")
        dst_html_path = os.path.join(BROADCASTER_GAMES_DIR, slug, "index.html")

        # 1. Arquivo de Origem
        total_tests += 1
        if os.path.exists(src_html_path):
            print(f"  [PASS] Arquivo fonte existe ({src_html_path})")
            total_passed += 1
        else:
            print(f"  [FAIL] Arquivo fonte NÃO encontrado ({src_html_path})")

        # 2. Arquivo de Destino no Broadcaster
        total_tests += 1
        if os.path.exists(dst_html_path):
            print(f"  [PASS] Arquivo destino existe no Broadcaster ({dst_html_path})")
            total_passed += 1
        else:
            print(f"  [FAIL] Arquivo destino NÃO encontrado no Broadcaster ({dst_html_path})")

        # 3. Paridade de Conteúdo
        total_tests += 1
        with open(src_html_path, "r", encoding="utf-8") as f:
            src_content = f.read()

        if os.path.exists(dst_html_path):
            with open(dst_html_path, "r", encoding="utf-8") as f:
                dst_content = f.read()
            if src_content == dst_content:
                print(f"  [PASS] Paridade de bytes perfeita (100% idêntico)")
                total_passed += 1
            else:
                print(f"  [FAIL] Conteúdo do Broadcaster difere da fonte!")
        else:
            print(f"  [FAIL] Impossível comparar paridade (arquivo destino ausente)")

        # 4. Lei 1: Formato 9:16 e Safe Zones
        total_tests += 1
        has_aspect_ratio = ("9 / 16" in src_content) or ("9/16" in src_content)
        has_safe_top = ("140px" in src_content) or ("top-header" in src_content)
        has_safe_bottom = ("180px" in src_content) or ("bottom-panel" in src_content)
        if has_aspect_ratio and (has_safe_top or has_safe_bottom):
            print(f"  [PASS] Lei 1: Formato 9:16 com Safe Zones Topo/Base")
            total_passed += 1
        else:
            print(f"  [FAIL] Lei 1 Violada: aspecto ou safe zones ausentes")

        # 5. Lei 2: Zero Teclado / Zero Mouse (Controle pelo Chat e Event Bus)
        total_tests += 1
        has_event_bus = ("v5_broadcaster_games" in src_content) and ("v5_event" in src_content)
        has_commands = any(cmd in src_content.lower() for cmd in game["commands"])
        if has_event_bus and has_commands:
            print(f"  [PASS] Lei 2: Event Bus V5 Broadcaster & Comandos de Chat ({game['commands']})")
            total_passed += 1
        else:
            print(f"  [FAIL] Lei 2 Violada: Event Bus ou comandos ausentes")

        # 6. Lei 3: Motor Anti-Silêncio Orgânico
        total_tests += 1
        has_anti_silence = ("anti-silêncio" in src_content.lower()) or ("mockusers" in src_content.lower()) or ("simula" in src_content.lower())
        if has_anti_silence:
            print(f"  [PASS] Lei 3: Motor Anti-Silêncio Orgânico embutido")
            total_passed += 1
        else:
            print(f"  [FAIL] Lei 3 Violada: Anti-silêncio ausente")

        # 7. Lei 4: Síntese de Áudio Procedural (Web Audio API)
        total_tests += 1
        has_audio_ctx = "AudioContext" in src_content
        has_no_audio_files = not bool(re.search(r'["\'][^"\']+\.(mp3|wav)["\']', src_content))
        if has_audio_ctx and has_no_audio_files:
            print(f"  [PASS] Lei 4: Web Audio API procedural pura (Zero .mp3/.wav)")
            total_passed += 1
        else:
            print(f"  [FAIL] Lei 4 Violada: áudio procedural ausente ou dependência de arquivos externos")

        # 8. Lei 5: Ciclo Fechado & Auto-Reset
        total_tests += 1
        has_reset = ("reset" in src_content.lower()) and ("5000" in src_content or "resetround" in src_content.lower() or "resetgame" in src_content.lower())
        if has_reset:
            print(f"  [PASS] Lei 5: Ciclo Fechado com Auto-Reset automático")
            total_passed += 1
        else:
            print(f"  [FAIL] Lei 5 Violada: auto-reset não detectado")

    # 9. Verificação do Manifesto do Broadcaster
    print("\n[VERIFICANDO] Manifesto Central do Broadcaster")
    total_tests += 1
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        manifest_slugs = [g["slug"] for g in manifest] if isinstance(manifest, list) else [g["slug"] for g in manifest.get("games", [])]
        all_present = all(g["slug"] in manifest_slugs for g in ELIMINATION_GAMES)

        if all_present:
            print(f"  [PASS] Todos os 4 cartuchos de eliminação estão devidamente catalogados no manifesto!")
            total_passed += 1
        else:
            missing = [g["slug"] for g in ELIMINATION_GAMES if g["slug"] not in manifest_slugs]
            print(f"  [FAIL] Jogos faltando no manifesto: {missing}")
    else:
        print(f"  [FAIL] Arquivo de manifesto não encontrado: {MANIFEST_PATH}")

    print("\n" + "=" * 75)
    print(f" RESULTADO FINAL: {total_passed}/{total_tests} CHECKS APROVADOS")
    print("=" * 75)

    if total_passed == total_tests:
        print("HOMOLOGAÇÃO DA FASE 7 CONCLUÍDA COM 100% DE SUCESSO!")
        return 0
    else:
        print("HOMOLOGAÇÃO FALHOU EM UM OU MAIS ITENS!")
        return 1

if __name__ == "__main__":
    exit(run_elimination_checks())
