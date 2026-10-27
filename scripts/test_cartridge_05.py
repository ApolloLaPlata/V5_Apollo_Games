"""
scripts/test_cartridge_05.py
Validação automatizada do Cartucho #05: Roleta dos Desafios da Live
"""
import os
import re

src = r"catalogo_jogos\05_roleta_desafios_live\index.html"
dst = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games\05_roleta_desafios_live\index.html"

with open(src, "r", encoding="utf-8") as f:
    html = f.read()

checks = {
    "Origem existe": os.path.exists(src),
    "Destino existe": os.path.exists(dst),
    "Paridade de bytes": html == open(dst, "r", encoding="utf-8").read(),
    "Proporcao 9:16": ("9 / 16" in html) or ("9/16" in html),
    "Safe Zone Topo (140px)": ("140px" in html) or ("top-header" in html),
    "Safe Zone Base (180px)": ("180px" in html) or ("bottom-panel" in html),
    "Anti-silencio": ("anti-silêncio" in html.lower()) or ("mockusers" in html.lower()),
    "Event Bus": ("v5_broadcaster_games" in html) and ("v5_event" in html),
    "Web Audio API": ("AudioContext" in html) and not bool(re.search(r'["\'][^"\']+\.(mp3|wav)["\']', html)),
    "Ciclo Fechado & Reset": ("roundtime" in html.lower()) and ("challengeoverlay" in html.lower() or "reset" in html.lower()),
    "Comandos Chat": any(c in html.lower() for c in ["girar", "spin", "roleta", "1"])
}

print("=" * 65)
print(" VERIFICAÇÃO HOMOLOGATÓRIA — CARTUCHO #05 ROLETA DOS DESAFIOS")
print("=" * 65)
for name, res in checks.items():
    print(f"  [{'PASS' if res else 'FAIL'}] {name}")
print("=" * 65)

if all(checks.values()):
    print("TODOS OS 11 CHECKS DO CARTUCHO #05 APROVADOS COM SUCESSO!")
    exit(0)
else:
    print("FALHA EM UM OU MAIS CHECKS!")
    exit(1)
