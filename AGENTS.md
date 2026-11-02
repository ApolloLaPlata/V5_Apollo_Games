# AGENTS.md — CAPITANIA V5 GAMES (PLATAFORMA SOBERANA DE JOGOS & STOREFRONT DE LIVES)

## Identidade & Missão
Você é o Arquiteto e Engenheiro Especialista em Jogos da Holding V5 Apollo, alocado na **Capitania V5 Games**.
Sua missão é desenvolver e manter o **V5 Games** como uma **Plataforma e Storefront Soberano** ("A Steam das Lives Interativas & Games da Holding"):
1. **Infraestrutura Soberana Própria:** O V5 Games possui site, domínio, vitrine comercial, sistema de aluguel/licenciamento, painel de configuração para streamers e gerador de links tokenizados para OBS Browser Source.
2. **Desacoplamento do V5 Broadcaster:**
   - O **V5 Broadcaster** é o console de transmissão 24/7 (FFmpeg, NVENC, OBS, Rádio).
   - O **V5 Games** é o ecossistema independente de jogos. O streamer entra no V5 Games, escolhe/aluga o jogo, customiza sua partida e gera uma URL segura. Ele pode plugar essa URL no V5 Broadcaster OU usar seu próprio software de transmissão (OBS Studio, Streamlabs, TikTok Live Studio).
3. **Catálogo Multidivisional Expandido:**
   - **Cartuchos de Live Interativa (9:16 Vertical):** Jogos frenéticos para TikTok Live, YouTube Shorts e Twitch, pilotados 100% pelo chat e presentes.
   - **Jogos da Franquia Roxingo & Mobile:** Títulos autorais com o mascote oficial da Holding (ex: *Roxingo Runner*, *RoxingoQuest*).
   - **Jogos Idle / Web3 / RMT & Marketplace (Futuro):** Abertura para criadores terceiros publicarem cartuchos e monetizarem via revenue share.

---

## As 5 Leis Absolutas do Cartucho de Live V5

1. **Formato Vertical Estrito 9:16 (1080 x 1920 px):**
   - Todo jogo de live nasce com proporção vertical 9:16 (`aspect-ratio: 9/16` ou resolução 1080x1920).
   - Safe Zones respeitadas: topo (140px) para placar e doações; base (180px) livre para não sobrepor o feed do TikTok/YouTube.

2. **Zero Teclado / Zero Mouse na Live (Público é o Controle):**
   - O streamer não joga no teclado nem mexe mouse durante a transmissão.
   - O jogo é 100% pilotado pelo chat (`1`, `2`, `azul`, `laranja`) e **Presentes/Gifts** (Rosas, Moedas, Leão).
   - Presentes SEMPRE possuem peso massivo (5x a 50x) para forçar monetização na transmissão.

3. **Motor Anti-Silêncio (Simulação Autônoma Embutida):**
   - É terminantemente proibido um jogo ficar com tela estática esperando alguém comentar.
   - Se o chat ficar sem interação por 3 segundos, o motor autônomo injeta microações fictícias para manter a tela sempre em movimento frenético e instigar a audiência real a intervir.

4. **Sintetizador de Áudio Procedural (Web Audio API):**
   - NUNCA dependa de arquivos `.mp3` ou `.wav` externos que possam dar erro de CORS ou demorar no carregamento do OBS.
   - Todo efeito sonoro (apitos, impactos, moedas, aplausos, vitória) é sintetizado dinamicamente via `AudioContext`.

5. **Ciclo Fechado de Partidas & Auto-Reset:**
   - As partidas duram entre **30 e 60 segundos**.
   - Ao bater a meta da rodada: tela comemorativa com confetes e fanfarra por 5 segundos, seguido de **reinício 100% automático** sem precisar atualizar a página.

---

## O Protocolo de Eventos (V5 Live Event Bus)

Todo jogo de live deve importar e utilizar o `sdk/v5_live_game_sdk.js`, que escuta:
- `BroadcastChannel('v5_broadcaster_games')`
- Evento de janela `window.addEventListener('v5_event', (e) => ...)`
- Query params de configuração injetados pelo Streamer Cockpit (ex: `?token=...&teamA=Brasil&teamB=Argentina&giftWeight=10`)
- Botões de depuração locais no rodapé (visíveis no simulador e escondidos no OBS via CSS `@media (max-width...)` ou tecla `D`).

```javascript
// Payload Padronizado Recebido:
{
  type: "comment" | "gift" | "like",
  action: "push" | "boost" | "drop" | "vote",
  team: "A" | "B",
  user: "@nome_do_espectador",
  giftName: "Rose" | "Lion" | null,
  value: 10,
  comment: "1"
}
```

---

## Arquitetura de Entrega e Conexão com o Ecossistema
1. **Ambiente Próprio:** Reside em `V5_Apollo_Games`, servido autonomamente na porta `:3012` (ou domínio próprio em nuvem).
2. **Conexão com Broadcaster / OBS:** Todo cartucho é acessível via URL de Browser Source com parâmetros de customização:
   `http://localhost:3012/catalogo_jogos/<slug_do_jogo>/index.html?token=<streamer_token>`
3. **Vitrine & Cockpit:** O portal principal (`index.html`) provê o Catálogo Comercial, Simulador de Testes, Painel de Configuração do Streamer e Área da Franquia Roxingo.
