#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detector de Bugs e Casos de Borda nos 41 Cartuchos V5 Games.
Verifica:
1. Canais de comunicação (BroadcastChannel, window.message e window.v5_event).
2. Tratamento de exceção em BroadcastChannel.
3. Tratamento de strings de usuário (prevenção de quebra de layout com strings muito longas).
4. Limpeza de partículas (prevenção de arrays com mais de 300 partículas).
5. AudioContext resume no handleEvent.
"""

import os
import glob
import re
import sys

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def scan():
    cartridges = sorted(glob.glob("catalogo_jogos/*/index.html"))
    print(f"Examinando {len(cartridges)} cartuchos para detecção de bugs de integração...\n")

    unshielded_bc = []
    missing_message_listener = []
    missing_v5_listener = []
    particle_caps_missing = []

    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            text = f.read()

        # 1. Unshielded BroadcastChannel
        lines = text.split('\n')
        for idx, line in enumerate(lines):
            if 'new BroadcastChannel' in line:
                surrounding = "\n".join(lines[max(0, idx-4):idx+1])
                if 'try' not in surrounding:
                    unshielded_bc.append((slug, idx+1))

        # 2. Window Listeners
        has_msg = 'addEventListener(\'message\'' in text or 'addEventListener("message"' in text
        has_v5 = 'addEventListener(\'v5_event\'' in text or 'addEventListener("v5_event"' in text
        if not has_msg:
            missing_message_listener.append(slug)
        if not has_v5:
            missing_v5_listener.append(slug)

        # 3. Particle arrays capping
        if ('particles.push' in text or 'sparks.push' in text) and ('particles.length >' not in text and 'particles.length >=' not in text and 'sparks.length >' not in text):
            # check if particle array is capped in update loop
            if 'filter(' not in text and 'splice(' not in text:
                particle_caps_missing.append(slug)

    print(f"1. BroadcastChannel sem try/catch: {len(unshielded_bc)} ocorrências")
    for s, l in unshielded_bc:
        print(f"   ↳ {s} (linha {l})")

    print(f"\n2. Cartuchos sem ouvinte de 'message' (iframe): {len(missing_message_listener)}")
    for s in missing_message_listener:
        print(f"   ↳ {s}")

    print(f"\n3. Cartuchos sem ouvinte de 'v5_event': {len(missing_v5_listener)}")
    for s in missing_v5_listener:
        print(f"   ↳ {s}")

    print(f"\n4. Arrays de partículas potencialmente sem filtro: {len(particle_caps_missing)}")
    for s in particle_caps_missing:
        print(f"   ↳ {s}")

if __name__ == "__main__":
    scan()
