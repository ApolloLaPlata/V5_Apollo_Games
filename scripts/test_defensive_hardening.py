import os
import re
import subprocess
import sys

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def run_tests():
    print("=" * 70)
    print("SUÍTE DE TESTES: VALIDAÇÃO DE CORREÇÕES CIRÚRGICAS & BLINDAGEM")
    print("=" * 70)
    
    # Test 1: 02_plinko_pachinko_fortuna giftName guard
    p02 = os.path.join(GAMES_DIR, "02_plinko_pachinko_fortuna", "index.html")
    with open(p02, "r", encoding="utf-8") as f:
        c02 = f.read()
    assert "const gStr = (giftName || '').toLowerCase();" in c02, "02_plinko falta gStr guard"
    assert "const giftName = payload.giftName || 'Presente';" in c02, "02_plinko falta fallback para giftName"
    print("[TEST 1] 02_plinko_pachinko_fortuna: Blindagem contra giftName nulo - PASSOU")

    # Test 2: 23_sobrevivencia_na_lava giftName guard
    p23 = os.path.join(GAMES_DIR, "23_sobrevivencia_na_lava", "index.html")
    with open(p23, "r", encoding="utf-8") as f:
        c23 = f.read()
    assert 'const gName = (giftName || "").toLowerCase();' in c23, "23_lava falta gName guard"
    print("[TEST 2] 23_sobrevivencia_na_lava: Blindagem contra giftName nulo - PASSOU")

    # Test 3: 15_corrida_maluca_espacial meteor spawner
    p15 = os.path.join(GAMES_DIR, "15_corrida_maluca_espacial", "index.html")
    with open(p15, "r", encoding="utf-8") as f:
        c15 = f.read()
    assert "if (isGameOver) return;\n      if (Math.random() < 0.65) spawnMeteor();" in c15, "15_corrida meteoro falta isGameOver check"
    print("[TEST 3] 15_corrida_maluca_espacial: Pausa de spawn em isGameOver - PASSOU")

    # Test 4: Guard in handleGameEvent for 08, 10, 23, 24, 25
    guarded = ["08_caca_tesouro_coordenadas", "10_queda_dos_blocos", "23_sobrevivencia_na_lava", "24_campo_minado_neon", "25_batalha_naval_live"]
    for g in guarded:
        pg = os.path.join(GAMES_DIR, g, "index.html")
        with open(pg, "r", encoding="utf-8") as f:
            cg = f.read()
        assert 'if (!data || typeof data !== "object") return;' in cg, f"{g} falta guarda defensiva em handleGameEvent"
    print(f"[TEST 4] 5/5 jogos auditados com guarda defensiva 'if (!data) return' - PASSOU")

    # Test 5: Node syntax check on all modified files
    all_files = [p02, p23, p15] + [os.path.join(GAMES_DIR, g, "index.html") for g in guarded]
    for path in set(all_files):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        scripts = []
        for m in re.finditer(r'<script\b[^>]*>([\s\S]*?)<\/script>', content, re.IGNORECASE):
            if 'src=' not in m.group(0):
                scripts.append(m.group(1))
        js = '\n'.join(scripts)
        res = subprocess.run(['node', '--check'], input=js.encode('utf-8'), capture_output=True)
        assert res.returncode == 0, f"Erro de sintaxe em {path}: {res.stderr.decode('utf-8', errors='replace')}"
    print(f"[TEST 5] Sintaxe validada com sucesso em 100% dos cartuchos corrigidos - PASSOU")

    print("\n" + "=" * 70)
    print("TODOS OS 5 TESTES DE CORREÇÃO E BLINDAGEM PASSARAM COM SUCESSO (100%)!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
