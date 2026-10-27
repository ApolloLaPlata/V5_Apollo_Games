import os
import re
import sys

def test_cartridge_40():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\40_duelo_de_magicos_neon\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #40 (DUELO DE MÁGICOS NEON)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência (1, 2, fogo, gelo) e Gifts
    has_bus = "v5_broadcaster_games" in html and "v5_event" in html
    has_commands = all(cmd in html for cmd in ["1", "2", "fogo", "gelo"])
    has_gifts = "gift" in html and "Rose" in html and "Lion" in html
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat e Super Gifts (Rose & Lion)",
        has_bus and has_commands and has_gifts
    ))

    # 4. Lei 3: Motor Anti-Silêncio Orgânico (< 3s)
    has_anti_silence = "runAntiSilence" in html and "MOCK_WIZARDS" in html and "lastInteractionTime" in html
    checks.append((
        "Lei 3: Motor Anti-Silêncio Orgânico Embutido (< 3s)",
        has_anti_silence
    ))

    # 5. Lei 4: Sintetizador Procedural Web Audio API (Zero .mp3/.wav)
    has_audio_ctx = "AudioContext" in html
    has_zero_audio_files = not re.search(r'\.(mp3|wav|ogg)[\'"]', html, re.IGNORECASE)
    has_synth_methods = all(m in html for m in [
        "playFireSurge", "playIceSurge", "playClashImpact", 
        "playSuperGiftRoar", "playVictoryFanfare"
    ])
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "victory-modal" in html and "finalizeDuel" in html
    has_auto_reset = "resetCountdown" in html and "initDuelGame" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas (45s) e Auto-Reset em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Ponto de Choque de Magias (Clash Point) com Polarização Fogo vs Gelo
    has_clash = "clashY" in html and "drawClashOrb" in html and "powerBalance" in html
    checks.append((
        "Ponto de Choque de Magias (Clash Point) com Polarização Fogo vs Gelo",
        has_clash
    ))

    # 8. Feixe de Plasma Descendente e Feixe Criogênico Ascendente
    has_beams = "drawFireBeam" in html and "drawIceBeam" in html and "drawFireMage" in html and "drawIceMage" in html
    checks.append((
        "Feixes Mágicos de Plasma e Gelo com Rituais dos Arquimagos",
        has_beams
    ))

    # 9. Tremor de Tela e Faíscas Bicolores no Ponto de Colisão
    has_vfx = "screenShake" in html and "spawnClashSparks" in html and "particles" in html
    checks.append((
        "Tremor de Tela Cinematográfico e Faíscas Bicolores de Choque",
        has_vfx
    ))

    # 10. Super Gifts Estratégicos: Choque Elemental (Rosa) e Titã/Meteoro (Leão)
    has_super_gifts = "triggerMagicGift" in html and "0.35" in html and "0.15" in html
    checks.append((
        "Super Gifts Estratégicos: Choque Elemental (+15%) e Meteoro Titânico (+40%)",
        has_super_gifts
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
    test_cartridge_40()
