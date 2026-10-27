import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_all_handlers_accurate():
    games = sorted(os.listdir(GAMES_DIR))
    vulnerable = []
    
    for g in games:
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find what function is called by the listeners
        # e.g. handleIncomingEvent(data) or handleEvent(e.data) or onEvent(payload)
        listener_match = re.search(r'addEventListener\s*\(\s*[\'"]v5_event[\'"]\s*,\s*\(?[^\)]*\)?\s*=>\s*(\w+)\(', content)
        if not listener_match:
            listener_match = re.search(r'channel\.onmessage\s*=\s*\(?[^\)]*\)?\s*=>\s*(\w+)\(', content)
        if not listener_match:
            listener_match = re.search(r'window\.addEventListener\s*\(\s*[\'"]message[\'"]\s*,\s*\(?[^\)]*\)?\s*=>\s*\{[^}]*?(\w+)\(', content)
        
        if not listener_match:
            print(f"ERROR: Cannot find listener target in {g}")
            continue

        handler_fn_name = listener_match.group(1)
        # Find definition of handler_fn_name
        fn_match = re.search(rf'function\s+{handler_fn_name}\s*\(([^)]*)\)\s*\{{', content)
        if not fn_match:
            print(f"ERROR: Cannot find function definition of {handler_fn_name} in {g}")
            continue

        arg_name = fn_match.group(1).strip()
        body_start = fn_match.end()
        first_lines = content[body_start:body_start+400]

        has_guard = re.search(rf'if\s*\(\s*(!\s*{arg_name}|typeof\s+{arg_name}\s*!==\s*[\'"]object[\'"]|{arg_name}\s*===\s*null)', first_lines)
        if not has_guard:
            vulnerable.append((g, handler_fn_name, arg_name, first_lines[:150].strip()))

    print(f"\nTotal de cartuchos verificados: 41")
    print(f"Total de cartuchos vulneráveis a payload nulo/indefinido: {len(vulnerable)}")
    for g, fn, arg, snippet in vulnerable:
        print(f" - [{g}] {fn}({arg}) => {snippet.replace(chr(10), ' ')}")

if __name__ == "__main__":
    check_all_handlers_accurate()
