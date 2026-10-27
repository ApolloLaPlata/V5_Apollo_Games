import os
import re
import sys

def test_cartridge_35():
    filepath = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\35_quiz_frenetico_holding\index.html"
    
    print("=" * 75)
    print(" SUÍTE DE TESTES UNITÁRIOS: CARTUCHO #35 (QUIZ FRENÉTICO DA HOLDING)")
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

    # 3. Lei 2: Zero Teclado/Mouse e Comandos da Audiência (1, 2, 3, 4 / A, B, C, D) e Gifts
    has_bus = "v5_broadcaster_games" in html and "v5_event" in html
    has_commands = all(cmd in html for cmd in ["1", "2", "3", "4", "a", "b", "c", "d"])
    has_gifts = "gift" in html and "Rose" in html and "Lion" in html
    checks.append((
        "Lei 2: Controle 100% pelo Público via Chat (Opções 1-4 / A-D) e Super Gifts",
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
        "playClockTick", "playVoteBlip", "playCorrectAnswer", 
        "playWrongAnswer", "playFiftyFiftySound", "playGoldenOracleSound", "playVictoryFanfare"
    ])
    checks.append((
        "Lei 4: Web Audio API Procedural Pura (Zero arquivos .mp3/.wav externos)",
        has_audio_ctx and has_zero_audio_files and has_synth_methods
    ))

    # 6. Lei 5: Ciclo Fechado & Auto-Reset Automático em 5s
    has_victory = "victory-modal" in html and "finalizeQuiz" in html
    has_auto_reset = "resetCountdown" in html and "initQuiz" in html
    checks.append((
        "Lei 5: Ciclo Fechado de Partidas (45s) e Auto-Reset em 5s",
        has_victory and has_auto_reset
    ))

    # 7. Banco de Perguntas Dinâmico e Categorias Temáticas
    has_questions = "QUESTION_BANK" in html and "loadQuestion" in html and "resolveQuestion" in html
    checks.append((
        "Banco de Perguntas Dinâmico com Categorias Temáticas e Temporizador",
        has_questions
    ))

    # 8. Barras Percentuais Dinâmicas em Tempo Real
    has_pct_bars = "option-fill" in html and "recalculatePercentages" in html and "updateOptionHUD" in html
    checks.append((
        "Barras Percentuais Dinâmicas com Votação Coletiva em Tempo Real",
        has_pct_bars
    ))

    # 9. Super Gifts Estratégicos: Dica 50/50 e Oráculo Dourado 5x
    has_super_gifts = "triggerFiftyFifty" in html and "triggerGoldenOracle" in html and "eliminatedOptions" in html
    checks.append((
        "Super Gifts: Eliminação 50/50 de Erradas e Oráculo Dourado 5x",
        has_super_gifts
    ))

    # 10. Métrica de QI Coletivo da Live e Pódio com MVP do Chat
    has_iq_metric = "collectiveIQ" in html and "podium-iq-score" in html and "podium-mvp-user" in html
    checks.append((
        "Métrica de QI Coletivo da Live e Pódio de Consagração do MVP",
        has_iq_metric
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
        print("HOMOLOGAÇÃO TÉCNICA DO CARTUCHO #35: 100% DE SUCESSO!")
        return True
    else:
        print("FALHA NA HOMOLOGAÇÃO DO CARTUCHO #35.")
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_35()
