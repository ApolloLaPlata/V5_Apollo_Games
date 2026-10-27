import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def scan_string_method_crashes():
    issues = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for unshielded giftName.toLowerCase
        # e.g., giftName.toLowerCase() where giftName is not guarded
        matches = re.finditer(r'(\b\w+)\.(toLowerCase|toUpperCase|trim|includes|slice|substring)\(', content)
        for m in matches:
            var_name = m.group(1)
            method = m.group(2)
            # Find the line
            line_start = content.rfind('\n', 0, m.start()) + 1
            line_end = content.find('\n', m.end())
            line = content[line_start:line_end].strip()

            if var_name in ('giftName', 'gift', 'user', 'comment', 'action', 'type'):
                # Check if there is a guard on the same line or right before
                # e.g. (giftName && giftName.toLowerCase...) or String(giftName)
                if f"({var_name} &&" not in line and f"{var_name} &&" not in line and f"!{var_name}" not in line and f"String({var_name})" not in line and f"({var_name} ||" not in line:
                    # Let's see if var_name is guaranteed to be string
                    # e.g. const giftName = payload.giftName || null; -> NOT guaranteed!
                    issues.append((g, var_name, method, line))

    return issues

if __name__ == "__main__":
    findings = scan_string_method_crashes()
    print(f"Total de potenciais chamadas inseguras em strings: {len(findings)}")
    for g, var, meth, line in findings:
        print(f"[{g}] {var}.{meth}(): {line}")
