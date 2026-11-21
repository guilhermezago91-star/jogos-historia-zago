/* =====================================================================
   PIRATININGA – ESTILO VISUAL OFICIAL
   Referência única: STARDEW VALLEY, desenhado direto na grade de 32 px
   ---------------------------------------------------------------------
   Este arquivo é a "lei" do visual do jogo. Vale para todas as épocas
   (1554, 1640, 1830, 1888, 1922), para todas as conversas e para qualquer IA
   ou ferramenta (Claude, Canva, geradores/oficinas).
   Ele diz o mesmo que a skill "arte-piratininga-canva".

   REGRA DE OURO: se não respeita o jeito de desenhar do Stardew Valley
   E a realidade histórica de São Paulo, não entra em Piratininga.
   O Stardew decide COMO se desenha. A documentação histórica decide
   O QUE se desenha. Quando as duas brigam, a história ganha.

   PRANCHAS DE REFERÊNCIA: todo tipo de peça nova (boneco, prédio, mata,
   encosta...) tem primeiro uma prancha de teste aprovada pelo professor.
   As peças seguintes são feitas a partir dela.

   UM MODELO SÓ (decisão do professor, 21/11/2026): o jogo inteiro, de 1554 a
   1922, usa o mapa montado por quadradinhos, como 1830. Mapa pintado inteiro
   é proibido (um estudante mostrou que ficava poluído e não dava para ver onde
   se anda). Única exceção: a Serra do Mar de 1554. Ver "modelo" logo abaixo.

   O conferidor no fim do arquivo só mede tamanho e preto puro. Passar
   nele NÃO quer dizer que o desenho está aprovado.

   Zelda: A Link to the Past e Chrono Trigger servem só como CONSULTA
   para resolver um problema específico (encosta alta, quarteirão).
   O resultado é sempre redesenhado no jeito Stardew.
   ===================================================================== */

