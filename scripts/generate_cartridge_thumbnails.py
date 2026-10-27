import os
import json

BASE_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games"
CATALOG_DIR = os.path.join(BASE_DIR, "catalogo_jogos")
BROADCASTER_GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games"

# Definições visuais temáticas dos 41 cartuchos (Cores, Ícones, Títulos, Subtítulos)
CARTRIDGE_THEMES = {
    "01_cabo_de_guerra_neon": {
        "title": "CABO DE GUERRA",
        "sub": "DISPUTA 1V1 NEON",
        "category": "POLARIZAÇÃO",
        "color1": "#ff0077",
        "color2": "#00f0ff",
        "accent": "#ffd700",
        "symbol": """
            <line x1="80" y1="250" x2="320" y2="250" stroke="#ffd700" stroke-width="8" stroke-dasharray="12 6"/>
            <circle cx="200" cy="250" r="24" fill="#ffd700" filter="url(#glow)"/>
            <polygon points="120,220 80,250 120,280" fill="#ff0077"/>
            <polygon points="280,220 320,250 280,280" fill="#00f0ff"/>
            <text x="100" y="320" fill="#ff0077" font-size="28" font-weight="900" text-anchor="middle">TIME 1</text>
            <text x="300" y="320" fill="#00f0ff" font-size="28" font-weight="900" text-anchor="middle">TIME 2</text>
        """
    },
    "01b_cabo_de_guerra_elementos": {
        "title": "FOGO VS GELO",
        "sub": "CABO ELEMENTAL",
        "category": "POLARIZAÇÃO",
        "color1": "#ff3300",
        "color2": "#00d4ff",
        "accent": "#ffaa00",
        "symbol": """
            <circle cx="140" cy="240" r="45" fill="#ff3300" opacity="0.8" filter="url(#glow)"/>
            <text x="140" y="255" font-size="45" text-anchor="middle">🔥</text>
            <circle cx="260" cy="240" r="45" fill="#00d4ff" opacity="0.8" filter="url(#glow)"/>
            <text x="260" y="255" font-size="45" text-anchor="middle">❄️</text>
            <path d="M185 240 L215 240" stroke="#ffffff" stroke-width="6"/>
            <circle cx="200" cy="240" r="10" fill="#ffffff" filter="url(#glow)"/>
        """
    },
    "02_plinko_pachinko_fortuna": {
        "title": "PLINKO DA FORTUNA",
        "sub": "JACKPOT x50 NEON",
        "category": "FÍSICA",
        "color1": "#ffd700",
        "color2": "#7928ca",
        "accent": "#00ff88",
        "symbol": """
            <circle cx="200" cy="180" r="14" fill="#ffd700" filter="url(#glow)"/>
            <circle cx="160" cy="230" r="5" fill="#ffffff"/>
            <circle cx="200" cy="230" r="5" fill="#ffffff"/>
            <circle cx="240" cy="230" r="5" fill="#ffffff"/>
            <circle cx="140" cy="280" r="5" fill="#ffffff"/>
            <circle cx="180" cy="280" r="5" fill="#ffffff"/>
            <circle cx="220" cy="280" r="5" fill="#ffffff"/>
            <circle cx="260" cy="280" r="5" fill="#ffffff"/>
            <rect x="110" y="310" width="180" height="25" rx="5" fill="#00ff88" opacity="0.3" stroke="#00ff88" stroke-width="2"/>
            <text x="200" y="328" fill="#00ff88" font-size="16" font-weight="900" text-anchor="middle">50x JACKPOT</text>
        """
    },
    "03_corrida_avatares_holding": {
        "title": "CORRIDA AVATARES",
        "sub": "CIRCUITO NITRO 3D",
        "category": "CORRIDA",
        "color1": "#00f0ff",
        "color2": "#ff0077",
        "accent": "#ffd700",
        "symbol": """
            <polygon points="120,330 200,180 280,330" fill="none" stroke="#334155" stroke-width="4"/>
            <line x1="200" y1="180" x2="200" y2="330" stroke="#ffd700" stroke-width="3" stroke-dasharray="10 8"/>
            <circle cx="170" cy="270" r="18" fill="#ff0077" filter="url(#glow)"/>
            <circle cx="230" cy="250" r="18" fill="#00f0ff" filter="url(#glow)"/>
            <text x="200" y="210" font-size="32" text-anchor="middle">🏎️</text>
        """
    },
    "04_boss_raid_cooperativo": {
        "title": "BOSS RAID",
        "sub": "TITÃ 1.000.000 HP",
        "category": "COOP BOSS",
        "color1": "#ef4444",
        "color2": "#7f1d1d",
        "accent": "#ffd700",
        "symbol": """
            <rect x="130" y="180" width="140" height="20" rx="4" fill="#1e293b" stroke="#ffffff" stroke-width="2"/>
            <rect x="132" y="182" width="95" height="16" rx="2" fill="#ef4444"/>
            <text x="200" y="270" font-size="64" text-anchor="middle">👾</text>
            <text x="200" y="320" fill="#ffd700" font-size="16" font-weight="900" text-anchor="middle">CHAT COOP COMBO</text>
        """
    },
    "05_roleta_desafios_live": {
        "title": "ROLETA DA SORTE",
        "sub": "GIROS & DESAFIOS",
        "category": "SORTEIO",
        "color1": "#a855f7",
        "color2": "#ec4899",
        "accent": "#ffd700",
        "symbol": """
            <circle cx="200" cy="245" r="75" fill="none" stroke="#ffd700" stroke-width="8" filter="url(#glow)"/>
            <circle cx="200" cy="245" r="68" fill="#1e1b4b"/>
            <line x1="200" y1="177" x2="200" y2="313" stroke="#ffd700" stroke-width="3"/>
            <line x1="132" y1="245" x2="268" y2="245" stroke="#ffd700" stroke-width="3"/>
            <polygon points="200,165 190,145 210,145" fill="#ef4444"/>
            <circle cx="200" cy="245" r="16" fill="#ffd700"/>
        """
    },
    "06_batalha_dos_baloes": {
        "title": "BATALHA DOS BALÕES",
        "sub": "EXPLOSÃO PNEUMÁTICA",
        "category": "POLARIZAÇÃO",
        "color1": "#38bdf8",
        "color2": "#f97316",
        "accent": "#ffffff",
        "symbol": """
            <ellipse cx="150" cy="240" rx="35" ry="45" fill="#38bdf8" filter="url(#glow)"/>
            <ellipse cx="250" cy="235" rx="42" ry="52" fill="#f97316" filter="url(#glow)"/>
            <polygon points="150,285 145,295 155,295" fill="#38bdf8"/>
            <polygon points="250,287 245,297 255,297" fill="#f97316"/>
            <text x="200" y="325" fill="#ffd700" font-size="20" font-weight="900" text-anchor="middle">BOOM!</text>
        """
    },
    "07_pendulo_destruidor": {
        "title": "PÊNDULO DEMOLIDOR",
        "sub": "COLISÃO DINÂMICA",
        "category": "ELIMINAÇÃO",
        "color1": "#eab308",
        "color2": "#713f12",
        "accent": "#ef4444",
        "symbol": """
            <line x1="200" y1="160" x2="160" y2="260" stroke="#94a3b8" stroke-width="4"/>
            <circle cx="160" cy="260" r="30" fill="#eab308" filter="url(#glow)"/>
            <rect x="230" y="240" width="30" height="50" fill="#ef4444" opacity="0.8"/>
            <rect x="265" y="220" width="25" height="70" fill="#ef4444" opacity="0.8"/>
        """
    },
    "08_caca_tesouro_coordenadas": {
        "title": "CAÇA AO TESOURO",
        "sub": "MATRIZ A1-D4",
        "category": "TABULEIRO",
        "color1": "#ffd700",
        "color2": "#0284c7",
        "accent": "#10b981",
        "symbol": """
            <rect x="130" y="180" width="140" height="140" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="3"/>
            <line x1="165" y1="180" x2="165" y2="320" stroke="#334155" stroke-width="2"/>
            <line x1="200" y1="180" x2="200" y2="320" stroke="#334155" stroke-width="2"/>
            <line x1="235" y1="180" x2="235" y2="320" stroke="#334155" stroke-width="2"/>
            <line x1="130" y1="215" x2="270" y2="215" stroke="#334155" stroke-width="2"/>
            <line x1="130" y1="250" x2="270" y2="250" stroke="#334155" stroke-width="2"/>
            <line x1="130" y1="285" x2="270" y2="285" stroke="#334155" stroke-width="2"/>
            <text x="218" y="275" font-size="24" text-anchor="middle">👑</text>
        """
    },
    "09_tsunami_de_curtidas": {
        "title": "TSUNAMI DE LIKES",
        "sub": "PRESSÃO HIDRÁULICA",
        "category": "POLARIZAÇÃO",
        "color1": "#ec4899",
        "color2": "#06b6d4",
        "accent": "#ffffff",
        "symbol": """
            <path d="M110 280 Q 160 210, 200 240 T 290 200 L 290 320 L 110 320 Z" fill="#06b6d4" opacity="0.8" filter="url(#glow)"/>
            <text x="160" y="220" font-size="28" text-anchor="middle">❤️</text>
            <text x="240" y="190" font-size="34" text-anchor="middle">💖</text>
        """
    },
    "10_queda_dos_blocos": {
        "title": "TETRIS DA DISCORDIA",
        "sub": "COLISÃO DE BLOCOS",
        "category": "TABULEIRO",
        "color1": "#a855f7",
        "color2": "#3b82f6",
        "accent": "#00ff88",
        "symbol": """
            <rect x="140" y="200" width="30" height="30" fill="#3b82f6" stroke="#ffffff" stroke-width="2"/>
            <rect x="170" y="200" width="30" height="30" fill="#3b82f6" stroke="#ffffff" stroke-width="2"/>
            <rect x="200" y="200" width="30" height="30" fill="#3b82f6" stroke="#ffffff" stroke-width="2"/>
            <rect x="170" y="230" width="30" height="30" fill="#3b82f6" stroke="#ffffff" stroke-width="2"/>
            <rect x="140" y="280" width="30" height="30" fill="#a855f7" stroke="#ffffff" stroke-width="2"/>
            <rect x="200" y="280" width="30" height="30" fill="#00ff88" stroke="#ffffff" stroke-width="2"/>
            <rect x="230" y="280" width="30" height="30" fill="#00ff88" stroke="#ffffff" stroke-width="2"/>
        """
    },
    "11_queda_de_braco_titas": {
        "title": "QUEDA DE BRAÇO",
        "sub": "DUELO DE TITÃS",
        "category": "POLARIZAÇÃO",
        "color1": "#f59e0b",
        "color2": "#dc2626",
        "accent": "#ffffff",
        "symbol": """
            <rect x="130" y="290" width="140" height="20" rx="4" fill="#334155"/>
            <text x="200" y="260" font-size="64" text-anchor="middle">🤼</text>
        """
    },
    "12_pachinko_pinball_neon": {
        "title": "PINBALL PACHINKO",
        "sub": "BUMPERS & PINS",
        "category": "FÍSICA",
        "color1": "#06b6d4",
        "color2": "#d946ef",
        "accent": "#facc15",
        "symbol": """
            <circle cx="200" cy="220" r="25" fill="#d946ef" filter="url(#glow)"/>
            <circle cx="150" cy="250" r="15" fill="#06b6d4"/>
            <circle cx="250" cy="250" r="15" fill="#06b6d4"/>
            <line x1="140" y1="310" x2="180" y2="300" stroke="#facc15" stroke-width="8" stroke-linecap="round"/>
            <line x1="260" y1="310" x2="220" y2="300" stroke="#facc15" stroke-width="8" stroke-linecap="round"/>
        """
    },
    "13_cascata_de_moedas": {
        "title": "CASCATA DE MOEDAS",
        "sub": "DOZER MULTIPLICADOR",
        "category": "FÍSICA",
        "color1": "#eab308",
        "color2": "#ca8a04",
        "accent": "#ffffff",
        "symbol": """
            <circle cx="170" cy="220" r="22" fill="#ffd700" stroke="#ca8a04" stroke-width="3" filter="url(#glow)"/>
            <circle cx="220" cy="210" r="22" fill="#ffd700" stroke="#ca8a04" stroke-width="3" filter="url(#glow)"/>
            <circle cx="195" cy="250" r="22" fill="#ffd700" stroke="#ca8a04" stroke-width="3" filter="url(#glow)"/>
            <rect x="130" y="280" width="140" height="25" rx="4" fill="#64748b"/>
        """
    },
    "14_vortex_gravitacional": {
        "title": "VORTEX CÓSMICO",
        "sub": "GRAVIDADE NEGRA",
        "category": "FÍSICA",
        "color1": "#8b5cf6",
        "color2": "#1e1b4b",
        "accent": "#38bdf8",
        "symbol": """
            <circle cx="200" cy="245" r="50" fill="#030712" stroke="#8b5cf6" stroke-width="6" filter="url(#glow)"/>
            <circle cx="200" cy="245" r="20" fill="#000000"/>
            <circle cx="160" cy="210" r="8" fill="#38bdf8"/>
            <circle cx="240" cy="260" r="10" fill="#f43f5e"/>
            <circle cx="210" cy="300" r="6" fill="#ffd700"/>
        """
    },
    "15_corrida_maluca_espacial": {
        "title": "CORRIDA ESPACIAL",
        "sub": "HIPER-PROPULSÃO",
        "category": "CORRIDA",
        "color1": "#6366f1",
        "color2": "#06b6d4",
        "accent": "#ffd700",
        "symbol": """
            <text x="170" y="230" font-size="42" text-anchor="middle">🚀</text>
            <text x="230" y="270" font-size="42" text-anchor="middle">🛸</text>
            <line x1="110" y1="310" x2="290" y2="310" stroke="#38bdf8" stroke-width="3" stroke-dasharray="10 5"/>
        """
    },
    "16_arrancada_noturna_neon": {
        "title": "ARRANCADA NOTURNA",
        "sub": "DRAG RACE NITRO",
        "category": "CORRIDA",
        "color1": "#ef4444",
        "color2": "#22c55e",
        "accent": "#ffd700",
        "symbol": """
            <circle cx="170" cy="180" r="10" fill="#ef4444"/>
            <circle cx="170" cy="205" r="10" fill="#eab308"/>
            <circle cx="170" cy="230" r="10" fill="#22c55e" filter="url(#glow)"/>
            <text x="240" y="260" font-size="52" text-anchor="middle">🏎️</text>
        """
    },
    "17_caca_niquel_neon_777": {
        "title": "SLOTS VEGAS 777",
        "sub": "CASSINO NEON",
        "category": "CASSINO",
        "color1": "#f59e0b",
        "color2": "#b45309",
        "accent": "#ffd700",
        "symbol": """
            <rect x="120" y="190" width="160" height="90" rx="10" fill="#1e1b4b" stroke="#ffd700" stroke-width="4"/>
            <text x="150" y="255" fill="#ef4444" font-size="42" font-weight="900" text-anchor="middle">7</text>
            <text x="200" y="255" fill="#ffd700" font-size="42" font-weight="900" text-anchor="middle">7</text>
            <text x="250" y="255" fill="#ef4444" font-size="42" font-weight="900" text-anchor="middle">7</text>
        """
    },
    "18_roleta_russa_baloes": {
        "title": "ROLETA DOS BALÕES",
        "sub": "TENSÃO DE DISPARO",
        "category": "ELIMINAÇÃO",
        "color1": "#ef4444",
        "color2": "#1e293b",
        "accent": "#38bdf8",
        "symbol": """
            <circle cx="200" cy="240" r="55" fill="#1e293b" stroke="#64748b" stroke-width="6"/>
            <circle cx="200" cy="200" r="12" fill="#38bdf8"/>
            <circle cx="235" cy="225" r="12" fill="#38bdf8"/>
            <circle cx="235" cy="260" r="12" fill="#ef4444" filter="url(#glow)"/>
            <circle cx="200" cy="280" r="12" fill="#38bdf8"/>
            <circle cx="165" cy="260" r="12" fill="#38bdf8"/>
            <circle cx="165" cy="225" r="12" fill="#38bdf8"/>
        """
    },
    "19_defesa_da_torre_chat": {
        "title": "DEFESA DA TORRE",
        "sub": "TURRETAS & CHAT",
        "category": "COOPERATIVO",
        "color1": "#10b981",
        "color2": "#065f46",
        "accent": "#38bdf8",
        "symbol": """
            <polygon points="200,160 160,200 170,200 170,300 230,300 230,200 240,200" fill="#10b981" stroke="#38bdf8" stroke-width="3"/>
            <line x1="200" y1="160" x2="280" y2="190" stroke="#38bdf8" stroke-width="4" filter="url(#glow)"/>
            <text x="290" y="200" font-size="24">👾</text>
        """
    },
    "20_subida_da_montanha_sagrada": {
        "title": "MONTANHA SAGRADA",
        "sub": "ESCALADA EXTREMA",
        "category": "ELIMINAÇÃO",
        "color1": "#f59e0b",
        "color2": "#78350f",
        "accent": "#ffffff",
        "symbol": """
            <polygon points="200,160 110,310 290,310" fill="#475569" stroke="#94a3b8" stroke-width="3"/>
            <polygon points="200,160 180,200 220,200" fill="#ffffff"/>
            <text x="215" y="240" font-size="28">🧗</text>
        """
    },
    "21_batata_quente_explosiva": {
        "title": "BATATA QUENTE",
        "sub": "FUSÍVEL CURTO",
        "category": "ELIMINAÇÃO",
        "color1": "#ea580c",
        "color2": "#7c2d12",
        "accent": "#facc15",
        "symbol": """
            <circle cx="195" cy="250" r="45" fill="#1e293b" stroke="#ea580c" stroke-width="4" filter="url(#glow)"/>
            <path d="M210 210 Q 230 190, 240 180" stroke="#facc15" stroke-width="4" fill="none"/>
            <text x="250" y="180" font-size="26">💥</text>
            <text x="195" y="265" font-size="32" text-anchor="middle">💣</text>
        """
    },
    "22_ponte_de_vidro_quebradico": {
        "title": "PONTE DE VIDRO",
        "sub": "PASSO A PASSO",
        "category": "ELIMINAÇÃO",
        "color1": "#06b6d4",
        "color2": "#0e7490",
        "accent": "#ef4444",
        "symbol": """
            <rect x="130" y="190" width="55" height="35" rx="4" fill="#06b6d4" opacity="0.6" stroke="#ffffff" stroke-width="2"/>
            <rect x="215" y="190" width="55" height="35" rx="4" fill="#ef4444" opacity="0.4" stroke="#ef4444" stroke-width="2"/>
            <rect x="130" y="245" width="55" height="35" rx="4" fill="#06b6d4" opacity="0.6" stroke="#ffffff" stroke-width="2"/>
            <rect x="215" y="245" width="55" height="35" rx="4" fill="#06b6d4" opacity="0.6" stroke="#ffffff" stroke-width="2"/>
            <text x="200" y="320" font-size="24" text-anchor="middle">👟</text>
        """
    },
    "23_sobrevivencia_na_lava": {
        "title": "CHÃO É LAVA",
        "sub": "PLATAFORMAS MÓVEIS",
        "category": "ELIMINAÇÃO",
        "color1": "#f97316",
        "color2": "#b91c1c",
        "accent": "#facc15",
        "symbol": """
            <polygon points="150,220 170,205 190,220 190,245 170,260 150,245" fill="#334155" stroke="#facc15" stroke-width="2"/>
            <polygon points="210,240 230,225 250,240 250,265 230,280 210,265" fill="#334155" stroke="#facc15" stroke-width="2"/>
            <rect x="110" y="280" width="180" height="30" fill="#b91c1c" opacity="0.9" filter="url(#glow)"/>
            <text x="200" y="300" font-size="20" text-anchor="middle">🔥 LAVA 🔥</text>
        """
    },
    "24_campo_minado_neon": {
        "title": "CAMPO MINADO",
        "sub": "RADAR & BOMBAS",
        "category": "TABULEIRO",
        "color1": "#ef4444",
        "color2": "#10b981",
        "accent": "#ffd700",
        "symbol": """
            <rect x="130" y="180" width="65" height="65" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
            <text x="162" y="225" fill="#10b981" font-size="32" font-weight="900" text-anchor="middle">2</text>
            <rect x="205" y="180" width="65" height="65" rx="6" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
            <text x="237" y="225" font-size="28" text-anchor="middle">💣</text>
            <rect x="130" y="255" width="65" height="65" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
            <text x="162" y="298" font-size="28" text-anchor="middle">🚩</text>
            <rect x="205" y="255" width="65" height="65" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
            <text x="237" y="300" fill="#10b981" font-size="32" font-weight="900" text-anchor="middle">1</text>
        """
    },
    "25_batalha_naval_live": {
        "title": "BATALHA NAVAL",
        "sub": "TORPEDOS DE CHAT",
        "category": "TABULEIRO",
        "color1": "#0284c7",
        "color2": "#0c4a6e",
        "accent": "#38bdf8",
        "symbol": """
            <circle cx="200" cy="245" r="60" fill="none" stroke="#0284c7" stroke-width="3"/>
            <circle cx="200" cy="245" r="40" fill="none" stroke="#0284c7" stroke-width="2"/>
            <line x1="200" y1="175" x2="200" y2="315" stroke="#0284c7" stroke-width="2"/>
            <line x1="130" y1="245" x2="270" y2="245" stroke="#0284c7" stroke-width="2"/>
            <text x="200" y="255" font-size="34" text-anchor="middle">🚢</text>
        """
    },
    "26_guerra_dos_tanques_neon": {
        "title": "GUERRA DOS TANQUES",
        "sub": "ARTILHARIA BALÍSTICA",
        "category": "ARTILHARIA",
        "color1": "#22c55e",
        "color2": "#eab308",
        "accent": "#ffffff",
        "symbol": """
            <text x="150" y="280" font-size="44" text-anchor="middle">🛡️</text>
            <text x="250" y="280" font-size="44" text-anchor="middle">🎯</text>
            <path d="M160 260 Q 200 180, 240 260" stroke="#ffd700" stroke-width="4" stroke-dasharray="6 4" fill="none"/>
        """
    },
    "27_meteoro_defensor": {
        "title": "METEORO DEFENSOR",
        "sub": "DEFESA PLANETÁRIA",
        "category": "ARCADE DEFESA",
        "color1": "#38bdf8",
        "color2": "#6366f1",
        "accent": "#ef4444",
        "symbol": """
            <circle cx="200" cy="265" r="45" fill="#38bdf8" filter="url(#glow)"/>
            <text x="200" y="278" font-size="38" text-anchor="middle">🌍</text>
            <line x1="200" y1="220" x2="250" y2="160" stroke="#22c55e" stroke-width="4"/>
            <text x="260" y="165" font-size="28">☄️</text>
        """
    },
    "28_labirinto_pacman_neon": {
        "title": "PACMAN NEON",
        "sub": "LABIRINTO RETRÔ",
        "category": "ARCADE",
        "color1": "#facc15",
        "color2": "#3b82f6",
        "accent": "#ef4444",
        "symbol": """
            <path d="M170 245 L 205 220 A 40 40 0 1 0 205 270 Z" fill="#facc15" filter="url(#glow)"/>
            <circle cx="230" cy="245" r="6" fill="#ffffff"/>
            <circle cx="255" cy="245" r="6" fill="#ffffff"/>
            <text x="280" y="255" font-size="26">👻</text>
        """
    },
    "29_basquete_street_neon": {
        "title": "BASQUETE STREET",
        "sub": "TABELA & SWISH",
        "category": "ESPORTES",
        "color1": "#f97316",
        "color2": "#ea580c",
        "accent": "#ffffff",
        "symbol": """
            <rect x="230" y="170" width="10" height="70" fill="#ffffff"/>
            <rect x="180" y="220" width="50" height="8" fill="#f97316"/>
            <path d="M185 228 L 225 228 L 215 270 L 195 270 Z" fill="none" stroke="#ffffff" stroke-width="3" stroke-dasharray="4 2"/>
            <circle cx="150" cy="245" r="22" fill="#f97316" stroke="#000000" stroke-width="2" filter="url(#glow)"/>
        """
    },
    "30_gol_de_penalti_live": {
        "title": "GOL DE PÊNALTI",
        "sub": "CHAT VS GOLEIRO",
        "category": "ESPORTES",
        "color1": "#22c55e",
        "color2": "#15803d",
        "accent": "#ffd700",
        "symbol": """
            <rect x="130" y="180" width="140" height="80" fill="none" stroke="#ffffff" stroke-width="4"/>
            <line x1="130" y1="220" x2="270" y2="220" stroke="#334155" stroke-width="2"/>
            <text x="200" y="240" font-size="36" text-anchor="middle">🧤</text>
            <circle cx="200" cy="295" r="18" fill="#ffffff" stroke="#000000" stroke-width="2"/>
        """
    },
    "31_guitar_hero_neon": {
        "title": "GUITAR HERO LIVE",
        "sub": "RITMO & NOTAS",
        "category": "RITMO",
        "color1": "#a855f7",
        "color2": "#ec4899",
        "accent": "#00ff88",
        "symbol": """
            <polygon points="150,170 250,170 280,310 120,310" fill="#1e1b4b" stroke="#6366f1" stroke-width="3"/>
            <circle cx="155" cy="285" r="14" fill="#22c55e"/>
            <circle cx="185" cy="285" r="14" fill="#ef4444"/>
            <circle cx="215" cy="285" r="14" fill="#eab308"/>
            <circle cx="245" cy="285" r="14" fill="#3b82f6"/>
        """
    },
    "32_corte_de_frutas_neon": {
        "title": "CORTE DE FRUTAS",
        "sub": "LÂMINAS LASER",
        "category": "REFLEXO",
        "color1": "#ef4444",
        "color2": "#10b981",
        "accent": "#38bdf8",
        "symbol": """
            <text x="160" y="240" font-size="38" text-anchor="middle">🍉</text>
            <text x="240" y="260" font-size="34" text-anchor="middle">🍊</text>
            <line x1="120" y1="280" x2="280" y2="180" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" filter="url(#glow)"/>
        """
    },
    "33_corrida_de_cavalos_retro": {
        "title": "CORRIDA DE CAVALOS",
        "sub": "HIPÓDROMO 4 RAIAS",
        "category": "CORRIDA",
        "color1": "#b45309",
        "color2": "#78350f",
        "accent": "#ffd700",
        "symbol": """
            <line x1="110" y1="200" x2="290" y2="200" stroke="#64748b" stroke-width="2"/>
            <line x1="110" y1="240" x2="290" y2="240" stroke="#64748b" stroke-width="2"/>
            <line x1="110" y1="280" x2="290" y2="280" stroke="#64748b" stroke-width="2"/>
            <text x="180" y="235" font-size="34" text-anchor="middle">🏇</text>
            <text x="230" y="275" font-size="34" text-anchor="middle">🐎</text>
        """
    },
    "34_pinball_galactico": {
        "title": "PINBALL GALÁCTICO",
        "sub": "MESA CÓSMICA",
        "category": "FÍSICA",
        "color1": "#3b82f6",
        "color2": "#8b5cf6",
        "accent": "#f43f5e",
        "symbol": """
            <circle cx="200" cy="210" r="30" fill="#f43f5e" filter="url(#glow)"/>
            <circle cx="160" cy="260" r="18" fill="#3b82f6"/>
            <circle cx="240" cy="260" r="18" fill="#3b82f6"/>
            <line x1="140" y1="315" x2="185" y2="305" stroke="#ffd700" stroke-width="8" stroke-linecap="round"/>
            <line x1="260" y1="315" x2="215" y2="305" stroke="#ffd700" stroke-width="8" stroke-linecap="round"/>
        """
    },
    "35_quiz_frenetico_holding": {
        "title": "QUIZ FRENÉTICO",
        "sub": "PERGUNTAS & QI",
        "category": "TRIVIA",
        "color1": "#06b6d4",
        "color2": "#3b82f6",
        "accent": "#ffd700",
        "symbol": """
            <text x="200" y="230" font-size="52" text-anchor="middle">🧠</text>
            <rect x="130" y="255" width="65" height="22" rx="4" fill="#3b82f6"/>
            <text x="162" y="271" fill="#fff" font-size="12" font-weight="900" text-anchor="middle">A: 45%</text>
            <rect x="205" y="255" width="65" height="22" rx="4" fill="#10b981"/>
            <text x="237" y="271" fill="#fff" font-size="12" font-weight="900" text-anchor="middle">B: 55%</text>
        """
    },
    "36_pula_corda_extremo": {
        "title": "PULA-CORDA EXTREMO",
        "sub": "RPM & RITMO 3D",
        "category": "RITMO",
        "color1": "#00ff88",
        "color2": "#06b6d4",
        "accent": "#ffd700",
        "symbol": """
            <path d="M120 280 Q 200 160, 280 280" stroke="#00ff88" stroke-width="6" fill="none" filter="url(#glow)"/>
            <text x="200" y="255" font-size="44" text-anchor="middle">🦘</text>
        """
    },
    "37_torre_de_blocos_equilibrada": {
        "title": "TORRE DE BLOCOS",
        "sub": "JENGA OSCILANTE",
        "category": "EQUILÍBRIO",
        "color1": "#f59e0b",
        "color2": "#38bdf8",
        "accent": "#ef4444",
        "symbol": """
            <rect x="160" y="190" width="80" height="20" rx="3" fill="#f59e0b"/>
            <rect x="155" y="215" width="80" height="20" rx="3" fill="#38bdf8"/>
            <rect x="165" y="240" width="80" height="20" rx="3" fill="#f59e0b"/>
            <rect x="150" y="265" width="80" height="20" rx="3" fill="#ef4444"/>
            <rect x="160" y="290" width="80" height="20" rx="3" fill="#f59e0b"/>
        """
    },
    "38_fuga_da_prisao_espacial": {
        "title": "FUGA ESPACIAL",
        "sub": "JETPACK & LASERS",
        "category": "REFLEXO",
        "color1": "#38bdf8",
        "color2": "#ef4444",
        "accent": "#ffd700",
        "symbol": """
            <line x1="120" y1="210" x2="280" y2="210" stroke="#ef4444" stroke-width="4" stroke-dasharray="8 4" filter="url(#glow)"/>
            <line x1="120" y1="270" x2="280" y2="270" stroke="#ef4444" stroke-width="4" stroke-dasharray="8 4" filter="url(#glow)"/>
            <text x="200" y="255" font-size="42" text-anchor="middle">🧑‍🚀</text>
        """
    },
    "39_alvo_movel_snipers": {
        "title": "ALVO DOS SNIPERS",
        "sub": "PONTARIA & LOCK-ON",
        "category": "PONTARIA",
        "color1": "#ef4444",
        "color2": "#38bdf8",
        "accent": "#ffd700",
        "symbol": """
            <circle cx="200" cy="240" r="55" fill="none" stroke="#ef4444" stroke-width="8"/>
            <circle cx="200" cy="240" r="35" fill="none" stroke="#ffffff" stroke-width="6"/>
            <circle cx="200" cy="240" r="16" fill="#ffd700" filter="url(#glow)"/>
            <line x1="200" y1="170" x2="200" y2="310" stroke="#38bdf8" stroke-width="2"/>
            <line x1="130" y1="240" x2="270" y2="240" stroke="#38bdf8" stroke-width="2"/>
            <text x="200" y="247" font-size="16" text-anchor="middle">🎯</text>
        """
    },
    "40_duelo_de_magicos_neon": {
        "title": "DUELO DE MÁGICOS",
        "sub": "FOGO VS GELO",
        "category": "POLARIZAÇÃO",
        "color1": "#ff4500",
        "color2": "#00e5ff",
        "accent": "#ffd700",
        "symbol": """
            <line x1="200" y1="160" x2="200" y2="245" stroke="#ff4500" stroke-width="12" filter="url(#glow)"/>
            <line x1="200" y1="330" x2="200" y2="245" stroke="#00e5ff" stroke-width="12" filter="url(#glow)"/>
            <circle cx="200" cy="245" r="28" fill="#ffffff" filter="url(#glow)"/>
            <text x="200" y="180" font-size="28" text-anchor="middle">🧙‍♂️</text>
            <text x="200" y="325" font-size="28" text-anchor="middle">🧙</text>
        """
    }
}

