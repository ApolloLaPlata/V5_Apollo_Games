import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

# 1. Fix 26_guerra_dos_tanques_neon: floatingTexts cleanup and playPowderNoise volume guard
p26 = os.path.join(GAMES_DIR, "26_guerra_dos_tanques_neon", "index.html")
with open(p26, "r", encoding="utf-8") as f:
    c26 = f.read()

# Clear floatingTexts in resetMatch
old_reset26 = "state.shockwaves = [];"
new_reset26 = "state.shockwaves = [];\n      floatingTexts.length = 0;"
if old_reset26 in c26 and "floatingTexts.length = 0;" not in c26:
    c26 = c26.replace(old_reset26, new_reset26, 1)
    print("[FIXED] 26_guerra_dos_tanques_neon: floatingTexts.length = 0 adicionado em resetMatch()")

# Powder noise defaults and clamping
old_powder = "playPowderNoise(duration, volume) {"
new_powder = "playPowderNoise(duration = 0.25, volume = 0.4) {"
if old_powder in c26:
    c26 = c26.replace(old_powder, new_powder, 1)

old_gain26 = "gain.gain.setValueAtTime(volume, this.ctx.currentTime);"
new_gain26 = "gain.gain.setValueAtTime(Math.min(1.0, Math.max(0.01, volume || 0.4)), this.ctx.currentTime);"
if old_gain26 in c26:
    c26 = c26.replace(old_gain26, new_gain26, 1)
    print("[FIXED] 26_guerra_dos_tanques_neon: volume clamping e defaults adicionados a playPowderNoise()")

with open(p26, "w", encoding="utf-8") as f:
    f.write(c26)

# 2. Fix 27_meteoro_defensor: playNoise volume guard
p27 = os.path.join(GAMES_DIR, "27_meteoro_defensor", "index.html")
with open(p27, "r", encoding="utf-8") as f:
    c27 = f.read()

old_noise27 = "playNoise(duration, volume) {"
new_noise27 = "playNoise(duration = 0.3, volume = 0.5) {"
if old_noise27 in c27:
    c27 = c27.replace(old_noise27, new_noise27, 1)

old_gain27 = "gain.gain.setValueAtTime(volume, this.ctx.currentTime);"
new_gain27 = "gain.gain.setValueAtTime(Math.min(1.0, Math.max(0.01, volume || 0.5)), this.ctx.currentTime);"
if old_gain27 in c27:
    c27 = c27.replace(old_gain27, new_gain27, 1)
    print("[FIXED] 27_meteoro_defensor: volume clamping e defaults adicionados a playNoise()")

with open(p27, "w", encoding="utf-8") as f:
    f.write(c27)

print("Correções cirúrgicas da Rodada 3 concluídas!")
