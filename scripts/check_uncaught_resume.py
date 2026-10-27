import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_uncaught_resume():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find .resume() calls
        matches = re.finditer(r'(\b\w+)\.resume\s*\(\s*\)', content)
        for m in matches:
            var_name = m.group(1)
            pos = m.end()
            # check if followed by .catch
            following = content[pos:pos+30]
            if ".catch" not in following:
                # check if it's inside a try/catch or await
                line_start = content.rfind('\n', 0, m.start()) + 1
                line_end = content.find('\n', m.end())
                line = content[line_start:line_end].strip()
                if "await " not in line:
                    findings.append((g, var_name, line))

    print(f"Total de chamadas a .resume() sem .catch(): {len(findings)}")
    for g, v, line in findings:
        print(f" - [{g}] {line}")
    return findings

if __name__ == "__main__":
    check_uncaught_resume()
