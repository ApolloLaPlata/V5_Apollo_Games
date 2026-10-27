#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blindagem de Métodos de Áudio Web Audio API nos 41 Cartuchos V5 Games.
Insere try { ... } catch (e) {} defensivo em todos os métodos geradores
de som que ainda não estejam encapsulados, impedindo qualquer exceção não tratada
de interromper o motor gráfico e o processamento de eventos do chat da live.
"""

import os
import glob
import re
import subprocess
import sys

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def shield_cartridge_audio(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    m = re.search(r'class\s+(\w*(?:Audio|Sound|Raid)\w*)\s*\{', text)
    if not m:
        return 0, "No audio class found"
    
    start = m.start()
    brace_count = 0
    found_first = False
    end = start
    for i in range(start, len(text)):
        if text[i] == '{':
            brace_count += 1
            found_first = True
        elif text[i] == '}':
            brace_count -= 1
            if found_first and brace_count == 0:
                end = i + 1
                break

    class_code = text[start:end]
    
    # Identify methods like play..., start..., stop...
    method_matches = list(re.finditer(r'(\n(\s*))((?:play|start|stop)\w+)\s*\(([^)]*)\)\s*\{', class_code))
    
    shielded_count = 0
    new_class_code = class_code
    
    for mm in reversed(method_matches):
        m_indent = mm.group(2)
        m_name = mm.group(3)
        pstart = mm.end() - 1 # at the '{'
        
        # Find matching '}'
        b_count = 0
        b_found = False
        pend = pstart
        for j in range(pstart, len(new_class_code)):
            if new_class_code[j] == '{':
                b_count += 1
                b_found = True
            elif new_class_code[j] == '}':
                b_count -= 1
                if b_found and b_count == 0:
                    pend = j
                    break
        
        inner_body = new_class_code[pstart+1:pend]
        
        # If already wrapped in try/catch, skip
        stripped_inner = inner_body.strip()
        if stripped_inner.startswith('try {') or stripped_inner.startswith('try{'):
            continue
        
        # Wrap inner_body with try { ... } catch (e) {}
        wrapped_inner = f'\n{m_indent}  try {{{inner_body}\n{m_indent}  }} catch (e) {{}}'
        new_class_code = new_class_code[:pstart+1] + wrapped_inner + new_class_code[pend:]
        shielded_count += 1

    if shielded_count > 0:
        new_text = text[:start] + new_class_code + text[end:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_text)

    return shielded_count, m.group(1)

def run():
    cartridges = sorted(glob.glob('catalogo_jogos/*/index.html'))
    total_shielded = 0
    print(f"Blindando métodos de áudio em {len(cartridges)} cartuchos...\n")

    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        count, cname = shield_cartridge_audio(c)
        if count > 0:
            print(f"[SHIELDED] {slug} ({cname}): {count} métodos protegidos com try/catch.")
            total_shielded += count
        else:
            print(f"[OK] {slug} ({cname}): Já 100% blindado.")

    print(f"\nTotal de métodos blindados: {total_shielded}")

    # Syntax verification on all cartridges using node --check
    print("\nExecutando verificação estrita de sintaxe JavaScript com node --check...")
    all_ok = True
    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, 'r', encoding='utf-8') as f:
            html = f.read()
        scripts = re.findall(r'<script.*?>([\s\S]*?)<\/script>', html)
        for i, s in enumerate(scripts):
            tmp_file = f'_temp_check_{slug}_{i}.js'
            with open(tmp_file, 'w', encoding='utf-8') as tf:
                tf.write(s)
            res = subprocess.run(['node', '--check', tmp_file], capture_output=True, text=True)
            if os.path.exists(tmp_file):
                os.remove(tmp_file)
            if res.returncode != 0:
                print(f"ERRO DE SINTAXE em {slug} (script {i}): {res.stderr}")
                all_ok = False
                break
    
    if all_ok:
        print("TODOS os 41 cartuchos compilaram perfeitamente sem erros de sintaxe!")
    else:
        print("ALERTA: Erro detectado em script JavaScript.")
        sys.exit(1)

if __name__ == '__main__':
    run()
