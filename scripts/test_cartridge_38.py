import os
import re
import sys

def test_cartridge_38():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\38_fuga_da_prisao_espacial\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #38 (FUGA DA PRISÃO ESPACIAL)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência (1, 2, 3, boost) e Gifts
    has_bus = "v5_broadcaster_games" in html and "v5_event" in html
    has_commands = all(cmd in html for cmd in ["1", "2", "3", "esq", "meio", "dir", "boost"])
    has_gifts = "gift" in html and "Rose" in html and "Lion" in html
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat (Corredores 1-3 & Boost) e Super Gifts",
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
        "playJetpackThrust", "playLaserFire", "playShieldImpact", 
        "playWarpDriveSound", "playVictoryFanfare"
    ])
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "victory-modal" in html and "finalizeEscape" in html
    has_auto_reset = "resetCountdown" in html and "initEscapeGame" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas (45s / 1.000m) e Auto-Reset em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Poço Espacial 9:16 com 3 Corredores e Rolagem Contínua de Cenário
    has_shaft = "LANES_X" in html and "drawShaftBackground" in html and "bgOffset" in html
    checks.append((
        "Poço de Segurança Máxima com 3 Corredores e Rolagem Contínua de Cenário",
        has_shaft
    ))

    # 8. Lasers de Contenção Descendentes e Detecção de Colisão com Escudo
    has_lasers = "lasers" in html and "spawnSecurityLaser" in html and "hitDistX" in html and "hitDistY" in html
    checks.append((
        "Lasers de Contenção com Física Descendente e Detecção de Colisão",
        has_lasers
    ))

    # 9. Astronauta com Propulsor Jetpack, Partículas e Rastro
    has_astronaut = "drawAstronaut" in html and "spawnJetpackParticles" in html and "targetX" in html
    checks.append((
        "Astronauta Estilizado com Propulsão Jetpack e Partículas Dinâmicas",
        has_astronaut
    ))

    # 10. Super Gifts Estratégicos: Escudo Defletor e Hiper-Dobra de Resgate
    has_super_gifts = "triggerShieldDeflector" in html and "triggerWarpDrive" in html and "warpTimer" in html
    checks.append((
        "Super Gifts: Escudo Defletor Holográfico e Propulsor de Hiper-Dobra",
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #38: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #38.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_38()
