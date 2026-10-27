import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_sound_params():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find methods like playX(a, b, c) inside sound or audio objects
        matches = re.finditer(r'(\b(?:play|trigger|spawn|init)\w*)\s*\(([^)]+)\)\s*\{', content)
        for m in matches:
            fn_name = m.group(1)
            params = m.group(2)
            # check if any param is used directly in setValueAtTime
            pos = m.start()
            body = content[pos:pos+500]
            if "setValueAtTime" in body:
                param_list = [p.strip() for p in params.split(',')]
                for p in param_list:
                    p_name = p.split('=')[0].strip()
                    if f"setValueAtTime({p_name}," in body and "=" not in p:
                        findings.append((g, fn_name, p_name))

    print(f"Total de parâmetros de som sem default usados em setValueAtTime: {len(findings)}")
    for g, fn, p in findings:
        print(f" - [{g}] {fn}(... {p} ...) usado sem default em setValueAtTime")
    return findings

if __name__ == "__main__":
    check_sound_params()
