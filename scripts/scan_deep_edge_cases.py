import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def scan_bugs():
    results = {}
    for entry in sorted(os.listdir(GAMES_DIR)):
        index_path = os.path.join(GAMES_DIR, entry, "index.html")
        if not os.path.isfile(index_path):
            continue
        
        with open(index_path, "r", encoding="utf-8") as f:
            code = f.read()

        issues = []
        
        # 1. AudioContext resume on event
        has_audio = "AudioContext" in code or "webkitAudioContext" in code
        has_resume = "resume()" in code
        if has_audio and not has_resume:
            issues.append("AudioContext sem audioCtx.resume() defensivo contra Audio Autoplay Policy")

        # 2. Particle array unbounded growth check
        # Look for particles.push or similar
        particle_pushes = re.findall(r'(\w+)\.push\s*\([^)]*particle', code, re.IGNORECASE)
        # Check if there is an array capping or splice/filter
        for arr in set(particle_pushes):
            if f"{arr}.length >" not in code and f"{arr}.length>=" not in code and f"{arr}.splice" not in code and f"{arr}.filter" not in code and f"{arr}.shift" not in code:
                issues.append(f"Possível vazamento de memória: array de partículas '{arr}' sem limite máximo")

        # 3. Delta time clamping in requestAnimationFrame
        if "requestAnimationFrame" in code and "dt" in code:
            if "Math.min(" not in code and "dt >" not in code and "dt>" not in code:
                issues.append("Delta time (dt) sem clamping defensivo (risco de clipping se frame rate cair)")

        # 4. Math.max / Math.min or NaN guard on gift value
        # Look for parseInt(data.value) or Number(data.value)
        if "data.value" in code or "payload.value" in code or "event.value" in code:
            # check if NaN check exists
            if "isNaN" not in code and "Number.isFinite" not in code and "|| 1" not in code and "|| 0" not in code:
                issues.append("Valor do payload sem fallback defensivo para NaN")

        # 5. Timer cleanup on round reset
        # If setInterval is used, check if it's cleared or managed
        set_intervals = re.findall(r'setInterval\s*\(', code)
        clear_intervals = re.findall(r'clearInterval\s*\(', code)
        if len(set_intervals) > len(clear_intervals) and len(set_intervals) > 2:
            issues.append(f"Múltiplos setInterval ({len(set_intervals)}) com poucos clearInterval ({len(clear_intervals)})")

        results[entry] = issues

    return results

if __name__ == "__main__":
    findings = scan_bugs()
    total_issues = 0
    for game, issues in findings.items():
        if issues:
            print(f"[{game}]")
            for iss in issues:
                print(f"  - {iss}")
                total_issues += 1
    print(f"\nTotal de potenciais pontos de melhoria/bugs: {total_issues}")