const ESTILO = {
  referencia: "Stardew Valley, em pixel art nativa na grade de 32 px",
  // "nativa": o desenho já nasce em 32 px, com detalhe de verdade.
  // Nunca desenhar pequeno (16 px) e ampliar: isso não acrescenta detalhe.
  consultaSecundaria: ["Zelda: A Link to the Past", "Chrono Trigger"],
  descartados: ["Ninja Adventure", "pastel estilo Pokémon/GBA", "gráfico desenhado por código"],

  /* ---------- UM MODELO SÓ ---------- */
  modelo: {
    epocas: [1554, 1640, 1830, 1888, 1922],
    chao: "mapa montado por quadradinhos (tiles) de 32 px que se repetem; cada prédio, veículo, placa e objeto é um PNG separado",
    proibido: "mapa pintado inteiro (um desenho único com chão e prédios dentro), em qualquer época",
    excecao: "Serra do Mar de 1554 (SERRA54_MAPA), que fica como está",
    leitura: [
      "leitura antes de beleza: caminho, parede, água e porta têm de se ver de relance",
      "o que não se atravessa tem de parecer que não se atravessa",
      "pouca gente e poucos objetos por lugar; sem enfeite que não ensina nada",
      "antes de trocar o visual de um lugar inteiro, mostrar ao professor antes e depois, lado a lado"
    ],
    chave1554: "no piratininga.html, window.CENARIO54_ANTIGO=true desliga os mapas pintados de 1554 (v161, v194, v196, v197, v205); não religar",
    cuidado: "o centro de 1922 é sorteado a partir do mapa dos bairros (colunas 58-132, linhas 64-116 de sp22): não mexer sem avisar"
  },

  /* ---------- TAMANHOS (em pixels, sem escala) ---------- */
  tile: 32,                                 // 1 quadradinho do jogo = 32 px
  boneco: { largura: 32, altura: 64 },      // quadro do boneco andando
  folhaBoneco: { largura: 512, altura: 64,  // 16 quadros em uma linha
                 ordem: "frente 0-3, costas 4-7, esquerda 8-11, direita 12-15" },
  // altura do corpo DENTRO do quadro de 32x64 (pés sempre na linha de baixo)
  bonecoAltura: {
    adulto:  { min: 56, max: 64 },          // alturas variadas, ninguém gigante
    jovem:   { min: 48, max: 56 },
    crianca: { min: 40, max: 48 }
  },
  animal: { grande: { largura: 40, altura: 32 }, // cavalo, mula, burro
            pequeno: { largura: 16, altura: 16 } }, // pombo, galinha
  retratoFala: { largura: 85, altura: 78 }, // tamanho próprio, fora da grade
  veiculo: "tamanho livre (não precisa bater na grade); 4 PNGs: frente, costas, esquerda, direita",
  vista: "de cima em três quartos (vê o topo e a fachada), nunca isométrico",

  /* ---------- LUZ E SOMBRA ---------- */
  luz: "vem de cima e da esquerda",
  sombra: "para baixo e para a direita, oval suave embaixo de bonecos e objetos",

  /* ---------- CONTORNO ---------- */
  contorno: "escuro da própria cor do objeto; nunca preto puro (#000)",

  /* ---------- CORES ----------
     Cores quentes e médias. Nem pastel, nem neon.
     Paleta-base, comum às quatro épocas. Cada época soma a sua
     paleta própria (paletaPorEpoca, logo abaixo). */
  paleta: {
    contornoGeral: "#2b1d16",
    terraEscura:   "#5c3a21",
    terra:         "#8a5a33",
    terraClara:    "#c08a52",
    pedraEscura:   "#4f4a45",
    pedra:         "#8a8178",
    pedraClara:    "#c2b8a8",
    matoEscuro:    "#2f4d22",
    mato:          "#4f7a2c",
    matoClaro:     "#8db44a",
    aguaFunda:     "#24507a",
    agua:          "#3f7fb0",
    aguaRasa:      "#7fb8d6",
    telha:         "#a8502e",
    telhaClara:    "#d07a4a",
    cal:           "#e8dcc0",   // parede caiada
    madeira:       "#6e4428",
    pele1: "#5a3420", pele2: "#8a5636", pele3: "#c08a62", pele4: "#e6b896"
  },

  /* ---------- CORES DE CADA ÉPOCA (somam à paleta-base) ---------- */
  paletaPorEpoca: {
    1554: { tema: "terra, Mata Atlântica, madeira e palha",
            palha: "#c9a85a", palhaEscura: "#96783a", mataFunda: "#1f3a24",
            mataClara: "#5f9440", barro: "#9a5f3c", troncoUmido: "#4a3324" },
    1830: { tema: "taipa, cal, telha e rua de terra",
            taipa: "#b08a62", calSuja: "#d6c8a8", telhaVelha: "#8f4a30",
            ruaDeTerra: "#a57c52", madeiraPintada: "#3f6a5a", pedraDeCantaria: "#9c9488" },
    1888: { tema: "tijolo, ferro, café e cidade crescendo",
            tijolo: "#a04a34", tijoloClaro: "#c46a4a", ferro: "#3d4347",
            cafe: "#5a2f22", folhaDeCafe: "#3d6b33", paralelepipedo: "#7d766d" },
    1922: { tema: "arquitetura eclética, asfalto e fábrica",
            reboco: "#d8cdb4", rebocoOcre: "#c9a868", asfalto: "#4a4a4e",
            fuligem: "#5e554e", ferroPintado: "#2f4a44", tijoloDeFabrica: "#8f4534" }
  },

  /* ---------- O QUE É PROIBIDO ---------- */
  proibido: [
    "arte esticada ou ampliada em tamanho quebrado (só por número inteiro)",
    "pixel borrado (sempre pixels nítidos, sem suavizar)",
    "preto puro no contorno",
    "vista isométrica",
    "piso de uma cor só com borda quadrada (transições irregulares)",
    "prédio pequeno demais perto do boneco (casinha de boneca)",
    "excesso de telhado marrom de cenário",
    "objeto fora da época",
    "letra de pixel pequena demais para ler no celular",
    "texto, moldura ou chão desenhado dentro da imagem",
    "mapa pintado inteiro (só a Serra do Mar de 1554 fica como está)"
  ],

  /* ---------- PROIBIDO SÓ EM UMA ÉPOCA ----------
     Em 1554 e 1830 a cidade TEM mato, quintal e terreno vazio:
     a documentação histórica manda. */
  proibidoPorEpoca: {
    1922: [
      "lote vazio ou mato no centro da cidade",
      "grama fora dos parques no centro"
    ]
  },

  /* ---------- ARQUIVOS ---------- */
  arquivo: "PNG com fundo transparente, tamanho final reduzido (sem metadados)"
};

