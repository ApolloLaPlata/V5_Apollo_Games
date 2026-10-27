import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_keydown_bugs():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        matches = re.finditer(r'addEventListener\s*\(\s*[\'"]keydown[\'"]\s*,\s*\(?(\w+)\)?\s*=>\s*\{([\s\S]*?)\n    \}\)', content)
        for m in matches:
            evt_name = m.group(1)
            body = m.group(2)
            # check if evt_name.key.toLowerCase() is called without guard
            if f"{evt_name}.key.toLowerCase()" in body and f"{evt_name}.key &&" not in body and f"({evt_name}.key ||" not in body:
                findings.append((g, f"Chamada direta a {evt_name}.key.toLowerCase() sem guarda"))

    print(f"Total de bugs em keydown: {len(findings)}")
    for g, desc in findings:
        print(f" - [{g}] {desc}")
    return findings

if __name__ == "__main__":
    check_keydown_bugs()
