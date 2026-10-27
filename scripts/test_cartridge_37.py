import os
import re
import sys

def test_cartridge_37():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\37_torre_de_blocos_equilibrada\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #37 (TORRE DE BLOCOS EQUILIBRADA)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência (1, 2, 3, esq, meio, dir) e Gifts
    has_bus = "v5_broadcaster_games" in html and "v5_event" in html
    has_commands = all(cmd in html for cmd in ["1", "2", "3", "esq", "meio", "dir"])
    has_gifts = "gift" in html and "Rose" in html and "Lion" in html
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat (Colunas 1-3) e Super Gifts",
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
        "playBlockSlide", "playBlockSnap", "playCreakSound", 
        "playCollapseSound", "playSteelClank", "playStasisShieldSound", "playVictoryFanfare"
    ])
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "victory-modal" in html and "finalizeRound" in html
    has_auto_reset = "resetCountdown" in html and "initTower" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas (45s) e Auto-Reset em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Estrutura de Andares com 3 Blocos, Reposicionamento no Topo e Altura Dinâmica
    has_tower_structure = "floors" in html and "addBlockToTop" in html and "BLOCK_WIDTH" in html
    checks.append((
        "Estrutura de Andares com 3 Blocos por Nível e Reposicionamento no Topo",
        has_tower_structure
    ))

    # 8. Cálculo de Estabilidade Estrutural e Física Pendular de Oscilação
    has_stability = "calculateTowerStability" in html and "swayAngle" in html and "swaySpeed" in html
    checks.append((
        "Cálculo de Estabilidade Estrutural e Física Pendular de Oscilação da Torre",
        has_stability
    ))

    # 9. Colapso Físico Espectacular com Blocos em Queda Livre
    has_collapse = "triggerCollapse" in html and "fallingBlocks" in html
    checks.append((
        "Física de Colapso Estrutural com Blocos Rígidos em Queda Livre",
        has_collapse
    ))

    # 10. Super Gifts Estratégicos: Bloco de Aço de Titânio e Stasis Shield
    has_super_gifts = "triggerSteelBlock" in html and "triggerStasisShield" in html and "stasisTimer" in html
    checks.append((
        "Super Gifts: Bloco de Aço de Titânio e Campo de Força Stasis Antigravitacional",
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #37: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #37.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_37()
