# Centro de 1922 como mapa fixo (v276)

O centro (`m_centro22`) vem pronto das chaves `C22F_*` no fim de `jogos/arte/arte_1922.js`:

- `C22F_dados`: mapa (quadradinhos), prédios e objetos (lugar, tamanho, nome, texto, porta, sala), pessoas, itens, quem anda, nomes de rua, saídas.
- `C22F_chao`: o chão do centro já desenhado.
- `C22F_a0`: desenhos dos prédios no tamanho normal. `C22F_b0`, `C22F_b1`...: os mesmos desenhos em tamanho dobrado (tela HD).

O bloco `v276 — CENTRO DE 1922 VIRA MAPA FIXO` do `piratininga.html` lê esses dados. Os blocos antigos do centro continuam no arquivo, mas só rodam com `window.__centroAntigo=true` (ou `#centroantigo` no endereço).

## Ferramentas desta pasta

- `hook.py`: faz uma cópia de teste do jogo com um "gancho" para os testes lerem o estado (nunca subir essa cópia).
- `foto.js`: abre o jogo com Playwright, espera tudo assentar e guarda a "foto" do centro (dados, chão, foto inteira, desenhos de cada prédio).
- `extrai.py`: transforma uma foto nas chaves `C22F_*`. `injeta.py`: põe as chaves no `arte_1922.js`.
- `compara.py`: compara duas fotos (antes e depois) e lista tudo o que mudou.
- `medir.js`: mede o tempo de entrada no centro e de volta de uma loja.

Para consertar o centro (Etapa 5): mexer direto nos dados de `C22F_dados`, uma coisa de cada vez, com peça de antes e depois, e rodar `abertura_rapida.py` antes de subir.
