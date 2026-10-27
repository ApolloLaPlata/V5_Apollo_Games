import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def apply_mobile_and_channel_hardening():
    patched_css = 0
    patched_channel = 0

    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            code = f.read()

        mod = code

        # 1. Add user-select: none; touch-action: none; to body if missing
        if "touch-action: none" not in mod:
            # find body {
            body_match = re.search(r'(body\s*\{[^}]*?)(\})', mod)
            if body_match:
                existing_body = body_match.group(1)
                new_props = ""
                if "user-select: none" not in existing_body:
                    new_props += "\n      user-select: none;\n      -webkit-user-select: none;"
                new_props += "\n      touch-action: none;"
                
                new_body = existing_body + new_props + "\n    }"
                mod = mod[:body_match.start()] + new_body + mod[body_match.end():]
                patched_css += 1

        # 2. Add beforeunload to close BroadcastChannel
        # Look for const channel = new BroadcastChannel... or const liveChannel = ...
        if "new BroadcastChannel" in mod and "beforeunload" not in mod:
            # find channel.onmessage = ...
            channel_match = re.search(r'(\b(\w+)\s*=\s*new\s+BroadcastChannel\([^\)]+\);[\s\S]*?\2\.onmessage\s*=\s*[^;]+;)', mod)
            if channel_match:
                full_stmt = channel_match.group(1)
                ch_var = channel_match.group(2)
                cleanup_stmt = f"\n      window.addEventListener('beforeunload', () => {{ try {{ {ch_var}.close(); }} catch(e) {{}} }});"
                mod = mod.replace(full_stmt, full_stmt + cleanup_stmt, 1)
                patched_channel += 1

        if mod != code:
            with open(index_file, "w", encoding="utf-8") as f:
                f.write(mod)
            print(f"[HARDENED] {g}")

    print(f"\nResumo de Blindagem:")
    print(f" - Cartuchos com CSS touch-action e user-select aplicados: {patched_css}")
    print(f" - Cartuchos com beforeunload BroadcastChannel.close(): {patched_channel}")

if __name__ == "__main__":
    apply_mobile_and_channel_hardening()