def generate_svg_thumbnail(slug, theme):
    title = theme["title"].replace("&", "&amp;")
    sub = theme["sub"].replace("&", "&amp;")
    category = theme["category"].replace("&", "&amp;")
    color1 = theme["color1"]
    color2 = theme["color2"]
    accent = theme["accent"]
    symbol = theme["symbol"].replace(" & ", " &amp; ")

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="100%" height="100%">
  <defs>
    <!-- Gradiente de Fundo -->
    <linearGradient id="bg-grad-{slug}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#030712"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>

    <!-- Gradiente de Borda Neon -->
    <linearGradient id="border-grad-{slug}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{color1}"/>
      <stop offset="50%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="{color2}"/>
    </linearGradient>

    <!-- Filtro de Brilho Neon -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Fundo com Borda Estilizada -->
  <rect x="5" y="5" width="390" height="490" rx="24" fill="url(#bg-grad-{slug})" stroke="url(#border-grad-{slug})" stroke-width="4"/>

  <!-- Grid Tecnológico Sutil -->
  <path d="M20 70 L380 70 M20 410 L380 410" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <circle cx="200" cy="245" r="140" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="2"/>

  <!-- Badge Topo Esquerda: V5 9:16 LIVE -->
  <rect x="25" y="25" width="115" height="26" rx="13" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
  <circle cx="40" cy="38" r="4" fill="#ef4444"/>
  <text x="52" y="42" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="800" letter-spacing="1">V5 9:16</text>

  <!-- Pill Categoria Topo Direita -->
  <rect x="255" y="25" width="120" height="26" rx="13" fill="rgba(255,255,255,0.08)" stroke="{color1}" stroke-width="1"/>
  <text x="315" y="42" fill="{color1}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="900" letter-spacing="1" text-anchor="middle">{category}</text>

  <!-- Elemento Central Simbólico do Jogo -->
  <g>
    {symbol}
  </g>

  <!-- Título e Subtítulo Inferior -->
  <text x="200" y="445" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="900" letter-spacing="1" text-anchor="middle">{title}</text>
  <text x="200" y="470" fill="{accent}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" letter-spacing="2" text-anchor="middle">{sub}</text>
