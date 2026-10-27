import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def analyze_event_handling():
    reports = []
    for entry in sorted(os.listdir(GAMES_DIR)):
        index_path = os.path.join(GAMES_DIR, entry, "index.html")
        if not os.path.isfile(index_path):
            continue
        with open(index_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Check how incoming event handles undefined user, undefined comment, undefined giftName
        # Does it assume payload is always well-formed?
        issues = []

        # Check if handleIncomingEvent or onLiveEvent has guards
        # Find the function definition
        handler_match = re.search(r'function\s+(handleLiveEvent|onLiveEvent|handleIncomingEvent|handleGameEvent)\s*\(([^)]*)\)\s*\{', code)
        if handler_match:
            fn_name = handler_match.group(1)
            fn_arg = handler_match.group(2).strip()
            # extract first 30 lines of the function
            start_pos = handler_match.start()
            fn_chunk = code[start_pos:start_pos+2000]

            # Check if payload could be null
            if f"if (!{fn_arg}) return;" not in fn_chunk and f"if (!{fn_arg} || typeof {fn_arg} !== 'object') return;" not in fn_chunk and f"!{fn_arg}" not in fn_chunk:
                issues.append(f"Falta guarda defensiva contra payload null/undefined em {fn_name}")

            # Check if payload.user might be undefined and called .toUpperCase() or similar directly
            # e.g., payload.user.toUpperCase() without (payload.user || 'Anônimo')
            user_direct_calls = re.findall(rf'({fn_arg}\.user|user)\.to(Upper|Lower)Case\(\)', fn_chunk)
            # Check if user is guarded before
            if "user = " in fn_chunk or "const user = " in fn_chunk or "let user = " in fn_chunk:
                pass
            elif user_direct_calls:
                issues.append(f"Chamada direta a .toUpperCase() em 'user' sem fallback defensivo")

        if issues:
            reports.append((entry, issues))

    return reports

if __name__ == "__main__":
    results = analyze_event_handling()
    print(f"Total de jogos com potenciais falhas de defensividade em eventos: {len(results)}")
    for game, issues in results:
        print(f"[{game}]: {issues}")
