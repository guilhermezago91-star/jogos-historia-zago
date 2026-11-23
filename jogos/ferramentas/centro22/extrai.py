#!/usr/bin/env python3
# Transforma a "foto" do centro (pasta de foto.js) nos dados do mapa fixo:
#   C22F_dados (JSON), C22F_chao (chão em WebP sem perda), C22F_a0.. (folhas de desenhos dos prédios).
# uso: python3 extrai.py <pasta_foto> <saida.json> [criar.json]
#   criar.json (opcional): {"obj":[ids],"npc":[ids],"it":[ids]} = o que o jogo não cria sozinho no modo fixo.
import json, sys, os, base64, io, re, hashlib
from PIL import Image

F, SAI = sys.argv[1], sys.argv[2]
CRIAR = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {"obj": [], "npc": [], "it": []}
K = 'm_centro22'
d = json.load(open(os.path.join(F, 'dados.json')))
spr = json.load(open(os.path.join(F, 'desenhos.json')))
avisos = []

IGN = {'__i', '__novo', '__cena0', '__drawIgual', 'draw'}
def ruim(v):
    if isinstance(v, str):
        return v.startswith('ƒ') or v.startswith('[img') or v in ('[ciclo]', '[fundo]') or v.startswith('[Map') or v.startswith('[Set') or (v.startswith('[') and ' ' in v and v.endswith(']') and v[1:2].isupper() and 'Array' in v)
    if isinstance(v, list): return any(ruim(x) for x in v)
    if isinstance(v, dict): return any(ruim(x) for x in v.values())
    return False
def campos(o, quem):
    r = {}
    for k, v in o.items():
        if k in IGN: continue
        if ruim(v):
            if not (isinstance(v, str) and v.startswith('ƒ')): avisos.append(f'{quem}: campo {k} não copiável: {str(v)[:60]}')
            continue
        r[k] = v
    return r

# ---------- objetos ----------
O = d['objetos']
idx_spr = {int(i): v for i, v in spr.items()}
usados = {}
obj = []
for o in O:
    if o.get('scene') != K and not o.get('__czOld'): continue
    i = o['__i']; s = idx_spr.get(i)
    criar = o['id'] in CRIAR['obj']
    if s is None: avisos.append('sem desenho: ' + o['id']); dsp = 'e'
    elif s.get('vazio'): dsp = 'e'
    elif o['__drawIgual'] is True and not criar: dsp = 'n'
    elif not o['__novo'] and o['__drawIgual'] is False: dsp = ['A', s['k'], s['ox'], s['oy']]
    elif o['__novo'] and not criar and o.get('__cena0') is None and o['id'] in CRIAR.get('nativos', []): dsp = 'n'
    else: dsp = ['A', s['k'], s['ox'], s['oy']]
    if isinstance(dsp, list): usados[s['k']] = 1
    if s and (s.get('vivo') or s.get('noite')) and dsp != 'n': avisos.append(f"desenho que muda com o tempo/noite vai parado: {o['id']} vivo={s.get('vivo')} noite={s.get('noite')}")
    obj.append({'id': o['id'], 's0': o.get('__cena0'), 'c': 1 if criar else 0, 'd': dsp, 'f': campos(o, o['id'])})
# originais do mapa dos bairros que a montagem escondeu
fora = []

# ---------- folhas de desenhos ----------
chaves = sorted(usados, key=lambda k: -Image.open(os.path.join(F, 'spr', k + '.png')).size[1])
LARG = 2048
folhas = []; pos = {}
x = y = alt = 0; cur = []
def fecha():
    global cur
    if cur: folhas.append(cur); cur = []
for k in chaves:
    im = Image.open(os.path.join(F, 'spr', k + '.png')).convert('RGBA')
    w, h = im.size
    if x + w > LARG: x = 0; y += alt; alt = 0
    if y + h > 2048: fecha(); x = y = alt = 0
    cur.append((k, x, y, im)); pos[k] = (len(folhas), x, y, w, h)
    x += w; alt = max(alt, h)
fecha()
saida_img = {}
for n, fl in enumerate(folhas):
    W = max(xx + im.size[0] for _, xx, _, im in fl); H = max(yy + im.size[1] for _, _, yy, im in fl)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for _, xx, yy, im in fl: sh.paste(im, (xx, yy))
    b = io.BytesIO(); sh.save(b, 'WEBP', lossless=True, quality=100, method=6, exact=True)
    volta = Image.open(io.BytesIO(b.getvalue())).convert('RGBA')
    if volta.tobytes() != sh.tobytes(): avisos.append(f'folha {n}: WebP mudou pixels!')
    saida_img['C22F_a%d' % n] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
for e in obj:
    if isinstance(e['d'], list):
        k = e['d'][1]; f, sx, sy, w, h = pos[k]
        e['d'] = [f, sx, sy, w, h, e['d'][2], e['d'][3]]
# ---------- folhas em resolução dobrada (modo HD do jogo) ----------
spr2 = json.load(open(os.path.join(F, 'desenhos2.json'))) if os.path.exists(os.path.join(F, 'desenhos2.json')) else {}
id2i = {o['id']: o['__i'] for o in O if o.get('scene') == K or o.get('__czOld')}
usados2 = {}
for e in obj:
    if isinstance(e['d'], list):
        s2 = spr2.get(str(id2i.get(e['id'])))
        if s2: usados2[s2['k']] = 1; e['d2'] = s2
        else: avisos.append('sem desenho HD: ' + e['id'])
