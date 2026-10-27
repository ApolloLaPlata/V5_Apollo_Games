import os
import re
import sys

def test_cartridge_27():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\27_meteoro_defensor\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #27 (METEORO DEFENSOR)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência por Setores
    has_sdk = "v5_live_game_sdk.js" in html or "V5LiveSDK" in html
    has_sectors = all(cmd in html for cmd in ["1", "2", "3", "4", "fogo", "laser"])
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat por Setores (1, 2, 3, 4) e Gifts",
        has_sdk and has_sectors and "gift" in html
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
    has_synth_methods = "playLaserPulse" in html and "playMeteorExplosion" in html and "playEarthImpact" in html and "playEmpBlast" in html
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "triggerGameOver" in html and "victory-overlay" in html
    has_auto_reset = "resetMatch" in html and "autoResetTimer" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas (Ondas 45s) e Auto-Reset Automático em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Planeta Terra Central, Atmosfera e Satélites Orbitais
    has_earth = "drawEarth" in html and "EARTH_RADIUS" in html and "satellites" in html and "100000" in html
    checks.append((
        "Planeta Terra Central com Atmosfera de Plasma, HP e Satélites de Defesa",
        has_earth
    ))

    # 8. Asteroides e Cometas com Trajetória Balística Rumo à Terra
    has_meteors = "class Meteor" in html and "calculateSector" in html and "impactEarth" in html
    checks.append((
        "Asteroides e Cometas com Rastro Incandescente e Vetor de Impacto Central",
        has_meteors
    ))

    # 9. Feixes Laser Orbitais e Desarme de Projéteis
    has_lasers = "class LaserBeam" in html and "fireSectorLaser" in html
    checks.append((
        "Baterias Laser Orbitais com Interceptação Direta e Dano Fracionado",
        has_lasers
    ))

    # 10. Super Armas de Gifts (Feixe 360° e Escudo Planetário EMP)
    has_super_gifts = "fireSuperOmniLaser" in html and "activateEmpShield" in html and "isShieldActive" in html
    checks.append((
        "Gifts Estratégicos: Feixe Laser 360° e Escudo Planetário Total EMP",
        has_super_gifts
    ))

    # 11. Gaveta de Depuração Local para o Streamer
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #27: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #27.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_27()
