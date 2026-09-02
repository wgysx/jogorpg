/*
 * game.js
 * --------
 * Versão para navegador de "A Última Chama de Eldareth".
 *
 * Segue a mesma arquitetura do jogo em Python (main.py / scenes.py):
 * cada cena é uma função independente que recebe o estado do jogador,
 * narra o que acontece e devolve o nome da próxima cena. Aqui, em vez
 * de retornar uma string consumida por um laço `while`, cada função
 * chama diretamente a próxima (o equivalente, no navegador, a um
 * roteador de cenas por botões de escolha).
 */

/* ---------------------- estado do jogador ---------------------- */
const jogador = {
  nome: "",
  vida: 100,
  coragem: 0,
  sabedoria: 0,
  inventario: [],
};

const DESCRICOES_ITENS = {
  "lanterna de vaga-lume": "Uma pequena lanterna de vidro com um vaga-lume eterno preso dentro. Nunca se apaga.",
  "amuleto da anciã": "Um amuleto de osso e prata, gasto pelo tempo. Dizem que afasta o medo de quem o carrega.",
  "adaga enferrujada": "Uma adaga simples, com o cabo gasto de tanto uso. Melhor que lutar de mãos vazias.",
  "essência do rio": "Um frasco com água que brilha sob a luz da lua, colhida no Rio Encantado.",
  "pergaminho do feiticeiro": "Um pergaminho com símbolos antigos, escrito pelo Feiticeiro da Torre.",
  "fragmento de cristal": "Um fragmento afiado e translúcido, retirado do coração da Caverna de Cristal.",
  "chama de Eldareth": "A lendária Última Chama. Pequena, mas quente como mil sóis.",
};

function adicionarItem(item) {
  if (!jogador.inventario.includes(item)) jogador.inventario.push(item);
}
function temItem(item) {
  return jogador.inventario.includes(item);
}
function alterarVida(valor) {
  jogador.vida = Math.max(0, Math.min(100, jogador.vida + valor));
}
function ganharCoragem(v = 1) { jogador.coragem += v; }
function ganharSabedoria(v = 1) { jogador.sabedoria += v; }
function estaVivo() { return jogador.vida > 0; }

/* ---------------------- renderização ---------------------- */
const elTexto = document.getElementById("texto-cena");
const elEscolhas = document.getElementById("area-escolhas");
const elBarraVida = document.getElementById("barra-vida");
const elCoragem = document.getElementById("valor-coragem");
const elSabedoria = document.getElementById("valor-sabedoria");
const elItens = document.getElementById("valor-itens");

function atualizarHud() {
  elBarraVida.style.width = jogador.vida + "%";
  elCoragem.textContent = jogador.coragem;
  elSabedoria.textContent = jogador.sabedoria;
  elItens.textContent = jogador.inventario.length ? jogador.inventario.join(", ") : "nenhum";
}

/**
 * Renderiza uma cena: uma lista de parágrafos e uma lista de escolhas.
 * @param {string[]} paragrafos
 * @param {{texto:string, aoClicar:Function}[]} escolhas
 * @param {string|null} rotulo - selo opcional (usado nos finais)
 */
function renderCena(paragrafos, escolhas, rotulo = null) {
  atualizarHud();
  elTexto.innerHTML =
    (rotulo ? `<span class="rotulo-final">${rotulo}</span>` : "") +
    paragrafos.map((p) => `<p>${p}</p>`).join("");
  elEscolhas.innerHTML = "";

  if (!escolhas || escolhas.length === 0) return;

  escolhas.forEach((op) => {
    const botao = document.createElement("button");
    botao.className = "botao-escolha";
    botao.textContent = op.texto;
    botao.addEventListener("click", op.aoClicar);
    elEscolhas.appendChild(botao);
  });

  elTexto.scrollIntoView({ behavior: "smooth", block: "start" });
}

function itemComDestaque(item) {
  const descricao = DESCRICOES_ITENS[item] || "";
  return `<br><span class="destaque">Você obteve: ${item}. "${descricao}"</span>`;
}

