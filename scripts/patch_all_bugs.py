#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Cirúrgico de Correção de Bugs e Hardening Arquitetural
Holding V5 Apollo — Capitania V5 Games
"""

import os
import glob
import re
import subprocess
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def patch_cartridge(filepath):
    slug = os.path.basename(os.path.dirname(filepath))
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # 1. Identify handler name
    handler_name = None
    if 'function handleLivePayload(' in content:
        handler_name = 'handleLivePayload'
    elif 'function handleIncomingEvent(' in content:
        handler_name = 'handleIncomingEvent'
    elif 'function handleGameEvent(' in content:
        handler_name = 'handleGameEvent'
    elif 'function handleLiveCommand(' in content:
        handler_name = 'handleLiveCommand'
    elif 'function processLiveEvent(' in content:
        handler_name = 'processLiveEvent'
    elif 'function handleEvent(' in content:
        handler_name = 'handleEvent'

    # 2. Fix unshielded BroadcastChannel in 03, 04, 05, 07, 15, 16, 17, 18, 19, 20, 21, 22
    bc_search = "const broadcasterChannel = new BroadcastChannel('v5_broadcaster_games');"
    start_bc = content.find(bc_search)
    if start_bc != -1 and handler_name:
        fn_marker = f"function {handler_name}("
        end_bc = content.find(fn_marker, start_bc)
        if end_bc != -1:
            line_start = content.rfind('\n', 0, start_bc) + 1
            indent = content[line_start:start_bc]

            unified_bus = f"""// --- PROTOCOLO DE EVENTOS UNIFICADO (V5 LIVE EVENT BUS) ---
{indent}try {{
{indent}  const broadcasterChannel = new BroadcastChannel('v5_broadcaster_games');
{indent}  broadcasterChannel.onmessage = (event) => {{
{indent}    if (event && event.data) {handler_name}(event.data);
{indent}  }};
{indent}}} catch (err) {{
{indent}  console.warn('[V5Games] BroadcastChannel offline ou restrito:', err);
{indent}}}

{indent}window.addEventListener('v5_event', (e) => {{
{indent}  const data = e.detail || e.data;
{indent}  if (data) {handler_name}(data);
{indent}}});

