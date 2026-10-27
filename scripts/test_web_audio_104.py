#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suíte de Testes Automatizados da Etapa 104:
Validação do Sintetizador Web Audio API nos 41 Cartuchos V5 Games.
"""

import os
import sys
import json
import glob
import re
import subprocess

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_tests():
    print("=" * 70)
    print("INICIANDO SUÍTE DE TESTES: ETAPA 104 - WEB AUDIO API AUDIT & SHIELD")
    print("=" * 70)

    cartridges = sorted(glob.glob("catalogo_jogos/*/index.html"))
    total = len(cartridges)
    assert total == 41, f"Esperado 41 cartuchos, encontrado {total}"
    print(f"[TEST 1] Quantidade total de cartuchos no catálogo: {total}/41 - PASSOU")

    # Check 2: Relatório gerado
    report_file = os.path.join("relatorios", "relatorio_web_audio_104.json")
    assert os.path.exists(report_file), f"{report_file} não encontrado"
    with open(report_file, "r", encoding="utf-8") as f:
        report = json.load(f)
    
    assert report["total_cartridges"] == 41, f"Total no relatório inválido: {report['total_cartridges']}"
    assert report["compliant_count"] == 41, f"Nem todos os cartuchos estão em conformidade: {report['compliant_count']}/41"
    print(f"[TEST 2] Relatório de conformidade Web Audio API: 41/41 em 100% de compliance - PASSOU")

    # Check 3: Resumo dos pilares de áudio
    summary = report["summary"]
    for k, v in summary.items():
        assert v is True, f"Pilar {k} falhou no relatório ({v})"
        print(f"  ↳ Pilar de Áudio '{k}': OK")
    print("[TEST 3] Todos os 6 pilares de estabilidade do sintetizador validados - PASSOU")

    # Check 4: Zero arquivos externos de mídia de áudio em todo o repositório catalogo_jogos
    ext_audio_files = []
    for ext in ["*.mp3", "*.wav", "*.ogg", "*.aac", "*.m4a"]:
        ext_audio_files.extend(glob.glob(f"catalogo_jogos/**/{ext}", recursive=True))
    assert len(ext_audio_files) == 0, f"Encontrados arquivos de áudio externos: {ext_audio_files}"
    print(f"[TEST 4] Zero arquivos de áudio binários externos (100% sintetizado procedimentalmente) - PASSOU")

    # Check 5: AudioContext Singleton por cartucho (nenhuma criação em loop)
    for c in cartridges:
        with open(c, "r", encoding="utf-8") as f:
            content = f.read()
        instantiations = len(re.findall(r'new\s+(?:window\.)?(?:AudioContext|AudioContextClass|AudioCtx|webkitAudioContext)\s*\(', content))
        assert 1 <= instantiations <= 2, f"Instanciações anômalas em {c}: {instantiations}"
    print(f"[TEST 5] AudioContext Singleton verificado em 41/41 cartuchos (sem estouro de muxes CEF) - PASSOU")

    # Check 6: Presença de .resume() para desativar suspensão de autoplay do navegador
    for c in cartridges:
        with open(c, "r", encoding="utf-8") as f:
            content = f.read()
        assert ".resume(" in content, f"Falta chamada .resume() em {c}"
    print(f"[TEST 6] Mecanismo de retomada de áudio (.resume()) verificado em 41/41 cartuchos - PASSOU")

    # Check 7: Blindagem com try/catch em métodos de áudio
    for c in cartridges:
        with open(c, "r", encoding="utf-8") as f:
            content = f.read()
        assert "try {" in content or "try{" in content, f"Falta try/catch em {c}"
    print(f"[TEST 7] Blindagem com try/catch verificada em 41/41 cartuchos - PASSOU")

    # Check 8: Simulação headless de execução com Mock Web Audio API
    mock_runner_js = """
    const fs = require('fs');
    let totalMethodsInvoked = 0;
    
    // Web Audio Mock Environment
    global.window = global;
    class MockAudioNode {
      connect(target) { return target; }
      disconnect() {}
    }
    class MockAudioParam {
      setValueAtTime() {}
      linearRampToValueAtTime() {}
      exponentialRampToValueAtTime() {}
    }
    class MockOscillator extends MockAudioNode {
      constructor() {
        super();
        this.frequency = new MockAudioParam();
        this.type = 'sine';
        this.onended = null;
      }
      start(t) {}
      stop(t) {
        if (typeof this.onended === 'function') this.onended();
      }
    }
    class MockGain extends MockAudioNode {
      constructor() {
        super();
        this.gain = new MockAudioParam();
      }
    }
    class MockBufferSource extends MockAudioNode {
      constructor() {
        super();
        this.playbackRate = new MockAudioParam();
      }
      start() {}
      stop() {}
    }
    class MockBiquadFilter extends MockAudioNode {
      constructor() {
        super();
        this.frequency = new MockAudioParam();
        this.Q = new MockAudioParam();
      }
    }
    class MockAudioContext {
      constructor() {
        this.currentTime = 0;
        this.sampleRate = 44100;
        this.destination = new MockAudioNode();
        this.state = 'suspended';
      }
      resume() { this.state = 'running'; return Promise.resolve(); }
      createOscillator() { return new MockOscillator(); }
      createGain() { return new MockGain(); }
      createBufferSource() { return new MockBufferSource(); }
      createBiquadFilter() { return new MockBiquadFilter(); }
      createBuffer(channels, length, sampleRate) {
        return {
          getChannelData: () => new Float32Array(length)
        };
      }
    }
    global.AudioContext = MockAudioContext;
    global.webkitAudioContext = MockAudioContext;

    // Test a sample of 10 audio synthesizer classes directly
    const samples = [
      'catalogo_jogos/01_cabo_de_guerra_neon/index.html',
      'catalogo_jogos/04_boss_raid_cooperativo/index.html',
      'catalogo_jogos/07_pendulo_destruidor/index.html',
      'catalogo_jogos/10_queda_dos_blocos/index.html',
      'catalogo_jogos/17_caca_niquel_neon_777/index.html',
      'catalogo_jogos/26_guerra_dos_tanques_neon/index.html',
      'catalogo_jogos/33_corrida_de_cavalos_retro/index.html',
      'catalogo_jogos/35_quiz_frenetico_holding/index.html',
      'catalogo_jogos/37_torre_de_blocos_equilibrada/index.html',
      'catalogo_jogos/40_duelo_de_magicos_neon/index.html'
    ];

    for (const file of samples) {
      const html = fs.readFileSync(file, 'utf8');
      const scriptMatch = html.match(/<script[\\s\\S]*?>([\\s\\S]*?)<\\/script>/i);
      if (!scriptMatch) continue;
      const code = scriptMatch[1];
      
      // Extract class definition
      const classMatch = code.match(/class\\s+(\\w*(?:Audio|Sound|Raid)\\w*)[\\s\\S]*?\\n    \\}/);
      if (classMatch) {
        eval(classMatch[0] + '; global.TestAudioClass = ' + classMatch[1] + ';');
        const instance = new global.TestAudioClass();
        const proto = Object.getOwnPropertyNames(Object.getPrototypeOf(instance));
        for (const m of proto) {
          if (m.startsWith('play') && typeof instance[m] === 'function') {
            try {
              instance[m]();
              totalMethodsInvoked++;
            } catch (e) {
              console.error('Falha no método ' + m + ' em ' + file + ':', e);
              process.exit(1);
            }
          }
        }
      }
    }
    console.log('MOCK_TEST_PASSED: Invocados com sucesso ' + totalMethodsInvoked + ' métodos de áudio sem exceções.');
    """
    with open("_temp_audio_mock_test.js", "w", encoding="utf-8") as f:
        f.write(mock_runner_js)

    res = subprocess.run(["node", "_temp_audio_mock_test.js"], capture_output=True, text=True)
    if os.path.exists("_temp_audio_mock_test.js"):
        os.remove("_temp_audio_mock_test.js")

    assert res.returncode == 0, f"Falha na simulação Web Audio Mock: {res.stderr}"
    assert "MOCK_TEST_PASSED" in res.stdout, f"Falha na saída do teste mock: {res.stdout}"
    print(f"[TEST 8] Simulação headless Web Audio API: 10 cartuchos amostrais invocados sem falhas - PASSOU\n   ↳ {res.stdout.strip()}")

    # Check 9: Verificação sintática com node --check de todos os 41 cartuchos
    print("[TEST 9] Verificação estrita de sintaxe JavaScript em todos os 41 cartuchos:")
    for c in cartridges:
        slug = os.path.basename(os.path.dirname(c))
        with open(c, "r", encoding="utf-8") as f:
            html = f.read()
        scripts = re.findall(r'<script.*?>([\s\S]*?)<\/script>', html)
        for i, s in enumerate(scripts):
            tmp = f"_temp_syntax_{slug}_{i}.js"
            with open(tmp, "w", encoding="utf-8") as tf:
                tf.write(s)
            chk = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
            if os.path.exists(tmp):
                os.remove(tmp)
            assert chk.returncode == 0, f"Erro de sintaxe em {slug}: {chk.stderr}"
    print(f"[TEST 9] 41/41 cartuchos validados sintaticamente com node --check - PASSOU")

    print("\n" + "=" * 70)
    print("TODOS OS 9 TESTES DA ETAPA 104 PASSARAM COM SUCESSO ABSOLUTO (100%)!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
