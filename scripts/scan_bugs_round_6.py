import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def scan_bugs_round_6():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Check for width: ${...}% without Math.max(0, ...)
        pct_width_matches = re.finditer(r'style\.width\s*=\s*`?([a-zA-Z0-9_\.\(\)\s\*\/\-\+]+)%`?', content)
        for m in pct_width_matches:
            expr = m.group(1).strip()
            # check if expr has Math.max(0, ...)
            if "Math.max" not in expr and "Math.min" not in expr and ">=" not in expr:
                # check if variable could be negative (e.g. hp, health, life, score, time)
                if any(v in expr.lower() for v in ['hp', 'health', 'life', 'timer', 'time', 'remaining']):
                    pos = m.start()
                    line_start = content.rfind('\n', 0, pos) + 1
                    line_end = content.find('\n', pos)
                    line = content[line_start:line_end].strip()
                    if "Math.max(0" not in line and "Math.max( 0" not in line:
                        findings.append((g, f"Barra de progresso sem Math.max(0, ...): {line}"))

        # 2. Check for touch-action / user-select on game container
        if "user-select: none" not in content and "-webkit-user-select: none" not in content:
            findings.append((g, "Falta 'user-select: none' para evitar seleção acidental de texto na transmissão"))

        if "touch-action: none" not in content and "touch-action: manipulation" not in content:
            findings.append((g, "Falta 'touch-action: none' para evitar zoom acidental no mobile/OBS"))

        # 3. Check for BroadcastChannel close on unload
        if "BroadcastChannel" in content and "beforeunload" not in content and "unload" not in content:
            findings.append((g, "BroadcastChannel não é fechado explicitamente no evento beforeunload"))

    print(f"Total de potenciais achados (Rodada 6): {len(findings)}")
    for g, issue in findings:
        print(f"[{g}] {issue}")
    return findings

if __name__ == "__main__":
    scan_bugs_round_6()
