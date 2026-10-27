import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_audio_gain():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find gain.gain.setValueAtTime(..., ...)
        matches = re.finditer(r'gain\.setValueAtTime\s*\(\s*([^,]+)\s*,', content)
        for m in matches:
            val_expr = m.group(1).strip()
            # check if it's a number
            try:
                num = float(val_expr)
                if num > 1.0:
                    findings.append((g, f"Gain fixo > 1.0: {num}"))
            except ValueError:
                # Dynamic expression
                # Check if it has Math.min or clamping
                if "Math.min" not in val_expr and "Math.max" not in val_expr and "||" not in val_expr:
                    if any(v in val_expr for v in ['volume', 'vol', 'intensity', 'weight', 'val', 'power']):
                        findings.append((g, f"Gain dinâmico sem clamping: {val_expr}"))

    print(f"Total de questões de volume/gain de áudio: {len(findings)}")
    for g, issue in findings:
        print(f" - [{g}] {issue}")
    return findings

if __name__ == "__main__":
    check_audio_gain()
