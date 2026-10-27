import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_all_time_deltas():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find patterns like (now - lastTime) or (currentTime - lastTime) or (time - last)
        matches = re.finditer(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:\(?\s*(\w+)\s*-\s*(\w+)\s*\)?)(?:\s*/\s*(\d+))?', content)
        for m in matches:
            var_name = m.group(1)
            t1 = m.group(2)
            t2 = m.group(3)
            div = m.group(4)
            if any(k in var_name.lower() for k in ['dt', 'delta', 'elapsed', 'step']) and any(k in t1.lower() for k in ['now', 'time', 'current', 'timestamp']) and any(k in t2.lower() for k in ['last', 'prev']):
                start = m.start()
                nearby = content[start:start+300]
                has_clamp = ("Math.min" in nearby or f"{var_name} >" in nearby or f"{var_name}>" in nearby or "min(" in nearby)
                if not has_clamp:
                    findings.append((g, var_name, m.group(0), nearby.replace('\n', ' ')[:100]))

    print(f"Total de deltas sem clamping: {len(findings)}")
    for g, v, full, nearby in findings:
        print(f" - [{g}] {full} => {nearby}")

if __name__ == "__main__":
    check_all_time_deltas()
