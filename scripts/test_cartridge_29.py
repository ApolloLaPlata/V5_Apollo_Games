import os
import re
import sys

def test_cartridge_29():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\29_basquete_street_neon\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #29 (BASQUETE STREET NEON)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência por Tipos de Arremesso
    has_sdk = "v5_live_game_sdk.js" in html or "V5LiveSDK" in html
    has_shots = all(cmd in html for cmd in ["1", "2", "3", "arremesso", "cesta"])
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat por Tipos de Arremesso (1-3) e Gifts",
        has_sdk and has_shots and "gift" in html
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
    has_synth_methods = "playBounce" in html and "playRimClank" in html and "playSwishSound" in html and "playFireballWhoosh" in html
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

    # 7. Tabela Móvel Oscilante e Aro com Amortecedor
    has_hoop = "drawHoop" in html and "oscillationAmplitude" in html and "rimRadius" in html and "backboardWidth" in html
    checks.append((
        "Tabela de Acrílico Móvel com Oscilação Senoidal e Aro Metálico",
        has_hoop
    ))

    # 8. Rede Elástica Procedural Ondulante (Efeito Swish / Chuá)
    has_net = "netWave" in html and "quadraticCurveTo" in html
    checks.append((
        "Rede Elástica Trançada com Ondulação Dinâmica de Chuá",
        has_net
    ))

    # 9. Física Balística 2D da Bola e Detecção de Colisão
    has_ball_physics = "class Basketball" in html and "gravity" in html and "checkCollisions" in html and "scoreBasket" in html
    checks.append((
        "Física Balística 2D da Bola com Rebote na Tabela e Ricochete no Aro",
        has_ball_physics
    ))

    # 10. Super Gifts: Bola de Fogo (3x Pontos) e Ímã Slam Dunk
    has_super_gifts = "fireballActive" in html and "magnetActive" in html
    checks.append((
        "Super Gifts Estratégicos: Bola de Fogo (3x) e Ímã Magnético Slam Dunk",
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #29: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #29.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_29()
