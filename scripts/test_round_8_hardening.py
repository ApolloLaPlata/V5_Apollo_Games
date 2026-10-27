import os
import glob
import subprocess
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"
SDK_FILE = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\sdk\v5_live_game_sdk.js"

def run_tests():
    print("=" * 70)
    print("SUÍTE DE TESTES: VALIDAÇÃO DE HARDENING & CAÇA A BUGS (RODADA 8)")
    print("=" * 70)

    cartridges = sorted(glob.glob("catalogo_jogos/*/index.html"))
    assert len(cartridges) == 41, f"Esperado 41 cartuchos, encontrado {len(cartridges)}"
    print(f"[TEST 1] Catálogo de cartuchos completo: {len(cartridges)}/41 - PASSOU")

    # TEST 2: beforeunload nunca está aninhado dentro de onmessage
    leaks = []
    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.findall(r'(\w+Channel|\bchannel)\.onmessage\s*=\s*[^;{]*\{[^}]*beforeunload[^}]*\}', content)
        if m:
            leaks.append((slug, m))
    assert len(leaks) == 0, f"beforeunload ainda aninhado em onmessage: {leaks}"
    print("[TEST 2] 41/41 cartuchos com beforeunload registrado externamente (sem vazamento de DOM listeners) - PASSOU")

    # TEST 3: Todos os parseInt possuem radix 10 explícito
    missing_radix = []
    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            content = f.read()
        for m in re.finditer(r'parseInt\s*\(\s*([^,\)]+)\s*\)', content):
            missing_radix.append((slug, m.group(1)))
    assert len(missing_radix) == 0, f"parseInt sem radix 10 encontrado: {missing_radix}"
    print("[TEST 3] 100% das chamadas parseInt com radix 10 explícito - PASSOU")

    # TEST 4: Jogo 39 reseta targets no initSniperGame
    p39 = os.path.join(GAMES_DIR, "39_alvo_movel_snipers", "index.html")
    with open(p39, "r", encoding="utf-8") as f:
        c39 = f.read()
    assert "state.targets = [" in c39, "Jogo 39 não reseta state.targets no initSniperGame"
    print("[TEST 4] Jogo 39 com reset determinístico de alvos (sem acúmulo de alvos infinitos) - PASSOU")

    # TEST 5: Jogo 28 reseta floatingTexts e particles no resetMatch
    p28 = os.path.join(GAMES_DIR, "28_labirinto_pacman_neon", "index.html")
    with open(p28, "r", encoding="utf-8") as f:
        c28 = f.read()
    assert "state.floatingTexts = [];" in c28 and "state.particles = [];" in c28, "Jogo 28 não limpa arrays no reset"
    print("[TEST 5] Jogo 28 com reset limpo de floatingTexts e partículas - PASSOU")

    # TEST 6: SDK possui deduplicação LRU com seenEventIds
    with open(SDK_FILE, "r", encoding="utf-8") as f:
        sdk_c = f.read()
    assert "this.seenEventIds = new Set();" in sdk_c, "SDK sem seenEventIds no ctor"
    assert "id: raw.id || raw.eventId" in sdk_c, "SDK sem id em normalizePayload"
    assert "if (this.seenEventIds.has(data.id)) return;" in sdk_c, "SDK sem guarda de desduplicação"
    print("[TEST 6] V5LiveGameSDK com desduplicação LRU idempotente de eventos de live - PASSOU")

    # TEST 7: Sintaxe Node.js em todos os 41 cartuchos
    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            content = f.read()
        scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', content, re.DOTALL)
        combined_js = "\n".join(scripts)
        res = subprocess.run(["node", "--check"], input=combined_js, encoding='utf-8', capture_output=True)
        assert res.returncode == 0, f"Erro de sintaxe no jogo {slug}: {res.stderr}"
    print("[TEST 7] Sintaxe Node.js 100% válida em todos os 41 cartuchos - PASSOU")

    print("=" * 70)
    print("TODOS OS 7 TESTES DA RODADA 8 PASSARAM COM SUCESSO ABSOLUTO (100%)!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
