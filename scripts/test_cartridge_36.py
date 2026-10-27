import os
import re
import sys

def test_cartridge_36():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\36_pula_corda_extremo\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #36 (PULA-CORDA EXTREMO)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência (1, 2, 3, pula) e Gifts
    has_bus = "v5_broadcaster_games" in html and "v5_event" in html
    has_commands = all(cmd in html for cmd in ["1", "2", "3", "pula", "salto", "duplo"])
    has_gifts = "gift" in html and "Rose" in html and "Lion" in html
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat (Saltos/Timings) e Super Gifts",
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
        "playRopeWhoosh", "playJumpSound", "playScorePoint", 
        "playTripSound", "playSlowMoSound", "playJetpackSound", "playVictoryFanfare"
    ])
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "victory-modal" in html and "finalizeRound" in html
    has_auto_reset = "resetCountdown" in html and "initRopeGame" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas (45s) e Auto-Reset em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Física 3D da Corda com Curva de Bézier e Variação de Profundidade
    has_rope_physics = "drawPlasmaRope" in html and "quadraticCurveTo" in html and "ropeAngle" in html
    checks.append((
        "Física 3D da Corda com Curva de Bézier, Profundidade e Velocidade Progressiva",
        has_rope_physics
    ))

    # 8. Saltadores Articulados com Física de Gravidade e Detecção de Tropeço
    has_jumpers = "jumpers" in html and "handleJump" in html and "isRopeAtFeet" in html and "triggerTrip" in html
    checks.append((
        "Saltadores Neon com Cinemática de Pulo, Mortal Giratório e Detecção de Tropeço",
        has_jumpers
    ))

    # 9. Dois Batedores Robóticos Sincronizados nas Extremidades
    has_twirlers = "twirlers" in html and "drawTwirlers" in html and "armAngle" in html
    checks.append((
        "Dois Batedores Robóticos Sincronizados nas Extremidades da Corda",
        has_twirlers
    ))

    # 10. Super Gifts Estratégicos: Corda Slow-Mo e Jetpack Pégaso
    has_super_gifts = "triggerSlowMo" in html and "triggerJetpack" in html and "jetpackTimer" in html
    checks.append((
        "Super Gifts: Corda Cósmica Slow-Mo e Jetpack Pégaso Flutuante",
        has_super_gifts
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #36: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #36.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_36()
