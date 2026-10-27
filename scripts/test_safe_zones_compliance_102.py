import os
import json
import sys

def test_safe_zones_compliance_102():
    base_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games"
    json_path = os.path.join(base_dir, "relatorios", "relatorio_auditoria_safe_zones_916.json")
    md_path = os.path.join(base_dir, "relatorios", "relatorio_auditoria_safe_zones_916.md")

    print("=" * 80)
    print(" SUÍTE DE TESTES: CONFORMIDADE DE SAFE ZONES 9:16 (ETAPA 102)")
    print(" Holding V5 Apollo — Capitania V5 Games & V5 Broadcaster")
    print("=" * 80)

    checks = []

    # 1. Existência física dos relatórios
    checks.append((
        "Relatório JSON de safe zones presente em relatorios/relatorio_auditoria_safe_zones_916.json",
        os.path.exists(json_path)
    ))
    checks.append((
        "Relatório Markdown executivo presente em relatorios/relatorio_auditoria_safe_zones_916.md",
        os.path.exists(md_path)
    ))

    if not os.path.exists(json_path) or not os.path.exists(md_path):
        print("[FAIL] Relatórios não encontrados.")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. Métricas de auditoria
    total = data.get("total_cartridges_audited", 0)
    compliant = data.get("total_compliant", 0)
    rate = data.get("compliance_rate_percent", 0.0)

    checks.append((
        f"Todos os 41 cartuchos foram auditados ({total} == 41)",
        total == 41
    ))
    checks.append((
        f"Todos os 41 cartuchos foram aprovados ({compliant} == 41)",
        compliant == 41
    ))
    checks.append((
        f"Taxa de conformidade de safe zones é de 100.0% ({rate}%)",
        rate == 100.0
    ))

    # 3. Verificação detalhada de cada cartucho
    cartridges = data.get("cartridges", [])
    zero_top_violations = all(c.get("top_safe_zone_px") >= 140 for c in cartridges)
    zero_bottom_violations = all(c.get("bottom_safe_zone_px") >= 180 for c in cartridges)
    zero_viewport_violations = all(c.get("viewport_zoom_locked") for c in cartridges)
    all_aspect_ratio_ok = all(c.get("aspect_ratio_9_16") for c in cartridges)

    checks.append((
        "Top Safe Zone (>= 140px para avatares/contagem de live) atendida em 100% dos cartuchos",
        zero_top_violations
    ))
    checks.append((
        "Bottom Safe Zone (>= 180px para chat/presentes) atendida em 100% dos cartuchos",
        zero_bottom_violations
    ))
    checks.append((
        "Bloqueio de Zoom / Pinch Mobile no OBS atendido em 100% dos cartuchos",
        zero_viewport_violations
    ))
    checks.append((
        "Proporção estrita 9:16 (1080x1920) presente em 100% dos cartuchos",
        all_aspect_ratio_ok
    ))

    # 4. Status de homologação formal
    status = data.get("status")
    checks.append((
        f"Status de homologação formal: {status}",
        status == "HOMOLOGADO_SAFE_ZONES"
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
    print(f" Resultado: {passed}/{len(checks)} verificações de safe zones aprovadas.")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    test_safe_zones_compliance_102()
