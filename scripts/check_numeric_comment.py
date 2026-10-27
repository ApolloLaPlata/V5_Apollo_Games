import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_numeric_comment_handling():
    vulnerable = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check where comment is assigned
        # e.g., const comment = (data.comment || '').trim().toLowerCase();
        # If data.comment is a number, e.g. 1, then (1 || '') is 1. (1).trim() throws TypeError!
        matches = re.finditer(r'(?:const|let|var)\s+comment\s*=\s*([^;\n]+);', content)
        for m in matches:
            expr = m.group(1).strip()
            # Does it convert to String(...) or .toString()?
            if "String(" not in expr and ".toString()" not in expr and "'' +" not in expr and '"" +' not in expr and f"`${{" not in expr:
                if ".trim(" in expr or ".toLowerCase(" in expr or ".includes(" in expr:
                    vulnerable.append((g, expr))

    print(f"Total de cartuchos vulneráveis a comment numérico (ex: comment: 1): {len(vulnerable)}")
    for g, expr in vulnerable:
        print(f" - [{g}] const comment = {expr}")
    return vulnerable

if __name__ == "__main__":
    check_numeric_comment_handling()