/* ------------------------------------------------------------------ */
/*  TELA INICIAL                                                       */
/* ------------------------------------------------------------------ */
function telaInicial() {
  elEscolhas.innerHTML = "";
  elTexto.innerHTML = `
    <p>Há sete invernos o sol não aquece mais o vale de Eldareth. A neve
    cobre os telhados até as portas e as colheitas apodrecem sob o gelo.
    Diz a lenda que uma Chama viva, guardada nas profundezas do vale, é
    a única coisa capaz de devolver o calor à terra.</p>
    <p>Você é o único viajante disposto a atravessar o vale amaldiçoado
    para encontrá-la. Antes de partir, diga ao velho guarda do portão
    como deseja ser chamado.</p>
  `;
  const form = document.createElement("div");
  form.className = "campo-nome";
  form.innerHTML = `
    <input type="text" id="input-nome" placeholder="Nome do seu personagem" maxlength="24" />
    <button class="botao-primario" id="botao-comecar">Iniciar jornada</button>
  `;
  elEscolhas.appendChild(form);

  const iniciar = () => {
    const valor = document.getElementById("input-nome").value.trim();
    jogador.nome = valor || "Viajante";
    introducao();
  };
  document.getElementById("botao-comecar").addEventListener("click", iniciar);
  document.getElementById("input-nome").addEventListener("keydown", (e) => {
    if (e.key === "Enter") iniciar();
  });
}

/* ------------------------------------------------------------------ */
/*  CENAS                                                               */
/* ------------------------------------------------------------------ */
function introducao() {
  renderCena(
    [
      `${jogador.nome}, o velho guarda estende um mapa gasto sobre a mesa
       e aponta dois caminhos possíveis.`,
    ],
    [
      { texto: "Seguir a Estrada do Mercador — mais longa, porém mais segura", aoClicar: estradaDoMercador },
      { texto: "Cortar caminho pela Floresta Sombria — um atalho perigoso", aoClicar: florestaSombria },
    ]
  );
}

function estradaDoMercador() {
  renderCena(
    [
      `A estrada é longa, mas segura. Ao entardecer, você encontra Bilo,
       um mercador de carroça quebrada, tentando consertar uma roda
       presa no gelo. Em troca de ajuda, ele oferece um presente de sua
       bagagem.`,
    ],
    [
      {
        texto: "Aceitar a lanterna de vaga-lume",
        aoClicar: () => {
          adicionarItem("lanterna de vaga-lume");
          renderCena(
            [
              `Bilo entrega a lanterna. "Ela nunca se apaga", ele diz.${itemComDestaque("lanterna de vaga-lume")}`,
              `"A vila de Cinza-Alta fica logo depois daquela colina", ele avisa. "Cuidado — dizem que lá só restaram cinzas e memórias."`,
            ],
            [{ texto: "Seguir para Cinza-Alta", aoClicar: vilaAbandonada }]
          );
        },
      },
      {
        texto: "Aceitar a adaga enferrujada",
        aoClicar: () => {
          adicionarItem("adaga enferrujada");
          renderCena(
            [
              `Bilo entrega a adaga. "Ainda corta", ele garante.${itemComDestaque("adaga enferrujada")}`,
              `"A vila de Cinza-Alta fica logo depois daquela colina", ele avisa. "Cuidado — dizem que lá só restaram cinzas e memórias."`,
            ],
            [{ texto: "Seguir para Cinza-Alta", aoClicar: vilaAbandonada }]
          );
        },
      },
    ]
  );
}

function florestaSombria() {
  renderCena(
    [
      `As árvores da Floresta Sombria não têm folhas há anos. Um rosnado
       corta o silêncio: é Uivante, o último lobo do vale, magro e
       faminto, bloqueando o caminho.`,
    ],
    [
      {
        texto: "Enfrentar o lobo de frente",
        aoClicar: () => {
          ganharCoragem(1);
          let texto;
          if (temItem("adaga enferrujada")) {
            texto = `Você saca a adaga de Bilo. A lâmina enferrujada ainda corta o
              suficiente para afastar o animal, que foge mancando entre as árvores.`;
            alterarVida(-8);
          } else {
            texto = `Sem arma alguma, você luta com as próprias mãos. O lobo crava
              os dentes em seu braço antes de finalmente recuar, ganindo de dor.
              O ferimento é sério.`;
            alterarVida(-55);
          }
          if (!estaVivo()) return finalTragico();
          renderCena([texto, `Mais à frente, a floresta se abre e você avista os
              telhados cobertos de cinzas de uma vila.`],
            [{ texto: "Seguir em frente", aoClicar: vilaAbandonada }]
          );
        },
      },
      {
        texto: "Ficar imóvel e observar",
        aoClicar: () => {
          ganharSabedoria(1);
          renderCena(
            [
              `Você prende a respiração e não se move um centímetro. Uivante
               fareja o ar, hesita, e por fim se afasta.`,
              `Mais à frente, a floresta se abre e você avista os telhados
               cobertos de cinzas de uma vila.`,
            ],
            [{ texto: "Seguir em frente", aoClicar: vilaAbandonada }]
          );
        },
      },
    ]
  );
}

