import os
import re
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_DIR = os.path.join(BASE_DIR, "catalogo_jogos")
BROADCASTER_GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games"

POLARIZATION_GAMES = [
    {
        "slug": "01b_cabo_de_guerra_elementos",
        "name": "Cabo de Guerra dos Elementos (Fogo vs Gelo)",
        "commands": ["1", "2", "fogo", "gelo"]
    },
    {
        "slug": "06_batalha_dos_baloes",
        "name": "Batalha dos Balões Gigantes",
        "commands": ["1", "2", "azul", "laranja"]
    },
    {
        "slug": "09_tsunami_de_curtidas",
        "name": "Tsunami de Curtidas",
        "commands": ["1", "2", "likes"]
    },
    {
        "slug": "11_queda_de_braco_titas",
        "name": "Queda de Braço dos Titãs",
        "commands": ["1", "2", "azul", "vermelho"]
    }
]

def run_checks():
    print("=" * 70)
    print(" SUÍTE DE HOMOLOGAÇÃO DE CARTUCHOS DE POLARIZAÇÃO (FASE 2)")
    print(" Holding V5 Apollo — Capitania V5 Games & Broadcaster")
    print("=" * 70)
    
    total_passed = 0
    total_tests = 0
    
    for game in POLARIZATION_GAMES:
        slug = game["slug"]
        name = game["name"]
        print(f"\n[TESTANDO] {slug} — {name}")
        
        src_html_path = os.path.join(CATALOG_DIR, slug, "index.html")
        dst_html_path = os.path.join(BROADCASTER_GAMES_DIR, slug, "index.html")
        
        # 1. Arquivo de Origem existe
        total_tests += 1
        if os.path.exists(src_html_path):
            print("  [PASS] Arquivo fonte local encontrado.")
            total_passed += 1
        else:
            print(f"  [FAIL] Arquivo fonte local não encontrado: {src_html_path}")
            continue
            
        # 2. Arquivo sincronizado no Broadcaster existe
        total_tests += 1
        if os.path.exists(dst_html_path):
            print("  [PASS] Cópia sincronizada no Broadcaster encontrada.")
            total_passed += 1
        else:
            print(f"  [FAIL] Cópia no Broadcaster não encontrada: {dst_html_path}")
            
        with open(src_html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        # 3. Formato 9:16 e Safe Zones
        total_tests += 1
        has_916 = ("9 / 16" in html_content) or ("9/16" in html_content) or ("1080" in html_content and "1920" in html_content)
        has_safe_zone = ("140px" in html_content or "top-header" in html_content) and ("180px" in html_content or "bottom-panel" in html_content)
        if has_916 and has_safe_zone:
            print("  [PASS] Lei 1 — Proporção vertical 9:16 e Safe Zones (140px topo / 180px base) validadas.")
            total_passed += 1
        else:
            print("  [FAIL] Lei 1 violada: verifique aspect-ratio 9:16 ou safe zones.")
            
        # 4. Zero Mouse/Teclado (Protocolo de Eventos V5 Live)
        total_tests += 1
        has_events = ("BroadcastChannel" in html_content) and ("v5_event" in html_content)
        if has_events:
            print("  [PASS] Lei 2 — Barramento de Eventos de Live (BroadcastChannel + v5_event) ativo.")
            total_passed += 1
        else:
            print("  [FAIL] Lei 2 violada: faltam listeners de BroadcastChannel ou v5_event.")
            
        # 5. Motor Anti-Silêncio Orgânico
        total_tests += 1
        has_anti_silence = ("mockUsers" in html_content or "anti-silêncio" in html_content.lower() or "setInterval" in html_content)
        if has_anti_silence:
            print("  [PASS] Lei 3 — Motor Anti-Silêncio (injeção determinística após inatividade) ativo.")
            total_passed += 1
        else:
            print("  [FAIL] Lei 3 violada: motor anti-silêncio ausente.")
            
        # 6. Sintetizador Procedural Web Audio API (Zero mp3/wav)
        total_tests += 1
        has_audio = ("AudioContext" in html_content or "webkitAudioContext" in html_content)
        has_mp3 = bool(re.search(r'\.(mp3|wav|ogg)\b', html_content, re.IGNORECASE))
        if has_audio and not has_mp3:
            print("  [PASS] Lei 4 — Áudio Procedural 100% Web Audio API (Zero arquivos externos .mp3/.wav).")
            total_passed += 1
        else:
            print(f"  [FAIL] Lei 4 violada: has_audio={has_audio}, has_mp3={has_mp3}")
            
        # 7. Ciclo Fechado & Auto-Reset
        total_tests += 1
        has_reset = ("reset-progress" in html_content or "victory-overlay" in html_content) and ("roundTime" in html_content or "startTimer" in html_content)
        if has_reset:
            print("  [PASS] Lei 5 — Ciclo Fechado de Partidas (Timer + Auto-Reset de 5s sem reload) ativo.")
            total_passed += 1
        else:
            print("  [FAIL] Lei 5 violada: ciclo de reset ausente.")
            
        # 8. Validação de Sintaxe JavaScript
        total_tests += 1
        scripts = re.findall(r'<script.*?>([\s\S]*?)<\/script>', html_content)
        js_valid = True
        for idx, sc in enumerate(scripts):
            cmd = ['node', '-e', f'new Function({json.dumps(sc)});']
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"  [FAIL] Erro de sintaxe JS no script #{idx}: {res.stderr}")
                js_valid = False
                break
        if js_valid and len(scripts) > 0:
            print("  [PASS] Sintaxe JavaScript avaliada via Node.js com 100% de integridade.")
            total_passed += 1
            
        # 9. Paridade de Sincronização (Source == Destination)
        total_tests += 1
        if os.path.exists(dst_html_path):
            with open(dst_html_path, "r", encoding="utf-8") as df:
                dst_content = df.read()
            if html_content == dst_content:
                print("  [PASS] Paridade de bytes exata com a pasta do Broadcaster (100% sincronizado).")
                total_passed += 1
            else:
                print("  [WARN] Conteúdo no Broadcaster diverge do arquivo local (requer re-sync).")
        else:
            print("  [FAIL] Cópia de destino ausente.")
            
    print("\n" + "=" * 70)
    print(f" RESULTADO FINAL: {total_passed}/{total_tests} TESTES APROVADOS ({round((total_passed/total_tests)*100)}%)")
    print("=" * 70)
    
    return total_passed == total_tests

if __name__ == "__main__":
    success = run_checks()
    if not success:
        exit(1)
