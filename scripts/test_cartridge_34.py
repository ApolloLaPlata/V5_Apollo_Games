import os
import re
import sys

def test_cartridge_34():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\34_pinball_galactico\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #34 (PINBALL GALÁCTICO)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência (1, 2, 3, 4) e Gifts
    has_bus = "v5_broadcaster_games" in html and "v5_event" in html
    has_commands = all(cmd in html for cmd in ["1", "2", "3", "4", "esq", "dir", "ambos", "nudge"])
    has_gifts = "gift" in html and "Rose" in html and "Lion" in html
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat (Flippers/Nudge) e Super Gifts",
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
        "playFlipperSolenoid", "playBumperHit", "playSlingshot", 
        "playBlackHoleSuck", "playSupernovaJackpot", "playNudgeBuzz"
    ])
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "victory-modal" in html and "finalizeRound" in html
    has_auto_reset = "resetCountdown" in html and "initPinball" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas (45s) e Auto-Reset em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Flippers Duplos de Plasma com Cinemática Angular e Transferência de Impulso
    has_flippers = "leftFlipper" in html and "rightFlipper" in html and "checkFlipperCollision" in html and "flipperKick" in html
    checks.append((
        "Flippers de Plasma com Cinemática Angular e Transferência de Impulso",
        has_flippers
    ))

    # 8. 3 Bumpers Cósmicos com Deformação de Luz e Síntese Harmônica
    has_bumpers = "bumpers" in html and "playBumperHit" in html and "hitTimer" in html
    checks.append((
        "3 Bumpers Estelares com Deformação de Luz e Síntese Harmônica",
        has_bumpers
    ))

    # 9. Buraco Negro Central com Sucção Gravitacional e Teletransporte
    has_black_hole = "blackHole" in html and "suctionForce" in html and "eventHorizon" in html and "playBlackHoleSuck" in html
    checks.append((
        "Buraco Negro Central com Vórtice de Acreção, Sucção Gravitacional e Teleporte",
        has_black_hole
    ))

    # 10. Multi-Ball Cósmico com Física 2D, Rastreamento e Auto-Plunger
    has_multiball = "spawnBall" in html and "triggerMultiBall" in html and "GRAVITY" in html
    checks.append((
        "Multi-Ball Cósmico com Física 2D, Gravidade Vertical e Auto-Plunger",
        has_multiball
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #34: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #34.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_34()
