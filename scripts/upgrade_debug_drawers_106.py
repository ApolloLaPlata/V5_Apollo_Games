#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Padronização da Gaveta de Depuração Oculta (Tecla 'D') nos 6 Cartuchos.
Garante:
1. .debug-drawer estilizado com display: none por padrão.
2. Função toggleDebug() implementada e conectada.
3. Listener de keydown para tecla 'd'/'D'.
"""

import os
import re

targets = [
    '04_boss_raid_cooperativo',
    '07_pendulo_destruidor',
    '19_defesa_da_torre_chat',
    '20_subida_da_montanha_sagrada',
    '21_batata_quente_explosiva',
    '22_ponte_de_vidro_quebradico'
]

for t in targets:
    path = f'catalogo_jogos/{t}/index.html'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Update CSS: change .debug-drawer { display: flex; ... } to display: none;
    # Or add display: none; to .debug-drawer
    m_css = re.search(r'(\.debug-drawer\s*\{)([^}]*)(\})', text)
    if m_css:
        css_body = m_css.group(2)
        if 'display:' in css_body:
            new_css_body = re.sub(r'display:\s*flex', 'display: none', css_body)
        else:
            new_css_body = ' display: none; ' + css_body
        text = text[:m_css.start(2)] + new_css_body + text[m_css.end(2):]
    else:
        # Add CSS if missing
        insert_css = "\n    .debug-drawer { display: none; gap: 6px; justify-content: center; }\n"
        text = text.replace('</style>', insert_css + '  </style>')

    # 2. Check if toggleDebug and keydown are present
    if 'toggleDebug' not in text and 'toggleDrawer' not in text:
        js_code = """
    // --- GAVETA DE DEPURAÇÃO OCULTA (TECLA 'D') ---
    function toggleDebug() {
      const drawer = document.querySelector('.debug-drawer') || document.getElementById('debug-drawer');
      if (drawer) {
        drawer.style.display = (drawer.style.display === 'flex' || drawer.style.display === 'block') ? 'none' : 'flex';
      }
    }

    window.addEventListener('keydown', (e) => {
      if (e.key === 'd' || e.key === 'D') toggleDebug();
    });
"""
        # Insert before </script>
        last_script_end = text.rfind('</script>')
        if last_script_end != -1:
            text = text[:last_script_end] + js_code + text[last_script_end:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Atualizado {t} com sucesso!")

print("\nTodos os 6 cartuchos atualizados.")
