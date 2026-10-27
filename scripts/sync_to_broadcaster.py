import os
import shutil
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_DIR = os.path.join(BASE_DIR, "catalogo_jogos")
BROADCASTER_GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games"

GAME_METADATA = {
    "01_cabo_de_guerra_neon": {
        "name": "Cabo de Guerra Neon",
        "category": "polarizacao",
        "description": "Cabo de guerra neon 1v1 disputado por votos no chat e presentes aceleradores",
        "commands": ["1", "2"],
        "status": "HOMOLOGADO",
        "version": "2.0.0"
    },
    "01b_cabo_de_guerra_elementos": {
        "name": "Cabo de Guerra dos Elementos",
        "category": "polarizacao",
        "description": "Fogo Vermelho vs Gelo Azul com termômetro dinâmico (-100°C a +1000°C) e partículas térmicas",
        "commands": ["1", "2", "fogo", "gelo"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "02_plinko_pachinko_fortuna": {
        "name": "Plinko da Fortuna",
        "category": "fisica_pachinko",
        "description": "Pachinko vertical com física de pinos, canaletas multiplicadoras e 50x Jackpot",
        "commands": ["1", "2", "3"],
        "status": "HOMOLOGADO",
        "version": "2.0.0"
    },
    "03_corrida_avatares_holding": {
        "name": "Corrida dos Avatares da Holding",
        "category": "corrida_velocidade",
        "description": "Roxingo, Baiano e Macaco Driver disputando circuito pseudo-3D com nitros acionados pelo chat",
        "commands": ["1", "2", "3", "roxingo", "baiano", "macaco"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "04_boss_raid_cooperativo": {
        "name": "Boss Raid do Chat",
        "category": "cooperativo_boss",
        "description": "Titã Neon com 1.000.000 HP enfrentando o chat inteiro com combos, meteoros de presentes e ranking MVP",
        "commands": ["1", "atacar", "fogo", "espada"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "05_roleta_desafios_live": {
        "name": "Roleta dos Desafios da Live",
        "category": "sorteios_roletas",
        "description": "Roleta determinística com palheta mecânica clicante, customizador de fatias e super-giros frenesi acionados por presentes",
        "commands": ["girar", "1", "spin", "roleta"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "06_batalha_dos_baloes": {
        "name": "Batalha dos Balões Gigantes",
        "category": "polarizacao",
        "description": "Disputa de enchimento pneumático elástico até o estouro com som procedural realista",
        "commands": ["1", "2", "azul", "laranja"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "07_pendulo_destruidor": {
        "name": "Pêndulo Demolidor",
        "category": "tensao_eliminacao",
        "description": "Chat ajusta o ângulo do pêndulo para liberar a bola demolidora e esmagar a fortaleza rival com super impacto de gifts",
        "commands": ["1", "2", "3", "puxar", "soltar", "turbo"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "08_caca_tesouro_coordenadas": {
        "name": "Caça ao Baú do Tesouro",
        "category": "tabuleiro_coordenadas",
        "description": "Grade 4x4 de 16 baús mecânicos; o chat vota em coordenadas A1-D4 para desarmar armadilhas, coletar 3 chaves douradas e achar o grande tesouro",
        "commands": ["A1", "B2", "C3", "D4", "coordenadas"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "09_tsunami_de_curtidas": {
        "name": "Tsunami de Curtidas",
        "category": "polarizacao",
        "description": "Pressômetro hidráulico com micro-ondas de choque subaquáticas e alarme de inundação",
        "commands": ["1", "2", "likes"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "10_queda_dos_blocos": {
        "name": "Tetris da Discórdia",
        "category": "tabuleiro_coordenadas",
        "description": "Matriz 6x11 de blocos pesados onde o chat vota em colunas 1 a 6 e gira peças para fechar linhas com lasers ou sobrecarregar a matriz",
        "commands": ["1", "2", "3", "4", "5", "6", "r", "girar"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "11_queda_de_braco_titas": {
        "name": "Queda de Braço dos Titãs",
        "category": "polarizacao",
        "description": "Braços cibernéticos articulados com medidor de torque em tempo real e impacto mecha",
        "commands": ["1", "2", "azul", "vermelho"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "12_pachinko_pinball_neon": {
        "name": "Pachinko Pinball Neon",
        "category": "fisica_pachinko",
        "description": "Flippers automáticos, canaletas magnéticas e 100x Super Jackpot ativado por moedas do chat",
        "commands": ["1", "2", "3", "azul", "vermelho", "jackpot"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "13_cascata_de_moedas": {
        "name": "Cascata de Moedas Douradas",
        "category": "fisica_pachinko",
        "description": "Coin Pusher 2.5D com pá motorizada, atrito de empilhamento, lingotes gigantes e avalanches de prêmios",
        "commands": ["1", "2", "3", "safira", "rubi", "ouro"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "14_vortex_gravitacional": {
        "name": "Vortex Gravitacional",
        "category": "fisica_pachinko",
        "description": "Buraco negro cósmico com atração gravitacional não-linear, órbitas caóticas, áudio Doppler e pulsos de Quasar",
        "commands": ["1", "2", "3", "orb", "quasar", "blackhole"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "15_corrida_maluca_espacial": {
        "name": "Corrida Maluca Espacial",
        "category": "corrida_velocidade",
        "description": "Foguetes espaciais rumo à órbita com chuva de meteoros, escudos defletores e hiper-dobra ativada por presentes",
        "commands": ["1", "2", "3", "apollo", "solaris", "nebula"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "16_arrancada_noturna_neon": {
        "name": "Arrancada Noturna Neon",
        "category": "corrida_velocidade",
        "description": "Drag Race 402m em linha reta com troca de marchas por votos, fumaça de burnout, nitro e photofinish",
        "commands": ["1", "2", "cyber", "viper"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "17_caca_niquel_neon_777": {
        "name": "Caça-Níquel Neon 777",
        "category": "sorteios_roletas",
        "description": "Slot machine clássica de 3 rolos com símbolos neon, paradas escalonadas, modo Frenesi e cascata de moedas",
        "commands": ["777", "girar", "1", "spin"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "18_roleta_russa_baloes": {
        "name": "Roleta Russa de Balões",
        "category": "sorteios_roletas",
        "description": "Roleta russa com balão sob tensão crescente, aproximação milimétrica da agulha em 6 câmaras, estouro explosivo e spotlight de espectador",
        "commands": ["1", "2", "balao", "agulha", "sorteio"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "19_defesa_da_torre_chat": {
        "name": "Defesa da Torre do Chat",
        "category": "cooperativo_boss",
        "description": "Hordas de inimigos descendo em 3 lanes verticais enquanto o chat ativa e aprimora canhões nos slots com bomba orbital de gifts",
        "commands": ["1", "2", "3", "esq", "centro", "dir"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "20_subida_da_montanha_sagrada": {
        "name": "Subida da Montanha Sagrada",
        "category": "cooperativo_boss",
        "description": "Chat empurra guerreiro montanha acima até 1000m desviando de avalanches e pedregulhos com voo da fênix de gifts",
        "commands": ["1", "2", "3", "subir", "esq", "dir"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "21_batata_quente_explosiva": {
        "name": "Batata Quente Explosiva",
        "category": "tensao_eliminacao",
        "description": "Bomba com pavio aceso passando entre avatares na tela com tempo aleatório de 20 a 40s, BPM acelerado e eliminação",
        "commands": ["1", "2", "3", "passar"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "22_ponte_de_vidro_quebradico": {
        "name": "Ponte de Vidro Quebradiço",
        "category": "tensao_eliminacao",
        "description": "Travessia de 8 degraus suspensa no abismo onde o chat escolhe esquerda ou direita, com revelação raio-X de gifts",
        "commands": ["1", "2", "esq", "dir"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "23_sobrevivencia_na_lava": {
        "name": "Sobrevivência na Lava",
        "category": "tensao_eliminacao",
        "description": "Plataformas flutuantes que afundam na lava neon conforme recebem peso e calor, com erupção de partículas e borbulhamento procedural",
        "commands": ["1", "2", "3", "4", "ciano", "roxo", "ouro", "verde"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    },
    "24_campo_minado_neon": {
        "name": "Campo Minado Neon",
        "category": "tabuleiro_coordenadas",
        "description": "Matriz tática 5x5 de desarme de minas; chat vota coordenadas A1-E5 com flood-fill de vazios, escudos de vida e sensores raio-X",
        "commands": ["A1", "B3", "C2", "D4", "E5", "coordenadas"],
        "status": "HOMOLOGADO",
        "version": "1.0.0"
    }
}

def sync_games():
    if not os.path.exists(BROADCASTER_GAMES_DIR):
        os.makedirs(BROADCASTER_GAMES_DIR, exist_ok=True)

    manifest = []
    
    for item in sorted(os.listdir(CATALOG_DIR)):
        src_path = os.path.join(CATALOG_DIR, item)
        if os.path.isdir(src_path):
            dest_path = os.path.join(BROADCASTER_GAMES_DIR, item)
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            print(f"[SYNC] Jogo sincronizado: {item} -> {dest_path}")
            
            meta = GAME_METADATA.get(item, {
                "name": item.replace("_", " ").title(),
                "category": "outros",
                "description": "Cartucho de live interativa V5",
                "commands": ["1", "2"],
                "status": "HOMOLOGADO",
                "version": "1.0.0"
            })
            
            manifest.append({
                "slug": item,
                "name": meta["name"],
                "category": meta["category"],
                "description": meta["description"],
                "commands": meta["commands"],
                "status": meta["status"],
                "version": meta["version"],
                "path": f"/games/{item}/index.html",
                "aspectRatio": "9:16",
                "resolution": "1080x1920",
                "updatedAt": datetime.now().isoformat()
            })

    manifest_path = os.path.join(BROADCASTER_GAMES_DIR, "v5_games_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n[SUCCESS] {len(manifest)} jogos homologados e sincronizados com sucesso no Broadcaster!")
    print(f"[MANIFEST] {manifest_path}")

if __name__ == "__main__":
    sync_games()
