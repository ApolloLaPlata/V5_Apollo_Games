import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_audio_resumes():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        if "AudioContext" in content:
            # check if resume is present
            if "resume()" not in content:
                findings.append((g, "Sem chamada a resume()"))
            elif "state === 'suspended'" not in content and 'state === "suspended"' not in content:
                findings.append((g, "Chama resume() sem checar state === 'suspended'"))

    print(f"Total de questões de audio resume: {len(findings)}")
    for g, issue in findings:
        print(f" - [{g}] {issue}")
    return findings

if __name__ == "__main__":
    check_audio_resumes()
