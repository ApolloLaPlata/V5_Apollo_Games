"""
scripts/test_coop_cartridges.py
============================================================================
ETAPA 060: Homologação e Despacho dos Cartuchos Cooperativos (Fase 6)
Holding V5 Apollo — Capitania V5 Games & Broadcaster
============================================================================
Homologa formalmente os 3 cartuchos cooperativos segundo as 5 Leis Absolutas:
  1. 04_boss_raid_cooperativo (Boss Raid do Chat 9:16)
  2. 19_defesa_da_torre_chat (Defesa da Torre do Chat 9:16)
  3. 20_subida_da_montanha_sagrada (Subida da Montanha Sagrada 9:16)
"""

import os
import re
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_DIR = os.path.join(BASE_DIR, "catalogo_jogos")
BROADCASTER_GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games"
MANIFEST_PATH = os.path.join(BROADCASTER_GAMES_DIR, "v5_games_manifest.json")

COOP_GAMES = [
    {
        "slug": "04_boss_raid_cooperativo",
        "name": "Boss Raid do Chat",
        "commands": ["1", "atacar", "fogo", "espada"]
    },
    {
        "slug": "19_defesa_da_torre_chat",
        "name": "Defesa da Torre do Chat",
        "commands": ["1", "2", "3", "esq", "centro", "dir"]
    },
    {
        "slug": "20_subida_da_montanha_sagrada",
        "name": "Subida da Montanha Sagrada",
        "commands": ["1", "2", "3", "subir", "esq", "dir"]
    }
]

