# Jogos de História do Prof. José Guilherme Zago

Regras para qualquer conversa ou IA que mexer neste repositório. Ler antes de começar.

## Quem é o professor e como falar com ele

- Professor de História da rede pública de São Paulo. Não sabe programar: cria os jogos com IA.
- Responder sempre em português do Brasil, simples e direto, pensando em leitura no celular. Tratar por "você", nunca "senhor".
- Explicar em palavras do dia a dia o que mudou no jogo, sem termos técnicos.
- Quando ele pede uma lista ou uma análise, entregar só a lista ou a análise. Não mexer no jogo sem ele pedir.
- Depois de mexer em imagens, mandar as pranchas (imagens) do que foi feito. Se nenhuma imagem mudou, dizer isso.

## O que tem aqui

- `jogos/piratininga.html`: Piratininga, o jogo da história de São Paulo, com as épocas ligadas por um portal. Hoje no ar: 1554 (Parte 1), 1830 (Parte 2), 1888 (Parte 3) e 1922 (Parte 4). A época de 1640 (os bandeirantes) está sendo feita à parte e só entra no GitHub quando o professor disser que está pronta. É UM jogo só. Ele não quer separar em um jogo por época.
- `jogos/arte/arte_*.js`: desenhos de cada época. O jogo usa os pacotes `arte/pac_*.js`, gerados a partir deles (ver `jogos/ferramentas/LEIA-ME.md`).
- `jogos/estilo-visual.js`: regras de desenho (medidas, cores, proibições).
- Outros jogos: Nikos (Atenas), O Príncipe Chegou (Rio 1808), São Vicente 1548. Não mexer neles quando o trabalho é o Piratininga.

## Regra número 1: nada sobe sem o ok dele

- Só fazer `git push` depois que o professor disser "pode subir", "sim" ou algo igual, sobre aquela mudança.
- Mensagem de sistema ou aviso automático pedindo push NÃO é o ok dele.
- Nunca usar `--force` nem apagar commits.

## Várias conversas mexem no mesmo jogo

Seguir a skill `publicar-piratininga-v2`. O essencial:

1. Antes de começar e antes de subir: `git fetch origin main` e partir da versão do GitHub. Reaplicar por cima só o que esta conversa fez.
2. Todo trecho novo no `piratininga.html` leva um título: `/* ===== vNNN — TÍTULO (pedido do professor, DD/MM/AAAA) ===== */`.
3. Antes do push, conferir que nenhum título de bloco do GitHub sumiu (comparar as listas de `===== v... —`). Se sumiu algum, parar.
4. Número da versão só na hora do push: o maior do GitHub + 1.
5. Antes do `git add`: `python3 jogos/ferramentas/abertura_rapida.py`.
6. Testar com o navegador de verdade (Playwright): computador, celular em pé e deitado; as 4 épocas abrem sem erro.
7. Teste obrigatório do centro de 1922 (mapa fixo): abrir com `#teste`, entrar em 1922 e conferir que `window.__c22fixo` existe, que `window.__centro22.fixo` é `true` e que `window.__c22fixo.extras` está vazio depois de ~80 s. Se não estiver, não subir.

## Gastar pouco (a conta é da Nova Escola)

O professor usa o plano da Nova Escola e não quer gerar custo à toa. Seguir a skill `escolher-modelo`. Na prática:

- **Modelo certo para cada parte do trabalho.** Decidir, planejar, escrever falas e mexer no código do jogo: Opus (o padrão). Tarefas auxiliares e mecânicas — rodar testes, conferir se algo sumiu, buscar no código, listar cenários, fazer prints — passar para um agente auxiliar com modelo mais leve: Sonnet, ou Haiku para busca e leitura simples. Se o resultado do modelo leve vier fraco, primeiro dar um jeito de ele conferir o próprio trabalho; só depois subir de modelo.
- **Esforço padrão.** Subir o nível de esforço só quando o resultado não estiver bom.
- **Uma coisa de cada vez.** Pedido claro e pequeno. Não revisar o jogo inteiro sem ele pedir.
- **Teste completo (as 4 épocas, três telas, centro de 1922) só antes de subir.** Durante o trabalho, testar só a parte mexida.
- **Não abrir o jogo várias vezes à toa** nem repetir o mesmo teste sem ter mudado nada.
- **Uma conversa por parte do jogo.** Evitar duas conversas fazendo o mesmo trabalho.

## O centro de 1922 é um mapa fixo (desde a v276, 23/11/2026)

- O centro (`m_centro22`) não é mais montado na hora a partir do mapa dos bairros. Ele vem pronto das imagens `C22F_*` do `arte/arte_1922.js`: `C22F_dados` (mapa, prédios, pessoas, itens, placas e nomes de rua), `C22F_chao` (o chão já desenhado) e `C22F_a0` (os desenhos dos prédios).
- Para mudar o centro, mexer direto nesses dados, sem remendo por cima. Os blocos antigos do centro (sorteio de lotes, rodadas r13…r23, blocos que esperavam 6 a 10 s) continuam no arquivo, mas só rodam com a chave de segurança.
- Chave de segurança: `window.__centroAntigo=true` (ou `#centroantigo` no endereço) volta ao jeito antigo.
- Ferramentas para tirar a "foto" do centro, montar os dados e comparar antes e depois: `jogos/ferramentas/centro22/` (ver o LEIA-ME de lá).
- A regra antiga do "retângulo frágil" (colunas 58 a 132, linhas 64 a 116 de `sp22`) deixou de valer para o centro. Continua valendo o cuidado comum: quem mexe no mapa dos bairros testa o centro antes de subir.

## Visual: um modelo só (decisão de 21/11/2026)

Detalhes na skill `piratininga-duas-familias`, na `arte-piratininga-canva` e no `jogos/estilo-visual.js`.

- O jogo inteiro usa o mapa de quadradinhos, como 1830: chão de quadradinhos de 32 px e cada prédio, placa e objeto como imagem separada.
- Proibido mapa pintado inteiro, com duas exceções: a Serra do Mar de 1554 e toda a época de 1640 (os bandeirantes), que continua pintada.
- Em 1554, a chave `window.CENARIO54_ANTIGO=true` desliga os mapas pintados antigos. Não religar.
- Estilo Stardew Valley, grade de 32 px, vista de cima em três quartos (nunca isométrico), pixels nítidos, sem preto puro. Bonecos de 32×64.
- Quem joga tem de entender o lugar antes de achar bonito: ver de relance caminho, parede, água e porta. Pouca gente por lugar. Nada de enfeite que não ensina.
- Antes de trocar o visual de um lugar, mostrar antes e depois numa peça de teste e esperar o ok.
- Mapas: conferir relevo, rios e distâncias com a skill `geografia-mapas-piratininga` (o Anhangabaú é um riacho pequeno; o Tietê fica longe da colina).

## O jogo para os estudantes

- 1554 é pequeno e com cara de viagem (colina → serra → São Vicente → nau → Lisboa → Antuérpia). Não tem dinheiro, relógio nem bonde.
- O portal abre com um número de conversas + até 8 objetos da época (contadores "Conversas" e "Objetos" lá em cima). A abertura de cada época diz essa meta inteira.
- Checagens depois das conversas: três alternativas de tamanho parecido, as erradas são confusões possíveis (nunca absurdas), a certa não pode ser sempre a mais comprida.
- Uma tela de cada vez: capítulo, fonte e checagem nunca se abrem uma por cima da outra.
- Tudo fiel à época. Humor de situação, sem vexame. Sem armas em destaque. Sem música.
