path = r'catalogo_jogos/21_batata_quente_explosiva/index.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Revert the first replacement in declarations
c = c.replace('let isGameOver = false;\n      passRank.clear();\n      topPasser = null;\n', 'let isGameOver = false;\n')

# Add to resetRound
target = 'function resetRound() {\n      totalRoundTime = 22.0 + Math.random() * 16.0; // 22 a 38 segundos\n      timeRemaining = totalRoundTime;\n      isGameOver = false;\n'
repl = 'function resetRound() {\n      totalRoundTime = 22.0 + Math.random() * 16.0; // 22 a 38 segundos\n      timeRemaining = totalRoundTime;\n      isGameOver = false;\n      passRank.clear();\n      topPasser = null;\n'

if target in c:
    c = c.replace(target, repl, 1)
    print("FIXED IN RESETROUND")
else:
    # Try with CRLF
    target_crlf = target.replace('\n', '\r\n')
    repl_crlf = repl.replace('\n', '\r\n')
    if target_crlf in c:
        c = c.replace(target_crlf, repl_crlf, 1)
        print("FIXED IN RESETROUND (CRLF)")
    else:
        print("TARGET STILL NOT FOUND")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