function vilaAbandonada() {
  renderCena(
    [
      `Cinza-Alta já foi um vilarejo próspero. Agora, apenas casas vazias
       e um silêncio pesado. Numa das poucas casas com fumaça saindo da
       chaminé, uma anciã chamada Ovena tenta, sozinha, empilhar lenha
       para sobreviver mais uma noite.`,
    ],
    [
      {
        texto: "Parar e ajudá-la a carregar a lenha",
        aoClicar: () => {
          ganharSabedoria(1);
          adicionarItem("amuleto da anciã");
          renderCena(
            [
              `Vocês trabalham em silêncio até o anoitecer. Antes de você
               partir, Ovena tira do pescoço um amuleto de osso e prata e o
               coloca em suas mãos. "Carregue-o até a Chama", ela diz. "Talvez
               o medo o abandone no caminho, como abandonou a ele."${itemComDestaque("amuleto da anciã")}`,
              `No fim da vila, o caminho se divide em três trilhas marcadas
               por pedras antigas.`,
            ],
            [{ texto: "Seguir até a encruzilhada", aoClicar: encruzilhada }]
          );
        },
      },
      {
        texto: "Acenar de longe e seguir viagem",
        aoClicar: () => {
          renderCena(
            [
              `Você segue em frente. Ao longe, ainda ouve Ovena arrastando a
               lenha sozinha pela neve.`,
              `No fim da vila, o caminho se divide em três trilhas marcadas
               por pedras antigas.`,
            ],
            [{ texto: "Seguir até a encruzilhada", aoClicar: encruzilhada }]
          );
        },
      },
    ]
  );
}

function encruzilhada() {
  renderCena(
    [
      `Cada trilha tem uma pedra entalhada com um símbolo diferente: um
       cristal, uma onda e uma torre.`,
    ],
    [
      { texto: "Seguir a trilha do cristal", aoClicar: cavernaCristal },
      { texto: "Seguir a trilha da onda", aoClicar: rioEncantado },
      { texto: "Seguir a trilha da torre", aoClicar: torreDoFeiticeiro },
    ]
  );
}

function cavernaCristal() {
  renderCena(
    [
      `Dentro da caverna, milhares de cristais cobrem as paredes e cantam
       em uníssono. No centro, um enigma está gravado na pedra: "Não
       tenho voz, mas canto. Não tenho corpo, mas corto. O que sou?"`,
    ],
    [
      {
        texto: "Ignorar o enigma e arrancar um cristal à força",
        aoClicar: () => {
          ganharCoragem(1);
          adicionarItem("fragmento de cristal");
          alterarVida(-50);
          if (!estaVivo()) return finalTragico();
          renderCena(
            [`Os cristais vibram furiosamente. Lascas afiadas cortam
              profundamente seus braços antes que você consiga fugir com um
              fragmento nas mãos.${itemComDestaque("fragmento de cristal")}`],
            [{ texto: "Seguir para o salão da Chama", aoClicar: confrontoFinal }]
          );
        },
      },
      {
        texto: 'Responder com calma: "o vento"',
        aoClicar: () => {
          ganharSabedoria(1);
          adicionarItem("fragmento de cristal");
          renderCena(
            [`O canto dos cristais muda de tom, como um suspiro de aprovação.
              Um fragmento se solta sozinho e cai suavemente em sua
              mão.${itemComDestaque("fragmento de cristal")}`],
            [{ texto: "Seguir para o salão da Chama", aoClicar: confrontoFinal }]
          );
        },
      },
    ]
  );
}

