import os
import re

GAMES_DIR = r"E:\MEUS PROGRAMAS\V5_APOLLO_SITES\V5_Apollo_Games\catalogo_jogos"

def scan_bugs_round_8():
    findings = []
    for g in sorted(os.listdir(GAMES_DIR)):
        index_file = os.path.join(GAMES_DIR, g, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Check for Event Deduplication
        # Does the cartridge have deduplication for payload.id or payload.eventId?
        has_dedup = "processedEventIds" in content or "recentEventIds" in content or "seenEvents" in content or "lastEventId" in content
        if not has_dedup:
            findings.append((g, "DEDUP_MISSING", "Sem cache de desduplicação contra eventos redundantes em múltiplos barramentos"))

        # 2. Check for integer parsing on votes/actions (e.g. parseInt without radix)
        parse_ints = re.finditer(r'parseInt\s*\(\s*([^,\)]+)\s*\)', content)
        for m in parse_ints:
            arg = m.group(1).strip()
            findings.append((g, "PARSEINT_NO_RADIX", f"parseInt({arg}) sem radix 10 explícito"))

        # 3. Check for Math.round / Math.floor on canvas coordinates for crisp pixel rendering
        # High subpixel rendering can cause fuzzy edges on fonts and borders
        if "ctx.imageSmoothingEnabled" not in content and "<canvas" in content:
            # check if pixelated or image smoothing
            pass

        # 4. Check for unhandled exceptions in JSON.parse inside postMessage
        # Is JSON.parse always inside try/catch?
        raw_json_parses = re.finditer(r'JSON\.parse\s*\([^)]+\)', content)
        for m in raw_json_parses:
            pos = m.start()
            nearby = content[max(0, pos-100):min(len(content), pos+100)]
            if "try" not in nearby:
                findings.append((g, "RAW_JSON_PARSE", f"JSON.parse fora de try/catch próximo a: {nearby[:40]}"))

    print(f"Total de potenciais achados (Rodada 8): {len(findings)}")
    # group by category
    cats = {}
    for g, cat, desc in findings:
        cats[cat] = cats.get(cat, 0) + 1
    for cat, count in cats.items():
        print(f" - {cat}: {count} ocorrências")

    return findings

if __name__ == "__main__":
    scan_bugs_round_8()
