import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_all_comment_assignments():
    vulnerable = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            # Look for lines assigning comment or cmd
            if re.search(r'\b(const|let|var)\s+(comment|cmd|command|txt|text)\s*=\s*', line):
                if any(k in line for k in ['comment', 'action', 'data', 'payload', 'msg']):
                    # Check if String( or .toString() is NOT used
                    if "String(" not in line and ".toString()" not in line and "'' +" not in line and '"" +' not in line and "`" not in line:
                        if ".trim(" in line or ".toLowerCase(" in line or ".includes(" in line:
                            vulnerable.append((g, idx + 1, line.strip()))

    print(f"Total de atribuições vulneráveis encontradas: {len(vulnerable)}")
    for g, line_no, code in vulnerable:
        print(f"[{g}:{line_no}] {code}")
    return vulnerable

if __name__ == "__main__":
    check_all_comment_assignments()