function rioEncantado() {
  renderCena(
    [
      `O Rio Encantado brilha com luz própria. Da água emerge um espírito
       translúcido: "Ninguém atravessa sem oferecer algo em troca."`,
    ],
    [
      {
        texto: "Oferecer um item que você carrega",
        aoClicar: () => {
          if (jogador.inventario.length > 0) {
            ganharSabedoria(1);
            const itemOferecido = jogador.inventario[0];
            adicionarItem("essência do rio");
            renderCena(
              [`Você entrega ${itemOferecido} ao espírito, que o segura com
                reverência antes de dissolvê-lo em luz. Em troca, ele lhe
                entrega um frasco que brilha sob a lua.${itemComDestaque("essência do rio")}`],
              [{ texto: "Seguir para o salão da Chama", aoClicar: confrontoFinal }]
            );
          } else {
            alterarVida(-18);
            if (!estaVivo()) return finalTragico();
            renderCena(
              [`Suas mãos estão vazias. O espírito balança a cabeça,
                desapontado, e afunda de volta na água sem lhe dar passagem
                fácil.`],
              [{ texto: "Seguir para o salão da Chama", aoClicar: confrontoFinal }]
            );
          }
        },
      },
      {
        texto: "Atravessar à força pela correnteza",
        aoClicar: () => {
          ganharCoragem(1);
          alterarVida(-40);
          if (!estaVivo()) return finalTragico();
          renderCena(
            [`Você avança pela correnteza gelada. A água é mais forte do que
              parece, e você é jogado contra as pedras antes de alcançar a
              outra margem, exausto e ferido.`],
            [{ texto: "Seguir para o salão da Chama", aoClicar: confrontoFinal }]
          );
        },
      },
    ]
  );
}

function torreDoFeiticeiro() {
  renderCena(
    [
      `A Torre do Feiticeiro se ergue torta entre as rochas. No topo,
       Aurelin, o último feiticeiro do vale, observa você chegar sem
       surpresa. "Vou saber em um instante o que você busca de verdade."`,
    ],
    [
      {
        texto: "Aceitar o teste de Aurelin",
        aoClicar: () => {
          ganharSabedoria(1);
          adicionarItem("pergaminho do feiticeiro");
          renderCena(
            [`Aurelin pergunta: "O que pesa mais, o medo de falhar ou o
              arrependimento de nunca tentar?" Sua resposta sincera parece
              satisfazê-lo, e ele lhe entrega um pergaminho antigo.${itemComDestaque("pergaminho do feiticeiro")}`],
            [{ texto: "Seguir para o salão da Chama", aoClicar: confrontoFinal }]
          );
        },
      },
      {
        texto: "Recusar o teste e seguir seu caminho",
        aoClicar: () => {
          renderCena(
            [`Você recusa educadamente. Aurelin dá de ombros e volta a
              observar o horizonte, sem insistir.`],
            [{ texto: "Seguir para o salão da Chama", aoClicar: confrontoFinal }]
          );
        },
      },
    ]
  );
}

/* ------------------------------------------------------------------ */
/*  CONFRONTO FINAL E DESFECHOS                                         */
/* ------------------------------------------------------------------ */
function confrontoFinal() {
  const temAmuleto = temItem("amuleto da anciã");
  const itensDosTresCaminhos = ["fragmento de cristal", "essência do rio", "pergaminho do feiticeiro"]
    .filter((i) => temItem(i)).length;

  renderCena(
    [
      `Após dias de jornada, você encontra a caverna final: um salão de
       gelo onde a Última Chama de Eldareth queima, pequena, azul e
       solitária, no centro de um altar de pedra. Diante dela, um
       Guardião das Cinzas barra sua passagem.`,
    ],
    [{ texto: "Avançar em direção à Chama", aoClicar: () => decidirFinal(temAmuleto, itensDosTresCaminhos) }]
  );
}

function decidirFinal(temAmuleto, itensDosTresCaminhos) {
  if (temAmuleto && itensDosTresCaminhos >= 1 && jogador.sabedoria >= 3) return finalSecreto();
  if (temAmuleto && jogador.coragem >= 1) return finalHeroico();
  if (jogador.sabedoria >= 2) return finalSabio();
  if (jogador.vida <= 60) return finalSombrio();
  return finalCovarde();
}

function telaFinal(rotulo, paragrafos) {
  renderCena(paragrafos, [{ texto: "Recomeçar jornada", aoClicar: reiniciar }], rotulo);
}

function finalHeroico() {
  adicionarItem("chama de Eldareth");
  telaFinal("Final: O Herói de Eldareth", [
    `O Guardião das Cinzas ergue sua lâmina de brasa, mas o amuleto da
     anciã Ovena brilha em seu peito, afastando o medo. Com passos
     firmes, ${jogador.nome} avança e retira a Chama do altar sem
     hesitar.${itemComDestaque("chama de Eldareth")}`,
    `O Guardião se desfaz em cinzas. Quando você retorna a Cinza-Alta
     com a Chama nas mãos, o gelo dos telhados começa a derreter pela
     primeira vez em sete invernos. Ovena chora ao ver a luz voltar ao
     vale.`,
  ]);
}

