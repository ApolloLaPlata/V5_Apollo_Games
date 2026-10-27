import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_raf_in_resets():
    duplicate_loops = []
    for entry in sorted(os.listdir(GAMES_DIR)):
        index_path = os.path.join(GAMES_DIR, entry, "index.html")
        if not os.path.isfile(index_path):
            continue
        with open(index_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Find functions with reset / restart / restartRound / resetGame
        matches = re.finditer(r'function\s+(reset\w*|restart\w*|newRound\w*)\s*\([^)]*\)\s*\{([\s\S]*?)\n    \}', code)
        for m in matches:
            fn_name = m.group(1)
            body = m.group(2)
            if "requestAnimationFrame" in body:
                duplicate_loops.append((entry, fn_name))

    print(f"Jogos com rAF dentro de funções de reset: {len(duplicate_loops)}")
    for g, fn in duplicate_loops:
        print(f" - [{g}] chama rAF em {fn}()")

if __name__ == "__main__":
    check_raf_in_resets()
