import os

bus_path = r"C:\Users\v5est\.gemini\antigravity\brain\9270dd65-160e-47e8-aea2-6a92fd50cfc6\antigravity_hive_bus.md"

entry = """
### [27/10/2026 - 11:45] CAPITANIA V5 GAMES - ETAPAS 064 E 065 CONCLUÍDAS: CARTUCHO #21 BATATA QUENTE EXPLOSIVA
- **Cartucho Homologado:** `21_batata_quente_explosiva` (Batata Quente Explosiva - BPM Cardíaco & Eliminação 9:16).
- **Inovações de Engenharia:**
  1. Bomba esférica com pavio aceso voando em trajetória parabólica suave entre 5 avatares posicionados na tela vertical.
  2. Sintetizador procedural de áudio (Web Audio API - Etapa 065): chiado contínuo estalante de pavio (`startFuseSound`), pulso cardíaco tum-tum cuja cadência escala de 75 BPM para 180 BPM nos segundos finais, whoosh de passe e detonação de 35Hz.
  3. Vinheta visual periférica de estresse pulsando em sincronia com os batimentos cardíacos.
  4. Tempo de detonação secreto entre 22s e 38s garantindo suspense absoluto na live.
  5. Presentes ativam Escudo Repulsor que arremessa a bomba e dá 3.5s de imunidade com spotlight.
- **Sincronização:** Total de 20 cartuchos ativos no Broadcaster (`v5_games_manifest.json`).
- **Próximas Etapas:** Etapa 066 — Forjamento do Cartucho #22: Ponte de Vidro Quebradiço (Escolha esquerda/direita com precipício).
"""

if os.path.exists(bus_path):
    with open(bus_path, "a", encoding="utf-8") as f:
        f.write(entry)
    print("Hive Bus updated successfully!")
else:
    print(f"Path not found: {bus_path}")

