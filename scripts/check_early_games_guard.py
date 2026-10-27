import os
import re

GAMES = [
    "01_cabo_de_guerra_neon",
    "01b_cabo_de_guerra_elementos",
    "02_plinko_pachinko_fortuna",
    "06_batalha_dos_baloes",
    "09_tsunami_de_curtidas",
    "11_queda_de_braco_titas",
    "12_pachinko_pinball_neon",
    "13_cascata_de_moedas",
    "14_vortex_gravitacional"
]

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

for g in GAMES:
    index_file = os.path.join(GAMES_DIR, g, "index.html")
    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # find function handleEvent or similar
    m = re.search(r'function\s+(handleEvent|onLiveEvent|handleGameEvent|handleLivePayload)\s*\(([^)]*)\)\s*\{', content)
    if m:
        fn_name = m.group(1)
        arg = m.group(2)
        body = content[m.end():m.end()+250]
        has_guard = f"!{arg}" in body or f"typeof {arg}" in body
        print(f"[{g}] {fn_name}({arg}): guarded={has_guard}")
        if not has_guard:
            print(f"   Snippet: {body[:100].replace(chr(10), ' ')}")
    else:
        print(f"[{g}] NO FUNCTION MATCH")
