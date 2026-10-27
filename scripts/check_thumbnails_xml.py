import os
import xml.etree.ElementTree as ET

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def check_thumbnails():
    results = []
    for g in sorted(os.listdir(GAMES_DIR)):
        thumb_path = os.path.join(GAMES_DIR, g, "thumbnail.svg")
        if not os.path.isfile(thumb_path):
            results.append((g, "MISSING_FILE", "thumbnail.svg não existe"))
            continue
        try:
            tree = ET.parse(thumb_path)
            root = tree.getroot()
            if not root.tag.endswith('svg'):
                results.append((g, "INVALID_ROOT", f"Tag raiz não é svg: {root.tag}"))
        except Exception as e:
            results.append((g, "XML_ERROR", str(e)))

    print(f"Total de problemas em thumbnails: {len(results)}")
    for g, err, desc in results:
        print(f" - [{g}] {err}: {desc}")
    return results

if __name__ == "__main__":
    check_thumbnails()
