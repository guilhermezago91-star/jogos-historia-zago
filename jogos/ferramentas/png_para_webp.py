#!/usr/bin/env python3
"""Piratininga — troca as imagens PNG/JPEG embutidas por WebP SEM PERDA (v209, 21/11/2026).

O desenho fica pixel por pixel igual (o script confere cada imagem: se mudar 1 pixel,
ou se o WebP não ficar menor, a imagem original fica como estava).
Mexe em: jogos/piratininga.html e jogos/arte/arte_*.js (as fontes).
Depois de rodar, rode também: python3 jogos/ferramentas/abertura_rapida.py
Pode rodar de novo quantas vezes quiser (só converte o que ainda não é WebP).
"""
import base64, io, re, sys, pathlib
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[1]
ALVOS = [RAIZ / 'piratininga.html'] + sorted((RAIZ / 'arte').glob('arte_*.js'))
RX = re.compile(r'data:image/(png|jpeg);base64,([A-Za-z0-9+/=]+)')


def pixels(im):
    im.load()
    if im.mode == 'P' and 'transparency' in im.info:
        im = im.convert('RGBA')
    modo = 'RGBA' if ('A' in im.getbands() or im.mode in ('P', 'LA', 'PA')) else 'RGB'
    return im.convert(modo)


def converte(tipo, b64):
    bruto = base64.b64decode(b64)
    orig = pixels(Image.open(io.BytesIO(bruto)))
    buf = io.BytesIO()
    orig.save(buf, 'WEBP', lossless=True, quality=100, method=6, exact=True)
    novo = buf.getvalue()
    if len(novo) >= len(bruto):
        return None, 'maior'
    volta = Image.open(io.BytesIO(novo)).convert(orig.mode)
    if volta.size != orig.size or volta.tobytes() != orig.tobytes():
        return None, 'diferente'
    return 'data:image/webp;base64,' + base64.b64encode(novo).decode(), 'ok'


def main():
    total_antes = total_depois = 0
    for arq in ALVOS:
        s = arq.read_text(encoding='utf-8')
        cont = {'ok': 0, 'maior': 0, 'diferente': 0, 'erro': 0}
        antes = depois = 0

        def troca(m):
            nonlocal antes, depois
            try:
                r, st = converte(m.group(1), m.group(2))
            except Exception:
                cont['erro'] += 1
                return m.group(0)
            cont[st] += 1
            if r:
                antes += len(m.group(0)); depois += len(r)
                return r
            return m.group(0)

        s2 = RX.sub(troca, s)
        if s2 != s:
            arq.write_text(s2, encoding='utf-8')
        total_antes += antes; total_depois += depois
        print(f'{arq.name}: {cont["ok"]} trocadas ({antes//1024} KB -> {depois//1024} KB); '
              f'ficaram como estavam: {cont["maior"]} (WebP maior), {cont["diferente"]} (mudaria pixel), {cont["erro"]} (erro)')
    print(f'TOTAL: {total_antes//1024} KB -> {total_depois//1024} KB')


if __name__ == '__main__':
    sys.exit(main())
