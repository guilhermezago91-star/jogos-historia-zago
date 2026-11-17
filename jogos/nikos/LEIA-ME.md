# Atenas, 415 a.C. — O dia de Nikos

Jogo 3D de História para o navegador.

## Como publicar
1. Suba esta pasta inteira para um repositório do GitHub (o `index.html` precisa ficar junto da pasta `modelos/`).
2. Publique pelo GitHub Pages ou pelo Vercel.
3. O jogo precisa de internet: o three.js e as fontes vêm de CDN.

Abrir o `index.html` direto do computador (com dois cliques) não carrega os modelos. Nesse caso, o jogo segue com as formas simples.

## Créditos dos modelos 3D
- Pessoas animadas: Universal Animation Library, de Quaternius (CC0), quaternius.com
- Comida do mercado: Food Kit, de Kenney (CC0), kenney.nl
- Barraca, cerâmica, biga, oliveiras e objetos: Greek & Roman, de Shuriken Studio, shuriken.studio
- Taças, bancos, braseiros, pithos e arbustos: Low Poly Greek Temple Pack, de reodesuxz
- Trirremes, doca do Pireu, ginásio, muralhas, torres, o portão do Dípilo, casas gregas, navio mercante, barcos de pesca, oficina do armeiro, caixotes, elmo, escudo e lança do hoplita, carrinho de mão, cestos e animais: 0 A.D., de Wildfire Games (wildfiregames.com), licença CC BY-SA 3.0. Os modelos foram convertidos para .glb e continuam sob a mesma licença (veja `modelos/0ad/LICENCA-0AD.txt`).
- Estátua de Atena dentro do Partenon: escaneamento 3D da Atena Varvakeion (Museu Arqueológico Nacional de Atenas), Scan-the-World (2026), Zenodo, https://doi.org/10.5281/zenodo.21375907, licença CC BY-NC-SA 4.0 (uso não comercial, com crédito; obras derivadas sob a mesma licença). A malha foi simplificada para o jogo (veja `modelos/estatuas/LICENCA-athena-varvakeion.txt`).

As licenças estão dentro de cada pasta em `modelos/`. Os pacotes da Shuriken e do reodesuxz permitem o uso em jogos, mas não permitem redistribuir os modelos soltos, como um pacote.

## Modo Missão: o Livro dos Deuses

Na tela inicial, o botão **Começar o Modo Missão** abre o capítulo 1, "Minha cidade". O avô de Nikos entrega um livro em branco, e Nikos encontra três deuses:

- **Héstia**, na cozinha de casa: recolher lenha, água e panela e acender o fogo.
- **Atena**, na Acrópole, no Partenon e no olival: o mito da oliveira, os três sinais da estátua, a colheita e o azeite.
- **Hermes**, nas hermas e no mercado: o mito da lira, três recados e as compras com óbolos.

Uma luz dourada e uma seta mostram o caminho, e o painel diz o que fazer. Se a estudante errar uma pergunta, recebe uma dica e tenta de novo, sem perder nada. No fim do capítulo aparecem os acertos de primeira tentativa. O Modo Missão guarda o progresso separado da exploração livre.

## Controles
- `W` e `S`: andar para a frente e para trás
- `A` e `D`: andar de lado
- Setas, `Q`/`E` ou arrastar o mouse: virar
- Rodinha do mouse ou botão 🎥: aproximar ou afastar a câmera
- `Shift`: correr; `E`: agir
- Botão de hora (☀️ Dia): troca entre amanhecer, dia, entardecer e noite
- No celular: círculo para andar e arrastar a tela para virar

O progresso é salvo sozinho no navegador. Na tela de abertura aparece "Continuar de onde parei".

- Mapa da Grécia (imagens/mapa-grecia.svg): desenhado para o jogo com contornos do Natural Earth (domínio público).
