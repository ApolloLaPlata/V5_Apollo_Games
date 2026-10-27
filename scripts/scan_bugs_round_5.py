import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def scan_bugs_round_5():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Check for audio oscillator stop without positive/finite time
        # osc.stop(now + duration) -> what if now + duration is NaN or negative?
        osc_stops = re.finditer(r'osc\.stop\s*\(\s*([^)]+)\s*\)', content)
        for m in osc_stops:
            arg = m.group(1).strip()
            if "+" not in arg and "now" not in arg and "currentTime" not in arg:
                findings.append((g, f"osc.stop() com argumento incomum: {arg}"))

        # 2. Check for event listeners added inside loops or repeated functions
        # e.g., window.addEventListener inside gameLoop, render, update, reset, pull, etc.
        fn_matches = re.finditer(r'function\s+(\w+)\s*\([^)]*\)\s*\{([\s\S]*?)\n    \}', content)
        for fm in fn_matches:
            fn_name = fm.group(1)
            fn_body = fm.group(2)
            if fn_name not in ('init', 'setup', 'initBroadcastChannel', 'initWindowListener', 'initKeyboard', 'initEvents'):
                if "addEventListener(" in fn_body:
                    findings.append((g, f"addEventListener adicionado dentro de função potencialmente repetitiva: {fn_name}()"))

        # 3. Check for memory leaks in Set / Map
        # e.g. participants = new Set() -> is it cleared on reset?
        has_set_or_map = re.search(r'\b(const|let|var)\s+(\w+)\s*=\s*new\s+(Set|Map)\s*\(', content)
        if has_set_or_map:
            var_name = has_set_or_map.group(2)
            # check if reset clears it
            reset_match = re.search(r'function\s+(reset\w*|restart\w*|startNewRound|initRound|newRound)\s*\([^)]*\)\s*\{([\s\S]*?)\n    \}', content)
            if reset_match:
                fn_name = reset_match.group(1)
                body = reset_match.group(2)
                if f"{var_name}.clear()" not in body and f"{var_name} = new" not in body:
                    findings.append((g, f"Set/Map '{var_name}' não é limpo com .clear() em {fn_name}()"))

        # 4. Check for CSS transition / animation memory accumulation
        # e.g., elements created and animated without removal
        keyframes_count = len(re.findall(r'@keyframes', content))
        if keyframes_count > 15:
            findings.append((g, f"Muitas @keyframes ({keyframes_count})"))

    print(f"Total de potenciais achados (Rodada 5): {len(findings)}")
    for g, issue in findings:
        print(f"[{g}] {issue}")
    return findings

if __name__ == "__main__":
    scan_bugs_round_5()
