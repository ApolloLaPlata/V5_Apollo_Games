import os
import re

GAMES = [
    "10_queda_dos_blocos",
    "23_sobrevivencia_na_lava",
    "24_campo_minado_neon",
    "25_batalha_naval_live",
    "28_labirinto_pacman_neon"
]

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

for g in GAMES:
    index_file = os.path.join(GAMES_DIR, g, "index.html")
    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # check if particles is declared
    has_particles = re.search(r'\b(const|let|var)\s+particles\s*=\s*\[\]', content)
    # check if reset clears particles
    reset_match = re.search(r'function\s+(reset\w*|restart\w*)\s*\([^)]*\)\s*\{([\s\S]*?)\n    \}', content)
    if has_particles and reset_match:
        fn_name = reset_match.group(1)
        body = reset_match.group(2)
        cleared = "particles.length = 0" in body or "particles = []" in body or "particles.splice" in body
        print(f"[{g}] has_particles=True, reset_fn={fn_name}, particles_cleared={cleared}")
