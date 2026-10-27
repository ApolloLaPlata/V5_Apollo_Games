import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

for g in sorted(os.listdir(GAMES_DIR)):
    f = os.path.join(GAMES_DIR, g, "index.html")
    if not os.path.isfile(f):
        continue
    with open(f, "r", encoding="utf-8") as fh:
        c = fh.read()
    for m in re.finditer(r'JSON\.parse\s*\([^)]+\)', c):
        pos = m.start()
        nearby = c[max(0, pos-120):min(len(c), pos+120)]
        if "try" not in nearby:
            print(f"[{g}] {m.group(0)}")
            print(f"   Context: {nearby.strip()}")