function finalSabio() {
  adicionarItem("chama de Eldareth");
  telaFinal("Final: O Sábio Silencioso", [
    `O Guardião pergunta, com voz de brasa crepitante: "O que você busca
     de verdade?" ${jogador.nome} responde com calma, citando tudo o que
     aprendeu no caminho.`,
    `O Guardião abaixa sua lâmina. "Poucos chegam até aqui entendendo
     mais do que buscando." Você retira a Chama sem lutar, e o vale
     volta a florescer, devagar, mas de forma duradoura.${itemComDestaque("chama de Eldareth")}`,
  ]);
}

function finalSombrio() {
  adicionarItem("chama de Eldareth");
  telaFinal("Final: A Chama Amarga", [
    `Ferido e exausto, ${jogador.nome} enfrenta o Guardião das Cinzas com
     o que resta de forças. A luta é dura, mas você arranca a Chama do
     altar por pouco, caindo de joelhos logo em seguida.${itemComDestaque("chama de Eldareth")}`,
    `Você sobrevive, mas as cicatrizes da jornada nunca desaparecem de
     verdade. O vale volta a aquecer — mas você observa tudo de longe,
     sabendo o preço real que pagou.`,
  ]);
}

function finalCovarde() {
  telaFinal("Final: O Inverno Eterno", [
    `Diante do Guardião das Cinzas, ${jogador.nome} hesita um segundo a
     mais do que deveria. Sem amuleto, sem sabedoria suficiente, sem
     coragem provada, o Guardião empurra você para fora do salão antes
     que a Chama sequer seja tocada.`,
    `Você volta para Cinza-Alta de mãos vazias. O inverno continua, e
     talvez outro viajante, mais preparado, precise terminar o que você
     não conseguiu.`,
  ]);
}

function finalSecreto() {
  adicionarItem("chama de Eldareth");
  telaFinal("Final secreto: O Verdadeiro Guardião", [
    `O Guardião das Cinzas para no meio do movimento. Ele reconhece o
     amuleto de Ovena e os sinais das outras trilhas — provas de alguém
     que percorreu o vale inteiro, ajudando e aprendendo em cada passo.`,
    `"Você não veio apenas buscar a Chama", diz o Guardião. "Você veio
     cuidar do vale." A armadura se abre, revelando que a Chama já
     reconhecia ${jogador.nome} havia tempo.${itemComDestaque("chama de Eldareth")}`,
    `Quando você retorna ao vale, a neve derrete em um único dia. Você se
     torna parte da lenda que um dia alguém mais vai contar a outro
     viajante perdido.`,
  ]);
}

function finalTragico() {
  telaFinal("Final: As Cinzas do Viajante", [
    `Os ferimentos acumulados ao longo do caminho são demais para
     ${jogador.nome} suportar. Em algum ponto da jornada, suas forças se
     esvaem antes que a Chama de Eldareth possa ser alcançada.`,
    `O vale permanece congelado, e seu nome se junta à lista de
     viajantes que tentaram e não voltaram.`,
  ]);
}

/* ------------------------------------------------------------------ */
/*  REINÍCIO E EFEITO DE NEVE                                           */
/* ------------------------------------------------------------------ */
function reiniciar() {
  jogador.vida = 100;
  jogador.coragem = 0;
  jogador.sabedoria = 0;
  jogador.inventario = [];
  telaInicial();
}

document.getElementById("botao-reiniciar").addEventListener("click", reiniciar);

function criarNeve() {
  const container = document.getElementById("neve");
  const quantidade = window.innerWidth < 600 ? 26 : 46;
  for (let i = 0; i < quantidade; i++) {
    const floco = document.createElement("span");
    const esquerda = Math.random() * 100;
    const duracao = 8 + Math.random() * 12;
    const atraso = Math.random() * 12;
    const deslocamento = (Math.random() * 60 - 30).toFixed(0) + "px";
    floco.style.left = esquerda + "vw";
    floco.style.animationDuration = duracao + "s";
    floco.style.animationDelay = "-" + atraso + "s";
    floco.style.setProperty("--deslocamento", deslocamento);
    container.appendChild(floco);
  }
}

criarNeve();
telaInicial();
