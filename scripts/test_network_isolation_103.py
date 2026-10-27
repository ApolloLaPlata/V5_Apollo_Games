import os
import json
import sys

def test_network_isolation_103():
    base_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games"
    json_path = os.path.join(base_dir, "relatorios", "relatorio_isolamento_rede_offline.json")
    md_path = os.path.join(base_dir, "relatorios", "relatorio_isolamento_rede_offline.md")

    print("=" * 80)
    print(" SUÍTE DE TESTES: ISOLAMENTO TOTAL DE REDE & OFFLINE (ETAPA 103)")
    print(" Holding V5 Apollo — Capitania V5 Games & V5 Broadcaster")
    print("=" * 80)

    checks = []

    # 1. Existência física dos relatórios
    checks.append((
        "Relatório JSON de isolamento presente em relatorios/relatorio_isolamento_rede_offline.json",
        os.path.exists(json_path)
    ))
    checks.append((
        "Relatório Markdown executivo presente em relatorios/relatorio_isolamento_rede_offline.md",
        os.path.exists(md_path)
    ))

    if not os.path.exists(json_path) or not os.path.exists(md_path):
        print("[FAIL] Relatórios não encontrados.")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. Métricas de auditoria de rede
    total = data.get("total_cartridges_audited", 0)
    isolated = data.get("total_isolated_compliant", 0)
    rate = data.get("isolation_rate_percent", 0.0)

    checks.append((
        f"Todos os 41 cartuchos foram auditados para isolamento ({total} == 41)",
        total == 41
    ))
    checks.append((
        f"Todos os 41 cartuchos foram aprovados sem nenhuma chamada externa ({isolated} == 41)",
        isolated == 41
    ))
    checks.append((
        f"Taxa de isolamento de rede é de 100.0% ({rate}%)",
        rate == 100.0
    ))

    # 3. Verificação detalhada de violações em cada cartucho
    cartridges = data.get("cartridges", [])
    total_violations = sum(len(c.get("violations", [])) for c in cartridges)
    checks.append((
        f"Zero violações de CDN externa, fontes remotas ou arquivos de áudio externos (total: {total_violations})",
        total_violations == 0
    ))

    # 4. Status de homologação formal
    status = data.get("status")
    checks.append((
        f"Status de homologação formal: {status}",
        status == "HOMOLOGADO_ISOLAMENTO_TOTAL"
    ))

    # Execução das validações
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
    print(f" Resultado: {passed}/{len(checks)} verificações de isolamento de rede aprovadas.")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    test_network_isolation_103()
