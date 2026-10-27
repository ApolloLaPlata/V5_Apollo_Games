import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def scan_other_gift_names():
    vulnerable = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            # Check gift.toLowerCase or gift.includes or giftType.toLowerCase
            if re.search(r'\b(gift|giftType|gift_name)\s*\.\s*(toLowerCase|toUpperCase|includes)', line):
                if not re.search(r'(\b\1\s*&&|\b\1\s*\?|\b\1\s*\|\||typeof\s+\1|\(\1\b)', line):
                    vulnerable.append((g, idx + 1, line.strip()))
                elif f"{re.search(r'(gift|giftType|gift_name)', line).group(1)}.toLowerCase()" in line and "&&" not in line and "||" not in line:
                    vulnerable.append((g, idx + 1, line.strip()))
    return vulnerable

if __name__ == "__main__":
    findings = scan_other_gift_names()
    print(f"Total de vulnerabilidades em outras vars de gift: {len(findings)}")
    for g, line_no, code in findings:
        print(f"[{g}:{line_no}] {code}")
