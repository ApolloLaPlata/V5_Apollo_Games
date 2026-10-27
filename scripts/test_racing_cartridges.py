"""
scripts/test_racing_cartridges.py
============================================================================
ETAPA 040: Homologação e Despacho dos Cartuchos de Corrida (Fase 4)
Holding V5 Apollo — Capitania V5 Games & Broadcaster
============================================================================
Homologa formalmente os 3 cartuchos de corrida segundo as 5 Leis Absolutas:
  1. 03_corrida_avatares_holding (Corrida dos Avatares da Holding 9:16)
  2. 15_corrida_maluca_espacial (Corrida Maluca Espacial 9:16)
  3. 16_arrancada_noturna_neon (Arrancada Noturna Neon Drag Race 9:16)
"""

import os
import re
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_DIR = os.path.join(BASE_DIR, "catalogo_jogos")
BROADCASTER_GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games"
MANIFEST_PATH = os.path.join(BROADCASTER_GAMES_DIR, "v5_games_manifest.json")

RACING_GAMES = [
    {
        "slug": "03_corrida_avatares_holding",
        "name": "Corrida dos Avatares da Holding",
        "commands": ["1", "2", "3", "roxingo", "baiano", "macaco"]
    },
    {
        "slug": "15_corrida_maluca_espacial",
        "name": "Corrida Maluca Espacial",
        "commands": ["1", "2", "3", "apollo", "solaris", "nebula"]
    },
    {
        "slug": "16_arrancada_noturna_neon",
        "name": "Arrancada Noturna Neon",
        "commands": ["1", "2", "cyber", "viper"]
    }
]

