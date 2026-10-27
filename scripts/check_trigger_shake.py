import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_trigger_screen_shake():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        matches = re.finditer(r'function\s+triggerScreenShake\s*\([^)]*\)\s*\{([\s\S]*?)\n    \}', content)
        for m in matches:
            body = m.group(1)
            # check if it uses setTimeout or adds a class
            if "classList.add" in body and "classList.remove" not in body:
                findings.append((g, "triggerScreenShake adiciona classe sem remover"))
            elif "style.transform" in body and "none" not in body and "''" not in body:
                findings.append((g, "triggerScreenShake altera style.transform sem reset para none/empty"))

    print(f"Total de problemas em triggerScreenShake: {len(findings)}")
    for g, desc in findings:
        print(f" - [{g}] {desc}")
    return findings

if __name__ == "__main__":
    check_trigger_screen_shake()
