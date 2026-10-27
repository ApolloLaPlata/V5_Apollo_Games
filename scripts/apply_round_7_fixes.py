import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def apply_round_7_fixes():
    fixed_comments = 0
    added_contextmenu = 0

    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            code = f.read()

        mod = code

        # 1. Patch comment assignments
        # e.g., const comment = (data.comment || '').trim().toLowerCase();
        pattern1 = r'const\s+comment\s*=\s*\((?:data|payload)\.comment\s*\|\|\s*[\'"][\'"]\)\.trim\(\)\.toLowerCase\(\);'
        replacement1 = 'const comment = String((data || payload || {}).comment || "").trim().toLowerCase();'
        if re.search(pattern1, mod):
            mod = re.sub(pattern1, replacement1, mod)
            fixed_comments += 1

        pattern2 = r'const\s+comment\s*=\s*\((?:data|payload)\.comment\s*\|\|\s*[\'"][\'"]\)\.trim\(\);'
        replacement2 = 'const comment = String((data || payload || {}).comment || "").trim();'
        if re.search(pattern2, mod):
            mod = re.sub(pattern2, replacement2, mod)
            fixed_comments += 1

        # 2. Add contextmenu preventDefault if missing
        if "addEventListener('contextmenu'" not in mod and 'addEventListener("contextmenu"' not in mod:
            # Add right before </script>
            target = "</script>"
            addon = "    window.addEventListener('contextmenu', (e) => e.preventDefault());\n  </script>"
            # Replace the last occurrence of </script>
            pos = mod.rfind(target)
            if pos != -1:
                mod = mod[:pos] + addon + mod[pos + len(target):]
                added_contextmenu += 1

        if mod != code:
            with open(index_file, "w", encoding="utf-8") as f:
                f.write(mod)
            print(f"[PATCHED] {g}")

    print(f"\nResumo da Rodada:")
    print(f" - Atribuições de comment blindadas com String(): {fixed_comments}")
    print(f" - Cartuchos com contextmenu preventDefault adicionado: {added_contextmenu}")

if __name__ == "__main__":
    apply_round_7_fixes()
