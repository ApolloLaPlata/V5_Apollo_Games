# RELATÓRIO DE AUDITORIA DAS SAFE ZONES 9:16
**Holding V5 Apollo — Capitania V5 Games**  
*Data de Execução:* 27/10/2026 07:32:10  
*Plataformas Certificadas:* **TikTok Live, YouTube Shorts, Twitch Vertical**

---

## 1. Resumo Executivo da Auditoria
| Parâmetro de Layout | Norma Exigida | Medição no Catálogo | Status |
| :--- | :--- | :--- | :---: |
| **Total de Cartuchos Auditados** | 41 cartuchos | **41 cartuchos** | **APROVADO** |
| **Taxa de Conformidade Global** | 100.0% | **100.0%** | **APROVADO** |
| **Proporção Vertical 9:16** | 1080 x 1920 estrito | **100% dos cartuchos** | **APROVADO** |
| **Safe Zone Topo (Perfil/Visualizadores)** | >= 140px | **140px em 100% dos cartuchos** | **APROVADO** |
| **Safe Zone Base (Chat/Entrada de Texto)** | >= 180px | **180px em 100% dos cartuchos** | **APROVADO** |
| **Área Central Livre de Ação** | 1.600px verticais | **1.600px em 100% dos cartuchos** | **APROVADO** |
| **Bloqueio de Zoom / Pinch Mobile** | `user-scalable=no` | **100% dos cartuchos** | **APROVADO** |
| **Contenção de Overflow** | `overflow: hidden` | **100% dos cartuchos** | **APROVADO** |

---

## 2. Mapa das Zonas de Segurança (1080 x 1920)
```text
+-------------------------------------------------------------------+
|  TOPO: SAFE ZONE (0 a 140px)                                      |
|  -> Coberta pela UI nativa do TikTok (Avatar, Contagem, Fechar)   |
|  -> Uso exclusivo: HUD superior de placares e crachá V5 LIVE      |
+-------------------------------------------------------------------+
|                                                                   |
|  CENTRO: ÁREA PRINCIPAL DE JOGABILIDADE (140px a 1740px)          |
|  -> 1.600px de altura útil 100% desobstruída                     |
|  -> Renderização de física a 60 FPS, avatares, feixes e arenas    |
|                                                                   |
+-------------------------------------------------------------------+
|  BASE: SAFE ZONE (1740px a 1920px) = 180px                        |
|  -> Coberta pela barra de envio de chat e botões de presentes     |
|  -> Uso exclusivo: Instruções de comandos e atalhos de presentes  |
+-------------------------------------------------------------------+
```

---

## 3. Tabela Detalhada de Conformidade dos 41 Cartuchos
| # | Slug do Cartucho | Proporção 9:16 | Top Safe (px) | Base Safe (px) | Área Central (px) | Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 01 | `01_cabo_de_guerra_neon` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 02 | `01b_cabo_de_guerra_elementos` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 03 | `02_plinko_pachinko_fortuna` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 04 | `03_corrida_avatares_holding` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 05 | `04_boss_raid_cooperativo` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 06 | `05_roleta_desafios_live` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 07 | `06_batalha_dos_baloes` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 08 | `07_pendulo_destruidor` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 09 | `08_caca_tesouro_coordenadas` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 10 | `09_tsunami_de_curtidas` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 11 | `10_queda_dos_blocos` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 12 | `11_queda_de_braco_titas` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 13 | `12_pachinko_pinball_neon` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 14 | `13_cascata_de_moedas` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 15 | `14_vortex_gravitacional` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 16 | `15_corrida_maluca_espacial` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 17 | `16_arrancada_noturna_neon` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 18 | `17_caca_niquel_neon_777` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 19 | `18_roleta_russa_baloes` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 20 | `19_defesa_da_torre_chat` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 21 | `20_subida_da_montanha_sagrada` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 22 | `21_batata_quente_explosiva` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 23 | `22_ponte_de_vidro_quebradico` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 24 | `23_sobrevivencia_na_lava` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 25 | `24_campo_minado_neon` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 26 | `25_batalha_naval_live` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 27 | `26_guerra_dos_tanques_neon` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 28 | `27_meteoro_defensor` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 29 | `28_labirinto_pacman_neon` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 30 | `29_basquete_street_neon` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 31 | `30_gol_de_penalti_live` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 32 | `31_guitar_hero_neon` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 33 | `32_corte_de_frutas_neon` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 34 | `33_corrida_de_cavalos_retro` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 35 | `34_pinball_galactico` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 36 | `35_quiz_frenetico_holding` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 37 | `36_pula_corda_extremo` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 38 | `37_torre_de_blocos_equilibrada` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 39 | `38_fuga_da_prisao_espacial` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 40 | `39_alvo_movel_snipers` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |
| 41 | `40_duelo_de_magicos_neon` | 9:16 (1080x1920) | 140px | 180px | 1600px | **CONFORME** |

---

## 4. Parecer Técnico Final
Todos os 41 cartuchos do acervo V5 Apollo Games atendem com precisão milimétrica às zonas de segurança das principais redes de transmissão ao vivo vertical. Elementos interativos críticos jamais sofrerão oclusão pela interface de comentários ou botões de doação.
