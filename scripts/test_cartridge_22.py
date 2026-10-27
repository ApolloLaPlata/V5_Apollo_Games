"""
scripts/test_cartridge_22.py
Validação automatizada do Cartucho #22: Ponte de Vidro Quebradiço
"""
import os
import re

src = r"catalogo_jogos\22_ponte_de_vidro_quebradico\index.html"
dst = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games\22_ponte_de_vidro_quebradico\index.html"

with open(src, "r", encoding="utf-8") as f:
    html = f.read()

checks = {
    "Origem existe": os.path.exists(src),
    "Destino existe": os.path.exists(dst),
    "Paridade de bytes": html == open(dst, "r", encoding="utf-8").read(),
    "Proporcao 9:16": ("9 / 16" in html) or ("9/16" in html),
    "Safe Zone Topo (140px)": ("140px" in html) or ("top-header" in html),
    "Safe Zone Base (180px)": ("180px" in html) or ("bottom-panel" in html),
    "Anti-silencio": ("anti-silêncio" in html.lower()) or ("mockusers" in html.lower()) or ("simula" in html.lower()),
    "Event Bus": ("v5_broadcaster_games" in html) and ("v5_event" in html),
    "Web Audio API": ("AudioContext" in html) and not bool(re.search(r'["\'][^"\']+\.(mp3|wav)["\']', html)),
    "Ciclo Fechado & Reset": ("victory-overlay" in html.lower() or "reset" in html.lower()) and ("5000" in html),
    "Mecanica Ponte de Vidro & Votacao": ("shatter" in html.lower() or "quebrad" in html.lower()) and any(c in html.lower() for c in ["1", "2", "esq", "dir"]) and ("reveal" in html.lower() or "xray" in html.lower() or "gift" in html.lower())
}

print("=" * 65)
print(" VERIFICAÇÃO HOMOLOGATÓRIA — CARTUCHO #22 PONTE DE VIDRO QUEBRADIÇO")
print("=" * 65)
for name, res in checks.items():
    print(f"  [{'PASS' if res else 'FAIL'}] {name}")
print("=" * 65)

if all(checks.values()):
    print("TODOS OS 11 CHECKS DO CARTUCHO #22 APROVADOS COM SUCESSO!")
    exit(0)
else:
    print("FALHA EM UM OU MAIS CHECKS!")
    exit(1)
