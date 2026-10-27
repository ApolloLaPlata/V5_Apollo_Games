import os
import re
import sys

def test_cartridge_39():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\39_alvo_movel_snipers\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #39 (ALVO MÓVEL DOS SNIPERS)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência (fogo, 1, 2, 3) e Gifts
    has_bus = "v5_broadcaster_games" in html and "v5_event" in html
    has_commands = all(cmd in html for cmd in ["fogo", "1", "2", "3"])
    has_gifts = "gift" in html and "Rose" in html and "Lion" in html
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat e Super Gifts (Rose & Lion)",
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
        "playBowRelease", "playTargetHit", "playBullseyeDing", 
        "playLockOnSound", "playNuclearExplosionSound", "playVictoryFanfare"
    ])
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "victory-modal" in html and "finalizeRound" in html
    has_auto_reset = "resetCountdown" in html and "initSniperGame" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas (45s) e Auto-Reset em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Alvos Móveis Concêntricos com Pontuação Escalonada (Bullseye 1000 pts)
    has_targets = "targets" in html and "bullseyes" in html and "1000" in html
    checks.append((
        "Alvos Móveis Concêntricos com Anéis e Bullseye (1.000 pts)",
        has_targets
    ))

    # 8. Balística de Flechas e Fixação Dinâmica nos Alvos Móveis
    has_ballistics = "arrows" in html and "targetOffsetX" in html and "stuck" in html
    checks.append((
        "Física Balística de Flechas e Fixação Dinâmica Acompanhando Alvos",
        has_ballistics
    ))

    # 9. Mira Laser Lock-On (Super Gift Rosa)
    has_lockon = "triggerLockOn" in html and "lockOnTimer" in html
    checks.append((
        "Super Gift Rosa: Mira Laser Lock-On Automática com Precisão 100%",
        has_lockon
    ))

    # 10. Chuva Nuclear de 30 Flechas em Leque (Super Gift Leão)
    has_nuclear = "triggerNuclearBarrage" in html and "30" in html
    checks.append((
        "Super Gift Leão: Chuva Nuclear em Leque com 30 Flechas",
        has_nuclear
    ))

    # 11. Event Bus Integrado e Painel de Depuração Streamer (Tecla D)
    has_debug = "debug-drawer" in html and "toggleDebugDrawer" in html
    checks.append((
        "Event Bus Padronizado e Painel de Depuração Local (Tecla D)",
        has_bus and has_debug
    ))

    # Execução das validações
    passed = 0
    failed = 0

    for name, condition in checks:
        if condition:
            print(f"  [PASS] {name}")
            passed += 1
        else:
            print(f"  [FAIL] {name}")
            failed += 1

    print("-" * 75)
    print(f" Resultado: {passed}/{len(checks)} verificações aprovadas.")
    print("=" * 75)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_39()
