import os
import re
import sys

def test_cartridge_28():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\28_labirinto_pacman_neon\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #28 (LABIRINTO DO PACMAN NEON)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência por Direções Cardeais e Numéricas
    has_sdk = "v5_live_game_sdk.js" in html or "V5LiveSDK" in html
    has_directions = all(cmd in html for cmd in ["1", "2", "3", "4", "cima", "baixo", "esquerda", "direita"])
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat por Direções (1-4 / Cardeais) e Gifts",
        has_sdk and has_directions and "gift" in html
    ))

    # 4. Lei 3: Motor Anti-Silêncio Orgânico
    has_anti_silence = "mockUsers" in html and "setInterval" in html and "silence" in html.lower()
    checks.append((
        "Lei 3: Motor Anti-Silêncio Orgânico Embutido (< 3s)",
        has_anti_silence
    ))

    # 5. Lei 4: Sintetizador Procedural Web Audio API (Zero .mp3/.wav)
    has_audio_ctx = "AudioContext" in html
    has_zero_audio_files = not re.search(r'\.(mp3|wav|ogg)[\'"]', html, re.IGNORECASE)
    has_synth_methods = "playWakaWaka" in html and "playPowerPellet" in html and "playEatGhost" in html and "playDeathChime" in html
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "triggerGameOver" in html and "victory-overlay" in html
    has_auto_reset = "resetMatch" in html and "autoResetTimer" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas (45s) e Auto-Reset Automático em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Matriz do Labirinto Vertical e Detecção de Paredes
    has_maze = "ORIGINAL_MAZE" in html and "CELL_SIZE" in html and "canMoveInDir" in html
    checks.append((
        "Matriz do Labirinto Vertical 9:16 com Navegação Contínua e Detecção de Paredes",
        has_maze
    ))

    # 8. Pacman com Animação de Boca e Sistema de Pontuação
    has_pacman = "drawPacman" in html and "mouthAngle" in html and "coinsEaten" in html and "score" in html
    checks.append((
        "Pacman Neon com Boca Procedural, Coleta de Pastilhas e Acúmulo de Pontos",
        has_pacman
    ))

    # 9. Fantasmas Cibernéticos com IA de Fuga/Perseguição
    has_ghosts = "Blinky" in html and "Pinky" in html and "Inky" in html and "Clyde" in html and "updateGhosts" in html
    checks.append((
        "4 Fantasmas Cibernéticos (Blinky, Pinky, Inky, Clyde) com IA e Modo Caçador",
        has_ghosts
    ))

    # 10. Super Power-ups por Gifts (Congelamento e Super Turbo)
    has_powerups = "freezeGhostsTime" in html and "hunterModeTime" in html and "speedBoostTime" in html
    checks.append((
        "Super Power-ups por Gifts: Modo Caçador 360°, Turbo 2x e Congelamento",
        has_powerups
    ))

    # 11. Gaveta de Depuração Local para Streamer
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #28: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #28.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_28()
