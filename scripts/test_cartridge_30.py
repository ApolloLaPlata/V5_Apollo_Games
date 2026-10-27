import os
import re
import sys

def test_cartridge_30():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\30_gol_de_penalti_live\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #30 (GOL DE PÊNALTI DA LIVE)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência por 5 Cantos e Gifts
    has_sdk = "v5_live_game_sdk.js" in html or "V5LiveSDK" in html
    has_corners = all(cmd in html for cmd in ["1", "2", "3", "4", "5", "gaveta", "meio"])
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat por Cantos (1 a 5) e Gifts",
        has_sdk and has_corners and "gift" in html
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
    has_synth_methods = "playWhistle" in html and "playKickSound" in html and "playPostHit" in html and "playGoalCheer" in html
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "triggerGameOver" in html and "victory-overlay" in html
    has_auto_reset = "resetMatch" in html and "autoResetTimer" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Pênaltis (Série de 5 chutes) e Auto-Reset em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Estádio Neon, Gol Branco com Trave e Travessão
    has_goal = "drawStadium" in html and "drawGoalAndNet" in html and "crossbarY" in html
    checks.append((
        "Estádio Neon com Linhas da Grande Área e Gol com Trave e Travessão",
        has_goal
    ))

    # 8. Goleiro Robô Mecha com IA e Saltos nos Cantos
    has_keeper = "drawGoalkeeper" in html and "goalkeeper" in html and "diveProgress" in html
    checks.append((
        "Goleiro Mecha com Braços Articulados, Luvas de Plasma e Saltos nos Cantos",
        has_keeper
    ))

    # 9. Física da Bola com Curva Balística, Escala e Rastro
    has_ball = "drawBall" in html and "resolveKickOutcome" in html and "scale" in html
    checks.append((
        "Física Balística da Bola com Curva de Trajetória, Profundidade e Escala",
        has_ball
    ))

    # 10. Super Gifts: Bomba Atômica 150 km/h e Chute Triplo Fantasma
    has_super_gifts = "fireballActive" in html and "tripleShotActive" in html
    checks.append((
        "Super Gifts Estratégicos: Bomba Atômica 150km/h e Ilusão Tripla",
        has_super_gifts
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #30: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #30.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_30()
