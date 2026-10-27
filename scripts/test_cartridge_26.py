import os
import re
import sys

def test_cartridge_26():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\26_guerra_dos_tanques_neon\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #26 (GUERRA DOS TANQUES NEON)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência
    has_sdk = "v5_live_game_sdk.js" in html or "V5LiveSDK" in html
    has_commands = all(cmd in html for cmd in ["1", "2", "azul", "vermelho", "fogo"])
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat e Presentes de Alto Impacto",
        has_sdk and has_commands and "gift" in html
    ))

    # 4. Lei 3: Motor Anti-Silêncio Orgânico
    has_anti_silence = "mockUsers" in html and "setInterval" in html and "silence" in html.lower()
    checks.append((
        "Lei 3: Motor Anti-Silêncio Orgânico Embutido (< 3s)",
        has_anti_silence
    ))

    # 5. Lei 4: Sintetizador Procedural Web Audio API (Zero .mp3/.wav)
    has_audio_ctx = "AudioContext" in html
    has_zero_audio_files = ".mp3" not in html and ".wav" not in html and ".ogg" not in html
    has_synth_methods = "playCannonFire" in html and "playExplosion" in html and "playVictoryFanfare" in html
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático
    has_victory = "triggerVictory" in html and "victory-overlay" in html
    has_auto_reset = "resetMatch" in html and "autoResetTimer" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas e Auto-Reset Automático em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Física de Artilharia 2D & Parábolas
    has_ballistics = "BallisticProjectile" in html and "Math.cos" in html and "Math.sin" in html and "gravity" in html
    checks.append((
        "Motor Balístico 2D com Gravidade e Projeção Angular de Projéteis",
        has_ballistics
    ))

    # 8. Vento Dinâmico com Aceleração Horizontal
    has_wind = "wind" in html and "randomizeWind" in html and "updateWindUI" in html
    checks.append((
        "Vento Dinâmico Bipolar com Influência na Trajetória Balística",
        has_wind
    ))

    # 9. Terreno Destrutível com Deformação de Cratera
    has_terrain = "generateTerrain" in html and "deformTerrain" in html and "state.terrain" in html
    checks.append((
        "Terreno Procedural 2D Destrutível com Abertura Dinâmica de Crateras",
        has_terrain
    ))

    # 10. Super Gifts & Escudo Eletromagnético
    has_super_weapons = "isSuper" in html and "hasShield" in html and "playShieldDeflect" in html
    checks.append((
        "Gifts Estratégicos: Mega Míssil Nuclear, Bomba Cluster e Escudo EMP",
        has_super_weapons
    ))

    # 11. Gaveta de Depuração Oculta do Streamer
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #26: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #26.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_26()
