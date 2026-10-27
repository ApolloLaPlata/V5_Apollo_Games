import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

for g in sorted(os.listdir(GAMES_DIR)):
    index_file = os.path.join(GAMES_DIR, g, "index.html")
    if not os.path.isfile(index_file):
        continue
    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Look for 'v5_event'
    m = re.search(r"addEventListener\s*\(\s*['\"]v5_event['\"],\s*\(?[^)]*\)?\s*=>\s*\{?([^;}\n]+)", content)
    if m:
        call = m.group(1).strip()
        print(f"{g}: {call}")
