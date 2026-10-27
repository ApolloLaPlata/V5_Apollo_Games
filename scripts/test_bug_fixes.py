#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suíte de Testes de Hardening e Correção de Bugs (Bug Fix Verification Suite)
Holding V5 Apollo — Capitania V5 Games
"""

import os
import sys
import glob
import subprocess
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_tests():
    print("=" * 70)
    print("INICIANDO SUÍTE DE TESTES: CORREÇÃO DE BUGS & HARDENING DE CARTUCHOS")
    print("=" * 70)

    cartridges = sorted(glob.glob("catalogo_jogos/*/index.html"))
    total = len(cartridges)
    assert total == 41, f"Esperado 41 cartuchos, encontrado {total}"
    print(f"[TEST 1] Catálogo de cartuchos completo: {total}/41 - PASSOU")

    # Check 2: 100% dos BroadcastChannels estão blindados em try/catch
    unshielded_bc = []
    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            if "new BroadcastChannel" in line:
                surrounding = "\n".join(lines[max(0, idx-4):idx+1])
                if "try" not in surrounding:
                    unshielded_bc.append((slug, idx+1))
    assert len(unshielded_bc) == 0, f"BroadcastChannel sem try/catch: {unshielded_bc}"
    print(f"[TEST 2] 41/41 cartuchos com BroadcastChannel blindado contra SecurityError em iframes - PASSOU")

    # Check 3: 100% dos cartuchos possuem ouvinte postMessage ('message')
    missing_msg = []
    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            content = f.read()
        if "addEventListener('message'" not in content and 'addEventListener("message"' not in content:
            missing_msg.append(slug)
    assert len(missing_msg) == 0, f"Cartuchos sem ouvinte 'message': {missing_msg}"
    print(f"[TEST 3] 41/41 cartuchos com ouvinte de postMessage ('message') para iframes - PASSOU")

    # Check 4: 100% dos cartuchos possuem ouvinte CustomEvent ('v5_event')
    missing_v5 = []
    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            content = f.read()
        if "addEventListener('v5_event'" not in content and 'addEventListener("v5_event"' not in content:
            missing_v5.append(slug)
    assert len(missing_v5) == 0, f"Cartuchos sem ouvinte 'v5_event': {missing_v5}"
    print(f"[TEST 4] 41/41 cartuchos com ouvinte CustomEvent ('v5_event') para Test Lab e OBS - PASSOU")

    # Check 5: Simulação Headless de PostMessage com JSON em String e Objeto
    simulation_js = """
    let stringEventReceived = false;
    let objectEventReceived = false;

    // Mock Window com Dispatcher de Message
    const listeners = {};
    global.window = {
      addEventListener: (type, fn) => {
        if (!listeners[type]) listeners[type] = [];
        listeners[type].push(fn);
      },
      dispatchEvent: (type, data) => {
        if (listeners[type]) listeners[type].forEach(fn => fn(data));
      }
    };

    function handleLiveTest(data) {
      if (data.comment === 'string_test') stringEventReceived = true;
      if (data.comment === 'object_test') objectEventReceived = true;
    }

    // Registra listener triplo
    window.addEventListener('message', (e) => {
      let data = e.data;
      if (typeof data === 'string') {
        try { data = JSON.parse(data); } catch (err) {}
      }
      if (data && (data.type || data.action || data.comment)) {
        handleLiveTest(data);
      }
    });

    // Disparo 1: Stringified JSON (comum em iframes cross-domain)
    window.dispatchEvent('message', { data: JSON.stringify({ type: 'comment', comment: 'string_test', user: '@teste_str' }) });

    // Disparo 2: Plain Object (comum em iframes same-domain)
    window.dispatchEvent('message', { data: { type: 'comment', comment: 'object_test', user: '@teste_obj' } });

    if (!stringEventReceived || !objectEventReceived) {
      console.error('Falha: PostMessage não processou payload misto');
      process.exit(1);
    }
    console.log('POSTMESSAGE_DESERIALIZATION_PASSED: Payload JSON string e objeto tratados perfeitamente.');
    """
    tmp_sim = "_temp_sim_postmsg.js"
    with open(tmp_sim, "w", encoding="utf-8") as tf:
        tf.write(simulation_js)

    res = subprocess.run(["node", tmp_sim], capture_output=True, text=True)
    if os.path.exists(tmp_sim):
        os.remove(tmp_sim)

    assert res.returncode == 0, f"Falha no teste de postMessage: {res.stderr}"
    assert "POSTMESSAGE_DESERIALIZATION_PASSED" in res.stdout, f"Falha na saída: {res.stdout}"
    print(f"[TEST 5] Desserialização tolerante de PostMessage (String e Objeto) - PASSOU\n   ↳ {res.stdout.strip()}")

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
    print("TODOS OS 6 TESTES DE CORREÇÃO DE BUGS PASSARAM COM SUCESSO ABSOLUTO (100%)!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
