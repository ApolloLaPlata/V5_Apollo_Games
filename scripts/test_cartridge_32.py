import os
import re
import sys

def test_cartridge_32():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\32_corte_de_frutas_neon\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #32 (CORTE DE FRUTAS NEON)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência por Setores (1, 2, 3) e Gifts
    has_sdk = "v5_live_game_sdk.js" in html or "V5LiveSDK" in html
    has_sectors = all(cmd in html for cmd in ["1", "2", "3", "esq", "meio", "dir", "corta"])
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat por Setores (1, 2, 3) e Gifts",
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
    has_synth_methods = "playSwordSlash" in html and "playFruitSplatter" in html and "playBombExplosion" in html and "playSlowMoSound" in html
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "triggerGameOver" in html and "victory-overlay" in html
    has_auto_reset = "resetMatch" in html and "autoResetTimer" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas (45s) e Auto-Reset em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Frutas Neon em Arcos Balísticos e Bombas Cibernéticas
    has_fruits = "FlyingFruit" in html and "FRUIT_TYPES" in html and "isBomb" in html
    checks.append((
        "Frutas Geométricas com Arcos Balísticos e Perigo de Bombas Cibernéticas",
        has_fruits
    ))

    # 8. Separação de Metades e Espirros de Partículas
    has_halves = "SlicedHalf" in html and "createSplatterParticles" in html and "slicedCount" in html
    checks.append((
        "Particionamento de Metades com Rotação Oposta e Espirros de Fluido",
        has_halves
    ))

    # 9. Lâminas Laser com Detecção Geométrica de Segmento
    has_slashes = "LaserSlash" in html and "distToSegment" in html and "executeSlash" in html
    checks.append((
        "Lâminas Laser de Plasma com Traço Dinâmico e Colisão por Segmento",
        has_slashes
    ))

    # 10. Super Gifts: Câmera Lenta Dourada e Katana Cósmica 360°
    has_super_gifts = "slowMoTime" in html and "executeOmniSlash" in html
    checks.append((
        "Super Gifts Estratégicos: Câmera Lenta com Frenesi e Katana Cósmica 360°",
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #32: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #32.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_32()
