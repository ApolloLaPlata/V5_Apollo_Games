import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_confetti_resets():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if confetti array exists
        has_confetti = re.search(r'\b(?:state\.)?confetti\s*=\s*\[\]', content)
        if has_confetti:
            # check if reset clears confetti
            reset_match = re.search(r'function\s+(reset\w*|restart\w*|startNewRound|initRound|newRound)\s*\([^)]*\)\s*\{([\s\S]*?)\n    \}', content)
            if reset_match:
                fn_name = reset_match.group(1)
                body = reset_match.group(2)
                cleared = ("confetti.length = 0" in body or "confetti = []" in body or "confetti.splice" in body)
                if not cleared:
                    findings.append((g, fn_name))

    print(f"Total de jogos onde 'confetti' não é limpo em reset: {len(findings)}")
    for g, fn in findings:
        print(f" - [{g}] confetti não é limpo em {fn}()")
    return findings

if __name__ == "__main__":
    check_confetti_resets()