</svg>"""
    return svg_content

def generate_all_thumbnails():
    print("=" * 80)
    print(" GERAÇÃO INDUSTRIAL DE MINIATURAS SVG VETORIAIS (FASE 10 - ETAPA 097)")
    print(" Holding V5 Apollo — Capitania V5 Games")
    print("=" * 80)

    cartridges = sorted([
        d for d in os.listdir(CATALOG_DIR) 
        if os.path.isdir(os.path.join(CATALOG_DIR, d)) and not d.startswith(".")
    ])

    generated = 0

    for c_slug in cartridges:
        theme = CARTRIDGE_THEMES.get(c_slug, {
            "title": c_slug.replace("_", " ").title(),
            "sub": "V5 LIVE CARTRIDGE",
            "category": "ARCADE",
            "color1": "#38bdf8",
            "color2": "#ec4899",
            "accent": "#ffd700",
            "symbol": '<text x="200" y="260" font-size="64" text-anchor="middle">🎮</text>'
        })

        svg = generate_svg_thumbnail(c_slug, theme)

        # 1. Salvar no repositório de cartuchos
        local_svg_path = os.path.join(CATALOG_DIR, c_slug, "thumbnail.svg")
        with open(local_svg_path, "w", encoding="utf-8") as f:
            f.write(svg)

        # 2. Salvar na pasta pública do Broadcaster
        broadcaster_game_dir = os.path.join(BROADCASTER_GAMES_DIR, c_slug)
        if os.path.exists(broadcaster_game_dir):
            broadcaster_svg_path = os.path.join(broadcaster_game_dir, "thumbnail.svg")
            with open(broadcaster_svg_path, "w", encoding="utf-8") as f:
                f.write(svg)

        generated += 1
        print(f"  [GEN] Miniatura gerada: {c_slug} -> thumbnail.svg")

    print("-" * 80)
    print(f"[SUCCESS] {generated} miniaturas SVG vetoriais geradas com sucesso!")
    print("=" * 80)

if __name__ == "__main__":
    generate_all_thumbnails()