ch2 = sorted(usados2, key=lambda k: -Image.open(os.path.join(F, 'spr2', k + '.png')).size[1])
LARG2 = 4096; folhas2 = []; pos2 = {}; x = y = alt = 0; cur = []
for k in ch2:
    im = Image.open(os.path.join(F, 'spr2', k + '.png')).convert('RGBA'); w, h = im.size
    if x + w > LARG2: x = 0; y += alt; alt = 0
    if y + h > 4096: folhas2.append(cur); cur = []; x = y = alt = 0
    cur.append((k, x, y, im)); pos2[k] = (len(folhas2), x, y, w, h); x += w; alt = max(alt, h)
if cur: folhas2.append(cur)
for n, fl in enumerate(folhas2):
    W = max(xx + im.size[0] for _, xx, _, im in fl); H = max(yy + im.size[1] for _, _, yy, im in fl)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for _, xx, yy, im in fl: sh.paste(im, (xx, yy))
    b = io.BytesIO(); sh.save(b, 'WEBP', lossless=True, quality=100, method=6, exact=True)
    if Image.open(io.BytesIO(b.getvalue())).convert('RGBA').tobytes() != sh.tobytes(): avisos.append(f'folha HD {n}: WebP mudou pixels!')
    saida_img['C22F_b%d' % n] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
for e in obj:
    s2 = e.pop('d2', None)
    if s2 and isinstance(e['d'], list):
        f, sx, sy, w, h = pos2[s2['k']]; e['d'] = e['d'] + [f, sx, sy, w, h, s2['ox'], s2['oy']]
# ---------- chão ----------
ch = Image.open(os.path.join(F, 'chao.png')).convert('RGBA')
b = io.BytesIO(); ch.save(b, 'WEBP', lossless=True, quality=100, method=6, exact=True)
if Image.open(io.BytesIO(b.getvalue())).convert('RGBA').tobytes() != ch.tobytes(): avisos.append('chão: WebP mudou pixels!')
saida_img['C22F_chao'] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

# ---------- pessoas, itens, quem anda ----------
npc = [{'id': n['id'], 'c': 1 if n['id'] in CRIAR['npc'] else 0, 'f': campos(n, 'npc ' + n['id'])} for n in d['npcs'] if n.get('scene') == K or n.get('__czOld') or n['id'] in CRIAR['npc'] or n['id'] in CRIAR.get('npcFixa', [])]
npcAlvo = {n['id'] for n in npc}
for n in d['npcs']:
    if n['id'] in CRIAR['npc'] and n['id'] not in npcAlvo: npc.append({'id': n['id'], 'c': 1, 'f': campos(n, 'npc ' + n['id'])})
it = [{'id': n['id'], 'c': 1 if n['id'] in CRIAR['it'] else 0, 'f': campos(n, 'item ' + n['id'])} for n in d['itens'] if n.get('scene') == K or n['id'] in CRIAR['it'] or (n.get('__cena0') is None and str(n.get('id', '')).startswith('jm22_'))]
wk = [campos(w, 'anda ' + w['id']) for w in d['walkers']]

c22 = d['centro22']
C = {k: c22[k] for k in ('X0', 'Y0', 'K', 'W', 'H', 'predios', 'placas', 'ruasNovas', 'movidos', 'saidas', 'liga', 'entradas') if k in c22}
C['P'] = []
dados = {
    'v': 1, 'mapa': d['mapa'], 'cena': {k: d['cena'][k] for k in ('label', 'title') if k in d['cena']}, 'C': C,
    'comp': d['comp'], 'placas22': d['placas22'], 'minhas': d['minhas'], 
    'glob': {k: v for k, v in d['glob'].items() if k in ('__mercRect22', '__semVale22', '__vale22', '__placasPequenas22', '__jmFundos22', '__jmPatio22', '__jmLimpa22', '__jmRua22', '__jmEnche22', '__jmJardim22', '__jmMarconi22', '__jmMerc22', '__jmSB22', '__jmMappin22', '__jmC3a22', '__jmC3b22', '__jmAbre')},
    
    'obj': obj, 'fora': fora, 'npc': npc, 'it': it, 'wk': wk,
    'fontes': {k: v for k, v in (d['fontesV'] or {}).items() if not ruim(v)}, 'fontesC': [k for k in CRIAR.get('fontes', [])],
    'cenaFlags': {k: v for k, v in d['cena'].items() if k.startswith('__') and not ruim(v)},
}
js = json.dumps(dados, ensure_ascii=False, separators=(',', ':'))
saida_img['C22F_dados'] = 'data:application/json;base64,' + base64.b64encode(js.encode('utf-8')).decode()
json.dump(saida_img, open(SAI, 'w'))
print('objetos', len(obj), 'criar', sum(e['c'] for e in obj), 'nativos', sum(1 for e in obj if e['d'] == 'n'), 'vazios', sum(1 for e in obj if e['d'] == 'e'), 'desenhos', len(usados), 'folhas', len(folhas))
print('pessoas', len(npc), 'itens', len(it), 'andam', len(wk), 'escondidos', len(fora), 'fontes', len(dados['fontes']))
print('tamanhos KB', {k: len(v) // 1024 for k, v in saida_img.items()})
for a in sorted(set(avisos))[:60]: print('AVISO', a)