/* =====================================================================
   CONFERIR UMA IMAGEM
   Uso no jogo: conferirImagem(img, tipo)
   tipo: "boneco", "folhaBoneco", "retrato", "animalGrande",
         "animalPequeno", "veiculo" ou "tile" (prédios, pisos, objetos)
   Mostra no console o que está fora do padrão. Nunca trava o jogo.
   ===================================================================== */
function conferirImagem(img, tipo) {
  const problemas = [];
  const w = img.naturalWidth || img.width, h = img.naturalHeight || img.height;
  const E = ESTILO;

  const exato = (L, A, nome) => {
    if (w !== L || h !== A) problemas.push(`${nome} precisa ter ${L}x${A} (está ${w}x${h})`);
  };
  const multiplo = (L, A, nome) => {
    if (w % L !== 0 || h % A !== 0) problemas.push(`${nome} precisa de quadros de ${L}x${A} (está ${w}x${h})`);
  };

  switch (tipo) {
    case "retrato":       exato(E.retratoFala.largura, E.retratoFala.altura, "retrato"); break;
    case "folhaBoneco":   exato(E.folhaBoneco.largura, E.folhaBoneco.altura, "folha do boneco"); break;
    case "boneco":        multiplo(E.boneco.largura, E.boneco.altura, "boneco"); break;
    case "animalGrande":  multiplo(E.animal.grande.largura, E.animal.grande.altura, "animal grande"); break;
    case "animalPequeno": multiplo(E.animal.pequeno.largura, E.animal.pequeno.altura, "animal pequeno"); break;
    case "veiculo":       break; // tamanho livre: só confere o preto puro
    default:              multiplo(E.tile, E.tile, "peça");
  }

  // procura preto puro (se o navegador bloquear a leitura, só avisa)
  try {
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    const ctx = c.getContext("2d");
    ctx.drawImage(img, 0, 0);
    const px = ctx.getImageData(0, 0, w, h).data;
    for (let i = 0; i < px.length; i += 4) {
      if (px[i + 3] > 0 && px[i] === 0 && px[i + 1] === 0 && px[i + 2] === 0) {
        problemas.push("tem preto puro (#000) – trocar por contorno escuro da cor");
        break;
      }
    }
  } catch (e) {
    console.info(`[estilo] não deu para ler as cores de ${img.src} (imagem de outro endereço)`);
  }

  if (problemas.length) console.warn(`[estilo] ${img.src}:`, problemas);
  return problemas;
}

/* Desenho sempre nítido, sem borrar */
function prepararTela(ctx) {
  ctx.imageSmoothingEnabled = false;
}

/* =====================================================================
   TEXTO PARA COLAR EM QUALQUER IA OU NO CANVA
   (trocar o ano pela época da peça: 1554, 1830, 1888 ou 1922)
   ===================================================================== */
const PEDIDO_PADRAO = `
Pixel art no estilo de Stardew Valley, desenhada direto na grade de 32 px
(não ampliar desenho pequeno), vista de cima em três quartos, nunca
isométrico. Personagens em quadros de 32x64 px. Pixels nítidos, sem borrar.
Contorno escuro da própria cor, nunca preto puro. Luz vindo de cima e da
esquerda. Cores quentes e médias, nem pastel nem neon. PNG com fundo
transparente, sem chão, moldura ou texto. São Paulo, [ANO]: tudo fiel à
época (arquitetura, roupa, veículos, plantas brasileiras), sem objetos
modernos. Prédios grandes em proporção aos personagens.
`.trim();

if (typeof module !== "undefined") module.exports = { ESTILO, conferirImagem, prepararTela, PEDIDO_PADRAO };
