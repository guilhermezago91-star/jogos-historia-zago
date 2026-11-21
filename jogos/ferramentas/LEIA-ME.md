# Abertura rápida do Piratininga

O jogo baixa só os desenhos da época que a pessoa vai jogar. O resto chega depois, por trás.

## Para quem monta o jogo (qualquer conversa)

Depois de montar e copiar `piratininga.html` e os 5 arquivos `arte/arte_*.js`, e **antes de subir**:

```
python3 jogos/ferramentas/abertura_rapida.py
git add -A jogos
```

- Pode rodar quantas vezes quiser.
- Se esquecer, o jogo funciona do jeito antigo, só mais lento.
- Os 5 arquivos `arte/arte_*.js` continuam no repositório: são a entrada da ferramenta. O jogo usa os `arte/pac_*.js`.

## Como funciona

- `uso_arte.json` diz quais épocas usam cada imagem. Imagem nova, que não está no mapa, vai para o pacote geral (se veio do `arte_comum.js`) ou para o pacote da época do arquivo dela.
- Pacotes `pac_e1234.js`, `pac_e3.js`, `pac_e34.js`...: os números são as épocas que usam (1 = 1554, 2 = 1830, 3 = 1888, 4 = 1922).
- Pacotes `pac_depois_*.js`: imagens grandes que não são usadas na largada (fotos, anúncios). Chegam por trás.
- Ao trocar de época (botão de começar, portal, código), o jogo busca os pacotes que faltam, mostra uma tela de espera e recarrega a página já na época nova, sem perder o progresso.
- Com `#teste` no endereço o jogo carrega tudo, como antes. Para testar o modo rápido com `#teste`: `localStorage.setItem('pira_teste_rapido','1')`.

## Se uma imagem de outra época sumir

Um desenho novo de 1922 usado numa cena de 1830, por exemplo, precisa estar nos dois pacotes.
Abra `uso_arte.json`, ache a imagem e acrescente a época (`"e2"`). Rode a ferramenta de novo.

## Imagens em WebP sem perda (v209)

`python3 jogos/ferramentas/png_para_webp.py` troca as imagens PNG embutidas por WebP sem perda (desenho pixel por pixel igual, arquivo menor). Confere cada imagem; se mudaria um pixel ou ficaria maior, deixa como estava. Depois rode `abertura_rapida.py`.