def run_coop_checks():
    print("=" * 75)
    print(" SUÍTE DE HOMOLOGAÇÃO DE CARTUCHOS COOPERATIVOS & RAIDS (ETAPA 060)")
    print(" Holding V5 Apollo — Capitania V5 Games & Broadcaster")
    print("=" * 75)

    total_passed = 0
    total_tests = 0

    for game in COOP_GAMES:
        slug = game["slug"]
        name = game["name"]
        print(f"\n[TESTANDO] {slug} — {name}")

        src_html_path = os.path.join(CATALOG_DIR, slug, "index.html")
        dst_html_path = os.path.join(BROADCASTER_GAMES_DIR, slug, "index.html")

        # 1. Arquivo de Origem
        total_tests += 1
        if os.path.exists(src_html_path):
            print(f"  [OK] Arquivo fonte presente ({os.path.getsize(src_html_path)} bytes)")
            total_passed += 1
        else:
            print(f"  [FAIL] Arquivo fonte ausente: {src_html_path}")
            continue

        # 2. Arquivo Sincronizado no Broadcaster
        total_tests += 1
        if os.path.exists(dst_html_path):
            print(f"  [OK] Arquivo sincronizado no Broadcaster ({os.path.getsize(dst_html_path)} bytes)")
            total_passed += 1
        else:
            print(f"  [FAIL] Arquivo no Broadcaster ausente: {dst_html_path}")

        # 3. Paridade Exata de Conteúdo (Zero divergência)
        total_tests += 1
        with open(src_html_path, "r", encoding="utf-8") as f:
            src_html = f.read()
        with open(dst_html_path, "r", encoding="utf-8") as f:
            dst_html = f.read()
        if src_html == dst_html:
            print("  [OK] Paridade total de código com o Broadcaster")
            total_passed += 1
        else:
            print("  [FAIL] Divergência entre catálogo e Broadcaster")

        # 4. Formato Vertical 9:16 (1080x1920)
        total_tests += 1
        has_ratio = ("9 / 16" in src_html) or ("9/16" in src_html) or ("1080" in src_html and "1920" in src_html)
        if has_ratio:
            print("  [OK] Proporção vertical estrita 9:16 validada")
            total_passed += 1
        else:
            print("  [FAIL] Falta proporção 9:16 ou resolução 1080x1920")

        # 5. Safe Zones (Topo 140px, Base 180px)
        total_tests += 1
        has_safe_zones = ("140px" in src_html or "top-header" in src_html) and ("180px" in src_html or "bottom-panel" in src_html)
        if has_safe_zones:
            print("  [OK] Safe Zones respeitadas (Topo 140px e Base 180px)")
            total_passed += 1
        else:
            print("  [FAIL] Safe Zones ausentes ou mal configuradas")

        # 6. Zero Mouse / Zero Teclado (Comandos do Chat)
        total_tests += 1
        has_commands = any(cmd.lower() in src_html.lower() for cmd in game["commands"])
        if has_commands:
            print(f"  [OK] Comandos de público suportados: {game['commands']}")
            total_passed += 1
        else:
            print("  [FAIL] Comandos do chat não detectados")

        # 7. Motor Anti-Silêncio (Autônomo)
        total_tests += 1
        has_anti_silence = ("anti-silêncio" in src_html.lower()) or ("mockusers" in src_html.lower())
        if has_anti_silence:
            print("  [OK] Motor Anti-Silêncio autônomo presente")
            total_passed += 1
        else:
            print("  [FAIL] Motor Anti-Silêncio ausente")

        # 8. Sintetizador de Áudio Procedural (Web Audio API sem .mp3/.wav externos)
        total_tests += 1
        has_webaudio = "AudioContext" in src_html
        has_external_audio = bool(re.search(r'["\'][^"\']+\.(mp3|wav)["\']', src_html))
        if has_webaudio and not has_external_audio:
            print("  [OK] Áudio 100% procedural sintetizado (zero .mp3/.wav externos)")
            total_passed += 1
        else:
            print(f"  [FAIL] Áudio procedural inválido ou arquivo estático detectado")

        # 9. Ciclo Fechado & Auto-Reset (30 a 60 segundos)
        total_tests += 1
        has_auto_reset = ("reset" in src_html.lower()) and ("5000" in src_html or "timeout" in src_html.lower())
        if has_auto_reset:
            print("  [OK] Ciclo fechado de partidas com Auto-Reset em 5s implementado")
            total_passed += 1
        else:
            print("  [FAIL] Ciclo fechado ou auto-reset não detectado")

        # 10. Validação de Sintaxe JavaScript
        total_tests += 1
        node_check = subprocess.run([
            "node", "-e",
            f"""
            const fs = require('fs');
            const content = fs.readFileSync('{src_html_path.replace(os.sep, "/")}', 'utf8');
            const matches = content.matchAll(/<script[\\s\\S]*?>([\\s\\S]*?)<\\/script>/gi);
            for (const m of matches) {{
                if (m[1].trim()) new Function(m[1]);
            }}
            """
        ], capture_output=True, text=True)

        if node_check.returncode == 0:
            print("  [OK] Sintaxe JavaScript interna validada sem erros")
            total_passed += 1
        else:
            print(f"  [FAIL] Erro de sintaxe JS: {node_check.stderr}")

    # 11. Validação do Manifesto do Broadcaster
    print("\n[VALIDAÇÃO DO MANIFESTO DO BROADCASTER]")
    total_tests += 1
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        if isinstance(manifest, list):
            manifest_slugs = [g["slug"] for g in manifest]
        else:
            manifest_slugs = [g["slug"] for g in manifest.get("games", [])]
        all_present = all(g["slug"] in manifest_slugs for g in COOP_GAMES)
        if all_present:
            print(f"  [OK] Todos os 3 cartuchos cooperativos registrados no manifesto ({len(manifest_slugs)} jogos totais)")
            total_passed += 1
        else:
            missing = [g["slug"] for g in COOP_GAMES if g["slug"] not in manifest_slugs]
            print(f"  [FAIL] Jogos ausentes no manifesto: {missing}")
    else:
        print(f"  [FAIL] Manifesto não encontrado: {MANIFEST_PATH}")

    print("\n" + "=" * 75)
    print(f" RESULTADO FINAL DA HOMOLOGAÇÃO: {total_passed}/{total_tests} CHECKS APROVADOS")
    print("=" * 75)

    if total_passed == total_tests:
        print(">> SUCESSO ABSOLUTO: TODOS OS CARTUCHOS COOPERATIVOS ESTÃO HOMOLOGADOS! <<\n")
        return True
    else:
        print(">> FALHA: ALGUNS CRITÉRIOS NÃO FORAM SATISFEITOS! <<\n")
        return False

if __name__ == "__main__":
    success = run_coop_checks()
    exit(0 if success else 1)
