import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def inspect_gameloop_physics():
    report = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find gameLoop or loop definition
        m = re.search(r'function\s+(gameLoop|loop|render|update|tick)\s*\(([^)]*)\)\s*\{([\s\S]*?)(?:function|\Z)', content)
        if m:
            fn_name = m.group(1)
            body = m.group(3)[:800]
            # Check how time is tracked
            has_dt = "dt" in body
            has_clamp = "Math.min" in body or "clamp" in body or "min(" in body
            report.append((g, fn_name, has_dt, has_clamp))

    return report

if __name__ == "__main__":
    rep = inspect_gameloop_physics()
    for g, fn, has_dt, has_clamp in rep:
        if has_dt and not has_clamp:
            print(f"[{g}] {fn} has dt, but no clamping detected in first 800 chars")
