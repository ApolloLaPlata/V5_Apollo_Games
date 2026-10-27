import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_toasts():
    uncapped = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find addToast / spawnToast / pushActivityFeed / showToast
        matches = re.finditer(r'function\s+(addToast|spawnToast|pushActivityFeed|showToast)\s*\([^)]*\)\s*\{([\s\S]*?)\n    \}', content)
        for m in matches:
            fn_name = m.group(1)
            body = m.group(2)
            # check if it appends to an element
            append_m = re.search(r'(\w+)\.appendChild\s*\(', body)
            if append_m:
                container = append_m.group(1)
                # check if there's a while (container.children.length > ...) or if (children.length > ...)
                capped = ("children.length" in body or "childNodes.length" in body or "firstChild" in body or "firstElementChild" in body)
                if not capped:
                    uncapped.append((g, fn_name, container))

    print(f"Total de funções de toast sem limite de elementos filhos: {len(uncapped)}")
    for g, fn, container in uncapped:
        print(f" - [{g}] {fn}() em '{container}'")
    return uncapped

if __name__ == "__main__":
    check_toasts()
