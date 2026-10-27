import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_intervals_for_gameover():
    results = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find all setInterval( ... )
        # Using a regex that captures the body of setInterval
        intervals = re.findall(r'setInterval\s*\(\s*(?:\(\)\s*=>|function\s*\(\))\s*\{([^}]+)\}', content)
        for i, body in enumerate(intervals):
            # Check if it spawns or mutates state without checking isGameOver or roundActive
            if ("spawn" in body or "drop" in body or "add" in body or "push" in body) and "isGameOver" not in body and "roundActive" not in body and "gameState" not in body and "state !==" not in body and "state!==" not in body:
                results.append((g, i, body.strip().replace("\n", " ")[:120]))

    print(f"Total de setIntervals sem verificação de estado de jogo: {len(results)}")
    for g, idx, snippet in results:
        print(f" - [{g}] interval #{idx}: {snippet}")

if __name__ == "__main__":
    check_intervals_for_gameover()
