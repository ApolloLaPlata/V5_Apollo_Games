import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_screenshake():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        if "screenShake" in content or "triggerScreenShake" in content or "shake" in content.lower():
            # Check if screenShake uses canvas translate or CSS transform
            css_shake = re.findall(r'(\w+)\.style\.transform\s*=\s*`translate\(', content)
            canvas_shake = "ctx.translate(" in content and "shake" in content.lower()
            # If CSS shake is used, check if reset clears it
            if css_shake:
                # check if reset clears style.transform = ''
                has_reset_clear = "style.transform = ''" in content or "style.transform = 'none'" in content or 'style.transform = ""' in content
                if not has_reset_clear:
                    findings.append((g, "CSS shake sem limpeza em reset", css_shake))
            
            # If screenShake decay is used in canvas
            decay_match = re.search(r'screenShake\s*\*=\s*([0-9\.]+)', content)
            if decay_match:
                decay = float(decay_match.group(1))
                # Check if it resets to 0 when small
                cutoff = "screenShake < 0." in content or "screenShake < 1" in content
                if not cutoff:
                    findings.append((g, f"Canvas shake decai com fator {decay} sem ponto de corte zero (pode tremer indefinidamente com números subnormais)", []))

    print(f"Total de questões de screenshake: {len(findings)}")
    for g, desc, data in findings:
        print(f" - [{g}] {desc}")
    return findings

if __name__ == "__main__":
    check_screenshake()
