import os
import json
import hashlib
import sys

def test_md5_sync_report_98():
    base_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games"
    json_report_path = os.path.join(base_dir, "relatorios", "relatorio_despacho_broadcaster.json")
    md_report_path = os.path.join(base_dir, "relatorios", "relatorio_despacho_broadcaster.md")
    broadcaster_games_dir = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games"

    print("=" * 80)
    print(" SUÍTE DE TESTES: VERIFICAÇÃO CRIPTOGRÁFICA MD5 E DESPACHO (ETAPA 098)")
    print(" Holding V5 Apollo — Capitania V5 Games")
    print("=" * 80)

    checks = []

    # 1. Existência dos relatórios
    checks.append((
        "Relatório JSON de despacho presente em relatorios/relatorio_despacho_broadcaster.json",
        os.path.exists(json_report_path)
    ))
    checks.append((
        "Relatório Markdown executivo presente em relatorios/relatorio_despacho_broadcaster.md",
        os.path.exists(md_report_path)
    ))

    if not os.path.exists(json_report_path) or not os.path.exists(md_report_path):
        print("[FAIL] Arquivos de relatório não encontrados.")
        sys.exit(1)

    with open(json_report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. Métricas do relatório
    checks.append((
        f"Contagem de cartuchos consistente no relatório ({data.get('total_cartridges')} == 41)",
        data.get("total_cartridges") == 41
    ))
    checks.append((
        f"Total de arquivos verificados com MD5 consistente ({data.get('total_files_verified')} >= 82)",
        data.get("total_files_verified") >= 82
    ))
    checks.append((
        f"Taxa de integridade criptográfica perfeita (100.0% match, 0 mismatches)",
        data.get("md5_match_rate_percent") == 100.0 and data.get("md5_mismatches") == 0
    ))
    checks.append((
        f"Status formal do despacho homologado: {data.get('status')}",
        data.get("status") == "HOMOLOGADO_DESPACHADO"
    ))

    # 3. Auditoria física direta dos hashes MD5 no destino de produção
    hash_discrepancies = []
    for c in data.get("cartridges", []):
        slug = c["slug"]
        for fname, finfo in c["files"].items():
            expected_md5 = finfo["md5"]
            dest_file_path = os.path.join(broadcaster_games_dir, slug, fname)
            if not os.path.exists(dest_file_path):
                hash_discrepancies.append(f"{slug}/{fname} (não existe no destino)")
                continue
            
            hasher = hashlib.md5()
            with open(dest_file_path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    hasher.update(chunk)
            actual_md5 = hasher.hexdigest()

            if actual_md5 != expected_md5:
                hash_discrepancies.append(f"{slug}/{fname} (esperado: {expected_md5}, obtido: {actual_md5})")

    checks.append((
        f"Auditoria física ao vivo de integridade de todos os arquivos no Broadcaster (discrepâncias: {len(hash_discrepancies)})",
        len(hash_discrepancies) == 0
    ))

    # 4. Verificação de integridade do relatório Markdown
    with open(md_report_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    checks.append((
        "Relatório Markdown formatado com cabeçalho, métricas globais e tabela detalhada",
        "RELATÓRIO DE DESPACHO E SINCRONIZAÇÃO INDUSTRIAL" in md_text and 
        "100.0%" in md_text and 
        "HOMOLOGADO_DESPACHADO" in md_text
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
    print(f" Resultado: {passed}/{len(checks)} verificações criptográficas aprovadas.")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    test_md5_sync_report_98()
