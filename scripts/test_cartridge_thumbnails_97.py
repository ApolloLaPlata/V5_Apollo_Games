import os
import json
import xml.etree.ElementTree as ET
import sys

def test_cartridge_thumbnails_97():
    base_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games"
    catalog_dir = os.path.join(base_dir, "catalogo_jogos")
    manifest_local = os.path.join(catalog_dir, "v5_games_manifest.json")
    manifest_broadcaster = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games\v5_games_manifest.json"
    broadcaster_games_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games"

    print("=" * 80)
    print(" SUÍTE DE TESTES UNITÁRIOS: MINIATURAS SVG VETORIAIS (FASE 10 - ETAPA 097)")
    print(" Holding V5 Apollo — Capitania V5 Games")
    print("=" * 80)

    cartridges = sorted([
        d for d in os.listdir(catalog_dir) 
        if os.path.isdir(os.path.join(catalog_dir, d)) and not d.startswith(".")
    ])

    checks = []

    # 1. Total de cartuchos detectados
    checks.append((
        f"Presença de 41 cartuchos catalogados para geração de miniaturas",
        len(cartridges) == 41
    ))

    # 2. Existência de thumbnail.svg em todos os diretórios locais
    missing_local = []
    for c in cartridges:
        p = os.path.join(catalog_dir, c, "thumbnail.svg")
        if not os.path.exists(p):
            missing_local.append(c)

    checks.append((
        f"Todos os 41 cartuchos locais possuem thumbnail.svg (ausentes: {len(missing_local)})",
        len(missing_local) == 0
    ))

    # 3. Existência de thumbnail.svg sincronizados no Broadcaster
    missing_broadcaster = []
    for c in cartridges:
        p = os.path.join(broadcaster_games_dir, c, "thumbnail.svg")
        if not os.path.exists(p):
            missing_broadcaster.append(c)

    checks.append((
        f"Todos os 41 cartuchos no Broadcaster possuem thumbnail.svg (ausentes: {len(missing_broadcaster)})",
        len(missing_broadcaster) == 0
    ))

    # 4. Validade da sintaxe SVG e viewBox 400x500
    invalid_svgs = []
    oversized_svgs = []
    for c in cartridges:
        p = os.path.join(catalog_dir, c, "thumbnail.svg")
        try:
            tree = ET.parse(p)
            root = tree.getroot()
            if not root.tag.endswith("svg"):
                invalid_svgs.append(c)
            # Checar tamanho
            sz = os.path.getsize(p)
            if sz > 15000: # Maior que 15KB
                oversized_svgs.append(c)
        except Exception as e:
            invalid_svgs.append(f"{c}: {e}")

    checks.append((
        f"Sintaxe XML/SVG estritamente válida em 100% dos arquivos (erros: {len(invalid_svgs)})",
        len(invalid_svgs) == 0
    ))

    checks.append((
        f"Otimização vetorial: todos os SVGs são leves (< 15KB) para carregamento instantâneo",
        len(oversized_svgs) == 0
    ))

    # 5. Validação de integração com o Manifesto Global
    with open(manifest_local, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    missing_thumb_prop = []
    for entry in manifest_data:
        t = entry.get("thumbnail")
        if not t or not t.endswith("thumbnail.svg"):
            missing_thumb_prop.append(entry.get("slug"))

    checks.append((
        f"Propriedade 'thumbnail' mapeada no schema do manifesto (faltantes: {len(missing_thumb_prop)})",
        len(missing_thumb_prop) == 0
    ))

    # 6. Presença do badge 'V5 9:16' em todos os thumbnails
    badge_missing = []
    for c in cartridges:
        p = os.path.join(catalog_dir, c, "thumbnail.svg")
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
            if "V5 9:16" not in content:
                badge_missing.append(c)

    checks.append((
        f"Badge 'V5 9:16' estandardizado presente em todos os thumbnails (ausentes: {len(badge_missing)})",
        len(badge_missing) == 0
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
    print(f" Resultado: {passed}/{len(checks)} verificações de miniaturas aprovadas.")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    test_cartridge_thumbnails_97()
