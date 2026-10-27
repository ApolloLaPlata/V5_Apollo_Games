# MEMÓRIA ATIVA — CAPITANIA V5 GAMES (CATÁLOGO DE JOGOS DE LIVE)

**Última Atualização:** 27 de Outubro de 2026  
**Status do Projeto:** Fase 1 — Fundação da Infraestrutura & Catálogo Inicial (Meta: 30 Jogos Homologados)  
**Destino de Hospedagem:** `E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Broadcaster\frontend\public\games\`  
**Resolução Padrão:** 1080 x 1920 (Vertical 9:16)

---

## 0. O Propósito Sagrado do V5 Games & Aliança com o Broadcaster
- **Por que esta Capitania Existe:** O **V5 Broadcaster** é o motor de transmissão contínua 24/7 (FFmpeg, NVENC, OBS, Syndication, Rádio). Se o Broadcaster tentasse fabricar jogos, ele perderia o foco de infraestrutura pesada e se corromperia.
- **A Divisão dos Poderes:**
  - **V5 Broadcaster:** O Console e Estúdio de Streaming.
  - **V5 Games:** A Forja Exclusiva de Cartuchos. 
- **A Tese de Monetização & Dogfooding:** Jogos de live em formato 9:16 são máquinas de retenção e faturamento em presentes (TikTok Gifts, rosas, foguetes, leões, moedas). Nós seremos nossos próprios primeiros clientes (alimentando nossas lives 24/7 e os canais multimodais da holding, como o **Roxingo**).
- **Meta Primária:** Construir e homologar uma esteira de **~30 jogos ultra-polidos**, leves, sem dependências externas, com física suave (60 FPS), síntese de áudio procedural e psicologia de monetização afiada.

---

## 1. Visão do Catálogo Exclusivo (Meta: 30 Jogos Próprios)
O objetivo financeiro e técnico é possuir um acervo proprietário de alta qualidade que transforma transmissões de streamers e as nossas próprias lives em pólos de alta retenção e receita com presentes (TikTok Gifts / YouTube SuperChats).

### Tabela Mestra do Catálogo de Cartuchos:

| # | Slug do Jogo | Nome Comercial | Mecânica Principal | Status |
|---|---|---|---|---|
| **01** | `01_cabo_de_guerra_neon` | Cabo de Guerra Neon | Chat vota 1 ou 2 para puxar a corda; Presentes dão super-tração | **HOMOLOGADO** |
| **01B** | `01b_cabo_de_guerra_elementos` | Cabo de Guerra dos Elementos | Fogo vs Gelo com termômetro dinâmico (-100°C a +1000°C) e partículas térmicas | **HOMOLOGADO** |
| **02** | `02_plinko_pachinko_fortuna` | Plinko da Fortuna | Comentários e gifts soltam bolinhas físicas que caem em multiplicadores (50x Jackpot) | **HOMOLOGADO** |
| **03** | `03_corrida_avatares_holding` | Corrida dos Avatares | Roxingo, Baiano e Macaco Driver disputam pista acelerando com votos | Planejado |
| **04** | `04_boss_raid_cooperativo` | Boss Raid do Chat | Chat inteiro ataca monstro gigante com barra de HP em 45 segundos | Planejado |
| **05** | `05_roleta_desafios_live` | Roleta dos Desafios | Presentes giram a roleta de desafios cômicos para o streamer ou avatar | Planejado |
| **06** | `06_batalha_dos_baloes` | Estouro de Balão | Dois lados inflando balões colossais com física elástica até o estouro | **HOMOLOGADO** |
| **07** | `07_pendulo_destruidor` | Pêndulo da Demolição | Chat ajusta o ângulo do pêndulo para derrubar a torre adversária | Planejado |
| **08** | `08_caca_tesouro_coordenadas` | Caça ao Baú de Ouro | Chat escolhe quadrantes (A1 a D4) para desarmar bombas e achar o baú | Planejado |
| **09** | `09_tsunami_de_curtidas` | Tsunami de Likes | Disputa frenética de maré e pressão hidráulica, micro-ondas de choque e alarme de inundação | **HOMOLOGADO** |
| **10** | `10_queda_dos_blocos` | Tetris da Discórdia | Chat decide onde soltar blocos pesados para esmagar os inimigos | Planejado |
| **11** | `11_queda_de_braco_titas` | Queda de Braço dos Titãs | Braços cibernéticos com indicador de torque pilotados por votos e overdrive de gifts | **HOMOLOGADO** |

---

## 2. Contrato de Integração com o V5 Broadcaster
- O Broadcaster lê os eventos da live do TikTok e do YouTube e emite mensagens via:
  1. `BroadcastChannel('v5_broadcaster_games')`
  2. `window.dispatchEvent(new CustomEvent('v5_event', { detail: payload }))`
- O jogo roda dentro do OBS Studio como fonte de navegador (**Browser Source**) apontando para:
  `http://localhost:3000/games/<slug_do_jogo>/index.html` ou pela CDN do Broadcaster.

---

## 3. Diretrizes de Engenharia dos Cartuchos
1. **Zero Dependência de CDN Externa:** Tudo (HTML, CSS, JS, sintetizador de som) deve rodar localmente sem travar se a internet oscilar no OBS.
2. **60 FPS Estáveis em GPU/Canvas:** Renderização ultra otimizada com `requestAnimationFrame` que não consuma mais que 3% a 5% da CPU da máquina de transmissão.
3. **Painel de Depuração Embutido:** Toda tela tem uma gaveta oculta na base que permite testar votos e presentes manualmente antes de ligar a live (escondida com tecla `D` ou clique duplo no rodapé).
