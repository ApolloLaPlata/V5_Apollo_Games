import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

for entry in sorted(os.listdir(GAMES_DIR)):
    index_path = os.path.join(GAMES_DIR, entry, "index.html")
    if not os.path.isfile(index_path):
        continue
    with open(index_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    has_audio = "AudioContext" in code
    has_resume = "resume()" in code
    if has_audio and not has_resume:
        print(f"Game without audioCtx.resume(): {entry}")
