import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def patch_all_audio_resume():
    modified = 0
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Replace .resume() without .catch
        # Look for (\.resume\(\))(?![\.\w]*catch)
        new_code = re.sub(r'(\b\w+\.resume\(\))(?!\s*\.catch)', r'\1.catch(() => {})', code)

        if new_code != code:
            with open(index_file, "w", encoding="utf-8") as f:
                f.write(new_code)
            modified += 1
            print(f"[PATCHED RESUME] {g}: .catch(() => {{}}) adicionado a .resume()")

    print(f"\nTotal de cartuchos atualizados com .catch() em resume: {modified}/41")

if __name__ == "__main__":
    patch_all_audio_resume()
