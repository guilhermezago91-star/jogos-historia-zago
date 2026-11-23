#!/usr/bin/env python3
# Põe (ou troca) as chaves C22F_* no fim de jogos/arte/arte_1922.js, sem mexer no resto do arquivo.
import sys, json, re
arq, novo = sys.argv[1], sys.argv[2]
s = open(arq, encoding='utf-8').read()
N = json.load(open(novo))
# tira chaves C22F_ antigas
s = re.sub(r', "C22F_[A-Za-z0-9_]+": "[^"]*"', '', s)
fim = s.rstrip()
assert fim.endswith('};') or fim.endswith('}'), fim[-20:]
k = fim.rfind('}')
extra = ''.join(', ' + json.dumps(kk) + ': ' + json.dumps(v) for kk, v in N.items())
s = fim[:k] + extra + fim[k:] + ('\n' if s.endswith('\n') else '')
open(arq, 'w', encoding='utf-8').write(s)
print('ok', len(N), 'chaves')
