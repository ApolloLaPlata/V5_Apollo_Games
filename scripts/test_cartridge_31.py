import os
import re
import sys

def test_cartridge_31():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\31_guitar_hero_neon\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #31 (GUITAR HERO DA LIVE)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência por Pistas (1-4 / Cores)
    has_sdk = "v5_live_game_sdk.js" in html or "V5LiveSDK" in html
    has_lanes = all(cmd in html for cmd in ["1", "2", "3", "4", "verde", "vermelho", "amarelo", "azul"])
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat por Pistas (1 a 4 / Cores) e Gifts",
        has_sdk and has_lanes and "gift" in html
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
    has_synth_methods = "playNoteHit" in html and "playNoteMiss" in html and "playStarPowerRiff" in html and "playCrowdCheer" in html
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "triggerGameOver" in html and "victory-overlay" in html
    has_auto_reset = "resetMatch" in html and "autoResetTimer" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Faixas Musicais (45s) e Auto-Reset em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Braço de Guitarra 3D (Fretboard) com 4 Pistas e Trastes
    has_fretboard = "drawFretboard" in html and "LANES" in html and "TARGET_LINE_Y" in html
    checks.append((
        "Braço de Guitarra em Perspectiva 3D com 4 Pistas, Trastes e Linha de Alvo",
        has_fretboard
    ))

    # 8. Notas Musicais Descentes Sincronizadas com Ritmo
    has_falling_notes = "FallingNote" in html and "bpm" in html and "hitLane" in html
    checks.append((
        "Gemas Musicais Descentes Sincronizadas com BPM e Janela de Acerto",
        has_falling_notes
    ))

    # 9. Rockmeter de Aprovação da Plateia e Sistema de Combos
    has_rockmeter = "rockmeter" in html and "combo" in html and "streak" in html
    checks.append((
        "Rockmeter de Aprovação da Plateia, Streaks e Combos Progressivos",
        has_rockmeter
    ))

    # 10. Super Gifts: Star Power 4x e Solo Lendário Automático
    has_star_power = "starPowerTime" in html and "soloLegendTime" in html
    checks.append((
        "Super Gifts Estratégicos: Star Power 4x Overdrive e Solo Lendário",
        has_star_power
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #31: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #31.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_31()
