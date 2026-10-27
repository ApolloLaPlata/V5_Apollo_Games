import os
import json
import sys

def test_manifest_consolidation_96():
    base_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games"
    catalog_dir = os.path.join(base_dir, "catalogo_jogos")
    manifest_local = os.path.join(catalog_dir, "v5_games_manifest.json")
    manifest_broadcaster = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games\v5_games_manifest.json"

    print("=" * 80)
    print(" SUÍTE DE TESTES: AUDITORIA E CONSOLIDAÇÃO DO MANIFESTO GLOBAL (ETAPA 096)")
    print(" Holding V5 Apollo — Capitania V5 Games")
    print("=" * 80)

    checks = []

    # 1. Existência dos dois manifestos
    checks.append((
        "Manifesto local presente em catalogo_jogos/v5_games_manifest.json",
        os.path.exists(manifest_local)
    ))
    checks.append((
        "Manifesto de produção presente no Broadcaster",
        os.path.exists(manifest_broadcaster)
    ))

    if not os.path.exists(manifest_local) or not os.path.exists(manifest_broadcaster):
        print("[FAIL] Um ou mais manifestos não foram encontrados.")
        sys.exit(1)

    with open(manifest_local, "r", encoding="utf-8") as f:
        data_local = json.load(f)

    with open(manifest_broadcaster, "r", encoding="utf-8") as f:
        data_broadcaster = json.load(f)

    # 2. Contagem de cartuchos (41 entradas para todos os cartuchos catalogados)
    checks.append((
        f"Contagem do manifesto local consistente ({len(data_local)} entradas >= 40)",
        len(data_local) >= 40
    ))
    checks.append((
        f"Contagem do manifesto no Broadcaster consistente ({len(data_broadcaster)} entradas)",
        len(data_broadcaster) == len(data_local)
    ))

    # 3. Validação estrutural de campos obrigatórios do Schema
    required_keys = [
        "slug", "name", "category", "description", "commands", "gifts",
        "status", "version", "path", "aspectRatio", "resolution",
        "safeZones", "soundEngine", "antiSilence", "autoResetSeconds", "updatedAt"
    ]

    schema_errors = 0
    slugs = set()
    for entry in data_local:
        slugs.add(entry.get("slug"))
        for k in required_keys:
            if k not in entry or entry[k] is None:
                schema_errors += 1
        if entry.get("aspectRatio") != "9:16":
            schema_errors += 1
        if entry.get("status") != "HOMOLOGADO":
            schema_errors += 1
        if entry.get("safeZones", {}).get("top") != "140px":
            schema_errors += 1
        if entry.get("safeZones", {}).get("bottom") != "180px":
            schema_errors += 1
        if not entry.get("antiSilence"):
            schema_errors += 1
        if entry.get("autoResetSeconds") != 5:
            schema_errors += 1

    checks.append((
        f"Conformidade estrita de Schema (16 campos obrigatórios por cartucho, 0 erros)",
        schema_errors == 0
    ))

    # 4. Verificação de existência física de cada cartucho e index.html
    missing_files = 0
    for slug in slugs:
        local_html = os.path.join(catalog_dir, slug, "index.html")
        broadcaster_html = os.path.join(r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games", slug, "index.html")
        if not os.path.exists(local_html) or not os.path.exists(broadcaster_html):
            missing_files += 1

    checks.append((
        f"Integridade física de todos os arquivos index.html no Catálogo e Broadcaster",
        missing_files == 0
    ))

    # 5. Auditoria de unicidade de slugs
    checks.append((
        f"Unicidade estrita de slugs no catálogo (total {len(slugs)} únicos)",
        len(slugs) == len(data_local)
    ))

    # 6. Presença das categorias homologadas
    categories = set(e.get("category") for e in data_local)
    checks.append((
        f"Diversidade de categorias catalogadas ({len(categories)} categorias mapeadas)",
        len(categories) >= 10
    ))

    # Execução das verificações
    passed = 0
    failed = 0
    for name, condition in checks:
        if condition:
            print(f"  [PASS] {name}")
            passed += 1
        else:
            print(f"  [FAIL] {name}")
            failed += 1

    print("-" * 80)
    print(f" Resultado: {passed}/{len(checks)} verificações de auditoria aprovadas.")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    test_manifest_consolidation_96()
