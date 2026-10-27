import os

bus_path = r"C:\Users\v5est\.gemini\antigravity\brain\9270dd65-160e-47e8-aea2-6a92fd50cfc6\antigravity_hive_bus.md"

entry = """
### [27/10/2026 - 16:15] CAPITANIA V5 GAMES - ETAPA 084 CONCLUÍDA: CARTUCHO #29 BASQUETE STREET NEON
- **Cartucho Homologado:** `29_basquete_street_neon` (Basquete Street Neon da Live - Tabela Móvel & Física 2D 9:16).
- **Inovações de Engenharia:**
  1. Tabela de acrílico móvel com oscilação senoidal contínua ($x(t) = x_0 + A \sin(\omega t)$), aro metálico duplo com amortecedor e rede elástica com ondulação procedural de chuá.
  2. Arremessos 100% acionados pelo chat através de comandos numéricos e de força (1: Suave, 2: Perfeito, 3: Forte/Direto) com parábolas balísticas e detecção de rebote na tabela e ricochete no aro.
  3. Lógica de detecção de cesta limpa (Swish/Chuá +3 pts com faíscas douradas) vs cesta normal (+2 pts) com sistema de combos progressivos da live.
  4. Super Gifts Estratégicos: Bola de Fogo (3x pontuação com rastro de chamas) e Ímã Magnético Slam Dunk no aro (atrai todas as bolas para dentro da cesta por 8s).
  5. Síntese Web Audio API procedural completa: drible seco no asfalto, estalo metálico no aro (modulação em anel), som de tecido elástico de chuá e buzina clássica de estádio.
  6. Ciclo fechado de 45s com auto-reset em 5s e pódio do Maior Cestinha da Live (MVP).
- **Homologação:** 11/11 verificações aprovadas em `scripts/test_cartridge_29.py`.
- **Sincronização:** Total de 30 jogos homologados e sincronizados no V5 Broadcaster (`v5_games_manifest.json`).
- **Próxima Etapa:** Etapa 085 — Forjamento do Cartucho #30: Gol de Pênalti da Live (Disputa entre batedor e goleiro).
"""

if os.path.exists(bus_path):
    with open(bus_path, "a", encoding="utf-8") as f:
        f.write(entry)
    print("Hive Bus updated successfully!")
else:
    print(f"Path not found: {bus_path}")
