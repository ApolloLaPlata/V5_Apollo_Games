import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_percentage_divisions():
    vulnerable = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Look for * 100
        matches = re.finditer(r'([a-zA-Z0-9_\.]+\s*/\s*[a-zA-Z0-9_\.\(\)]+)\s*\*\s*100', content)
        for m in matches:
            expr = m.group(1)
            pos = m.start()
            line_start = content.rfind('\n', 0, pos) + 1
            line_end = content.find('\n', pos)
            line = content[line_start:line_end].strip()

            # check if denominator can be 0 and is not guarded
            # e.g. totalVotes > 0 ? (votes / totalVotes) * 100 : 50
            if "total" in expr.lower() or "sum" in expr.lower() or "count" in expr.lower():
                if "> 0" not in line and "|| 1" not in line and "Math.max(" not in line and "? " not in line and "?(" not in line:
                    vulnerable.append((g, line))

    print(f"Total de divisões percentuais potencialmente vulneráveis a zero: {len(vulnerable)}")
    for g, line in vulnerable:
        print(f" - [{g}] {line}")
    return vulnerable

if __name__ == "__main__":
    check_percentage_divisions()