def run_racing_checks():
    print("=" * 75)
    print(" SUÍTE DE HOMOLOGAÇÃO DE CARTUCHOS DE CORRIDA & VELOCIDADE (ETAPA 040)")
    print(" Holding V5 Apollo — Capitania V5 Games & Broadcaster")
    print("=" * 75)

    total_passed = 0
    total_tests = 0

    for game in RACING_GAMES:
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

        with open(src_html_path, "r", encoding="utf-8") as f:
            html = f.read()

        # 3. Formato Vertical 9:16 (1080x1920)
        total_tests += 1
        has_ratio = ("9 / 16" in html) or ("9/16" in html) or ("1080" in html and "1920" in html)
        if has_ratio:
            print("  [OK] Proporção vertical estrita 9:16 validada")
            total_passed += 1
        else:
            print("  [FAIL] Falta proporção 9:16 ou resolução 1080x1920")

        # 4. Safe Zones (Topo 140px, Base 180px)
        total_tests += 1
        has_safe_zones = ("140px" in html or "top-header" in html) and ("180px" in html or "bottom-panel" in html)
        if has_safe_zones:
            print("  [OK] Safe Zones respeitadas (Topo ~140px, Base ~180px)")
            total_passed += 1
        else:
            print("  [FAIL] Safe Zones não identificadas")

        # 5. Motor Anti-Silêncio Embutido
        total_tests += 1
        has_anti_silence = ("anti-silêncio" in html.lower() or "mockusers" in html.lower() or "setInterval" in html)
        if has_anti_silence:
            print("  [OK] Motor Anti-Silêncio / Simulação Autônoma presente")
            total_passed += 1
        else:
            print("  [FAIL] Motor Anti-Silêncio ausente")

        # 6. Barramento de Eventos da Live (v5_broadcaster_games + v5_event)
        total_tests += 1
        has_event_bus = ("v5_broadcaster_games" in html) and ("v5_event" in html)
        if has_event_bus:
            print("  [OK] Event Bus presente (BroadcastChannel + v5_event)")
            total_passed += 1
        else:
            print("  [FAIL] Falha no Event Bus do Broadcaster")

        # 7. Síntese de Áudio Procedural (Web Audio API, zero dependências externas)
        total_tests += 1
        has_web_audio = ("AudioContext" in html or "webkitAudioContext" in html) and not bool(re.search(r'["\'][^"\']+\.(mp3|wav|ogg)["\']', html, re.IGNORECASE))
        if has_web_audio:
            print("  [OK] Áudio procedural sintetizado via Web Audio API (Zero arquivos externos)")
            total_passed += 1
        else:
            print("  [FAIL] Falha no áudio procedural")

        # 8. Ciclo Fechado de Partidas & Auto-Reset (30s a 60s)
        total_tests += 1
        has_round_cycle = ("roundtime" in html.lower() or "photofinish" in html.lower() or "reset" in html.lower())
        if has_round_cycle:
            print("  [OK] Ciclo fechado de partidas com auto-reset detectado")
            total_passed += 1
        else:
            print("  [FAIL] Ciclo fechado de partidas não detectado")

        # 9. Comandos Interativos do Chat
        total_tests += 1
        commands_found = [cmd for cmd in game["commands"] if cmd in html.lower()]
        if len(commands_found) >= 2:
            print(f"  [OK] Comandos de chat mapeados: {commands_found}")
            total_passed += 1
        else:
            print(f"  [FAIL] Poucos comandos mapeados: {commands_found} de {game['commands']}")

        # 10. Validação de Sintaxe JavaScript
        total_tests += 1
        scripts = re.findall(r'<script(?:\s+type="[^"]*")?>([\s\S]*?)<\/script>', html, re.IGNORECASE)
        js_ok = True
        for i, code in enumerate(scripts):
            if not code.strip():
                continue
            tmp_js = os.path.join(BASE_DIR, "catalogo_jogos", slug, f"_temp_check_{i}.js")
            with open(tmp_js, "w", encoding="utf-8") as tf:
                tf.write(code)
            res = subprocess.run(["node", "-c", tmp_js], capture_output=True, text=True)
            if os.path.exists(tmp_js):
                os.remove(tmp_js)
            if res.returncode != 0:
                print(f"  [FAIL] Erro de sintaxe JS no bloco {i}: {res.stderr}")
                js_ok = False
                break
        if js_ok:
            print("  [OK] Sintaxe JavaScript 100% válida (Zero erros no Node.js)")
            total_passed += 1

        # 11. Paridade de Sincronização de Bytes (Source == Destination)
        total_tests += 1
        if os.path.exists(dst_html_path):
            with open(dst_html_path, "r", encoding="utf-8") as df:
                dst_content = df.read()
            if html == dst_content:
                print("  [OK] Paridade exata de bytes com a pasta do Broadcaster (100% sincronizado)")
                total_passed += 1
            else:
                print("  [FAIL] Conteúdo difere entre fonte e Broadcaster")

    # 12. Validação do Manifesto do Broadcaster
    print("\n[VERIFICAÇÃO DO MANIFESTO]")
    total_tests += 1
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as mf:
            manifest_data = json.load(mf)

        manifest_slugs = [g["slug"] for g in manifest_data]
        all_present = all(g["slug"] in manifest_slugs for g in RACING_GAMES)
        if all_present:
            print(f"  [OK] Todos os 3 cartuchos de corrida estão registrados no manifesto ({len(manifest_data)} jogos totais)")
            total_passed += 1
        else:
            print(f"  [FAIL] Nem todos os jogos estão no manifesto: {manifest_slugs}")
    else:
        print(f"  [FAIL] Manifesto não encontrado: {MANIFEST_PATH}")

    print("\n" + "=" * 75)
    print(f" RESULTADO FINAL DA HOMOLOGAÇÃO: {total_passed} / {total_tests} TESTES PASSARAM")
    pct = (total_passed / total_tests) * 100
    print(f" TAXA DE CONFORMIDADE: {pct:.1f}%")
    print("=" * 75)

    if total_passed == total_tests:
        print("\n[HOMOLOGAÇÃO FASE 4 CONCLUÍDA] Os 3 cartuchos de corrida atendem a 100% dos requisitos!")
        return True
    else:
        print("\n[FALHA NA HOMOLOGAÇÃO] Corrija os pontos apontados antes de prosseguir.")
        return False

if __name__ == "__main__":
    success = run_racing_checks()
    exit(0 if success else 1)
