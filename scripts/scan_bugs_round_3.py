import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def scan_bugs_round_3():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Division by total without zero check
        # Check for / (a + b) or / total
        div_matches = re.finditer(r'/\s*\(?\s*([a-zA-Z0-9_\.]+\s*\+\s*[a-zA-Z0-9_\.]+)\s*\)?', content)
        for m in div_matches:
            expr = m.group(1)
            # check if nearby has zero check
            pos = m.start()
            nearby = content[max(0, pos-150):min(len(content), pos+150)]
            if "=== 0" not in nearby and "== 0" not in nearby and "!=" not in nearby and "> 0" not in nearby and "|| 1" not in nearby and "Math.max(" not in nearby:
                findings.append((g, f"Possível divisão por zero (NaN): '/ ({expr})'", nearby.replace('\n', ' ')[:100]))

        # 2. LocalStorage / SessionStorage check
        storage_matches = re.findall(r'(localStorage|sessionStorage)\.\w+', content)
        if storage_matches:
            # Check if it's in try/catch
            for sm in set(storage_matches):
                if f"try" not in content or sm not in content:
                    findings.append((g, f"Uso de {sm} sem try/catch (risco de SecurityError em iframe/OBS)", ""))

        # 3. Canvas font sizing / text truncation
        # Check if fillText is called with user input without length truncation
        # e.g. ctx.fillText(user, ...) where user is not sliced
        fillText_matches = re.finditer(r'ctx\.fillText\s*\(\s*([a-zA-Z0-9_\.]+)\s*,', content)
        for m in fillText_matches:
            arg = m.group(1)
            if arg in ('user', 'username', 'name', 'msg', 'comment', 'text'):
                # check if there's .slice or .substring or max length before
                pos = m.start()
                nearby = content[max(0, pos-200):pos]
                if ".slice(" not in nearby and ".substring(" not in nearby and "maxWidth" not in content[pos:pos+50]:
                    pass # check if fillText has 4th param (maxWidth)

    print(f"Total de potenciais achados: {len(findings)}")
    for g, issue, context in findings:
        print(f"[{g}] {issue}")
        if context:
            print(f"   Contexto: {context}")
    return findings

if __name__ == "__main__":
    scan_bugs_round_3()
