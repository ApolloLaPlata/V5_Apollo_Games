import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def scan_giftname_vulnerabilities():
    vulnerable = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            # Look for giftName.to... or gift.to...
            if re.search(r'\bgiftName\s*\.\s*(toLowerCase|toUpperCase|includes)', line):
                # Check if line does NOT check giftName first
                if not re.search(r'(\bgiftName\s*&&|\bgiftName\s*\?|\bgiftName\s*\|\||typeof\s+giftName|\(giftName\b)', line):
                    vulnerable.append((g, idx + 1, line.strip()))
                elif "giftName.toLowerCase()" in line and "giftName &&" not in line and "(giftName ||" not in line:
                    vulnerable.append((g, idx + 1, line.strip()))
    return vulnerable

if __name__ == "__main__":
    findings = scan_giftname_vulnerabilities()
    print(f"Total de vulnerabilidades em giftName: {len(findings)}")
    for g, line_no, code in findings:
        print(f"[{g}:{line_no}] {code}")
