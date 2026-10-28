import json
import os

MANIFEST_PATH = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos\v5_games_manifest.json"
INDEX_HTML_PATH = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\index.html"

def build_portal():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    # Categories grouping mapping
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

    # Enrich manifest items
    for item in manifest_data:
        cat_key = item.get("category", "")
        group_info = CATEGORY_GROUPS.get(cat_key, {"name": "Geral & Arcade", "icon": "🎮"})
        item["groupName"] = group_info["name"]
        item["groupIcon"] = group_info["icon"]

    manifest_json_str = json.dumps(manifest_data, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>V5 Games — Portal Oficial de Cartuchos Interativos de Live 9:16</title>
  <style>
    /* ==========================================================================
       V5 GAMES STUDIO — DESIGN SYSTEM (DARK OBSIDIAN & NEON GLASS)
       Holding V5 Apollo — 100% Offline, Zero Dependências Externas
       ========================================================================== */
    :root {{
      --bg-primary: #030712;
      --bg-secondary: #0b1120;
      --bg-surface: #0f172a;
      --bg-surface-elevated: #1e293b;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(56, 189, 248, 0.3);
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
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }}

    body {{
      background-color: var(--bg-primary);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      line-height: 1.5;
    }}

    /* Scrollbar elegante */
    ::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
    }}
    ::-webkit-scrollbar-track {{
      background: #030712;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #1e293b;
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #334155;
    }}

    /* ==========================================================================
       HEADER & BARRA DE NAVEGAÇÃO
       ========================================================================== */
    header.main-header {{
      position: sticky;
      top: 0;
      background: rgba(11, 17, 32, 0.92);
      border-bottom: 1px solid var(--border-subtle);
      padding: 12px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      backdrop-filter: blur(14px);
      z-index: 1000;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 14px;
      cursor: pointer;
    }}

    .brand-badge {{
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
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.45);
    }}

    .brand-name {{
      font-size: 18px;
      font-weight: 900;
      letter-spacing: 1.5px;
      background: linear-gradient(90deg, #ffffff 0%, var(--neon-cyan) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      line-height: 1.2;
    }}

    .brand-sub {{
      font-size: 10px;
      color: var(--neon-cyan);
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 1px;
    }}

    /* Abas de Navegação */
    nav.nav-tabs {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-subtle);
      border-radius: 30px;
      padding: 4px;
    }}

    .nav-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 700;
      padding: 8px 18px;
      border-radius: 20px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .nav-btn:hover {{
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.05);
    }}

    .nav-btn.active {{
      background: linear-gradient(135deg, rgba(0, 240, 255, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
      border: 1px solid var(--border-accent);
      color: var(--neon-cyan);
      box-shadow: 0 0 14px rgba(0, 240, 255, 0.2);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .live-status-pill {{
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
      letter-spacing: 0.5px;
    }}

    .pulse-dot {{
      width: 7px;
      height: 7px;
      background: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 1.8s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
    }}

    .btn-quick-launch {{
      background: linear-gradient(135deg, var(--neon-cyan) 0%, #0284c7 100%);
      border: none;
      color: #030712;
      font-size: 12px;
      font-weight: 800;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 0 15px rgba(0, 240, 255, 0.35);
      transition: all 0.2s;
    }}

    .btn-quick-launch:hover {{
      transform: translateY(-1px);
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.55);
    }}

    /* ==========================================================================
       CONTAINER PRINCIPAL DAS VIEWS
       ========================================================================== */
    main.app-container {{
      flex: 1;
      display: flex;
      flex-direction: column;
    }}

    .app-view {{
      display: none;
      flex-direction: column;
      width: 100%;
      animation: fadeIn 0.25s ease-out;
    }}

    .app-view.active {{
      display: flex;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* ==========================================================================
       VIEW 1: ARCADE & CATÁLOGO
       ========================================================================== */
    .hero-banner {{
      padding: 40px 32px 30px;
      background: radial-gradient(circle at 50% 0%, rgba(56, 189, 248, 0.12) 0%, rgba(3, 7, 18, 0) 70%);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }}

    .hero-tag {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 800;
      color: var(--neon-cyan);
      background: rgba(0, 240, 255, 0.1);
      border: 1px solid rgba(0, 240, 255, 0.3);
      padding: 4px 14px;
      border-radius: 20px;
      margin-bottom: 14px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}

    .hero-title {{
      font-size: 36px;
      font-weight: 900;
      letter-spacing: -0.5px;
      color: #ffffff;
      max-width: 900px;
      margin-bottom: 12px;
      line-height: 1.2;
    }}

    .hero-title span {{
      background: linear-gradient(90deg, var(--neon-cyan) 0%, var(--neon-purple) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero-desc {{
      font-size: 15px;
      color: var(--text-muted);
      max-width: 750px;
      margin-bottom: 24px;
      line-height: 1.6;
    }}

    /* Faixa de Estatísticas de Produção */
    .hero-stats {{
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
      justify-content: center;
      margin-bottom: 10px;
    }}

    .stat-badge {{
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 10px 18px;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 140px;
    }}

    .stat-val {{
      font-size: 20px;
      font-weight: 900;
      color: var(--neon-cyan);
    }}

    .stat-label {{
      font-size: 11px;
      font-weight: 700;
      color: var(--text-subtle);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    /* Barra de Busca e Filtros */
    .catalog-controls {{
      padding: 24px 32px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      max-width: 1600px;
      width: 100%;
      margin: 0 auto;
    }}

    .search-row {{
      display: flex;
      gap: 16px;
      align-items: center;
    }}

    .search-input-wrap {{
      flex: 1;
      position: relative;
    }}

    .search-input {{
      width: 100%;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 14px 18px 14px 44px;
      color: #ffffff;
      font-size: 14px;
      font-weight: 500;
      outline: none;
      transition: all 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--neon-cyan);
      box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
    }}

    .search-icon {{
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 16px;
      color: var(--text-subtle);
    }}

    .catalog-counter {{
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      white-space: nowrap;
    }}

    /* Filtros em Pílulas */
    .filter-pills {{
      display: flex;
      gap: 10px;
      overflow-x: auto;
      padding-bottom: 4px;
    }}

    .pill-btn {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 700;
      padding: 8px 16px;
      border-radius: 20px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      transition: all 0.2s;
    }}

    .pill-btn:hover {{
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.2);
      background: #1e293b;
    }}

    .pill-btn.active {{
      background: #1e293b;
      border-color: var(--neon-cyan);
      color: var(--neon-cyan);
      box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }}

    /* Grid de Cartuchos */
    .games-grid {{
      padding: 0 32px 60px;
      max-width: 1600px;
      width: 100%;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 24px;
    }}

    /* Card de Jogo */
    .game-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }}

    .game-card:hover {{
      transform: translateY(-5px);
      border-color: rgba(56, 189, 248, 0.35);
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6), 0 0 25px rgba(0, 240, 255, 0.15);
    }}

    .card-thumb-wrap {{
      position: relative;
      width: 100%;
      height: 220px;
      background: #020617;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
    }}

    .card-thumb {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
    }}

    .game-card:hover .card-thumb {{
      transform: scale(1.05);
    }}

    .card-badges-top {{
      position: absolute;
      top: 10px;
      left: 10px;
      right: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      pointer-events: none;
    }}

    .badge-number {{
      background: rgba(3, 7, 18, 0.85);
      border: 1px solid var(--border-subtle);
      backdrop-filter: blur(8px);
      color: var(--neon-cyan);
      font-weight: 900;
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }}

    .badge-category {{
      background: rgba(3, 7, 18, 0.85);
      border: 1px solid var(--border-subtle);
      backdrop-filter: blur(8px);
      color: #ffffff;
      font-weight: 800;
      font-size: 10px;
      padding: 3px 8px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .card-body {{
      padding: 18px;
      display: flex;
      flex-direction: column;
      flex: 1;
      gap: 12px;
    }}

    .card-title-row {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 8px;
    }}

    .card-title {{
      font-size: 16px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.3;
    }}

    .badge-status {{
      font-size: 9px;
      font-weight: 900;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399;
      padding: 2px 6px;
      border-radius: 4px;
      white-space: nowrap;
    }}

    .card-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    /* Comandos do Chat e Presentes */
    .card-interaction-box {{
      background: rgba(3, 7, 18, 0.6);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 11px;
    }}

    .interaction-row {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .interaction-label {{
      color: var(--text-subtle);
      font-weight: 700;
      text-transform: uppercase;
      min-width: 65px;
      font-size: 10px;
    }}

    .interaction-tags {{
      display: flex;
      gap: 5px;
      flex-wrap: wrap;
    }}

    .cmd-tag {{
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: var(--neon-cyan);
      font-family: monospace;
      font-weight: 700;
      padding: 1px 6px;
      border-radius: 4px;
    }}

    .gift-tag {{
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: var(--neon-gold);
      font-weight: 700;
      padding: 1px 6px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      gap: 3px;
    }}

    /* Ações do Card */
    .card-actions {{
      display: flex;
      gap: 8px;
      margin-top: auto;
      padding-top: 6px;
    }}

    .btn-play-sim {{
      flex: 1;
      background: linear-gradient(135deg, rgba(0, 240, 255, 0.15) 0%, rgba(2, 132, 199, 0.25) 100%);
      border: 1px solid rgba(0, 240, 255, 0.4);
      color: var(--neon-cyan);
      font-size: 12px;
      font-weight: 800;
      padding: 9px 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
    }}

    .btn-play-sim:hover {{
      background: var(--neon-cyan);
      color: #030712;
      box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
    }}

    .btn-icon-action {{
      background: #1e293b;
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      width: 36px;
      height: 36px;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 14px;
      transition: all 0.2s;
      position: relative;
    }}

    .btn-icon-action:hover {{
      color: #ffffff;
      background: #334155;
      border-color: rgba(255, 255, 255, 0.25);
    }}

    /* ==========================================================================
       VIEW 2: SIMULADOR & TEST LAB 9:16
       ========================================================================== */
    .simulator-container {{
      display: flex;
      flex-direction: column;
      height: calc(100vh - 65px);
      padding: 16px 24px;
      gap: 16px;
      max-width: 1700px;
      margin: 0 auto;
      width: 100%;
    }}

    /* Topbar do Simulador */
    .sim-topbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 10px 20px;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .sim-title-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .sim-game-select {{
      background: #1e293b;
      border: 1px solid var(--border-accent);
      color: #ffffff;
      font-size: 14px;
      font-weight: 700;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      outline: none;
      cursor: pointer;
      max-width: 420px;
    }}

    .sim-controls-group {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .sim-btn {{
      background: #1e293b;
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 700;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}

    .sim-btn:hover {{
      color: #ffffff;
      background: #334155;
      border-color: rgba(255, 255, 255, 0.2);
    }}

    .sim-btn.active {{
      background: rgba(0, 240, 255, 0.15);
      border-color: var(--neon-cyan);
      color: var(--neon-cyan);
    }}

    /* Layout da Bancada de Testes */
    .sim-stage-wrap {{
      flex: 1;
      display: flex;
      gap: 20px;
      min-height: 0;
    }}

    /* Coluna do Celular 9:16 */
    .phone-viewport-col {{
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
    }}

    .phone-mockup {{
      position: relative;
      height: 100%;
      max-height: 780px;
      aspect-ratio: 9 / 16;
      background: #000000;
      border-radius: 40px;
      border: 10px solid #1e293b;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 35px rgba(0, 240, 255, 0.15);
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}

    .phone-notch {{
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 110px;
      height: 18px;
      background: #1e293b;
      border-bottom-left-radius: 12px;
      border-bottom-right-radius: 12px;
      z-index: 50;
      display: flex;
      justify-content: center;
      align-items: center;
    }}

    .phone-camera {{
      width: 7px;
      height: 7px;
      background: #050811;
      border-radius: 50%;
    }}

    #cartridge-iframe {{
      width: 100%;
      height: 100%;
      border: none;
      background: #000000;
      display: block;
    }}

    /* Safe Zones Overlay */
    .safe-zone-overlay {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 40;
      display: none;
      flex-direction: column;
      justify-content: space-between;
    }}

    .safe-zone-overlay.active {{
      display: flex;
    }}

    .sz-top {{
      height: 140px;
      background: rgba(239, 68, 68, 0.15);
      border-bottom: 2px dashed #ef4444;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 800;
      color: #fca5a5;
      letter-spacing: 0.5px;
    }}

    .sz-bottom {{
      height: 180px;
      background: rgba(239, 68, 68, 0.15);
      border-top: 2px dashed #ef4444;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 800;
      color: #fca5a5;
      letter-spacing: 0.5px;
    }}

    /* Coluna Lateral do Cockpit */
    .sim-cockpit-col {{
      width: 460px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      height: 100%;
    }}

    .cockpit-tabs {{
      display: flex;
      gap: 6px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 4px;
    }}

    .cockpit-tab-btn {{
      flex: 1;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 700;
      padding: 8px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .cockpit-tab-btn.active {{
      background: #1e293b;
      color: var(--neon-cyan);
    }}

    .cockpit-content {{
      flex: 1;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      overflow-y: auto;
    }}

    .cockpit-pane {{
      display: none;
      flex-direction: column;
      gap: 14px;
    }}

    .cockpit-pane.active {{
      display: flex;
    }}

    .section-headline {{
      font-size: 11px;
      font-weight: 800;
      color: var(--text-subtle);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* Botões de Votos Rápidos */
    .vote-buttons-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
    }}

    .btn-vote-sim {{
      background: #1e293b;
      border: 1px solid var(--border-subtle);
      color: #ffffff;
      font-size: 12px;
      font-weight: 800;
      padding: 10px 8px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s;
    }}

    .btn-vote-sim.cyan {{
      border-color: rgba(0, 240, 255, 0.4);
      color: var(--neon-cyan);
    }}

    .btn-vote-sim.cyan:hover {{
      background: rgba(0, 240, 255, 0.2);
    }}

    .btn-vote-sim.rose {{
      border-color: rgba(244, 63, 94, 0.4);
      color: var(--neon-rose);
    }}

    .btn-vote-sim.rose:hover {{
      background: rgba(244, 63, 94, 0.2);
    }}

    .btn-vote-sim.gold {{
      border-color: rgba(245, 158, 11, 0.4);
      color: var(--neon-gold);
    }}

    .btn-vote-sim.gold:hover {{
      background: rgba(245, 158, 11, 0.2);
    }}

    /* Comentário customizado */
    .custom-comment-box {{
      display: flex;
      gap: 8px;
    }}

    .sim-text-input {{
      flex: 1;
      background: #0b1120;
      border: 1px solid var(--border-subtle);
      color: #ffffff;
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      outline: none;
    }}

    .sim-text-input:focus {{
      border-color: var(--neon-cyan);
    }}

    .btn-sim-send {{
      background: #334155;
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #ffffff;
      font-size: 12px;
      font-weight: 700;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      cursor: pointer;
    }}

    .btn-sim-send:hover {{
      background: var(--neon-cyan);
      color: #030712;
    }}

    /* Seção de Presentes / Gifts */
    .gift-cards-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}

    .gift-trigger-btn {{
      background: #1e293b;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 10px;
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
      text-align: left;
      transition: all 0.15s;
    }}

    .gift-trigger-btn:hover {{
      border-color: var(--neon-gold);
      background: rgba(245, 158, 11, 0.12);
      transform: translateY(-2px);
    }}

    .gift-symb {{
      font-size: 22px;
    }}

    .gift-info-name {{
      font-size: 12px;
      font-weight: 800;
      color: #ffffff;
    }}

    .gift-info-weight {{
      font-size: 10px;
      color: var(--neon-gold);
      font-weight: 700;
    }}

    /* Terminal de Monitor */
    .event-log-terminal {{
      flex: 1;
      background: #020617;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 10px;
      font-family: monospace;
      font-size: 11px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 6px;
      max-height: 280px;
    }}

    .log-line {{
      color: var(--text-muted);
      line-height: 1.4;
    }}

    .log-line .timestamp {{
      color: var(--text-subtle);
    }}

    .log-line .ev-type {{
      color: var(--neon-cyan);
      font-weight: bold;
    }}

    .log-line .ev-val {{
      color: var(--neon-gold);
    }}

    /* ==========================================================================
       VIEW 3: GUIA DO OBS & TRANSMISSÃO
       ========================================================================== */
    .guide-container {{
      max-width: 1200px;
      width: 100%;
      margin: 0 auto;
      padding: 40px 32px 80px;
      display: flex;
      flex-direction: column;
      gap: 32px;
    }}

    .guide-step-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 24px;
      display: flex;
      gap: 20px;
    }}

    .step-number {{
      width: 48px;
      height: 48px;
      background: rgba(0, 240, 255, 0.1);
      border: 1px solid rgba(0, 240, 255, 0.4);
      color: var(--neon-cyan);
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 20px;
      font-weight: 900;
      flex-shrink: 0;
    }}

    .step-body {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .step-title {{
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
    }}

    .step-desc {{
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.6;
    }}

    .code-snippet {{
      background: #020617;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 12px 16px;
      font-family: monospace;
      font-size: 13px;
      color: var(--neon-cyan);
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 8px;
    }}

    /* ==========================================================================
       TOAST FLUTUANTE DE FEEDBACK
       ========================================================================== */
    #toast-notification {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #1e293b;
      border: 1px solid var(--border-accent);
      color: #ffffff;
      padding: 12px 20px;
      border-radius: var(--radius-md);
      font-size: 13px;
      font-weight: 700;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 240, 255, 0.25);
      display: flex;
      align-items: center;
      gap: 10px;
      z-index: 9999;
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: none;
    }}

    #toast-notification.show {{
      transform: translateY(0);
      opacity: 1;
    }}
  </style>
</head>
<body>

  <!-- HEADER OFICIAL DA PLATAFORMA -->
  <header class="main-header">
    <div class="brand-wrap" onclick="switchView('catalog')">
      <div class="brand-badge">V5</div>
      <div>
        <div class="brand-name">V5 GAMES STUDIO</div>
        <div class="brand-sub">Holding V5 Apollo • Live Cartridge Hub</div>
      </div>
    </div>

    <!-- Abas Principais -->
    <nav class="nav-tabs">
      <button class="nav-btn active" id="tab-catalog" onclick="switchView('catalog')">
        <span>🕹️ Catálogo Arcade</span>
      </button>
      <button class="nav-btn" id="tab-simulator" onclick="switchView('simulator')">
        <span>📱 Simulador 9:16</span>
      </button>
      <button class="nav-btn" id="tab-obs" onclick="switchView('obs')">
        <span>📡 Como Usar no OBS</span>
      </button>
      <button class="nav-btn" id="tab-laws" onclick="switchView('laws')">
        <span>⚡ As 5 Leis</span>
      </button>
    </nav>

    <!-- Status e Ação Rápida -->
    <div class="header-actions">
      <div class="live-status-pill">
        <span class="pulse-dot"></span>
        <span>41 CARTUCHOS PRONTOS</span>
      </div>
      <button class="btn-quick-launch" onclick="launchGameSimulator('01_cabo_de_guerra_neon')">
        <span>⚡ Testar #01</span>
      </button>
    </div>
  </header>

  <!-- CONTAINER DE VIEWS -->
  <main class="app-container">

    <!-- =======================================================================
         VIEW 1: ARCADE & CATÁLOGO
         ======================================================================= -->
    <section class="app-view active" id="view-catalog">
      
      <!-- Hero de Destaque -->
      <div class="hero-banner">
        <div class="hero-tag">✨ A MAIOR FORJA DE JOGOS INTERATIVOS VERTICAIS 9:16</div>
        <h1 class="hero-title">O Estúdio de Cartuchos para <span>Lives que Faturam 24/7</span></h1>
        <p class="hero-desc">
          Jogos desenvolvidos especificamente para TikTok Live, YouTube Shorts e Twitch. 
          Pilotados 100% pelo público digitando no chat ou enviando presentes. 60 FPS cravados, áudio procedural sintetizado e zero dependências de internet.
        </p>

        <!-- Métricas Rápidas -->
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
            <span class="stat-label">Renderização Ultra-Leve</span>
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

      <!-- Barra de Pesquisa e Filtros -->
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

        <!-- Categorias em Pílulas -->
        <div class="filter-pills" id="filter-pills-container">
          <!-- Injetado dinamicamente via JS -->
        </div>
      </div>

      <!-- Grid de Jogos -->
      <div class="games-grid" id="games-grid">
        <!-- Cards gerados dinamicamente via JS -->
      </div>
    </section>

    <!-- =======================================================================
         VIEW 2: SIMULADOR & TEST LAB 9:16
         ======================================================================= -->
    <section class="app-view" id="view-simulator">
      <div class="simulator-container">
        
        <!-- Barra Superior do Simulador -->
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
            <button class="sim-btn" onclick="openFullscreenGame()">🖥️ Tela Cheia (OBS)</button>
            <button class="sim-btn" onclick="copyCurrentObsUrl()">📋 Copiar Link OBS</button>
          </div>
        </div>

        <!-- Bancada Central -->
        <div class="sim-stage-wrap">
          
          <!-- Mockup do Smartphone 9:16 -->
          <div class="phone-viewport-col">
            <div class="phone-mockup">
              <div class="phone-notch">
                <div class="phone-camera"></div>
              </div>

              <!-- Iframe do Cartucho -->
              <iframe id="cartridge-iframe" src="catalogo_jogos/01_cabo_de_guerra_neon/index.html"></iframe>

              <!-- Safe Zones Overlay -->
              <div class="safe-zone-overlay" id="sim-safe-overlay">
                <div class="sz-top">⚠️ Safe Zone Topo (140px) — Placar & Metas</div>
                <div class="sz-bottom">⚠️ Safe Zone Base (180px) — Chat & Ícones do TikTok</div>
              </div>
            </div>
          </div>

          <!-- Cockpit de Controle Lateral -->
          <div class="sim-cockpit-col">
            
            <div class="cockpit-tabs">
              <button class="cockpit-tab-btn active" id="c-tab-injector" onclick="switchCockpitTab('injector')">⚡ Injetor de Live</button>
              <button class="cockpit-tab-btn" id="c-tab-obs" onclick="switchCockpitTab('obs')">📡 Dados OBS</button>
              <button class="cockpit-tab-btn" id="c-tab-logs" onclick="switchCockpitTab('logs')">📜 Event Log</button>
            </div>

            <div class="cockpit-content">
              
              <!-- PAINEL 1: INJETOR DE EVENTOS -->
              <div class="cockpit-pane active" id="pane-injector">
                
                <div>
                  <div class="section-headline">
                    <span>Comentários Rápidos (Votação)</span>
                    <span style="color:var(--neon-cyan)">Chat Interativo</span>
                  </div>
                  <div class="vote-buttons-grid" style="margin-top: 8px;">
                    <button class="btn-vote-sim cyan" onclick="injectVote('1', 'A')">🔵 Voto 1 (Azul)</button>
                    <button class="btn-vote-sim gold" onclick="injectVote('3', 'C')">👑 Voto 3 (Ouro)</button>
                    <button class="btn-vote-sim rose" onclick="injectVote('2', 'B')">🔴 Voto 2 (Red)</button>
                  </div>
                </div>

                <div>
                  <div class="section-headline">
                    <span>Comentário Customizado</span>
                    <span id="user-display" style="color:var(--text-muted)">@espectador</span>
                  </div>
                  <div class="custom-comment-box" style="margin-top: 8px;">
                    <input type="text" id="sim-comment-input" class="sim-text-input" placeholder="Digite uma mensagem ou comando..." onkeydown="if(event.key==='Enter') injectCustomComment()">
                    <button class="btn-sim-send" onclick="injectCustomComment()">Enviar</button>
                  </div>
                </div>

                <div>
                  <div class="section-headline">
                    <span>Presentes / Gifts Monetizados</span>
                    <span style="color:var(--neon-gold)">Multiplicador de Live</span>
                  </div>
                  <div class="gift-cards-grid" style="margin-top: 8px;">
                    <button class="gift-trigger-btn" onclick="injectGift('Rosa', 1, 5)">
                      <span class="gift-symb">🌸</span>
                      <div>
                        <div class="gift-info-name">Rosa (1c)</div>
                        <div class="gift-info-weight">Peso 5x • Boost</div>
                      </div>
                    </button>

                    <button class="gift-trigger-btn" onclick="injectGift('Moeda V5', 5, 15)">
                      <span class="gift-symb">🪙</span>
                      <div>
                        <div class="gift-info-name">Moeda V5 (5c)</div>
                        <div class="gift-info-weight">Peso 15x • Turbo</div>
                      </div>
                    </button>

                    <button class="gift-trigger-btn" onclick="injectGift('Diamante', 20, 35)">
                      <span class="gift-symb">💎</span>
                      <div>
                        <div class="gift-info-name">Diamante (20c)</div>
                        <div class="gift-info-weight">Peso 35x • Super</div>
                      </div>
                    </button>

                    <button class="gift-trigger-btn" onclick="injectGift('Leão', 500, 50)">
                      <span class="gift-symb">🦁</span>
                      <div>
                        <div class="gift-info-name">Leão Real</div>
                        <div class="gift-info-weight">Peso 50x • MÁXIMO</div>
                      </div>
                    </button>
                  </div>
                </div>

              </div>

              <!-- PAINEL 2: CONFIGURAÇÃO OBS -->
              <div class="cockpit-pane" id="pane-obs">
                <div class="section-headline">
                  <span>URL da Fonte de Navegador</span>
                  <span>OBS Studio</span>
                </div>
                <div class="code-snippet" style="margin-top: 4px;">
                  <span id="obs-current-url" style="word-break: break-all;">http://localhost:3012/catalogo_jogos/01_cabo_de_guerra_neon/</span>
                  <button class="sim-btn" onclick="copyCurrentObsUrl()" style="padding: 4px 8px; font-size:11px;">Copiar</button>
                </div>

                <div style="margin-top: 12px;">
                  <div class="section-headline">Parâmetros Recomendados</div>
                  <div style="font-size: 13px; color: var(--text-muted); margin-top: 6px; display:flex; flex-direction:column; gap:4px;">
                    <div>• <strong>Largura:</strong> 1080 px</div>
                    <div>• <strong>Altura:</strong> 1920 px</div>
                    <div>• <strong>FPS:</strong> 60 FPS</div>
                    <div>• <strong>Áudio:</strong> Marcar "Controlar áudio via OBS"</div>
                    <div>• <strong>Atualização:</strong> Marcar "Atualizar navegador ao ativar cena"</div>
                  </div>
                </div>

                <div style="margin-top: 12px;">
                  <div class="section-headline">Comandos do Jogo Atual</div>
                  <div id="sim-game-commands" style="display:flex; gap:6px; flex-wrap:wrap; margin-top:8px;">
                    <!-- Preenchido via JS -->
                  </div>
                </div>
              </div>

              <!-- PAINEL 3: EVENT LOG -->
              <div class="cockpit-pane" id="pane-logs">
                <div class="section-headline">
                  <span>Event Bus Terminal</span>
                  <button class="sim-btn" onclick="clearEventLogs()" style="padding:2px 8px; font-size:10px;">Limpar</button>
                </div>
                <div class="event-log-terminal" id="event-terminal">
                  <div class="log-line"><span class="timestamp">[00:00:00]</span> Terminal de eventos do BroadcastChannel iniciado.</div>
                </div>
              </div>

            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- =======================================================================
         VIEW 3: GUIA DO OBS & TRANSMISSÃO
         ======================================================================= -->
    <section class="app-view" id="view-obs">
      <div class="guide-container">
        
        <div style="text-align: center; margin-bottom: 10px;">
          <h2 style="font-size: 30px; font-weight: 900; color: #ffffff;">Como Transmitir no OBS Studio em 60 Segundos</h2>
          <p style="font-size: 15px; color: var(--text-muted); margin-top: 6px;">
            Qualquer jogo da Capitania V5 Games é uma página web autônoma e leve projetada para o OBS Browser Source.
          </p>
        </div>

        <div class="guide-step-card">
          <div class="step-number">1</div>
          <div class="step-body">
            <div class="step-title">Configure a Tela Vertical (9:16) no OBS</div>
            <div class="step-desc">
              Vá em <strong>Configurações > Vídeo</strong> no OBS Studio. Defina a <strong>Resolução de Base (Tela)</strong> e <strong>Resolução de Saída</strong> para <strong>1080x1920</strong>. Se estiver usando o plugin <em>Aitum Vertical</em> ou <em>OBS Vertical Canvas</em>, basta criar uma cena vertical.
            </div>
          </div>
        </div>

        <div class="guide-step-card">
          <div class="step-number">2</div>
          <div class="step-body">
            <div class="step-title">Adicione uma Fonte de Navegador (Browser Source)</div>
            <div class="step-desc">
              Clique com o botão direito na lista de Fontes do OBS, escolha <strong>Adicionar > Navegador</strong>. Cole a URL do jogo desejado (ex: <code>http://localhost:3012/catalogo_jogos/01_cabo_de_guerra_neon/</code>).
            </div>
            <div class="code-snippet">
              <span>http://localhost:3012/catalogo_jogos/01_cabo_de_guerra_neon/</span>
            </div>
          </div>
        </div>

        <div class="guide-step-card">
          <div class="step-number">3</div>
          <div class="step-body">
            <div class="step-title">Ajuste as Propriedades de Renderização</div>
            <div class="step-desc">
              Defina a <strong>Largura: 1080</strong> e a <strong>Altura: 1920</strong>. Marque a opção <strong>"Controlar áudio via OBS"</strong> para que os efeitos sonoros procedurais (Web Audio API) saiam perfeitamente na transmissão.
            </div>
          </div>
        </div>

        <div class="guide-step-card">
          <div class="step-number">4</div>
          <div class="step-body">
            <div class="step-title">Conecte o Leitor de Chat do TikTok / YouTube</div>
            <div class="step-desc">
              Inicie o <strong>V5 Apollo Broadcaster</strong> (`V5_Apollo_Broadcaster`), que captura o chat e os presentes em tempo real e os despacha diretamente para o jogo através do barramento <code>BroadcastChannel('v5_broadcaster_games')</code>.
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- =======================================================================
         VIEW 4: AS 5 LEIS ABSOLUTAS
         ======================================================================= -->
    <section class="app-view" id="view-laws">
      <div class="guide-container">
        
        <div style="text-align: center; margin-bottom: 10px;">
          <h2 style="font-size: 30px; font-weight: 900; color: #ffffff;">As 5 Leis Absolutas do Cartucho V5</h2>
          <p style="font-size: 15px; color: var(--text-muted); margin-top: 6px;">
            Princípios inegociáveis de engenharia e retenção para transmissões interativas 24/7.
          </p>
        </div>

        <div class="guide-step-card">
          <div class="step-number">1</div>
          <div class="step-body">
            <div class="step-title">Formato Vertical Estrito 9:16 (1080 x 1920 px)</div>
            <div class="step-desc">
              Todo jogo nasce vertical com Safe Zones reservadas: topo (140px) para placar e metas; base (180px) livre de elementos críticos para não sobrepor o feed do TikTok e YouTube Shorts.
            </div>
          </div>
        </div>

        <div class="guide-step-card">
          <div class="step-number">2</div>
          <div class="step-body">
            <div class="step-title">Zero Teclado / Zero Mouse (O Público é o Controle)</div>
            <div class="step-desc">
              O streamer não precisa jogar nem mexer o mouse. O jogo é 100% pilotado pelo chat (comentários rápidos como 1, 2, azul, laranja) e Presentes (Rosas, Moedas, Leão). Presentes sempre têm peso massivo (5x a 50x) para estimular monetização.
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
              Zero dependência de arquivos .mp3 ou .wav externos que possam sofrer erro de CORS ou demorar no carregamento do OBS. Todo som (apitos, impactos, moedas, aplausos e fanfarras) é sintetizado dinamicamente via Web Audio API.
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

  <!-- SCRIPT PRINCIPAL DO PORTAL -->
  <script>
    // Manifesto dos 41 Cartuchos embutido
    const GAMES_CATALOG = {manifest_json_str};

    let activeFilter = 'all';
    let currentSimSlug = '01_cabo_de_guerra_neon';
    let broadcastChannel = null;

    // Inicialização do Barramento
    try {{
      broadcastChannel = new BroadcastChannel('v5_broadcaster_games');
    }} catch (e) {{
      console.warn('BroadcastChannel não suportado neste navegador:', e);
    }}

    // =========================================================================
    // NAVEGAÇÃO DE VIEWS
    // =========================================================================
    function switchView(viewName) {{
      // Abas
      document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
      const activeNavBtn = document.getElementById(`tab-${{viewName}}`);
      if (activeNavBtn) activeNavBtn.classList.add('active');

      // Telas
      document.querySelectorAll('.app-view').forEach(view => view.classList.remove('active'));
      const targetView = document.getElementById(`view-${{viewName}}`);
      if (targetView) targetView.classList.add('active');

      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // =========================================================================
    // RENDERIZAÇÃO DO CATÁLOGO
    // =========================================================================
    function renderPills() {{
      const container = document.getElementById('filter-pills-container');
      const groupsMap = {{}};

      GAMES_CATALOG.forEach(g => {{
        const group = g.groupName || 'Outros';
        groupsMap[group] = (groupsMap[group] || 0) + 1;
      }});

      let html = `<button class="pill-btn active" onclick="setCategoryFilter('all', this)">✨ Todos (41)</button>`;
      
      const categoryOrder = [
        "Batalhas & Polarização",
        "Tabuleiro & Estratégia",
        "Corridas & Velocidade",
        "Boss Raid & Cooperativo",
        "Pachinko & Física",
        "Roletas & Sorte",
        "Tensão & Eliminação",
        "Ação, Ritmo & Esportes"
      ];

      categoryOrder.forEach(cat => {{
        if (groupsMap[cat]) {{
          html += `<button class="pill-btn" onclick="setCategoryFilter('${{cat}}', this)">${{cat}} (${{groupsMap[cat]}})</button>`;
        }}
      }});

      container.innerHTML = html;
    }}

    function setCategoryFilter(category, btnElement) {{
      activeFilter = category;
      document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      if (btnElement) btnElement.classList.add('active');
      filterGames();
    }}

    function renderGamesGrid(games) {{
      const grid = document.getElementById('games-grid');
      const counter = document.getElementById('catalog-counter');
      counter.innerText = `Exibindo ${{games.length}} de ${{GAMES_CATALOG.length}} cartuchos`;

      if (games.length === 0) {{
        grid.innerHTML = `
          <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
            <div style="font-size: 40px; margin-bottom: 12px;">🔍</div>
            <div style="font-size: 18px; font-weight: 800; color: #fff;">Nenhum cartucho encontrado</div>
            <div style="font-size: 13px; margin-top: 6px;">Tente pesquisar por outro termo ou selecione "Todos".</div>
          </div>
        `;
        return;
      }}

      let html = '';
      games.forEach(game => {{
        const numberMatch = game.slug.match(/^(\\d+[a-z]?)/i);
        const numberStr = numberMatch ? `#${{numberMatch[1].toUpperCase()}}` : '#V5';
        const gameUrl = `http://localhost:3012/catalogo_jogos/${{game.slug}}/index.html`;

        const commandsHtml = (game.commands || []).map(cmd => `<span class="cmd-tag">${{cmd}}</span>`).join('');
        const giftsHtml = (game.gifts || []).map(g => `<span class="gift-tag">🎁 ${{g}}</span>`).join('');

        html += `
          <div class="game-card">
            <div class="card-thumb-wrap">
              <img src="catalogo_jogos/${{game.slug}}/thumbnail.svg" alt="${{game.name}}" class="card-thumb" loading="lazy">
              <div class="card-badges-top">
                <span class="badge-number">${{numberStr}}</span>
                <span class="badge-category">${{game.groupIcon || '🎮'}} ${{game.groupName || 'Arcade'}}</span>
              </div>
            </div>

            <div class="card-body">
              <div class="card-title-row">
                <div class="card-title">${{game.name}}</div>
                <span class="badge-status">HOMOLOGADO</span>
              </div>

              <div class="card-desc">${{game.description}}</div>

              <div class="card-interaction-box">
                <div class="interaction-row">
                  <span class="interaction-label">Comandos:</span>
                  <div class="interaction-tags">${{commandsHtml || '<span style="color:#64748b">Votos automáticos</span>'}}</div>
                </div>
                <div class="interaction-row">
                  <span class="interaction-label">Presentes:</span>
                  <div class="interaction-tags">${{giftsHtml || '<span style="color:#64748b">Pesos 5x a 50x</span>'}}</div>
                </div>
              </div>

              <div class="card-actions">
                <button class="btn-play-sim" onclick="launchGameSimulator('${{game.slug}}')">
                  <span>📱 Testar no Simulador</span>
                </button>
                <button class="btn-icon-action" title="Abrir em Tela Cheia / OBS" onclick="openGameInNewTab('${{game.slug}}')">
                  <span>🖥️</span>
                </button>
                <button class="btn-icon-action" title="Copiar URL para OBS" onclick="copyObsUrl('${{gameUrl}}')">
                  <span>📋</span>
                </button>
              </div>
            </div>
          </div>
        `;
      }});

      grid.innerHTML = html;
    }}

    function filterGames() {{
      const query = (document.getElementById('search-input').value || '').toLowerCase().trim();

      const filtered = GAMES_CATALOG.filter(game => {{
        const matchesCategory = (activeFilter === 'all') || (game.groupName === activeFilter);
        const matchesQuery = !query || 
          game.name.toLowerCase().includes(query) ||
          game.slug.toLowerCase().includes(query) ||
          game.description.toLowerCase().includes(query) ||
          (game.commands || []).some(c => c.toLowerCase().includes(query));

        return matchesCategory && matchesQuery;
      }});

      renderGamesGrid(filtered);
    }}

    // =========================================================================
    // SIMULADOR 9:16 INTERATIVO
    // =========================================================================
    function populateSimSelect() {{
      const select = document.getElementById('sim-select');
      let html = '';
      GAMES_CATALOG.forEach(g => {{
        const numberMatch = g.slug.match(/^(\\d+[a-z]?)/i);
        const numberStr = numberMatch ? `${{numberMatch[1].toUpperCase()}} — ` : '';
        html += `<option value="${{g.slug}}">${{numberStr}}${{g.name}}</option>`;
      }});
      select.innerHTML = html;
      select.value = currentSimSlug;
    }}

    function onSimSelectChange() {{
      const select = document.getElementById('sim-select');
      loadGameInSimulator(select.value);
    }}

    function launchGameSimulator(slug) {{
      loadGameInSimulator(slug);
      switchView('simulator');
    }}

    function loadGameInSimulator(slug) {{
      currentSimSlug = slug;
      const select = document.getElementById('sim-select');
      if (select) select.value = slug;

      const iframe = document.getElementById('cartridge-iframe');
      if (iframe) {{
        iframe.src = `catalogo_jogos/${{slug}}/index.html`;
      }}

      // Atualiza URL do OBS no painel
      const fullUrl = `http://localhost:3012/catalogo_jogos/${{slug}}/index.html`;
      const urlEl = document.getElementById('obs-current-url');
      if (urlEl) urlEl.innerText = fullUrl;

      // Atualiza comandos do jogo atual
      const gameObj = GAMES_CATALOG.find(g => g.slug === slug);
      const cmdsEl = document.getElementById('sim-game-commands');
      if (cmdsEl && gameObj) {{
        const cmdsHtml = (gameObj.commands || []).map(c => `<span class="cmd-tag" style="font-size:12px;">${{c}}</span>`).join('');
        cmdsEl.innerHTML = cmdsHtml || '<span style="color:var(--text-subtle)">Sem comandos textuais</span>';
      }}

      logTerminalEvent({{ type: 'SYSTEM', comment: `Cartucho '${{slug}}' carregado com sucesso no simulador.` }});
    }}

    function reloadSimulator() {{
      const iframe = document.getElementById('cartridge-iframe');
      if (iframe) {{
        iframe.src = `catalogo_jogos/${{currentSimSlug}}/index.html?t=${{Date.now()}}`;
        showToast('Cartucho recarregado no simulador!');
      }}
    }}

    function toggleSimSafeZones() {{
      const overlay = document.getElementById('sim-safe-overlay');
      const btn = document.getElementById('btn-toggle-sz');
      if (overlay) {{
        overlay.classList.toggle('active');
        if (btn) btn.classList.toggle('active');
      }}
    }}

    function openFullscreenGame() {{
      window.open(`catalogo_jogos/${{currentSimSlug}}/index.html`, '_blank');
    }}

    function openGameInNewTab(slug) {{
      window.open(`catalogo_jogos/${{slug}}/index.html`, '_blank');
    }}

    function copyCurrentObsUrl() {{
      const fullUrl = `http://localhost:3012/catalogo_jogos/${{currentSimSlug}}/index.html`;
      copyObsUrl(fullUrl);
    }}

    function copyObsUrl(url) {{
      navigator.clipboard.writeText(url).then(() => {{
        showToast('Link do OBS copiado para a área de transferência!');
      }}).catch(() => {{
        const input = document.createElement('input');
        input.value = url;
        document.body.appendChild(input);
        input.select();
        document.execCommand('copy');
        document.body.removeChild(input);
        showToast('Link do OBS copiado!');
      }});
    }}

    function switchCockpitTab(tabName) {{
      document.querySelectorAll('.cockpit-tab-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById(`c-tab-${{tabName}}`);
      if (activeBtn) activeBtn.classList.add('active');

      document.querySelectorAll('.cockpit-pane').forEach(p => p.classList.remove('active'));
      const activePane = document.getElementById(`pane-${{tabName}}`);
      if (activePane) activePane.classList.add('active');
    }}

    // =========================================================================
    // INJETOR DE EVENTOS DO SIMULADOR
    // =========================================================================
    function injectVote(cmd, team) {{
      const payload = {{
        type: 'comment',
        action: 'vote',
        team: team,
        user: '@espectador',
        comment: cmd,
        weight: 1,
        timestamp: Date.now()
      }};
      dispatchSimEvent(payload);
      showToast(`Voto '${{cmd}}' enviado para a live!`);
    }}

    function injectCustomComment() {{
      const input = document.getElementById('sim-comment-input');
      const val = (input.value || '').trim();
      if (!val) return;

      const payload = {{
        type: 'comment',
        action: 'vote',
        user: '@espectador_vip',
        comment: val,
        weight: 1,
        timestamp: Date.now()
      }};
      dispatchSimEvent(payload);
      input.value = '';
      showToast(`Comentário '${{val}}' enviado!`);
    }}

    function injectGift(giftName, coins, weight) {{
      const payload = {{
        type: 'gift',
        action: 'boost',
        user: '@patrocinador_top',
        giftName: giftName,
        coins: coins,
        weight: weight,
        timestamp: Date.now()
      }};
      dispatchSimEvent(payload);
      showToast(`Presente '${{giftName}}' (${{weight}}x) disparado!`);
    }}

    function dispatchSimEvent(payload) {{
      logTerminalEvent(payload);

      // 1. BroadcastChannel global da holding
      if (broadcastChannel) {{
        try {{
          broadcastChannel.postMessage(payload);
        }} catch (e) {{}}
      }}

      // 2. Iframe postMessage direto
      const iframe = document.getElementById('cartridge-iframe');
      if (iframe && iframe.contentWindow) {{
        try {{
          iframe.contentWindow.postMessage(payload, '*');
        }} catch (e) {{}}
      }}
    }}

    function logTerminalEvent(payload) {{
      const terminal = document.getElementById('event-terminal');
      if (!terminal) return;

      const time = new Date().toLocaleTimeString();
      let typeLabel = payload.type ? payload.type.toUpperCase() : 'EVENT';
      let desc = payload.comment || payload.giftName || payload.action || '';

      const line = document.createElement('div');
      line.className = 'log-line';
      line.innerHTML = `<span class="timestamp">[${{time}}]</span> <span class="ev-type">${{typeLabel}}</span>: <span class="ev-val">${{desc}}</span> (${{payload.user || '@live'}})`;

      terminal.appendChild(line);
      terminal.scrollTop = terminal.scrollHeight;
    }}

    function clearEventLogs() {{
      const terminal = document.getElementById('event-terminal');
      if (terminal) terminal.innerHTML = '<div class="log-line"><span class="timestamp">[00:00:00]</span> Logs limpos.</div>';
    }}

    // =========================================================================
    // TOAST NOTIFICATION
    // =========================================================================
    let toastTimer = null;
    function showToast(message) {{
      const toast = document.getElementById('toast-notification');
      const text = document.getElementById('toast-text');
      if (!toast || !text) return;

      text.innerText = message;
      toast.classList.add('show');

      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {{
        toast.classList.remove('show');
      }}, 2600);
    }}

    // =========================================================================
    // INICIALIZAÇÃO GERAL AO CARREGAR
    // =========================================================================
    window.addEventListener('DOMContentLoaded', () => {{
      renderPills();
      renderGamesGrid(GAMES_CATALOG);
      populateSimSelect();
      loadGameInSimulator('01_cabo_de_guerra_neon');
    }});
  </script>
</body>
</html>
"""

    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Portal V5 Games construído com sucesso em index.html!")

if __name__ == "__main__":
    build_portal()
