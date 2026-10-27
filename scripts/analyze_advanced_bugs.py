import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def analyze_advanced_bugs():
    results = {}
    for entry in sorted(os.listdir(GAMES_DIR)):
        index_path = os.path.join(GAMES_DIR, entry, "index.html")
        if not os.path.isfile(index_path):
            continue
        with open(index_path, "r", encoding="utf-8") as f:
            code = f.read()

        issues = []

        # 1. Unbounded DOM toast/container child growth
        # Check if toast functions limit container children
        if "toast" in code.lower():
            # Check if there is an appendChild inside toast function
            toast_fns = re.findall(r'function\s+(\w*toast\w*)\s*\([^)]*\)\s*\{([^}]+)\}', code, re.IGNORECASE)
            for fn_name, fn_body in toast_fns:
                if "appendChild" in fn_body and ("children.length >" not in fn_body and "childNodes.length >" not in fn_body and "firstElementChild" not in fn_body and "firstChild" not in fn_body):
                    issues.append(f"Toast function '{fn_name}' appends elements without capping container max children")

        # 2. Reset completeness: check resetGame / restartRound / startNewRound
        reset_match = re.search(r'function\s+(resetGame|resetRound|restartRound|startNewRound|resetMatch)\s*\([^)]*\)\s*\{([\s\S]*?)\n    \}', code)
        if reset_match:
            fn_name = reset_match.group(1)
            fn_body = reset_match.group(2)
            # Check if particles array is cleared if particles exists
            if "particles" in code and "particles.length = 0" not in fn_body and "particles = []" not in fn_body and "particles" not in fn_body:
                issues.append(f"Função '{fn_name}' não limpa array de partículas")

        # 3. Canvas rendering: double requestAnimationFrame loop risk
        # If requestAnimationFrame is called inside reset or start, can it spawn multiple loops?
        raf_calls = len(re.findall(r'requestAnimationFrame\s*\(', code))
        if raf_calls > 1:
            # Check if animationFrameId or cancelAnimationFrame is used
            if "cancelAnimationFrame" not in code and "animId" not in code and "frameId" not in code and "animationFrameId" not in code:
                # Check if it's called inside a function that can be called repeatedly
                if "requestAnimationFrame(gameLoop)" in code or "requestAnimationFrame(loop)" in code or "requestAnimationFrame(update)" in code:
                    # Is it also called inside init() or reset()?
                    if re.search(r'function\s+(reset|restart|init)\w*\s*\([^)]*\)\s*\{[\s\S]*?requestAnimationFrame', code):
                        issues.append("Risco de múltiplos loops de requestAnimationFrame após reset/restart")

        # 4. Audio node disconnect
        # Check if createOscillator is called and whether onended disconnects it
        if "createOscillator" in code:
            if "onended" not in code and "disconnect()" not in code:
                issues.append("Nós de oscilador Web Audio podem acumular sem disconnect()")

        results[entry] = issues

    return results

if __name__ == "__main__":
    findings = analyze_advanced_bugs()
    count = 0
    for game, issues in findings.items():
        if issues:
            print(f"[{game}]")
            for iss in issues:
                print(f"  - {iss}")
                count += 1
    print(f"\nTotal de potenciais pontos encontrados: {count}")
