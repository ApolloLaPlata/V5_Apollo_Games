import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_all_sets_and_maps():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        matches = re.finditer(r'\b(?:const|let|var)\s+(\w+)\s*=\s*new\s+(Set|Map)\b', content)
        for m in matches:
            var_name = m.group(1)
            var_type = m.group(2)
            # check if reset clears it
            reset_match = re.search(r'function\s+(reset\w*|restart\w*|startNewRound|initRound|newRound)\s*\([^)]*\)\s*\{([\s\S]*?)\n    \}', content)
            if reset_match:
                fn_name = reset_match.group(1)
                body = reset_match.group(2)
                cleared = (f"{var_name}.clear()" in body or f"{var_name} = new" in body)
                if not cleared:
                    findings.append((g, var_name, var_type, fn_name))
            else:
                findings.append((g, var_name, var_type, "NENHUM_RESET"))

    print(f"Total de Sets/Maps encontrados sem limpeza em reset: {len(findings)}")
    for g, v, t, fn in findings:
        print(f" - [{g}] {t} '{v}' em {fn}")
    return findings

if __name__ == "__main__":
    check_all_sets_and_maps()
