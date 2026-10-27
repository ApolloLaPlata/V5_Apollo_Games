# V5 Games — Estúdio de Fabricação de Cartuchos de Live Interativa 9:16

Este repositório é a fábrica oficial de **Jogos Interativos de Transmissão (Stream Games)** do ecossistema V5 Apollo Holding.

Os jogos forjados aqui são consumidos e hospedados diretamente pelo **V5 Apollo Broadcaster** (`V5_Apollo_Broadcaster`), servindo como as fontes de navegador (Browser Sources) de transmissões 24/7 no TikTok Live, YouTube Shorts e Twitch.

## Estrutura do Projeto
- `sdk/v5_live_game_sdk.js`: SDK padronizado de escuta de eventos da live (`comment`, `gift`, `like`).
- `src/audio/v5_synth_audio.js`: Sintetizador de efeitos sonoros procedurais via Web Audio API (sem arquivos MP3 externos).
- `catalogo_jogos/`: Todos os cartuchos individuais finalizados e em produção.
- `scripts/sync_to_broadcaster.py`: Script de sincronização automática para a pasta pública do Broadcaster.

## Como Executar e Testar Localmente
Basta abrir qualquer `index.html` de um jogo no navegador ou iniciar um servidor local estático:
```bash
python -m http.server 3012
```
Acesse `http://localhost:3012/catalogo_jogos/01_cabo_de_guerra_neon/` para testar no formato 1080x1920.
