import os
import json
import sys

def test_general_sync_99():
    base_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games"
    catalog_dir = os.path.join(base_dir, "catalogo_jogos")
    broadcaster_games_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games"
    
    local_registry = os.path.join(catalog_dir, "games_registry.json")
    remote_registry = os.path.join(broadcaster_games_dir, "games_registry.json")
    local_manifest = os.path.join(catalog_dir, "v5_games_manifest.json")
    remote_manifest = os.path.join(broadcaster_games_dir, "v5_games_manifest.json")

    print("=" * 80)
    print(" SUÍTE DE TESTES: SINCRONIZAÇÃO GERAL DO CATÁLOGO DE JOGOS (ETAPA 099)")
    print(" Holding V5 Apollo — Capitania V5 Games -> V5 Broadcaster")
    print("=" * 80)

    checks = []

    # 1. Existência física dos registros e manifestos
    checks.append((
        "Manifestos v5_games_manifest.json presentes localmente e no Broadcaster",
        os.path.exists(local_manifest) and os.path.exists(remote_manifest)
    ))
    checks.append((
        "Registros games_registry.json presentes localmente e no Broadcaster",
        os.path.exists(local_registry) and os.path.exists(remote_registry)
    ))

    if not all([os.path.exists(p) for p in [local_manifest, remote_manifest, local_registry, remote_registry]]):
        print("[FAIL] Arquivos centrais ausentes.")
        sys.exit(1)

    # 2. Contagem e paridade dos manifestos
    with open(local_manifest, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)
    with open(remote_manifest, "r", encoding="utf-8") as f:
        remote_manifest_data = json.load(f)

    checks.append((
        f"Contagem do manifesto consolidada em 41 entradas (local: {len(manifest_data)}, remote: {len(remote_manifest_data)})",
        len(manifest_data) == 41 and len(remote_manifest_data) == 41
    ))

    # 3. Contagem e estrutura do games_registry.json para API do Broadcaster
    with open(remote_registry, "r", encoding="utf-8") as f:
        reg_data = json.load(f)

    reg_games = reg_data.get("games", [])
    checks.append((
        f"games_registry.json contém exatamente 41 cartuchos (detectado: {len(reg_games)})",
        reg_data.get("total") == 41 and len(reg_games) == 41
    ))

    # 4. Verificação de schema de games_registry.json
    invalid_reg_entries = []
    for g in reg_games:
        if not g.get("slug") or not g.get("url") or not g.get("thumbnail") or g.get("status") != "ready":
            invalid_reg_entries.append(g)

    checks.append((
        f"Conformidade de schema no games_registry.json (0 entradas inválidas)",
        len(invalid_reg_entries) == 0
    ))

    # 5. Integridade de cada uma das 41 pastas no Broadcaster
    missing_folders = []
    missing_html = []
    missing_thumb = []

    for entry in manifest_data:
        slug = entry["slug"]
        cart_dir = os.path.join(broadcaster_games_dir, slug)
        if not os.path.exists(cart_dir):
            missing_folders.append(slug)
            continue
        
        html_p = os.path.join(cart_dir, "index.html")
        thumb_p = os.path.join(cart_dir, "thumbnail.svg")

        if not os.path.exists(html_p) or os.path.getsize(html_p) == 0:
            missing_html.append(slug)
        if not os.path.exists(thumb_p) or os.path.getsize(thumb_p) == 0:
            missing_thumb.append(slug)

    checks.append((
        f"Todas as 41 pastas de cartuchos residem no Broadcaster (ausentes: {len(missing_folders)})",
        len(missing_folders) == 0
    ))

    checks.append((
        f"Todos os 41 index.html presentes e íntegros no Broadcaster (ausentes: {len(missing_html)})",
        len(missing_html) == 0
    ))

    checks.append((
        f"Todas as 41 miniaturas thumbnail.svg presentes e íntegras no Broadcaster (ausentes: {len(missing_thumb)})",
        len(missing_thumb) == 0
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
    print(f" Resultado: {passed}/{len(checks)} verificações de sincronização geral aprovadas.")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    test_general_sync_99()
