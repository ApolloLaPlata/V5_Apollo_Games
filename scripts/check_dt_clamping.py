import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_dt_clamping():
    unclamped_games = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if gameLoop calculates dt
        dt_match = re.search(r'const\s+dt\s*=\s*(?:\(?\s*now\s*-\s*\w+\s*\)?|\w+\s*-\s*\w+)\s*/\s*1000', content)
        if dt_match:
            # check if there is Math.min or dt clamping near it (within 150 chars)
            pos = dt_match.start()
            nearby = content[pos:pos+250]
            if "Math.min" not in nearby and "dt >" not in nearby and "dt>" not in nearby and "min(" not in nearby:
                unclamped_games.append((g, dt_match.group(0), nearby.replace('\n', ' ')[:100]))

    print(f"Total de jogos com dt sem clamping defensivo: {len(unclamped_games)}")
    for g, match_str, snippet in unclamped_games:
        print(f" - [{g}] {snippet}")
    return unclamped_games

if __name__ == "__main__":
    check_dt_clamping()
