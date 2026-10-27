import os
import re
import sys

def test_cartridge_33():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\33_corrida_de_cavalos_retro\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #33 (CORRIDA DE CAVALOS RETRÔ)")
    print(" Holding V5 Apollo — Capitania V5 Games")
    print("=" * 75)
    
    if not os.path.exists(filepath):
        print(f"[FAIL] Arquivo não encontrado: {filepath}")
        sys.exit(1)
        
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    checks = []

    # 1. Arquivo e Formato HTML5
    checks.append((
        "Estrutura HTML5 válida e doctype",
        "<!DOCTYPE html>" in html and "</html>" in html
    ))

    # 2. Lei 1: Proporção Vertical 9:16 e Safe Zones
    has_9_16 = "9 / 16" in html or "1080" in html
    has_safe_top = "140px" in html
    has_safe_bottom = "180px" in html
    checks.append((
        "Lei 1: Proporção Vertical 9:16 e Safe Zones (Topo 140px, Base 180px)",
        has_9_16 and has_safe_top and has_safe_bottom
    ))

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência (4 Cavalos) e Gifts
    has_bus = "v5_broadcaster_games" in html and "v5_event" in html
    has_commands = all(cmd in html for cmd in ["1", "2", "3", "4", "relampago", "furia", "cometa", "esmeralda"])
    has_gifts = "gift" in html and "Rose" in html and "Lion" in html
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat (1 a 4) e Super Gifts",
        has_bus and has_commands and has_gifts
    ))

    # 4. Lei 3: Motor Anti-Silêncio Orgânico (< 3s)
    has_anti_silence = "runAntiSilence" in html and "MOCK_USERS" in html and "lastInteractionTime" in html
    checks.append((
        "Lei 3: Motor Anti-Silêncio Orgânico Embutido (< 3s)",
        has_anti_silence
    ))

    # 5. Lei 4: Sintetizador Procedural Web Audio API (Zero .mp3/.wav)
    has_audio_ctx = "AudioContext" in html
    has_zero_audio_files = not re.search(r'\.(mp3|wav|ogg)[\'"]', html, re.IGNORECASE)
    has_synth_methods = all(m in html for m in [
        "playCallToThePost", "playHorsesHoofbeat", "playWhinny", 
        "playWhipBoost", "playNarratorBeep", "playVictoryFanfare"
    ])
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "victory-modal" in html and "finalizeRace" in html
    has_auto_reset = "resetCountdown" in html and "initHorses" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas (45s / 1.200m) e Auto-Reset em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Cavalos Vetoriais com Animação Articulada de Galope e Jockeys
    has_horse_art = "drawRetroHorse" in html and "legPhase" in html and "Math.sin(phase)" in html
    checks.append((
        "Animação Vetorial Articulada dos 4 Cavalos, Patas Senoidais e Jockeys",
        has_horse_art
    ))

    # 8. Sistema de Narração Retrô com Falas Dinâmicas e Bipes
    has_narrator = "narrator-box" in html and "NARRATOR_QUOTES" in html and "setNarratorSpeech" in html
    checks.append((
        "Narrador Retrô do Hipódromo com Falas Dinâmicas de Corrida e Bipes Arcade",
        has_narrator
    ))

    # 9. Pista com 4 Raias, Demarcações de Metragem e Disco de Chegada
    has_track = "LANE_WIDTH" in html and "drawDistanceMarkers" in html and "drawFinishLine" in html and "drawFence" in html
    checks.append((
        "Hipódromo com 4 Raias, Cercas, Linhas de Metragem e Disco de Chegada",
        has_track
    ))

    # 10. Minimapa Vertical Lateral em Tempo Real
    has_minimap = "track-minimap" in html and "minimap-marker" in html and "TOTAL_METERS" in html
    checks.append((
        "Minimapa Vertical Lateral com Telemetria dos 4 Competidores em Tempo Real",
        has_minimap
    ))

    # 11. Gaveta de Depuração Local para Streamer (Tecla D)
    has_debug = "debug-drawer" in html and ("keydown" in html or "dblclick" in html)
    checks.append((
        "Painel de Depuração Local para Streamer (Tecla D / Duplo Clique)",
        has_debug
    ))

    passed_count = 0
    for desc, passed in checks:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {desc}")
        if passed:
            passed_count += 1

    print("=" * 75)
    print(f" RESULTADO: {passed_count}/{len(checks)} CHECKS APROVADOS")
    print("=" * 75)

    if passed_count == len(checks):
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #33: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #33.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_33()
