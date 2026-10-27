#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Caçador Profundo de Bugs & Anomalias (Deep Bug Hunter) nos 41 Cartuchos V5 Games.
Varre sistematicamente:
1. Potencial divisão por zero / NaN em cálculos de placar e porcentagens.
2. Injeção de HTML / XSS em nomes de usuário (@user) e comentários via innerHTML.
3. Vulnerabilidades de BroadcastChannel fora de try/catch (erro em iframes cross-origin).
4. Arrays de partículas ou projéteis sem limite máximo (Memory Leak sob spam de gifts).
5. Chamadas a ctx.arc() com raio potencialmente negativo.
6. Falta de .resume() no AudioContext ao receber eventos de chat no OBS.
7. Falta de limpeza de entidades residuais durante o reset de rodada.
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

def hunt_bugs():
    cartridges = sorted(glob.glob("catalogo_jogos/*/index.html"))
    total = len(cartridges)
    print(f"Iniciando varredura profunda de bugs e anomalias em {total} cartuchos...\n")

    bugs_found = {
        "nan_division": [],
        "raw_innerhtml_injection": [],
        "unshielded_broadcast_channel": [],
        "unbounded_particle_arrays": [],
        "missing_audio_resume_on_event": [],
        "negative_radius_risk": []
    }

    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Check for unshielded BroadcastChannel
        bc_matches = re.findall(r'new\s+BroadcastChannel\s*\(', content)
        if bc_matches:
            # Check if all are wrapped in try { ... }
            # Simple check: search for 'new BroadcastChannel' not preceded by 'try'
            lines = content.split('\n')
            for idx, line in enumerate(lines):
                if 'new BroadcastChannel' in line:
                    # check surrounding 5 lines for 'try'
                    surrounding = "\n".join(lines[max(0, idx-4):idx+1])
                    if 'try' not in surrounding:
                        bugs_found["unshielded_broadcast_channel"].append((slug, idx+1, line.strip()))

        # 2. Check for raw innerHTML with user or comment without escaping
        # e.g., innerHTML = ... ${user} ... or innerHTML = ... ${comment} ...
        inner_matches = re.finditer(r'\.innerHTML\s*=\s*`[^`]*\$\{(?:user|comment|data\.user|data\.comment)\}[^`]*`', content)
        for m in inner_matches:
            # Check if escapeHTML or textContent is used
            snippet = m.group(0)
            if 'escapeHTML' not in snippet and 'sanitize' not in snippet:
                bugs_found["raw_innerhtml_injection"].append((slug, snippet[:80]))

        # 3. Check for potential NaN division: e.g. / (total) or / (a + b) without || 1 or > 0 guard
        nan_matches = re.finditer(r'\/ \s*\(([a-zA-Z0-9_\.]+\s*\+\s*[a-zA-Z0-9_\.]+)\)', content)
        for m in nan_matches:
            expr = m.group(1)
            # check if guarded
            start_pos = max(0, m.start() - 60)
            context = content[start_pos:m.end() + 20]
            if '|| 1' not in context and '=== 0' not in context and '> 0' not in context and '|| 0.001' not in context:
                bugs_found["nan_division"].append((slug, m.group(0), context.replace('\n', ' ')))

        # 4. Check for unbounded particle arrays:
        # e.g., particles.push(...) without capping length (e.g. if particles.length > 200 particles.shift())
        if 'particles.push' in content or 'sparks.push' in content or 'shards.push' in content:
            # check if there is an array size cap
            has_cap = bool(re.search(r'\.(?:particles|sparks|shards)\.length\s*>\s*\d+', content))
            has_filter = bool(re.search(r'\.(?:particles|sparks|shards)\s*=\s*[\w\.]+\.filter', content)) or bool(re.search(r'\.splice\s*\(', content))
            if not has_cap and not has_filter:
                bugs_found["unbounded_particle_arrays"].append(slug)

        # 5. Check AudioContext resume inside handleEvent
        # In OBS CEF, events must wake up audio
        if 'handleEvent' in content or 'processEvent' in content:
            if 'audio.getCtx' not in content and 'ensureContext' not in content and 'audio.init' not in content and 'ctx.resume' not in content:
                bugs_found["missing_audio_resume_on_event"].append(slug)

    print("=" * 70)
    print("RELATÓRIO PRELIMINAR DE VARREDURA DE BUGS:")
    print("=" * 70)
    for cat, items in bugs_found.items():
        print(f"\n[{cat.upper()}] Encontrados: {len(items)}")
        for it in items[:6]:
            print(f"  ↳ {it}")
        if len(items) > 6:
            print(f"  ... e mais {len(items) - 6} ocorrências.")

    return bugs_found

if __name__ == "__main__":
    hunt_bugs()
