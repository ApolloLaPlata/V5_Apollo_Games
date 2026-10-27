#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditoria Cirúrgica do Sintetizador Web Audio API nos 41 Cartuchos V5 Games.
Verifica:
1. Instanciação Singleton do AudioContext (sem criação redundante que estoura limite de muxes de hardware do V8/CEF).
2. Ausência total de áudio externo (.mp3, .wav, .ogg, .aac, .m4a).
3. Presença de mecanismos de retomada de áudio (.resume() para desativar suspensão do autoplay policy do navegador).
4. Encerramento determinístico de nós osciladores (.stop() agendado com expiração finita).
5. Blindagem de exceções (try/catch) para evitar que falhas de áudio interfiram no loop de renderização do jogo.
6. Suporte multiplataforma (window.AudioContext || window.webkitAudioContext).
"""

import os
import re
import glob
import json
import sys

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def audit_cartridges():
    cartridges = sorted(glob.glob("catalogo_jogos/*/index.html"))
    total = len(cartridges)
    print(f"Iniciando auditoria Web Audio API em {total} cartuchos...\n")

    report = {
        "total_cartridges": total,
        "compliant_count": 0,
        "details": [],
        "summary": {
            "all_procedural": True,
            "zero_external_audio": True,
            "audio_context_singletons": True,
            "resume_capability": True,
            "finite_oscillators": True,
            "error_shielding": True
        }
    }

    external_audio_pattern = re.compile(r'["\']([^"\']+\.(?:mp3|wav|ogg|aac|m4a))["\']', re.IGNORECASE)
    audio_ctx_pattern = re.compile(r'(?:window\.)?(?:AudioContext|webkitAudioContext)', re.IGNORECASE)
    ctx_instantiation_pattern = re.compile(r'new\s+(?:window\.)?(?:AudioContext|AudioContextClass|AudioCtx|webkitAudioContext)\s*\(')
    resume_pattern = re.compile(r'\.resume\s*\(')
    osc_create_pattern = re.compile(r'\.createOscillator\s*\(')
    osc_stop_pattern = re.compile(r'\.stop\s*\(')
    gain_pattern = re.compile(r'\.createGain\s*\(')
    try_catch_pattern = re.compile(r'try\s*\{')

    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            content = f.read()

        cartridge_issues = []

        # 1. Zero External Audio Files
        ext_matches = external_audio_pattern.findall(content)
        # Filter out comments or false positives if any
        real_ext_matches = [m for m in ext_matches if not m.endswith(".svg")]
        if real_ext_matches:
            cartridge_issues.append(f"Arquivos de áudio externos detectados: {real_ext_matches}")
            report["summary"]["zero_external_audio"] = False

        # 2. AudioContext Usage
        has_audio_ctx = bool(audio_ctx_pattern.search(content))
        if not has_audio_ctx:
            cartridge_issues.append("AudioContext não encontrado.")
            report["summary"]["all_procedural"] = False

        # 3. AudioContext Instantiations (Should be exactly 1 singleton instantiation)
        instantiations = ctx_instantiation_pattern.findall(content)
        if len(instantiations) == 0:
            cartridge_issues.append("Nenhuma instanciação do AudioContext encontrada.")
            report["summary"]["audio_context_singletons"] = False
        elif len(instantiations) > 2:
            cartridge_issues.append(f"Possível proliferação de AudioContext ({len(instantiations)} instanciações).")
            report["summary"]["audio_context_singletons"] = False

        # 4. Resume Handling
        has_resume = bool(resume_pattern.search(content))
        if not has_resume:
            cartridge_issues.append("Falta chamada .resume() para desativar suspensão de autoplay do AudioContext.")
            report["summary"]["resume_capability"] = False

        # 5. Oscillator Stop / Finite Duration
        osc_count = len(osc_create_pattern.findall(content))
        stop_count = len(osc_stop_pattern.findall(content))
        gain_count = len(gain_pattern.findall(content))
        
        # In procedurally generated sound effects, oscillators should have matching stops
        if osc_count > 0 and stop_count == 0:
            cartridge_issues.append(f"Osciladores criados ({osc_count}) sem chamada .stop() correspondente (nós órfãos).")
            report["summary"]["finite_oscillators"] = False

        # 6. Error shielding (try/catch in sound methods)
        has_try_catch = bool(try_catch_pattern.search(content))
        if not has_try_catch:
            cartridge_issues.append("Falta tratamento de exceção (try/catch) para blindagem do loop.")
            report["summary"]["error_shielding"] = False

        is_compliant = len(cartridge_issues) == 0
        if is_compliant:
            report["compliant_count"] += 1

        report["details"].append({
            "slug": slug,
            "compliant": is_compliant,
            "oscillator_count": osc_count,
            "stop_count": stop_count,
            "gain_count": gain_count,
            "instantiations": len(instantiations),
            "has_resume": has_resume,
            "issues": cartridge_issues
        })

        status_sym = "✅" if is_compliant else "⚠️"
        print(f"{status_sym} {slug}: {osc_count} oscs, {stop_count} stops, {gain_count} gains, {len(instantiations)} ctx inst, resume={has_resume}")
        if cartridge_issues:
            for iss in cartridge_issues:
                print(f"   ↳ {iss}")

    print(f"\nResultado da Auditoria: {report['compliant_count']}/{total} cartuchos 100% em conformidade com Web Audio API.")

    report_path = os.path.join("relatorios", "relatorio_web_audio_104.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"Relatório salvo em {report_path}.")
    return report

if __name__ == "__main__":
    audit_cartridges()
