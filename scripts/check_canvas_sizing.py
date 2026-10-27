import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_canvas_sizing():
    reports = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check canvas sizing
        # Does it use clientWidth or hardcoded 1080 / stage?
        has_canvas = "<canvas" in content
        if not has_canvas:
            continue

        # Look for canvas.width =
        w_matches = re.findall(r'canvas\.width\s*=\s*([^;\n]+);', content)
        h_matches = re.findall(r'canvas\.height\s*=\s*([^;\n]+);', content)
        reports.append((g, w_matches, h_matches))

    return reports

if __name__ == "__main__":
    reps = check_canvas_sizing()
    print(f"Total de jogos com canvas: {len(reps)}")
    for g, w, h in reps:
        print(f"[{g}] w: {w} | h: {h}")
