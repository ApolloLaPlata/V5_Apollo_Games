#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import os
import re
import sys

if sys.stdout.encoding != 'utf-8':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

files = sorted(glob.glob('catalogo_jogos/*/index.html'))
for f in files:
    slug = os.path.basename(os.path.dirname(f))
    with open(f, 'r', encoding='utf-8') as fl:
        text = fl.read()

    # Find function names like handleEvent, processEvent, handleIncomingEvent, etc.
    fns = re.findall(r'function\s+(handle\w+|process\w+|onEvent)\s*\(', text)
    
    # Check how BroadcastChannel onmessage is wired
    bc_wire = re.findall(r'channel\.(?:onmessage|addEventListener\(\s*[\'"]message[\'"])\s*=\s*(?:function|\()?[^;{]*\{?\s*(?:const|let|var|if)?\s*([a-zA-Z0-9_\.]+)\s*\(', text)

    print(f"{slug}: handlers={fns} | bc_wire={bc_wire}")
