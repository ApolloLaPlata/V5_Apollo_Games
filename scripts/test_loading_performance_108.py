#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suíte de Testes Automatizados da Etapa 108:
Teste de Carregamento Instantâneo como Browser Source no OBS Studio (Meta: < 200ms).
"""

import os
import sys
import json
import glob
import subprocess

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_tests():
    print("=" * 70)
    print("INICIANDO SUÍTE DE TESTES: ETAPA 108 - CARREGAMENTO INSTANTÂNEO OBS")
    print("=" * 70)

    cartridges = sorted(glob.glob("catalogo_jogos/*/index.html"))
    total = len(cartridges)
    assert total == 41, f"Esperado 41 cartuchos, encontrado {total}"
    print(f"[TEST 1] Catálogo total de cartuchos: {total}/41 - PASSOU")

    # Check 2: Relatório de benchmark JSON e Markdown
    json_path = os.path.join("relatorios", "relatorio_carregamento_obs_108.json")
    md_path = os.path.join("relatorios", "relatorio_carregamento_obs_108.md")
    assert os.path.exists(json_path), f"{json_path} não encontrado"
    assert os.path.exists(md_path), f"{md_path} não encontrado"

    with open(json_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    assert report["total_cartridges"] == 41, "Total de cartuchos divergente"
    assert report["compliant_count"] == 41, f"Cartuchos não-conformes: {report['compliant_count']}/41"
    assert report["compliance_rate_percent"] == 100.0, "Taxa de conformidade não é 100%"
    print(f"[TEST 2] Relatório de Benchmark OBS: 41/41 (100%) em conformidade - PASSOU")

    # Check 3: Tempo Médio de Abertura e Margem de Segurança (Headroom)
    avg_time = report["average_load_time_ms"]
    headroom = report["headroom_ms"]
    assert avg_time < 50.0, f"Tempo médio muito alto: {avg_time} ms"
    assert headroom > 150.0, f"Margem de segurança insuficiente: {headroom} ms"
    print(f"[TEST 3] Tempo médio da frota: {avg_time:.2f} ms | Folga: {headroom:.2f} ms (Meta < 200 ms) - PASSOU")

    # Check 4: Orçamento de Tamanho de Arquivo (< 100 KB por cartucho)
    for res in report["results"]:
        slug = res["slug"]
        sz = res["size_kb"]
        total_ms = res["total_load_ms"]
        assert sz < 100.0, f"Cartucho {slug} excedeu limite de 100 KB: {sz} KB"
        assert total_ms < 200.0, f"Cartucho {slug} excedeu limite de 200 ms: {total_ms} ms"
    print(f"[TEST 4] Limite de peso (< 100 KB) e tempo (< 200 ms) verificado individualmente em 41/41 cartuchos - PASSOU")

    # Check 5: Ausência de bloqueios síncronos de rede (link rel=stylesheet externo ou script src externo)
    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            content = f.read()
        import re
        external_css = re.findall(r'<link[^>]*rel=[\'"]stylesheet[\'"][^>]*href=[\'"]https?:\/\/', content, re.I)
        external_js = re.findall(r'<script[^>]*src=[\'"]https?:\/\/', content, re.I)
        assert len(external_css) == 0, f"CSS externo bloqueante em {slug}: {external_css}"
        assert len(external_js) == 0, f"JS externo bloqueante em {slug}: {external_js}"
    print(f"[TEST 5] Zero bloqueios síncronos de rede em 41/41 cartuchos - PASSOU")

    # Check 6: Verificação de sintaxe de todos os 41 cartuchos com node --check
    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            html = f.read()
        scripts = re.findall(r'<script.*?>([\s\S]*?)<\/script>', html)
        for i, s in enumerate(scripts):
            tmp = f"_temp_chk_{slug}_{i}.js"
            with open(tmp, "w", encoding="utf-8") as tf:
                tf.write(s)
            chk = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
            if os.path.exists(tmp):
                os.remove(tmp)
            assert chk.returncode == 0, f"Erro de sintaxe em {slug}: {chk.stderr}"
    print(f"[TEST 6] 41/41 cartuchos validados sintaticamente com node --check - PASSOU")

    print("\n" + "=" * 70)
    print("TODOS OS 6 TESTES DA ETAPA 108 PASSARAM COM SUCESSO ABSOLUTO (100%)!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
