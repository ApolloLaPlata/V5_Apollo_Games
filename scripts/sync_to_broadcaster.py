import os
import shutil
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_DIR = os.path.join(BASE_DIR, "catalogo_jogos")
BROADCASTER_GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games"

def sync_games():
    if not os.path.exists(BROADCASTER_GAMES_DIR):
        os.makedirs(BROADCASTER_GAMES_DIR, exist_ok=True)

    manifest = []
    
    for item in os.listdir(CATALOG_DIR):
        src_path = os.path.join(CATALOG_DIR, item)
        if os.path.isdir(src_path):
            dest_path = os.path.join(BROADCASTER_GAMES_DIR, item)
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            print(f"[SYNC] Jogo sincronizado: {item} -> {dest_path}")
            
            manifest.append({
                "slug": item,
                "name": item.replace("_", " ").title(),
                "path": f"/games/{item}/index.html",
                "aspectRatio": "9:16",
                "resolution": "1080x1920"
            })

    manifest_path = os.path.join(BROADCASTER_GAMES_DIR, "v5_games_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] {len(manifest)} jogos sincronizados com sucesso no Broadcaster!")
    print(f"[MANIFEST] {manifest_path}")

if __name__ == "__main__":
    sync_games()
