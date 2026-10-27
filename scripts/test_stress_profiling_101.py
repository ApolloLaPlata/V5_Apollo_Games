import os
import json
import sys

def test_stress_profiling_101():
    base_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games"
    json_path = os.path.join(base_dir, "relatorios", "relatorio_stress_profiling_60fps.json")
    md_path = os.path.join(base_dir, "relatorios", "relatorio_stress_profiling_60fps.md")

    print("=" * 80)
    print(" SUÍTE DE TESTES: PROFILING DE ESTRESSE & GC V8 EM 60 FPS (ETAPA 101)")
    print(" Holding V5 Apollo — Capitania V5 Games & V5 Broadcaster")
    print("=" * 80)

    checks = []

    # 1. Existência física dos relatórios
    checks.append((
        "Relatório JSON de profiling 60 FPS presente em relatorios/relatorio_stress_profiling_60fps.json",
        os.path.exists(json_path)
    ))
    checks.append((
        "Relatório Markdown executivo presente em relatorios/relatorio_stress_profiling_60fps.md",
        os.path.exists(md_path)
    ))

    if not os.path.exists(json_path) or not os.path.exists(md_path):
        print("[FAIL] Relatórios não encontrados.")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. Métricas de frames e duração
    frames = data.get("total_frames_simulated", 0)
    checks.append((
        f"Volume de frames simulados atende meta de sessão prolongada ({frames:,} >= 60.000)",
        frames >= 60000
    ))

    # 3. Métricas de frametimes e ausência de frame drops
    frametimes = data.get("frametimes_ms", {})
    avg_ms = frametimes.get("avg", 999.0)
    p95_ms = frametimes.get("p95", 999.0)
    checks.append((
        f"Tempo médio de processamento por frame ultra-otimizado ({avg_ms:.3f} ms < 4.000 ms)",
        avg_ms < 4.0
    ))
    checks.append((
        f"P95 Frametime consistente sem engasgos ({p95_ms:.3f} ms < 8.000 ms)",
        p95_ms < 8.0
    ))

    fps_metrics = data.get("fps_metrics", {})
    dropped = fps_metrics.get("dropped_frames", -1)
    headroom = fps_metrics.get("headroom_percent", 0.0)
    checks.append((
        f"Zero frame drops detectados durante carga contínua (drops: {dropped})",
        dropped == 0
    ))
    checks.append((
        f"Folga de CPU (Headroom) para OBS Studio atinge meta industrial ({headroom:.2f}% >= 75.0%)",
        headroom >= 75.0
    ))

    # 4. Telemetria de Heap V8 e ausência de memory leaks
    mem = data.get("v8_memory_mb", {})
    growth = mem.get("net_growth_mb", 999.0)
    peak = mem.get("peak_heap", 999.0)
    checks.append((
        f"Estabilidade de Heap V8 com variação contida ({growth:.2f} MB < 15.0 MB)",
        abs(growth) < 15.0 and peak < 80.0
    ))

    # 5. Status formal
    status = data.get("status")
    checks.append((
        f"Status de homologação 60 FPS aprovado: {status}",
        status == "HOMOLOGADO_60FPS"
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
    print(f" Resultado: {passed}/{len(checks)} verificações de profiling aprovadas.")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    test_stress_profiling_101()
