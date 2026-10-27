import os
import json
import sys

def audit_manifest():
    base_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games"
    catalog_dir = os.path.join(base_dir, "catalogo_jogos")
    manifest_broadcaster = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games\v5_games_manifest.json"
    manifest_local = os.path.join(catalog_dir, "v5_games_manifest.json")

    print("=" * 80)
    print(" AUDITORIA INDUSTRIAL DO MANIFESTO GLOBAL DE CARTUCHOS (FASE 10 - ETAPA 096)")
    print(" Holding V5 Apollo — Capitania V5 Games")
    print("=" * 80)

    # 1. Obter todos os diretórios de cartuchos
    cartridge_dirs = sorted([
        d for d in os.listdir(catalog_dir) 
        if os.path.isdir(os.path.join(catalog_dir, d)) and not d.startswith(".")
    ])
    print(f"[*] Total de diretórios de cartuchos detectados no catálogo: {len(cartridge_dirs)}")

    # 2. Carregar manifesto do Broadcaster
    if not os.path.exists(manifest_broadcaster):
        print(f"[FAIL] Manifesto não encontrado no Broadcaster: {manifest_broadcaster}")
        sys.exit(1)

    with open(manifest_broadcaster, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    print(f"[*] Total de entradas no manifesto: {len(manifest_data)}")

    # 3. Auditoria de integridade para cada cartucho
    missing_in_manifest = []
    missing_html = []
    invalid_schema = []

    required_keys = [
        "slug", "name", "category", "description", "commands", 
        "status", "version", "path", "aspectRatio", "resolution"
    ]

    manifest_slugs = {item["slug"]: item for item in manifest_data}

    for c_dir in cartridge_dirs:
        # Checar se index.html existe
        html_path = os.path.join(catalog_dir, c_dir, "index.html")
        if not os.path.exists(html_path):
            missing_html.append(c_dir)

        # Checar se está no manifesto
        if c_dir not in manifest_slugs:
            missing_in_manifest.append(c_dir)
        else:
            entry = manifest_slugs[c_dir]
            for key in required_keys:
                if key not in entry or not entry[key]:
                    invalid_schema.append((c_dir, key))

    # Resultados
    print("-" * 80)
    print(f"  Diretórios analisados: {len(cartridge_dirs)}")
    print(f"  Arquivos index.html ausentes: {len(missing_html)}")
    print(f"  Cartuchos ausentes no manifesto: {len(missing_in_manifest)}")
    print(f"  Erros de schema/campos faltantes: {len(invalid_schema)}")
    print("-" * 80)

    if missing_html:
        for m in missing_html:
            print(f"  [FAIL] index.html ausente: {m}")
    if missing_in_manifest:
        for m in missing_in_manifest:
            print(f"  [FAIL] Ausente no manifesto: {m}")
    if invalid_schema:
        for c_dir, key in invalid_schema:
            print(f"  [FAIL] Campo obrigatório '{key}' inválido em: {c_dir}")

    success = (len(missing_html) == 0 and len(missing_in_manifest) == 0 and len(invalid_schema) == 0)

    if success:
        print("[SUCCESS] Auditoria concluída: Todos os cartuchos estão 100% integrados e conformes!")
    else:
        print("[FAILED] Foram encontradas inconsistências no manifesto.")
        sys.exit(1)

if __name__ == "__main__":
    audit_manifest()