{indent}window.addEventListener('message', (e) => {{
{indent}  let data = e.data;
{indent}  if (typeof data === 'string') {{
{indent}    try {{ data = JSON.parse(data); }} catch (err) {{}}
{indent}  }}
{indent}  if (data && (data.type || data.action || data.comment)) {{
{indent}    {handler_name}(data);
{indent}  }}
{indent}}});\n\n{indent}"""
            content = content[:start_bc] + unified_bus + content[end_bc:]
            modified = True

    # 3. Add window.addEventListener('message', ...) to initEventBus() in 33 through 40
    if 'function initEventBus()' in content and 'addEventListener(\'message\'' not in content and 'addEventListener("message"' not in content and handler_name:
        old_bus = re.search(r'function initEventBus\(\)\s*\{([\s\S]*?)\n    \}', content)
        if old_bus:
            bus_body = old_bus.group(1)
            new_listener = f"""

      // 3. PostMessage (Iframe / Preview Dock / Broadcaster Cockpit)
      window.addEventListener('message', (e) => {{
        let data = e.data;
        if (typeof data === 'string') {{
          try {{ data = JSON.parse(data); }} catch (err) {{}}
        }}
        if (data && (data.type || data.action || data.comment)) {{
          {handler_name}(data);
        }}
      }});"""
            new_bus = f"function initEventBus() {{{bus_body}{new_listener}\n    }}"
            content = content[:old_bus.start()] + new_bus + content[old_bus.end():]
            modified = True

    # 4. Add window.addEventListener('message', ...) to board games (08, 10, 23, 24, 25)
    if slug in ['08_caca_tesouro_coordenadas', '10_queda_dos_blocos', '23_sobrevivencia_na_lava', '24_campo_minado_neon', '25_batalha_naval_live']:
        if 'addEventListener(\'message\'' not in content and 'addEventListener("message"' not in content and handler_name:
            v5_match = re.search(r'window\.addEventListener\([\'"]v5_event[\'"][\s\S]*?\n    \}\);', content)
            if v5_match:
                msg_listener = f"""\n\n    // 3. PostMessage (Iframe / Broadcaster Cockpit)
    window.addEventListener('message', (e) => {{
      let data = e.data;
      if (typeof data === 'string') {{
        try {{ data = JSON.parse(data); }} catch (err) {{}}
      }}
      if (data && (data.type || data.action || data.comment)) {{
        {handler_name}(data);
      }}
    }});"""
                content = content[:v5_match.end()] + msg_listener + content[v5_match.end():]
                modified = True

    # 5. Fix cartridges 26 to 32: Add direct v5_event and message bridges and sanitize HTML in toasts
    if slug in ['26_guerra_dos_tanques_neon', '27_meteoro_defensor', '28_labirinto_pacman_neon', '29_basquete_street_neon', '30_gol_de_penalti_live', '31_guitar_hero_neon', '32_corte_de_frutas_neon']:
        if 'addEventListener(\'v5_event\'' not in content and 'addEventListener("v5_event"' not in content and handler_name:
            sdk_hook = re.search(r'sdk\.on\([\'"]like[\'"][\s\S]*?\n    \}\);', content)
            if sdk_hook:
                bridge = f"""\n\n    // Redundant direct bridges for standalone testing
    window.addEventListener('v5_event', (e) => {{
      const d = e.detail || e.data;
      if (d) {handler_name}(d);
    }});
    window.addEventListener('message', (e) => {{
      let d = e.data;
      if (typeof d === 'string') {{
        try {{ d = JSON.parse(d); }} catch (err) {{}}
      }}
      if (d && (d.type || d.action || d.comment)) {handler_name}(d);
    }});"""
                content = content[:sdk_hook.end()] + bridge + content[sdk_hook.end():]
                modified = True

        # Sanitize toast innerHTML
        if 'sanitizeHtml' not in content:
            helper = """
    function sanitizeHtml(str) {
      return String(str).replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[m]);
    }
"""
            old_toast = re.search(r'toast\.innerHTML\s*=\s*user\s*\?\s*`<strong>\$\{user\}<\/strong>:\s*\$\{msg\}`\s*:\s*msg;', content)
            if old_toast:
                content = content[:old_toast.start()] + 'toast.innerHTML = user ? `<strong>${sanitizeHtml(user)}</strong>: ${sanitizeHtml(msg)}` : sanitizeHtml(msg);' + content[old_toast.end():]
                st_idx = content.find('function showToast(')
                if st_idx != -1:
                    content = content[:st_idx] + helper + '\n    ' + content[st_idx:]
                modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, "Patched successfully"
    return False, "No modifications needed"

def main():
    cartridges = sorted(glob.glob("catalogo_jogos/*/index.html"))
    total_patched = 0
    print(f"Iniciando ciclo de correções e hardening em {len(cartridges)} cartuchos...\n")

    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        patched, msg = patch_cartridge(c)
        if patched:
            print(f"[PATCHED] {slug}: {msg}")
            total_patched += 1
        else:
            print(f"[ALIGNED] {slug}: {msg}")

    print(f"\nTotal de cartuchos atualizados e blindados: {total_patched}/{len(cartridges)}")

    print("\nExecutando verificação de integridade sintática com node --check...")
    all_ok = True
    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, 'r', encoding='utf-8') as f:
            html = f.read()
        scripts = re.findall(r'<script.*?>([\s\S]*?)<\/script>', html)
        for i, s in enumerate(scripts):
            tmp = f"_temp_chk_{slug}_{i}.js"
            with open(tmp, 'w', encoding='utf-8') as tf:
                tf.write(s)
            res = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
            if os.path.exists(tmp):
                os.remove(tmp)
            if res.returncode != 0:
                print(f"ERRO SINTÁTICO em {slug}: {res.stderr}")
                all_ok = False
                break

    if all_ok:
        print("TODOS os 41 cartuchos compilaram perfeitamente sem erros de sintaxe!")
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
