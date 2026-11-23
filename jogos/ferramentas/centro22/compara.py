#!/usr/bin/env python3
# Compara duas fotos do centro (pastas geradas por foto.js). Lista tudo o que mudou.
# uso: python3 compara.py pastaA pastaB [--tudo]
import json, sys, os, collections
from PIL import Image, ImageChops

A, B = sys.argv[1], sys.argv[2]
TUDO = '--tudo' in sys.argv
da = json.load(open(os.path.join(A, 'dados.json')))
db = json.load(open(os.path.join(B, 'dados.json')))
IGN = {'__i', '__novo', '__drawIgual', '__cena0'}
MOVE = {'x', 'y', 'px', 'py', 'fx', 'fy', 'prog', 'wi', 'step', 'dir', 'wait', 'blocked', '__fr', 'moving', 'anim', '__dir', 'nextTurn', 'talked'}
out = []
def p(*a):
    out.append(' '.join(str(x) for x in a))

def limpa(o, ign=()):
    return {k: v for k, v in o.items() if k not in IGN and k not in ign}

def chave_obj(o):
    return (o.get('scene'), o.get('id'))

def compara_lista(nome, la, lb, chave, ign=(), so=None):
    ma = collections.defaultdict(list); mb = collections.defaultdict(list)
    for o in la:
        if so is None or so(o): ma[chave(o)].append(o)
    for o in lb:
        if so is None or so(o): mb[chave(o)].append(o)
    n = 0
    for k in sorted(set(ma) | set(mb), key=str):
        xa, xb = ma.get(k, []), mb.get(k, [])
        if len(xa) != len(xb):
            p(f'[{nome}] {k}: {len(xa)} em A, {len(xb)} em B'); n += 1; continue
        for a, b in zip(xa, xb):
            ca, cb = limpa(a, ign), limpa(b, ign)
            if ca != cb:
                dif = [kk for kk in set(ca) | set(cb) if ca.get(kk) != cb.get(kk)]
                p(f'[{nome}] {k}: campos diferentes: ' + ', '.join(f'{kk}: {str(ca.get(kk))[:80]} -> {str(cb.get(kk))[:80]}' for kk in sorted(dif)[:6])); n += 1
    return n

tot = {}
tot['mapa'] = sum(1 for y in range(max(len(da['mapa']), len(db['mapa']))) for x in range(150) if (da['mapa'][y][x:x+1] if y < len(da['mapa']) else '') != (db['mapa'][y][x:x+1] if y < len(db['mapa']) else ''))
if tot['mapa']:
    p('[mapa] quadradinhos diferentes:', tot['mapa'])
    k = 0
    for y in range(min(len(da['mapa']), len(db['mapa']))):
        for x in range(150):
            if da['mapa'][y][x] != db['mapa'][y][x] and k < 20:
                p(f'   ({x},{y}) {da["mapa"][y][x]} -> {db["mapa"][y][x]}'); k += 1
for k in ('cena', 'QT', 'Q', 'ROTEIRO4', 'GIVER', 'FONTES', 'cenas', 'INT', 'janela', 'minhas', 'placas22', 'plq22', 'ruaG', 'jmTeste'):
    if da.get(k) != db.get(k):
        tot[k] = 1
        a, b = da.get(k), db.get(k)
        if isinstance(a, list) and isinstance(b, list) and all(isinstance(x, str) for x in a + b):
            p(f'[{k}] só em A:', sorted(set(a) - set(b))[:20], ' só em B:', sorted(set(b) - set(a))[:20])
        elif isinstance(a, dict) and isinstance(b, dict):
            ks = [kk for kk in set(a) | set(b) if a.get(kk) != b.get(kk)]
            p(f'[{k}] chaves diferentes ({len(ks)}):', sorted(ks, key=str)[:15])
        else:
            p(f'[{k}] diferente', str(a)[:200], '|', str(b)[:200])
c22a, c22b = da.get('centro22') or {}, db.get('centro22') or {}
for k in sorted(set(c22a) | set(c22b)):
    if k in ('lotes', 'liga', 'M') and not TUDO: continue
    if c22a.get(k) != c22b.get(k): p('[centro22]', k, 'diferente'); tot['centro22'] = tot.get('centro22', 0) + 1
tot['objetos'] = compara_lista('objeto', da['objetos'], db['objetos'], chave_obj)
tot['npcs'] = compara_lista('pessoa', da['npcs'], db['npcs'], lambda n: n.get('id'), ign={'nextTurn','__ps','dir','__fr','__dir','talked','moving','anim'})
tot['itens'] = compara_lista('item', da['itens'], db['itens'], lambda n: n.get('id'))
# quem anda: só confere que existe e o caminho; posição pode variar
tot['walkers'] = compara_lista('anda', da['walkers'], db['walkers'], lambda n: n.get('id'), ign=MOVE)
if da['walkersPorCena'] != db['walkersPorCena']:
    p('[andam por cena]', {k: (da['walkersPorCena'].get(k), db['walkersPorCena'].get(k)) for k in set(da['walkersPorCena']) | set(db['walkersPorCena']) if da['walkersPorCena'].get(k) != db['walkersPorCena'].get(k)}); tot['walkersPorCena'] = 1
# imagens
for nome in ('chao.png', 'foto.png'):
    fa, fb = os.path.join(A, nome), os.path.join(B, nome)
    if not (os.path.exists(fa) and os.path.exists(fb)):
        p('[img]', nome, 'falta'); continue
    ia, ib = Image.open(fa).convert('RGBA'), Image.open(fb).convert('RGBA')
    if ia.size != ib.size:
        p('[img]', nome, 'tamanhos', ia.size, ib.size); tot[nome] = -1; continue
    d = ImageChops.difference(ia, ib)
    bb = d.getbbox(alpha_only=False)
    if bb:
        n = sum(1 for px in d.getdata() if px != (0, 0, 0, 0))
        p('[img]', nome, 'pixels diferentes:', n, 'na área', bb); tot[nome] = n
        d.convert('RGB').point(lambda v: 255 if v else 0).save(os.path.join(B, 'dif_' + nome))
    else:
        tot[nome] = 0
# desenhos dos objetos (por id)
sa = json.load(open(os.path.join(A, 'desenhos.json'))); sb = json.load(open(os.path.join(B, 'desenhos.json')))
ida = {da['objetos'][int(i)]['id']: v for i, v in sa.items()}; idb = {db['objetos'][int(i)]['id']: v for i, v in sb.items()}
nd = 0
for k in sorted(set(ida) | set(idb)):
    a, b = ida.get(k), idb.get(k)
    if a is None or b is None or a.get('kc', a.get('k')) != b.get('kc', b.get('k')) or a.get('ox') != b.get('ox') or a.get('oy') != b.get('oy'):
        if (a or {}).get('vivo') and (b or {}).get('vivo'): continue
        nd += 1
        if nd <= 25: p('[desenho]', k, (a or {}).get('k'), '->', (b or {}).get('k'))
tot['desenhos'] = nd
print('\n'.join(out if TUDO else out[:400]))
if len(out) > 400: print(f'... mais {len(out)-400} linhas')
print('RESUMO', json.dumps(tot))
