import json
import os

MANIFEST_PATH = r"catalogo_jogos/v5_games_manifest.json"
INDEX_HTML_PATH = r"index.html"

def build():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    # Agrupamentos de categorias
    CATEGORY_GROUPS = {
        "polarizacao": {"name": "Batalhas & Polarização", "icon": "⚔️"},
        "batalha_polarizacao": {"name": "Batalhas & Polarização", "icon": "⚔️"},
        "tabuleiro_coordenadas": {"name": "Tabuleiro & Estratégia", "icon": "🎯"},
        "corrida_velocidade": {"name": "Corridas & Velocidade", "icon": "🏎️"},
        "apostas_corrida": {"name": "Corridas & Velocidade", "icon": "🏎️"},
        "cooperativo_boss": {"name": "Boss Raid & Cooperativo", "icon": "👾"},
        "defesa_planetaria": {"name": "Boss Raid & Cooperativo", "icon": "👾"},
        "fisica_pachinko": {"name": "Pachinko & Física", "icon": "🔮"},
        "arcade_pinball": {"name": "Pachinko & Física", "icon": "🔮"},
        "equilibrio_fisica": {"name": "Pachinko & Física", "icon": "🔮"},
        "sorteios_roletas": {"name": "Roletas & Sorte", "icon": "🎰"},
        "tensao_eliminacao": {"name": "Tensão & Eliminação", "icon": "💣"},
        "artilharia_cinematica": {"name": "Ação, Ritmo & Esportes", "icon": "⚡"},
        "arcade_navegacao": {"name": "Ação, Ritmo & Esportes", "icon": "⚡"},
        "esportes_fisica": {"name": "Ação, Ritmo & Esportes", "icon": "⚡"},
        "esportes_penaltis": {"name": "Ação, Ritmo & Esportes", "icon": "⚡"},
        "ritmo_musical": {"name": "Ação, Ritmo & Esportes", "icon": "⚡"},
        "habilidade_reflexo": {"name": "Ação, Ritmo & Esportes", "icon": "⚡"},
        "quiz_trivia": {"name": "Ação, Ritmo & Esportes", "icon": "⚡"},
        "ritmo_agilidade": {"name": "Ação, Ritmo & Esportes", "icon": "⚡"},
        "fuga_reflexo": {"name": "Ação, Ritmo & Esportes", "icon": "⚡"},
        "pontaria_precisao": {"name": "Ação, Ritmo & Esportes", "icon": "⚡"}
    }

    for item in manifest_data:
        cat_key = item.get("category", "")
        group_info = CATEGORY_GROUPS.get(cat_key, {"name": "Geral & Arcade", "icon": "🎮"})
        item["groupName"] = group_info["name"]
        item["groupIcon"] = group_info["icon"]

    manifest_json_str = json.dumps(manifest_data, ensure_ascii=False)

    html_template = """<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>V5 Games — Plataforma Soberana de Jogos de Live & Storefront 9:16</title>
  <link rel="icon" href="/favicon.ico" type="image/x-icon">
  <link rel="manifest" href="/manifest.json">
  <meta name="description" content="A Steam das Lives Interativas 9:16 e Games Proprietários da Holding V5 Apollo.">
  <style>
    /* ==========================================================================
       V5 GAMES SOVEREIGN PLATFORM — DESIGN SYSTEM (DARK OBSIDIAN & NEON GLASS)
       Holding V5 Apollo — 100% Offline, Zero CDNs Externas
       ========================================================================== */
    :root {
      --bg-primary: #030712;
      --bg-secondary: #0b1120;
      --bg-surface: #0f172a;
      --bg-surface-elevated: #1e293b;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(56, 189, 248, 0.3);
      --border-purple: rgba(168, 85, 247, 0.4);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-subtle: #64748b;
      --neon-cyan: #00f0ff;
      --neon-purple: #a855f7;
      --neon-gold: #f59e0b;
      --neon-rose: #f43f5e;
      --neon-green: #10b981;
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-xl: 24px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }

    body {
      background-color: var(--bg-primary);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      line-height: 1.5;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #030712; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }

    /* ==========================================================================
       HEADER & BARRA DE NAVEGAÇÃO SOBERANA
       ========================================================================== */
    header.main-header {
      position: sticky;
      top: 0;
      background: rgba(11, 17, 32, 0.95);
      border-bottom: 1px solid var(--border-subtle);
      padding: 12px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      backdrop-filter: blur(16px);
      z-index: 1000;
    }

    .brand-wrap {
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
    }

    .brand-badge {
      width: 38px;
      height: 38px;
      background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-purple) 100%);
      border-radius: var(--radius-sm);
      display: flex;
      justify-content: center;
      align-items: center;
      font-weight: 900;
      font-size: 18px;
      color: #030712;
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
    }

    .brand-name {
      font-size: 18px;
      font-weight: 900;
      letter-spacing: 1.5px;
      background: linear-gradient(90deg, #ffffff 0%, var(--neon-cyan) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      line-height: 1.2;
    }

    .brand-sub {
      font-size: 10px;
      color: var(--neon-cyan);
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 1px;
    }

    /* Abas de Navegação */
    nav.nav-tabs {
      display: flex;
      align-items: center;
      gap: 4px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 30px;
      padding: 4px;
    }

    .nav-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 12.5px;
      font-weight: 700;
      padding: 8px 14px;
      border-radius: 20px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      white-space: nowrap;
    }

    .nav-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.05);
    }

    .nav-btn.active {
      background: linear-gradient(135deg, rgba(0, 240, 255, 0.22) 0%, rgba(168, 85, 247, 0.22) 100%);
      border: 1px solid var(--border-accent);
      color: var(--neon-cyan);
      box-shadow: 0 0 14px rgba(0, 240, 255, 0.2);
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .live-status-pill {
      font-size: 11px;
      font-weight: 800;
      padding: 5px 12px;
      border-radius: 20px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .pulse-dot {
      width: 7px;
      height: 7px;
      background: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    .btn-quick-cockpit {
      background: linear-gradient(135deg, var(--neon-purple) 0%, #7c3aed 100%);
      border: none;
      color: #ffffff;
      font-size: 12px;
      font-weight: 800;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 0 15px rgba(168, 85, 247, 0.35);
      transition: all 0.2s;
    }

    .btn-quick-cockpit:hover {
      transform: translateY(-1px);
      box-shadow: 0 0 20px rgba(168, 85, 247, 0.55);
    }

    /* ==========================================================================
       CONTAINER PRINCIPAL DAS VIEWS
       ========================================================================== */
    main.app-container {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .app-view {
      display: none;
      flex-direction: column;
      width: 100%;
      animation: fadeIn 0.25s ease-out;
    }

    .app-view.active {
      display: flex;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* ==========================================================================
       VIEW 1: ARCADE & CATÁLOGO
       ========================================================================== */
    .hero-banner {
      padding: 40px 32px 30px;
      background: radial-gradient(circle at 50% 0%, rgba(56, 189, 248, 0.12) 0%, rgba(3, 7, 18, 0) 70%);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }

    .hero-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(0, 240, 255, 0.08);
      border: 1px solid var(--border-accent);
      color: var(--neon-cyan);
      font-size: 11px;
      font-weight: 800;
      padding: 4px 14px;
      border-radius: 20px;
      margin-bottom: 14px;
      letter-spacing: 0.5px;
    }

    .hero-title {
      font-size: 34px;
      font-weight: 900;
      color: #ffffff;
      max-width: 850px;
      line-height: 1.25;
      margin-bottom: 12px;
    }

    .hero-title span {
      background: linear-gradient(90deg, var(--neon-cyan) 0%, var(--neon-purple) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-desc {
      font-size: 15px;
      color: var(--text-muted);
      max-width: 680px;
      line-height: 1.6;
      margin-bottom: 24px;
    }

    .hero-stats {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
      justify-content: center;
    }

    .stat-badge {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 10px 18px;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 120px;
    }

    .stat-val {
      font-size: 20px;
      font-weight: 900;
      color: var(--neon-cyan);
    }

    .stat-label {
      font-size: 11px;
      color: var(--text-subtle);
      text-transform: uppercase;
      font-weight: 700;
      margin-top: 2px;
    }

    /* Barra de Pesquisa e Filtros */
    .catalog-controls {
      padding: 24px 32px 16px;
      background: var(--bg-secondary);
      border-bottom: 1px solid var(--border-subtle);
    }

    .search-row {
      display: flex;
      gap: 16px;
      align-items: center;
      margin-bottom: 16px;
    }

    .search-input-wrap {
      flex: 1;
      position: relative;
    }

    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-subtle);
      font-size: 14px;
    }

    .search-input {
      width: 100%;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 12px 16px 12px 40px;
      color: var(--text-main);
      font-size: 14px;
      outline: none;
      transition: all 0.2s;
    }

    .search-input:focus {
      border-color: var(--neon-cyan);
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.25);
    }

    .catalog-counter {
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      white-space: nowrap;
    }

    .filter-pills {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .filter-pill {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 20px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }

    .filter-pill:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.05);
    }

    .filter-pill.active {
      background: rgba(0, 240, 255, 0.15);
      border-color: var(--neon-cyan);
      color: var(--neon-cyan);
    }

    /* Grid de Jogos */
    .games-grid {
      padding: 32px;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 24px;
    }

    .game-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }

    .game-card:hover {
      transform: translateY(-4px);
      border-color: var(--border-accent);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 240, 255, 0.15);
    }

    .card-thumb-wrap {
      position: relative;
      width: 100%;
      aspect-ratio: 9/16;
      max-height: 220px;
      background: #020617;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .card-thumb {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
    }

    .game-card:hover .card-thumb {
      transform: scale(1.05);
    }

    .card-badges-top {
      position: absolute;
      top: 10px;
      left: 10px;
      right: 10px;
      display: flex;
      justify-content: space-between;
      pointer-events: none;
    }

    .badge-number {
      background: rgba(3, 7, 18, 0.85);
      border: 1px solid var(--border-subtle);
      color: var(--neon-cyan);
      font-size: 11px;
      font-weight: 900;
      padding: 3px 8px;
      border-radius: var(--radius-sm);
    }

    .badge-category {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: var(--radius-sm);
    }

    .card-body {
      padding: 16px;
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .card-title {
      font-size: 16px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 6px;
      line-height: 1.3;
    }

    .card-desc {
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 14px;
      flex: 1;
    }

    .card-commands {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }

    .cmd-pill {
      background: var(--bg-secondary);
      border: 1px solid var(--border-subtle);
      color: var(--neon-gold);
      font-size: 10px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      font-family: monospace;
    }

    .card-actions {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .btn-card-test {
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      font-size: 12px;
      font-weight: 700;
      padding: 8px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }

    .btn-card-test:hover {
      background: rgba(0, 240, 255, 0.15);
      border-color: var(--neon-cyan);
      color: var(--neon-cyan);
    }

    .btn-card-config {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.2) 0%, rgba(56, 189, 248, 0.2) 100%);
      border: 1px solid var(--border-purple);
      color: #d8b4fe;
      font-size: 12px;
      font-weight: 700;
      padding: 8px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }

    .btn-card-config:hover {
      background: rgba(168, 85, 247, 0.35);
      color: #ffffff;
      transform: translateY(-1px);
    }

    /* ==========================================================================
       VIEW 2: COCKPIT DO STREAMER (SALA DE CONFIGURAÇÃO & TOKENIZADOR)
       ========================================================================== */
    .cockpit-wrap {
      max-width: 1200px;
      width: 100%;
      margin: 0 auto;
      padding: 32px 24px;
    }

    .cockpit-header {
      text-align: center;
      margin-bottom: 32px;
    }

    .cockpit-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(168, 85, 247, 0.1);
      border: 1px solid var(--border-purple);
      color: #d8b4fe;
      font-size: 11px;
      font-weight: 800;
      padding: 4px 14px;
      border-radius: 20px;
      margin-bottom: 12px;
    }

    .cockpit-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 28px;
    }

    @media (max-width: 900px) {
      .cockpit-grid { grid-template-columns: 1fr; }
    }

    .cockpit-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 28px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .cockpit-card-title {
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 14px;
    }

    .cockpit-form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .cockpit-label {
      font-size: 11px;
      font-weight: 800;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .cockpit-input, .cockpit-select {
      width: 100%;
      background: var(--bg-primary);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 11px 14px;
      color: var(--text-main);
      font-size: 13.5px;
      outline: none;
      transition: all 0.2s;
    }

    .cockpit-input:focus, .cockpit-select:focus {
      border-color: var(--neon-cyan);
      box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }

    .cockpit-row-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    .output-box {
      background: var(--bg-primary);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 12px 14px;
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 12px;
      color: var(--neon-cyan);
      word-break: break-all;
      user-select: all;
      max-height: 100px;
      overflow-y: auto;
    }

    .output-box.json {
      color: var(--neon-gold);
    }

    .output-box.chat {
      color: #34d399;
      font-family: inherit;
      font-size: 13px;
    }

    .btn-copy-cockpit {
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-accent);
      color: var(--neon-cyan);
      font-size: 12px;
      font-weight: 800;
      padding: 10px 14px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .btn-copy-cockpit:hover {
      background: rgba(0, 240, 255, 0.15);
      transform: translateY(-1px);
    }

    .btn-launch-configured {
      background: linear-gradient(135deg, var(--neon-cyan) 0%, #0284c7 100%);
      border: none;
      color: #030712;
      font-size: 13px;
      font-weight: 900;
      padding: 12px 16px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
      margin-top: 8px;
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.35);
      transition: all 0.2s;
    }

    .btn-launch-configured:hover {
      transform: translateY(-2px);
      box-shadow: 0 0 25px rgba(0, 240, 255, 0.6);
    }

    /* ==========================================================================
       VIEW 3: SIMULADOR & TEST LAB 9:16
       ========================================================================== */
    .simulator-container {
      padding: 24px 32px;
      display: flex;
      flex-direction: column;
      align-items: center;
      max-width: 1400px;
      margin: 0 auto;
      width: 100%;
    }

    .sim-topbar {
      width: 100%;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 12px;
    }

    .sim-title-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .sim-game-select {
      background: var(--bg-primary);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 700;
      outline: none;
    }

    .sim-controls-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .sim-btn {
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      font-size: 12px;
      font-weight: 700;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .sim-btn:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: var(--border-accent);
      color: var(--neon-cyan);
    }

    .sim-stage-wrap {
      display: flex;
      gap: 32px;
      justify-content: center;
      align-items: flex-start;
      width: 100%;
    }

    @media (max-width: 1000px) {
      .sim-stage-wrap { flex-direction: column; align-items: center; }
    }

    .phone-mockup {
      width: 380px;
      height: 675px;
      background: #020617;
      border: 8px solid #1e293b;
      border-radius: 42px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8), 0 0 30px rgba(0, 240, 255, 0.15);
      position: relative;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .phone-notch {
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 130px;
      height: 22px;
      background: #1e293b;
      border-bottom-left-radius: 14px;
      border-bottom-right-radius: 14px;
      z-index: 100;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .phone-camera {
      width: 8px;
      height: 8px;
      background: #030712;
      border-radius: 50%;
    }

    #cartridge-iframe {
      width: 100%;
      height: 100%;
      border: none;
      background: #000000;
    }

    .safe-zone-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      pointer-events: none;
      display: none;
      flex-direction: column;
      justify-content: space-between;
      z-index: 90;
    }

    .safe-zone-overlay.active {
      display: flex;
    }

    .sz-top {
      height: 140px;
      background: rgba(239, 68, 68, 0.2);
      border-bottom: 2px dashed #ef4444;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 11px;
      font-weight: 800;
      color: #ef4444;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .sz-bottom {
      height: 180px;
      background: rgba(239, 68, 68, 0.2);
      border-top: 2px dashed #ef4444;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 11px;
      font-weight: 800;
      color: #ef4444;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* Painel Lateral do Test Lab */
    .sim-sidebar {
      flex: 1;
      max-width: 480px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .injector-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .injector-title {
      font-size: 14px;
      font-weight: 800;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .injector-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }

    .btn-inj {
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      font-size: 11px;
      font-weight: 700;
      padding: 8px 4px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      text-align: center;
      transition: all 0.15s;
    }

    .btn-inj:hover {
      background: rgba(0, 240, 255, 0.2);
      border-color: var(--neon-cyan);
      color: var(--neon-cyan);
    }

    .btn-inj-gift {
      background: rgba(245, 158, 11, 0.15);
      border-color: rgba(245, 158, 11, 0.4);
      color: #fbbf24;
    }

    .btn-inj-gift:hover {
      background: rgba(245, 158, 11, 0.3);
      color: #ffffff;
    }

    .terminal-box {
      background: #020617;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      height: 140px;
      padding: 10px;
      font-family: 'Consolas', monospace;
      font-size: 11px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .log-line {
      color: var(--text-muted);
    }

    .log-line .timestamp { color: var(--text-subtle); }
    .log-line .ev-type { color: var(--neon-cyan); font-weight: 700; }
    .log-line .ev-val { color: var(--neon-gold); }

    /* ==========================================================================
       VIEW 4: FRANQUIA ROXINHO (GAMES WEB & MOBILE)
       ========================================================================== */
    .roxinho-container {
      max-width: 1200px;
      width: 100%;
      margin: 0 auto;
      padding: 40px 24px;
    }

    .roxinho-hero {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.18) 0%, rgba(56, 189, 248, 0.08) 100%);
      border: 1px solid rgba(168, 85, 247, 0.35);
      border-radius: var(--radius-xl);
      padding: 40px;
      display: flex;
      align-items: center;
      gap: 36px;
      margin-bottom: 40px;
      box-shadow: 0 10px 40px rgba(168, 85, 247, 0.12);
    }

    @media (max-width: 800px) {
      .roxinho-hero { flex-direction: column; text-align: center; }
    }

    .roxinho-avatar-big {
      width: 120px;
      height: 120px;
      background: radial-gradient(circle at 35% 35%, #c084fc 0%, #7e22ce 100%);
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 58px;
      box-shadow: 0 0 35px rgba(168, 85, 247, 0.6);
      flex-shrink: 0;
    }

    .roxinho-hero-content h2 {
      font-size: 28px;
      font-weight: 900;
      color: #ffffff;
      margin-bottom: 8px;
    }

    .roxinho-hero-content h2 span {
      color: #d8b4fe;
    }

    .roxinho-hero-content p {
      font-size: 14.5px;
      color: var(--text-muted);
      line-height: 1.6;
    }

    .roxinho-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 24px;
    }

    .rox-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: all 0.25s;
    }

    .rox-card:hover {
      transform: translateY(-4px);
      border-color: rgba(168, 85, 247, 0.5);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(168, 85, 247, 0.2);
    }

    .rox-card-banner {
      height: 140px;
      background: radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.3) 0%, rgba(3, 7, 18, 0.9) 100%);
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 50px;
    }

    .rox-card-body {
      padding: 24px;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .rox-badge-status {
      align-self: flex-start;
      font-size: 10px;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .status-alpha { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .status-concept { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }
    .status-planned { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); }

    .rox-card-title {
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
    }

    .rox-card-desc {
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
      flex: 1;
    }

    .rox-specs {
      display: flex;
      gap: 12px;
      font-size: 11px;
      color: var(--text-subtle);
      border-top: 1px solid var(--border-subtle);
      padding-top: 12px;
    }

    /* ==========================================================================
       VIEW 5: PLANOS & ALUGUEL (STOREFRONT DE LIVES)
       ========================================================================== */
    .store-container {
      max-width: 1100px;
      width: 100%;
      margin: 0 auto;
      padding: 40px 24px;
    }

    .store-header {
      text-align: center;
      margin-bottom: 36px;
    }

    .store-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 28px;
      align-items: stretch;
    }

    .store-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-xl);
      padding: 36px 28px;
      display: flex;
      flex-direction: column;
      position: relative;
      transition: all 0.25s;
    }

    .store-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
    }

    .store-card.featured {
      border: 2px solid var(--neon-cyan);
      box-shadow: 0 0 35px rgba(0, 240, 255, 0.2);
      background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(11, 17, 32, 0.95) 100%);
    }

    .popular-ribbon {
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%);
      background: linear-gradient(135deg, var(--neon-cyan) 0%, #0284c7 100%);
      color: #030712;
      font-size: 10px;
      font-weight: 900;
      padding: 4px 14px;
      border-radius: 20px;
      letter-spacing: 1px;
      text-transform: uppercase;
    }

    .plan-name {
      font-size: 20px;
      font-weight: 900;
      color: #ffffff;
      margin-bottom: 8px;
    }

    .plan-desc {
      font-size: 13px;
      color: var(--text-muted);
      margin-bottom: 24px;
      line-height: 1.4;
    }

    .plan-price-wrap {
      display: flex;
      align-items: baseline;
      gap: 6px;
      margin-bottom: 8px;
    }

    .plan-currency {
      font-size: 18px;
      font-weight: 800;
      color: var(--neon-cyan);
    }

    .plan-price {
      font-size: 38px;
      font-weight: 900;
      color: #ffffff;
    }

    .plan-period {
      font-size: 12px;
      color: var(--text-subtle);
    }

    .plan-crypto-equiv {
      font-size: 12px;
      color: var(--neon-gold);
      font-weight: 700;
      margin-bottom: 24px;
    }

    .plan-features {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 32px;
      flex: 1;
    }

    .plan-features li {
      font-size: 13px;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-plan {
      width: 100%;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      font-size: 13px;
      font-weight: 800;
      padding: 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.2s;
    }

    .btn-plan:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: var(--text-main);
    }

    .btn-plan.featured {
      background: linear-gradient(135deg, var(--neon-cyan) 0%, #0284c7 100%);
      border: none;
      color: #030712;
      box-shadow: 0 0 15px rgba(0, 240, 255, 0.35);
    }

    .btn-plan.featured:hover {
      box-shadow: 0 0 25px rgba(0, 240, 255, 0.55);
    }

    /* ==========================================================================
       VIEW 6 & 7: GUIAS OBS & LEIS
       ========================================================================== */
    .guide-container {
      max-width: 900px;
      width: 100%;
      margin: 0 auto;
      padding: 40px 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .guide-step-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 24px;
      display: flex;
      gap: 20px;
    }

    .step-number {
      width: 38px;
      height: 38px;
      background: rgba(0, 240, 255, 0.15);
      border: 1px solid var(--border-accent);
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      color: var(--neon-cyan);
      font-weight: 900;
      font-size: 16px;
      flex-shrink: 0;
    }

    .step-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .step-title {
      font-size: 16px;
      font-weight: 800;
      color: #ffffff;
    }

    .step-desc {
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.6;
    }

    /* Toast Flutuante */
    #toast-notification {
      position: fixed;
      bottom: 28px;
      right: 28px;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid var(--border-accent);
      color: #ffffff;
      padding: 12px 20px;
      border-radius: var(--radius-md);
      font-size: 13px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(0, 240, 255, 0.25);
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 9999;
    }

    #toast-notification.show {
      transform: translateY(0);
      opacity: 1;
    }
  </style>
</head>
<body>

  <!-- HEADER OFICIAL DA PLATAFORMA SOBERANA -->
  <header class="main-header">
    <div class="brand-wrap" onclick="switchView('catalog')">
      <div class="brand-badge">V5</div>
      <div>
        <div class="brand-name">V5 GAMES</div>
        <div class="brand-sub">Holding V5 Apollo • Sovereign Games Platform</div>
      </div>
    </div>

    <!-- Abas Principais -->
    <nav class="nav-tabs">
      <button class="nav-btn active" id="tab-catalog" onclick="switchView('catalog')">
        <span>🕹️ Catálogo Arcade</span>
      </button>
      <button class="nav-btn" id="tab-cockpit" onclick="switchView('cockpit')">
        <span>🎮 Cockpit do Streamer</span>
      </button>
      <button class="nav-btn" id="tab-simulator" onclick="switchView('simulator')">
        <span>📱 Simulador 9:16</span>
      </button>
      <button class="nav-btn" id="tab-roxinho" onclick="switchView('roxinho')">
        <span>🟣 Franquia Roxinho</span>
      </button>
      <button class="nav-btn" id="tab-store" onclick="switchView('store')">
        <span>💎 Planos & Aluguel</span>
      </button>
      <button class="nav-btn" id="tab-obs" onclick="switchView('obs')">
        <span>📡 OBS & Broadcaster</span>
      </button>
      <button class="nav-btn" id="tab-laws" onclick="switchView('laws')">
        <span>⚡ As 5 Leis</span>
      </button>
    </nav>

    <!-- Status e Ação Rápida -->
    <div class="header-actions">
      <div class="live-status-pill">
        <span class="pulse-dot"></span>
        <span>41 CARTUCHOS</span>
      </div>

      <button class="btn-quick-cockpit" onclick="switchView('cockpit')">
        <span>🎮 Configurar Partida</span>
      </button>
    </div>
  </header>

  <!-- CONTAINER DE VIEWS -->
  <main class="app-container">

    <!-- =======================================================================
         VIEW 1: ARCADE & CATÁLOGO
         ======================================================================= -->
    <section class="app-view active" id="view-catalog">
      <div class="hero-banner">
        <div class="hero-tag">✨ A MAIOR FORJA DE JOGOS INTERATIVOS VERTICAIS 9:16</div>
        <h1 class="hero-title">A Steam dos <span>Jogos de Live Interativa</span></h1>
        <p class="hero-desc">
          Jogos desenvolvidos especificamente para transmissões no TikTok Live, YouTube Shorts e Twitch. 
          O público comanda a partida pelo chat ou presentes. Funciona no <strong>V5 Broadcaster</strong> ou diretamente como fonte de navegador em qualquer <strong>OBS Studio</strong>.
        </p>

        <div class="hero-stats">
          <div class="stat-badge">
            <span class="stat-val">41</span>
            <span class="stat-label">Cartuchos Homologados</span>
          </div>
          <div class="stat-badge">
            <span class="stat-val">1080x1920</span>
            <span class="stat-label">Resolução 9:16 Nativa</span>
          </div>
          <div class="stat-badge">
            <span class="stat-val">60 FPS</span>
            <span class="stat-label">Renderização Ultraleve</span>
          </div>
          <div class="stat-badge">
            <span class="stat-val">100% Offline</span>
            <span class="stat-label">Zero Dependência de CDN</span>
          </div>
          <div class="stat-badge">
            <span class="stat-val">Web Audio</span>
            <span class="stat-label">Sintetizador Procedural</span>
          </div>
        </div>
      </div>

      <!-- Controles de Busca e Filtros -->
      <div class="catalog-controls">
        <div class="search-row">
          <div class="search-input-wrap">
            <span class="search-icon">🔍</span>
            <input 
              type="text" 
              id="search-input" 
              class="search-input" 
              placeholder="Pesquisar por título, mecânica ou comando (ex: Cabo de Guerra, Plinko, 1, 2, Rosa)..." 
              oninput="filterGames()"
            >
          </div>
          <div class="catalog-counter" id="catalog-counter">Exibindo 41 de 41 cartuchos</div>
        </div>

        <div class="filter-pills" id="filter-pills-container"></div>
      </div>

      <!-- Grid de Jogos -->
      <div class="games-grid" id="games-grid"></div>
    </section>

    <!-- =======================================================================
         VIEW 2: COCKPIT DO STREAMER (SALA DE CONFIGURAÇÃO & TOKENIZADOR)
         ======================================================================= -->
    <section class="app-view" id="view-cockpit">
      <div class="cockpit-wrap">
        <div class="cockpit-header">
          <div class="cockpit-tag">🛠️ SALA DE CONTROLE DE TRANSMISSÃO</div>
          <h2 style="font-size: 30px; font-weight: 900; color: #ffffff;">Configure sua Partida & Gere seu Link OBS</h2>
          <p style="font-size: 15px; color: var(--text-muted); margin-top: 6px;">
            Personalize nomes de times, comandos aceitos e pesos de presentes. Obtenha a URL pronta para o OBS Studio ou a configuração para o V5 Broadcaster.
          </p>
        </div>

        <div class="cockpit-grid">
          <!-- Coluna 1: Formulário de Configuração -->
          <div class="cockpit-card">
            <div class="cockpit-card-title">
              <span>⚙️ Parâmetros da Partida</span>
            </div>

            <div class="cockpit-form-group">
              <label class="cockpit-label">Selecione o Cartucho de Jogo</label>
              <select id="cockpit-game-select" class="cockpit-select" onchange="updateCockpit()">
                <!-- Preenchido via JS -->
              </select>
            </div>

            <div class="cockpit-row-2">
              <div class="cockpit-form-group">
                <label class="cockpit-label">Nome do Time A (Azul)</label>
                <input type="text" id="cockpit-team-a" class="cockpit-input" value="Time Roxinho" oninput="updateCockpit()">
              </div>
              <div class="cockpit-form-group">
                <label class="cockpit-label">Comando Chat Time A</label>
                <input type="text" id="cockpit-cmd-a" class="cockpit-input" value="1" oninput="updateCockpit()">
              </div>
            </div>

            <div class="cockpit-row-2">
              <div class="cockpit-form-group">
                <label class="cockpit-label">Nome do Time B (Laranja)</label>
                <input type="text" id="cockpit-team-b" class="cockpit-input" value="Time Dourado" oninput="updateCockpit()">
              </div>
              <div class="cockpit-form-group">
                <label class="cockpit-label">Comando Chat Time B</label>
                <input type="text" id="cockpit-cmd-b" class="cockpit-input" value="2" oninput="updateCockpit()">
              </div>
            </div>

            <div class="cockpit-row-2">
              <div class="cockpit-form-group">
                <label class="cockpit-label">Meta de Pontos / Duração</label>
                <select id="cockpit-goal" class="cockpit-select" onchange="updateCockpit()">
                  <option value="50">50 Pontos (Rodada Ultra-Rápida)</option>
                  <option value="100" selected>100 Pontos (Padrão Equilibrado)</option>
                  <option value="200">200 Pontos (Batalha Épica)</option>
                </select>
              </div>
              <div class="cockpit-form-group">
                <label class="cockpit-label">Multiplicador de Gifts</label>
                <select id="cockpit-gift-mul" class="cockpit-select" onchange="updateCockpit()">
                  <option value="5">5x (Moderado)</option>
                  <option value="10" selected>10x (Padrão Recomendado)</option>
                  <option value="25">25x (Super Monetização)</option>
                  <option value="50">50x (Chuva de Presentes)</option>
                </select>
              </div>
            </div>

            <div class="cockpit-form-group">
              <label class="cockpit-label">Identificador do Streamer</label>
              <input type="text" id="cockpit-streamer" class="cockpit-input" value="streamer_v5" oninput="updateCockpit()">
            </div>
          </div>

          <!-- Coluna 2: Saídas & Links Prontos -->
          <div class="cockpit-card">
            <div class="cockpit-card-title">
              <span>🚀 Integração & Transmissão</span>
            </div>

            <!-- OBS Browser Source Link -->
            <div class="cockpit-form-group">
              <label class="cockpit-label">1. URL para OBS Studio / Streamlabs (Browser Source)</label>
              <div class="output-box" id="cockpit-out-obs">Carregando...</div>
              <button class="btn-copy-cockpit" onclick="copyCockpitObsUrl()">
                <span>📋 Copiar Link do OBS (1080x1920)</span>
              </button>
            </div>

            <!-- Broadcaster Config Payload -->
            <div class="cockpit-form-group">
              <label class="cockpit-label">2. Payload de Vinculação para V5 Broadcaster</label>
              <div class="output-box json" id="cockpit-out-broadcaster">Carregando...</div>
              <button class="btn-copy-cockpit" onclick="copyBroadcasterConfig()">
                <span>⚡ Copiar JSON do Broadcaster</span>
              </button>
            </div>

            <!-- Chat Title / Call to Action -->
            <div class="cockpit-form-group">
              <label class="cockpit-label">3. Legenda Pronta para o Chat da Live</label>
              <div class="output-box chat" id="cockpit-out-chat">Carregando...</div>
              <button class="btn-copy-cockpit" onclick="copyChatHeadline()">
                <span>💬 Copiar Chamada do Chat</span>
              </button>
            </div>

            <button class="btn-launch-configured" onclick="launchFromCockpitToSimulator()">
              <span>📱 Testar no Simulador Agora</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- =======================================================================
         VIEW 3: SIMULADOR & TEST LAB 9:16
         ======================================================================= -->
    <section class="app-view" id="view-simulator">
      <div class="simulator-container">
        
        <div class="sim-topbar">
          <div class="sim-title-group">
            <span style="font-size: 12px; font-weight:800; color:var(--text-subtle); text-transform:uppercase;">Cartucho:</span>
            <select id="sim-select" class="sim-game-select" onchange="onSimSelectChange()">
              <!-- Preenchido via JS -->
            </select>
          </div>

          <div class="sim-controls-group">
            <button class="sim-btn" onclick="reloadSimulator()">🔄 Reiniciar</button>
            <button class="sim-btn" id="btn-toggle-sz" onclick="toggleSimSafeZones()">📐 Safe Zones (9:16)</button>
            <button class="sim-btn" onclick="openFullscreenGame()">🖥️ Tela Cheia</button>
            <button class="sim-btn" onclick="copyCurrentObsUrl()">📋 Copiar Link OBS</button>
          </div>
        </div>

        <div class="sim-stage-wrap">
          <!-- Mockup Smartphone 9:16 -->
          <div class="phone-viewport-col">
            <div class="phone-mockup">
              <div class="phone-notch">
                <div class="phone-camera"></div>
              </div>

              <iframe id="cartridge-iframe" src="catalogo_jogos/01_cabo_de_guerra_neon/index.html"></iframe>

              <div class="safe-zone-overlay" id="sim-safe-overlay">
                <div class="sz-top">⚠️ Safe Zone Topo (140px) — Placar & Metas</div>
                <div class="sz-bottom">⚠️ Safe Zone Base (180px) — Feed & Comentários</div>
              </div>
            </div>
          </div>

          <!-- Lateral: Injetor de Comandos e Terminal -->
          <div class="sim-sidebar">
            <div class="injector-card">
              <div class="injector-title">
                <span>⚡ Injetor Manual de Comentários</span>
              </div>
              <div class="injector-row">
                <button class="btn-inj" onclick="injectSimEvent({type:'comment', comment:'1', user:'@live_teste', team:'A'})">Voto "1"</button>
                <button class="btn-inj" onclick="injectSimEvent({type:'comment', comment:'2', user:'@live_teste', team:'B'})">Voto "2"</button>
                <button class="btn-inj" onclick="injectSimEvent({type:'comment', comment:'A', user:'@live_teste', team:'A'})">Voto "A"</button>
                <button class="btn-inj" onclick="injectSimEvent({type:'comment', comment:'B', user:'@live_teste', team:'B'})">Voto "B"</button>
              </div>
            </div>

            <div class="injector-card">
              <div class="injector-title">
                <span>🎁 Injetor de Presentes (Gifts)</span>
              </div>
              <div class="injector-row">
                <button class="btn-inj btn-inj-gift" onclick="injectSimEvent({type:'gift', giftName:'Rosa', value:1, team:'A', user:'@donator_a'})">🌹 Rosa (Time A)</button>
                <button class="btn-inj btn-inj-gift" onclick="injectSimEvent({type:'gift', giftName:'Rosa', value:1, team:'B', user:'@donator_b'})">🌹 Rosa (Time B)</button>
                <button class="btn-inj btn-inj-gift" onclick="injectSimEvent({type:'gift', giftName:'Leão', value:500, team:'A', user:'@whale_a'})">🦁 Leão (Time A)</button>
                <button class="btn-inj btn-inj-gift" onclick="injectSimEvent({type:'gift', giftName:'Leão', value:500, team:'B', user:'@whale_b'})">🦁 Leão (Time B)</button>
              </div>
            </div>

            <div class="injector-card">
              <div class="injector-title" style="justify-content: space-between;">
                <span>📡 Terminal de Eventos & Telemetria</span>
                <button style="background:transparent; border:none; color:var(--text-subtle); cursor:pointer; font-size:11px;" onclick="clearEventLogs()">Limpar</button>
              </div>
              <div class="terminal-box" id="event-terminal">
                <div class="log-line"><span class="timestamp">[00:00:00]</span> Barramento inicializado. Aguardando eventos...</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- =======================================================================
         VIEW 4: FRANQUIA ROXINHO (GAMES WEB & MOBILE)
         ======================================================================= -->
    <section class="app-view" id="view-roxinho">
      <div class="roxinho-container">
        
        <div class="roxinho-hero">
          <div class="roxinho-avatar-big">👾</div>
          <div class="roxinho-hero-content">
            <h2>O Universo de Jogos do <span>Roxinho</span></h2>
            <p>
              O mascote oficial da Holding V5 Apollo agora protagoniza sua própria franquia de games autorais. 
              Projetados para web rápida, celular (PWA) e transmissões interativas, com física responsiva e conexão com o ecossistema digital.
            </p>
          </div>
        </div>

        <div class="roxinho-grid">
          <!-- Card 1: Roxinho Runner -->
          <div class="rox-card">
            <div class="rox-card-banner">🏃‍♂️💨</div>
            <div class="rox-card-body">
              <span class="rox-badge-status status-alpha">Alpha Fechado • Web & Mobile</span>
              <h3 class="rox-card-title">Roxinho Runner</h3>
              <p class="rox-card-desc">
                Corrida infinita pelas cidades cibernéticas da Holding. Salte obstáculos, colete moedas douradas V5, pegue power-ups magnéticos e desafie o ranking global.
              </p>
              <div class="rox-specs">
                <span>📱 Touch & Teclado</span>
                <span>⚡ 60 FPS Canvas</span>
                <span>🏆 Ranking Online</span>
              </div>
            </div>
          </div>

          <!-- Card 2: Roxinho Galaxy Defender -->
          <div class="rox-card">
            <div class="rox-card-banner">🚀👾</div>
            <div class="rox-card-body">
              <span class="rox-badge-status status-concept">Em Forja • Live & Celular</span>
              <h3 class="rox-card-title">Roxinho Galaxy Defender</h3>
              <p class="rox-card-desc">
                Shoot 'em up vertical 9:16. Pode ser jogado com os polegares no celular ou transmitido na live onde o chat pilota os escudos e canhões da nave do Roxinho.
              </p>
              <div class="rox-specs">
                <span>🎮 Híbrido Live/Mobile</span>
                <span>💥 Boss Fights</span>
                <span>🔮 Web Audio</span>
              </div>
            </div>
          </div>

          <!-- Card 3: Roxinho Tycoon -->
          <div class="rox-card">
            <div class="rox-card-banner">🏰💎</div>
            <div class="rox-card-body">
              <span class="rox-badge-status status-planned">Conceito Aprovado • Idle & RMT</span>
              <h3 class="rox-card-title">Roxinho Idle Tycoon</h3>
              <p class="rox-card-desc">
                Simulador de império digital onde o Roxinho administra fazendas de servidores e nós de computação. Base para futuros experimentos de economia digital e RMT da Holding.
              </p>
              <div class="rox-specs">
                <span>🌐 Web3 Ready</span>
                <span>⏳ Progressão Idle</span>
                <span>💎 Economia Digital</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- =======================================================================
         VIEW 5: PLANOS & ALUGUEL (STOREFRONT DE LIVES)
         ======================================================================= -->
    <section class="app-view" id="view-store">
      <div class="store-container">
        
        <div class="store-header">
          <div class="hero-tag">💎 MONETIZAÇÃO & LICENCIAMENTO</div>
          <h2 style="font-size: 32px; font-weight: 900; color: #ffffff;">Alugue ou Adquira Cartuchos para sua Live</h2>
          <p style="font-size: 15px; color: var(--text-muted); margin-top: 6px;">
            Trilhos de pagamento soberanos da Holding V5 Apollo: PIX Instantâneo e USDT (Polygon PoS D+0).
          </p>
        </div>

        <div class="store-grid">
          <!-- Plano 1: Passe 24h -->
          <div class="store-card">
            <h3 class="plan-name">Passe 24h Live</h3>
            <p class="plan-desc">Ideal para uma transmissão especial no fim de semana ou evento pontual.</p>
            <div class="plan-price-wrap">
              <span class="plan-currency">R$</span>
              <span class="plan-price">19,90</span>
              <span class="plan-period">/ 24 horas</span>
            </div>
            <div class="plan-crypto-equiv">≈ 4 USDT (Polygon PoS)</div>
            <ul class="plan-features">
              <li>✅ 1 Cartucho liberado à sua escolha</li>
              <li>✅ Link de Browser Source ilimitado por 24h</li>
              <li>✅ Suporte a presentes e votos do chat</li>
              <li>✅ Áudio procedural sintetizado</li>
            </ul>
            <button class="btn-plan" onclick="simulateCheckout('Passe 24h Live', '19.90', '4 USDT')">Alugar por 24h</button>
          </div>

          <!-- Plano 2: Streamer Pro (Destaque) -->
          <div class="store-card featured">
            <div class="popular-ribbon">MAIS ESCOLHIDO</div>
            <h3 class="plan-name">Streamer Pro Mensal</h3>
            <p class="plan-desc">Acesso completo e ilimitado a todos os cartuchos da plataforma.</p>
            <div class="plan-price-wrap">
              <span class="plan-currency">R$</span>
              <span class="plan-price">79,90</span>
              <span class="plan-period">/ mês</span>
            </div>
            <div class="plan-crypto-equiv">≈ 15 USDT (Polygon PoS)</div>
            <ul class="plan-features">
              <li>✅ <strong>Todos os 41 Cartuchos Liberados</strong></li>
              <li>✅ Personalizador total no Cockpit do Streamer</li>
              <li>✅ Troca de times, cores e multiplicador de gifts</li>
              <li>✅ Atualizações de novos cartuchos inclusas</li>
              <li>✅ Suporte nativo ao V5 Broadcaster & OBS</li>
            </ul>
            <button class="btn-plan featured" onclick="simulateCheckout('Streamer Pro Mensal', '79.90', '15 USDT')">Assinar Mensalidade</button>
          </div>

          <!-- Plano 3: Agência / Whitelabel -->
          <div class="store-card">
            <h3 class="plan-name">Licença Whitelabel</h3>
            <p class="plan-desc">Para estúdios e agências que gerenciam múltiplos canais e streamers.</p>
            <div class="plan-price-wrap">
              <span class="plan-currency">R$</span>
              <span class="plan-price">299,00</span>
              <span class="plan-period">/ vitalício</span>
            </div>
            <div class="plan-crypto-equiv">≈ 60 USDT (Polygon PoS)</div>
            <ul class="plan-features">
              <li>✅ Acesso vitalício a todo o catálogo</li>
              <li>✅ Transmissões simultâneas ilimitadas</li>
              <li>✅ Customização completa de marcas e logotipos</li>
              <li>✅ Conector API direto para Broadcaster e OBS</li>
            </ul>
            <button class="btn-plan" onclick="simulateCheckout('Licença Whitelabel', '299.00', '60 USDT')">Adquirir Licença</button>
          </div>
        </div>

      </div>
    </section>

    <!-- =======================================================================
         VIEW 6: GUIA OBS & V5 BROADCASTER
         ======================================================================= -->
    <section class="app-view" id="view-obs">
      <div class="guide-container">
        
        <div style="text-align: center; margin-bottom: 10px;">
          <h2 style="font-size: 30px; font-weight: 900; color: #ffffff;">Transmitindo no OBS Studio ou V5 Broadcaster</h2>
          <p style="font-size: 15px; color: var(--text-muted); margin-top: 6px;">
            O V5 Games é desacoplado e funciona perfeitamente em ambos os cenários.
          </p>
        </div>

        <div class="guide-step-card">
          <div class="step-number">A</div>
          <div class="step-body">
            <div class="step-title">Cenário 1: Se você usa o V5 Broadcaster (Nosso Estúdio Automático)</div>
            <div class="step-desc">
              O V5 Broadcaster cuida da transmissão 24/7 e lê o chat do TikTok automaticamente.
              Basta entrar na aba <strong>🎮 Cockpit do Streamer</strong> aqui no V5 Games, copiar o <strong>Payload de Vinculação</strong> e inseri-lo no Broadcaster. O Broadcaster carrega o jogo via link sem inflar o repositório com arquivos estáticos.
            </div>
          </div>
        </div>

        <div class="guide-step-card">
          <div class="step-number">B</div>
          <div class="step-body">
            <div class="step-title">Cenário 2: Se você transmite com OBS Studio, Streamlabs ou TikTok Live Studio</div>
            <div class="step-desc">
              1. Crie uma cena com resolução <strong>1080x1920</strong> (Vertical 9:16).<br>
              2. Adicione uma <strong>Fonte de Navegador (Browser Source)</strong> com Largura: <code>1080</code> e Altura: <code>1920</code>.<br>
              3. Cole a URL gerada pelo Cockpit do Streamer (ex: <code>http://localhost:3012/catalogo_jogos/01_cabo_de_guerra_neon/index.html?teamA=Brasil&teamB=Argentina</code>).<br>
              4. Marque a opção <em>"Controlar áudio via OBS"</em> para que os sintetizadores do Web Audio saiam na sua live!
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- =======================================================================
         VIEW 7: AS 5 LEIS ABSOLUTAS
         ======================================================================= -->
    <section class="app-view" id="view-laws">
      <div class="guide-container">
        
        <div style="text-align: center; margin-bottom: 10px;">
          <h2 style="font-size: 30px; font-weight: 900; color: #ffffff;">As 5 Leis Absolutas do Cartucho V5</h2>
          <p style="font-size: 15px; color: var(--text-muted); margin-top: 6px;">
            Princípios de engenharia e retenção para transmissões interativas contínuas.
          </p>
        </div>

        <div class="guide-step-card">
          <div class="step-number">1</div>
          <div class="step-body">
            <div class="step-title">Formato Vertical Estrito 9:16 (1080 x 1920 px)</div>
            <div class="step-desc">
              Todo jogo nasce vertical com Safe Zones reservadas: topo (140px) para placar e metas; base (180px) livre para não sobrepor o feed do TikTok e YouTube Shorts.
            </div>
          </div>
        </div>

        <div class="guide-step-card">
          <div class="step-number">2</div>
          <div class="step-body">
            <div class="step-title">Zero Teclado / Zero Mouse na Live (O Público é o Controle)</div>
            <div class="step-desc">
              O streamer não joga. O jogo é 100% pilotado pelo chat (comentários rápidos como 1, 2, azul, laranja) e Presentes (Rosas, Moedas, Leão). Presentes sempre têm peso massivo (5x a 50x) para estimular monetização imediata.
            </div>
          </div>
        </div>

        <div class="guide-step-card">
          <div class="step-number">3</div>
          <div class="step-body">
            <div class="step-title">Motor Anti-Silêncio Orgânico Embutido</div>
            <div class="step-desc">
              É terminantemente proibido o jogo ficar com a tela estática esperando alguém comentar. Se o chat ficar sem interação por 3 segundos, o motor autônomo injeta microações fictícias para manter a tela em movimento frenético e provocar a audiência real a intervir.
            </div>
          </div>
        </div>

        <div class="guide-step-card">
          <div class="step-number">4</div>
          <div class="step-body">
            <div class="step-title">Sintetizador de Áudio Procedural (Web Audio API)</div>
            <div class="step-desc">
              Zero dependência de arquivos .mp3 ou .wav externos que possam sofrer erro de CORS ou atrasar o carregamento do OBS. Todo som é sintetizado matematicamente via Web Audio API.
            </div>
          </div>
        </div>

        <div class="guide-step-card">
          <div class="step-number">5</div>
          <div class="step-body">
            <div class="step-title">Ciclo Fechado de Partidas & Auto-Reset</div>
            <div class="step-desc">
              Partidas rápidas entre 30 e 60 segundos. Ao atingir a vitória: comemoração com fanfarra por 5 segundos, seguido de reinício 100% automático e limpeza total de memória sem necessidade de atualizar a página.
            </div>
          </div>
        </div>

      </div>
    </section>

  </main>

  <!-- TOAST NOTIFICATION FLUTUANTE -->
  <div id="toast-notification">
    <span id="toast-icon">📋</span>
    <span id="toast-text">Link copiado com sucesso!</span>
  </div>

  <!-- SCRIPT PRINCIPAL DO PORTAL SOBERANO -->
  <script>
    const GAMES_CATALOG = __MANIFEST_JSON_STR__;

    let activeFilter = 'all';
    let currentSimSlug = '01_cabo_de_guerra_neon';
    let broadcastChannel = null;

    try {
      broadcastChannel = new BroadcastChannel('v5_broadcaster_games');
    } catch (e) {
      console.warn('BroadcastChannel não suportado neste navegador:', e);
    }

    // =========================================================================
    // NAVEGAÇÃO ENTRE TELAS (VIEWS)
    // =========================================================================
    function switchView(viewName) {
      document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
      const activeNavBtn = document.getElementById(`tab-${viewName}`);
      if (activeNavBtn) activeNavBtn.classList.add('active');

      document.querySelectorAll('.app-view').forEach(view => view.classList.remove('active'));
      const targetView = document.getElementById(`view-${viewName}`);
      if (targetView) targetView.classList.add('active');

      window.scrollTo({ top: 0, behavior: 'smooth' });

      if (viewName === 'cockpit') {
        updateCockpit();
      }
    }

    // =========================================================================
    // CATÁLOGO DE JOGOS & FILTROS
    // =========================================================================
    function renderPills() {
      const container = document.getElementById('filter-pills-container');
      const groupsMap = {};

      GAMES_CATALOG.forEach(g => {
        const group = g.groupName || 'Outros';
        groupsMap[group] = (groupsMap[group] || 0) + 1;
      });

      let html = `<button class="filter-pill active" onclick="setFilter('all', this)">✨ Todos (${GAMES_CATALOG.length})</button>`;
      for (const [groupName, count] of Object.entries(groupsMap)) {
        html += `<button class="filter-pill" onclick="setFilter('${groupName}', this)">${groupName} (${count})</button>`;
      }
      container.innerHTML = html;
    }

    function setFilter(groupName, btnEl) {
      activeFilter = groupName;
      document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
      filterGames();
    }

    function filterGames() {
      const query = (document.getElementById('search-input').value || '').toLowerCase().trim();
      const filtered = GAMES_CATALOG.filter(game => {
        const matchesFilter = activeFilter === 'all' || game.groupName === activeFilter;
        if (!matchesFilter) return false;

        if (!query) return true;
        const inName = (game.name || '').toLowerCase().includes(query);
        const inDesc = (game.description || '').toLowerCase().includes(query);
        const inCmds = (game.commands || []).some(c => c.toLowerCase().includes(query));
        return inName || inDesc || inCmds;
      });

      renderGamesGrid(filtered);
      document.getElementById('catalog-counter').innerText = `Exibindo ${filtered.length} de ${GAMES_CATALOG.length} cartuchos`;
    }

    function renderGamesGrid(games) {
      const grid = document.getElementById('games-grid');
      if (!games || games.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted);">Nenhum cartucho encontrado para sua busca.</div>';
        return;
      }

      let html = '';
      games.forEach(game => {
        const numberStr = '#' + (game.slug.match(/^(\\d+)/) ? game.slug.match(/^(\\d+)/)[1] : '00');
        const commandsHtml = (game.commands || ['1', '2']).map(c => `<span class="cmd-pill">${c}</span>`).join('');

        html += `
          <div class="game-card">
            <div class="card-thumb-wrap">
              <img src="catalogo_jogos/${game.slug}/thumbnail.svg" alt="${game.name}" class="card-thumb" loading="lazy">
              <div class="card-badges-top">
                <span class="badge-number">${numberStr}</span>
                <span class="badge-category">${game.groupIcon || '🎮'} ${game.groupName || 'Arcade'}</span>
              </div>
            </div>
            <div class="card-body">
              <h3 class="card-title">${game.name}</h3>
              <p class="card-desc">${game.description}</p>
              <div class="card-commands">
                <span style="font-size: 10px; color: var(--text-subtle); align-self: center; font-weight: 700;">CHAT:</span>
                ${commandsHtml}
              </div>
              <div class="card-actions">
                <button class="btn-card-test" onclick="launchGameSimulator('${game.slug}')">📱 Testar</button>
                <button class="btn-card-config" onclick="openCockpitForGame('${game.slug}')">⚙️ Configurar</button>
              </div>
            </div>
          </div>
        `;
      });
      grid.innerHTML = html;
    }

    // =========================================================================
    // COCKPIT DO STREAMER (SALA DE CONFIGURAÇÃO & TOKENIZADOR)
    // =========================================================================
    function populateCockpitSelect() {
      const select = document.getElementById('cockpit-game-select');
      if (!select) return;

      let html = '';
      GAMES_CATALOG.forEach(g => {
        html += `<option value="${g.slug}">${g.name} (${g.slug})</option>`;
      });
      select.innerHTML = html;
    }

    function openCockpitForGame(slug) {
      switchView('cockpit');
      const select = document.getElementById('cockpit-game-select');
      if (select) {
        select.value = slug;
        updateCockpit();
      }
    }

    function updateCockpit() {
      const select = document.getElementById('cockpit-game-select');
      const slug = select ? select.value : '01_cabo_de_guerra_neon';
      const teamA = document.getElementById('cockpit-team-a').value || 'Time A';
      const cmdA = document.getElementById('cockpit-cmd-a').value || '1';
      const teamB = document.getElementById('cockpit-team-b').value || 'Time B';
      const cmdB = document.getElementById('cockpit-cmd-b').value || '2';
      const goal = document.getElementById('cockpit-goal').value || '100';
      const giftMul = document.getElementById('cockpit-gift-mul').value || '10';
      const streamer = document.getElementById('cockpit-streamer').value || 'streamer_v5';

      const origin = window.location.origin || 'http://localhost:3012';
      const obsUrl = `${origin}/catalogo_jogos/${slug}/index.html?streamer=${encodeURIComponent(streamer)}&teamA=${encodeURIComponent(teamA)}&teamB=${encodeURIComponent(teamB)}&cmdA=${encodeURIComponent(cmdA)}&cmdB=${encodeURIComponent(cmdB)}&goal=${goal}&giftMul=${giftMul}`;
      
      const broadcasterPayload = {
        type: "v5_bind_game",
        gameSlug: slug,
        url: obsUrl,
        streamer: streamer,
        settings: {
          teamA: teamA,
          teamB: teamB,
          cmdA: cmdA,
          cmdB: cmdB,
          goal: parseInt(goal, 10),
          giftMultiplier: parseFloat(giftMul)
        }
      };

      const chatHeadline = `🎮 LIVE INTERATIVA: Digite "${cmdA}" para ${teamA.toUpperCase()} | Digite "${cmdB}" para ${teamB.toUpperCase()} | Envie Rosas para nitro ${giftMul}x!`;

      document.getElementById('cockpit-out-obs').innerText = obsUrl;
      document.getElementById('cockpit-out-broadcaster').innerText = JSON.stringify(broadcasterPayload, null, 2);
      document.getElementById('cockpit-out-chat').innerText = chatHeadline;
    }

    function copyCockpitObsUrl() {
      const url = document.getElementById('cockpit-out-obs').innerText;
      navigator.clipboard.writeText(url).then(() => {
        showToast('✅ Link do OBS copiado com sucesso! Largura 1080, Altura 1920.');
      });
    }

    function copyBroadcasterConfig() {
      const json = document.getElementById('cockpit-out-broadcaster').innerText;
      navigator.clipboard.writeText(json).then(() => {
        showToast('⚡ JSON de vinculação do Broadcaster copiado!');
      });
    }

    function copyChatHeadline() {
      const text = document.getElementById('cockpit-out-chat').innerText;
      navigator.clipboard.writeText(text).then(() => {
        showToast('💬 Legenda copiada para colocar no chat ou tela!');
      });
    }

    function launchFromCockpitToSimulator() {
      const obsUrl = document.getElementById('cockpit-out-obs').innerText;
      switchView('simulator');
      const iframe = document.getElementById('cartridge-iframe');
      if (iframe) {
        iframe.src = obsUrl;
      }
      showToast('🚀 Carregado no simulador com parâmetros customizados!');
    }

    // =========================================================================
    // SIMULADOR 9:16 & TEST LAB
    // =========================================================================
    function populateSimSelect() {
      const select = document.getElementById('sim-select');
      if (!select) return;

      let html = '';
      GAMES_CATALOG.forEach(g => {
        html += `<option value="${g.slug}">${g.name}</option>`;
      });
      select.innerHTML = html;
    }

    function onSimSelectChange() {
      const select = document.getElementById('sim-select');
      if (select) loadGameInSimulator(select.value);
    }

    function loadGameInSimulator(slug) {
      currentSimSlug = slug;
      const iframe = document.getElementById('cartridge-iframe');
      if (iframe) {
        iframe.src = `catalogo_jogos/${slug}/index.html?testlab=1`;
      }
      const select = document.getElementById('sim-select');
      if (select) select.value = slug;
    }

    function launchGameSimulator(slug) {
      loadGameInSimulator(slug);
      switchView('simulator');
    }

    function reloadSimulator() {
      const iframe = document.getElementById('cartridge-iframe');
      if (iframe) {
        const curSrc = iframe.src;
        iframe.src = '';
        setTimeout(() => { iframe.src = curSrc; }, 50);
      }
    }

    function toggleSimSafeZones() {
      const overlay = document.getElementById('sim-safe-overlay');
      const btn = document.getElementById('btn-toggle-sz');
      if (!overlay) return;
      overlay.classList.toggle('active');
      if (btn) {
        btn.style.color = overlay.classList.contains('active') ? 'var(--neon-rose)' : 'var(--text-main)';
      }
    }

    function openFullscreenGame() {
      const iframe = document.getElementById('cartridge-iframe');
      if (iframe && iframe.src) {
        window.open(iframe.src, '_blank');
      }
    }

    function copyCurrentObsUrl() {
      const origin = window.location.origin || 'http://localhost:3012';
      const obsUrl = `${origin}/catalogo_jogos/${currentSimSlug}/index.html?obs=1`;
      navigator.clipboard.writeText(obsUrl).then(() => {
        showToast('Link do OBS copiado para a área de transferência!');
      });
    }

    function injectSimEvent(payload) {
      payload.timestamp = Date.now();
      logTerminalEvent(payload);

      if (broadcastChannel) {
        try { broadcastChannel.postMessage(payload); } catch (e) {}
      }

      const iframe = document.getElementById('cartridge-iframe');
      if (iframe && iframe.contentWindow) {
        try { iframe.contentWindow.postMessage(payload, '*'); } catch (e) {}
      }
    }

    function logTerminalEvent(payload) {
      const terminal = document.getElementById('event-terminal');
      if (!terminal) return;

      const time = new Date().toLocaleTimeString();
      let typeLabel = payload.type ? payload.type.toUpperCase() : 'EVENT';
      let desc = payload.comment || payload.giftName || payload.action || '';

      const line = document.createElement('div');
      line.className = 'log-line';
      line.innerHTML = `<span class="timestamp">[${time}]</span> <span class="ev-type">${typeLabel}</span>: <span class="ev-val">${desc}</span> (${payload.user || '@live'})`;

      terminal.appendChild(line);
      terminal.scrollTop = terminal.scrollHeight;
    }

    function clearEventLogs() {
      const terminal = document.getElementById('event-terminal');
      if (terminal) terminal.innerHTML = '<div class="log-line"><span class="timestamp">[00:00:00]</span> Logs limpos.</div>';
    }

    // =========================================================================
    // STOREFRONT & CHECKOUT SIMULADO
    // =========================================================================
    function simulateCheckout(planName, priceBrl, priceCrypto) {
      showToast(`🛒 Pedido de "${planName}" criado! Redirecionando para o Gateway Soberano...`);
      setTimeout(() => {
        alert(`🏛️ CHECKOUT SOBERANO HOLDING V5 APOLLO\\n\\nPlano Selecionado: ${planName}\\nValor em Real: R$ ${priceBrl} (PIX Imediato)\\nValor em Cripto: ${priceCrypto} (Polygon PoS D+0)\\n\\nTrilho de pagamento 100% autônomo sem intermediários bancários!`);
      }, 500);
    }

    // =========================================================================
    // TOAST NOTIFICATION
    // =========================================================================
    let toastTimer = null;
    function showToast(message) {
      const toast = document.getElementById('toast-notification');
      const text = document.getElementById('toast-text');
      if (!toast || !text) return;

      text.innerText = message;
      toast.classList.add('show');

      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {
        toast.classList.remove('show');
      }, 2800);
    }

    // =========================================================================
    // INICIALIZAÇÃO GERAL
    // =========================================================================
    window.addEventListener('DOMContentLoaded', () => {
      renderPills();
      renderGamesGrid(GAMES_CATALOG);
      populateSimSelect();
      populateCockpitSelect();
      loadGameInSimulator('01_cabo_de_guerra_neon');
      updateCockpit();
    });
  </script>
</body>
</html>
"""

    html = html_template.replace("__MANIFEST_JSON_STR__", manifest_json_str)
    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print("Portal Soberano V5 Games gerado com sucesso!")

if __name__ == "__main__":
    build()
