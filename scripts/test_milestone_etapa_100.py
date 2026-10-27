import os
import re
import json
import sys

def test_milestone_etapa_100():
    base_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games"
    memoria_path = os.path.join(base_dir, "MEMORIA_ATIVA_GAMES.md")
    plano_path = os.path.join(base_dir, "PLANO_MESTRE_100_ETAPAS.md")
    manifest_path = os.path.join(base_dir, "catalogo_jogos", "v5_games_manifest.json")
    registry_path = os.path.join(base_dir, "catalogo_jogos", "games_registry.json")
    report_path = os.path.join(base_dir, "relatorios", "relatorio_despacho_broadcaster.json")

    print("=" * 80)
    print(" SUÍTE DE TESTES: MARCO DE HOMOLOGAÇÃO TOTAL DO CATÁLOGO (ETAPA 100)")
    print(" Holding V5 Apollo — Capitania V5 Games (Fechamento da Fase 10)")
    print("=" * 80)

    checks = []

    # 1. Leitura e validação de MEMORIA_ATIVA_GAMES.md
    with open(memoria_path, "r", encoding="utf-8") as f:
        memoria_text = f.read()

    # Conta quantas linhas da tabela de cartuchos possuem status HOMOLOGADO
    table_rows = re.findall(r'\|\s*\*\*\d+[B]?\*\*\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*\*\*HOMOLOGADO\*\*\s*\|', memoria_text)
    checks.append((
        f"MEMORIA_ATIVA_GAMES.md lista todos os 41 cartuchos com status HOMOLOGADO (detectado: {len(table_rows)})",
        len(table_rows) == 41
    ))

    # 2. Confirmação do cabeçalho da Memória Ativa
    checks.append((
        "Cabeçalho de MEMORIA_ATIVA_GAMES.md declara Fase 10 Concluída e 40 Jogos Próprios",
        "Fase 10 Concluída" in memoria_text and "40 Jogos Próprios" in memoria_text
    ))

    # 3. Leitura e validação de PLANO_MESTRE_100_ETAPAS.md
    with open(plano_path, "r", encoding="utf-8") as f:
        plano_text = f.read()

    checked_steps = re.findall(r'-\s*\[x\]\s*\*\*Etapa\s+(\d+):?\*\*', plano_text)
    # Etapas 001 a 100 devem estar checadas
    int_steps = [int(s) for s in checked_steps if int(s) <= 100]
    checks.append((
        f"PLANO_MESTRE_100_ETAPAS.md possui as 100 primeiras etapas concluídas com [x] (total checado <= 100: {len(int_steps)}/100)",
        len(int_steps) == 100
    ))

    # 4. Paridade com v5_games_manifest.json
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    checks.append((
        f"v5_games_manifest.json possui paridade exata de 41 cartuchos ({len(manifest_data)} == 41)",
        len(manifest_data) == 41
    ))

    # 5. Paridade com games_registry.json
    with open(registry_path, "r", encoding="utf-8") as f:
        registry_data = json.load(f)

    checks.append((
        f"games_registry.json possui paridade de 41 cartuchos (total: {registry_data.get('total')})",
        registry_data.get("total") == 41 and len(registry_data.get("games", [])) == 41
    ))

    # 6. Paridade com relatorio_despacho_broadcaster.json
    with open(report_path, "r", encoding="utf-8") as f:
        report_data = json.load(f)

    checks.append((
        f"Relatório de despacho com 100.0% integridade MD5 e status HOMOLOGADO_DESPACHADO",
        report_data.get("md5_match_rate_percent") == 100.0 and report_data.get("status") == "HOMOLOGADO_DESPACHADO"
    ))

    # 7. Unicidade de todos os 41 slugs em todos os sistemas
    slugs_memoria = set(r[0] for r in table_rows)
    slugs_manifest = set(e["slug"] for e in manifest_data)
    slugs_registry = set(g["slug"] for g in registry_data["games"])

    checks.append((
        "Unicidade e paridade absoluta de slugs entre Memória, Manifesto e Registry",
        slugs_memoria == slugs_manifest == slugs_registry and len(slugs_memoria) == 41
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
    print(f" Resultado: {passed}/{len(checks)} verificações do marco da Etapa 100 aprovadas.")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    test_milestone_etapa_100()
