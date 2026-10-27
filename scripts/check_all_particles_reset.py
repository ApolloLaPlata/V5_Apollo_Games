import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_all_games_particle_resets():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if game has a particle array
        p_match = re.search(r'\b(const|let|var)\s+(particles|sparks|confetti|meteors|bullets)\s*=\s*\[\]', content)
        if not p_match:
            continue
        
        arr_name = p_match.group(2)

        # Find reset function
        reset_match = re.search(r'function\s+(reset\w*|restart\w*|startNewRound|initRound|newRound)\s*\([^)]*\)\s*\{([\s\S]*?)\n    \}', content)
        if not reset_match:
            continue

        fn_name = reset_match.group(1)
        body = reset_match.group(2)

        cleared = (f"{arr_name}.length = 0" in body or 
                   f"{arr_name} = []" in body or 
                   f"{arr_name}.splice(0" in body)
        
        if not cleared:
            findings.append((g, arr_name, fn_name))

    print(f"Total de jogos onde '{arr_name}' não é limpo em reset: {len(findings)}")
    for g, arr, fn in findings:
        print(f" - [{g}] array '{arr}' não é limpo em {fn}()")
    return findings

if __name__ == "__main__":
    check_all_games_particle_resets()
