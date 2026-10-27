import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_floating_texts_resets():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for arrays like floatTexts, floatingTexts, damageTexts, pops
        matches = re.finditer(r'\b(?:state\.)?(\w*(?:float|pop|dmg|damage|score|toast)\w*s)\s*=\s*\[\]', content, re.IGNORECASE)
        for m in matches:
            arr_name = m.group(1)
            # check if reset clears this array
            reset_match = re.search(r'function\s+(reset\w*|restart\w*|startNewRound|initRound|newRound)\s*\([^)]*\)\s*\{([\s\S]*?)\n    \}', content)
            if reset_match:
                fn_name = reset_match.group(1)
                body = reset_match.group(2)
                cleared = (f"{arr_name}.length = 0" in body or f"{arr_name} = []" in body or f"{arr_name}.splice" in body)
                if not cleared:
                    findings.append((g, arr_name, fn_name))

    print(f"Total de arrays de texto flutuante sem limpeza em reset: {len(findings)}")
    for g, arr, fn in set(findings):
        print(f" - [{g}] {arr} não é limpo em {fn}()")
    return findings

if __name__ == "__main__":
    check_floating_texts_resets()
