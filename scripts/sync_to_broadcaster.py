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
    "06_batalha_dos_baloes": {
        "name": "Batalha dos Balões Gigantes",
        "category": "polarizacao",
        "description": "Disputa de enchimento pneumático elástico até o estouro com som procedural realista",
        "commands": ["1", "2", "azul", "laranja"],
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
