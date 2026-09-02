# A Última Chama de Eldareth 🔥❄️

Jogo de aventura em texto, criado para a atividade de **modelagem de
cenas com funções, escolhas e múltiplos finais**.

Existem **duas versões idênticas na história**, para atender aos dois
requisitos da atividade:

| Versão | Onde roda | Arquivo de entrada |
|---|---|---|
| **Python** (o que a atividade pede) | Terminal / VS Code / Jupyter | `main.py` |
| **Navegador** (bônus, para apresentar facilmente) | Qualquer navegador, inclusive publicado no GitHub Pages | `web/index.html` |

---

## 🗂 Estrutura do projeto

```
eldareth-aventura/
├── main.py            # ponto de entrada: laço principal do jogo (Python)
├── player.py          # classe Jogador (vida, coragem, sabedoria, itens)
├── scenes.py          # UMA FUNÇÃO POR CENA — o coração da atividade
├── utils.py           # funções auxiliares (efeito de digitação, escolhas)
├── data/
│   └── itens.json     # dataset com a descrição de cada item do jogo
├── web/                # versão jogável no navegador (HTML + CSS + JS)
│   ├── index.html
│   ├── style.css
│   └── game.js
└── README.md
```

Cada cena da história (`introducao`, `floresta_sombria`,
`vila_abandonada`, `encruzilhada`, `caverna_cristal`, `rio_encantado`,
`torre_do_feiticeiro`, `confronto_final` e os 6 finais) é uma **função
independente** em `scenes.py`. O `main.py` só liga essas funções entre
si através de um dicionário (`MAPA_DE_CENAS`), então adicionar uma cena
nova não exige mexer no laço principal — só escrever a função e
registrá-la no mapa.

---

## ▶️ Como rodar a versão em Python

Pré-requisitos: **Python 3.x** instalado.

```bash
# dentro da pasta do projeto
python3 main.py
```

No VS Code, basta abrir a pasta e rodar `main.py` (botão ▶ ou `F5`).
Em Jupyter, rode `%run main.py` numa célula.

---

## 🌐 Como rodar a versão no navegador

**Opção 1 — abrir localmente:**
Dê duplo clique em `web/index.html` (ou clique com o botão direito →
"Abrir com" → seu navegador).

**Opção 2 — publicar no GitHub Pages (recomendado para apresentar):**

1. Crie um repositório novo no GitHub, por exemplo `eldareth-aventura`.
2. Suba **todos os arquivos e pastas** deste projeto para o repositório
   (veja o passo a passo completo abaixo).
3. No repositório, vá em **Settings → Pages**.
4. Em "Branch", selecione `main` e a pasta `/web`, depois clique em
   **Save**.
5. Espere ~1 minuto e o GitHub vai gerar um link parecido com:
   `https://SEU-USUARIO.github.io/eldareth-aventura/`
6. Esse é o link que você pode abrir na hora da apresentação — funciona
   em qualquer navegador, celular incluso.

---

## 🖥️ Passo a passo para subir tudo no GitHub

```bash
# 1. entre na pasta do projeto (depois de extrair o .zip)
cd eldareth-aventura

# 2. inicialize o git
git init

# 3. adicione todos os arquivos
git add .

# 4. faça o primeiro commit
git commit -m "Primeira versão do jogo A Última Chama de Eldareth"

# 5. crie o repositório no site github.com (botão "New repository")
#    NÃO marque a opção "Add a README" para não dar conflito

# 6. conecte seu projeto local ao repositório criado
git remote add origin https://github.com/SEU-USUARIO/eldareth-aventura.git

# 7. envie os arquivos
git branch -M main
git push -u origin main
```

Depois disso é só seguir o passo do GitHub Pages acima (Settings →
Pages → branch `main` → pasta `/web`).

> Se preferir, também dá pra fazer tudo isso pela própria interface do
> GitHub: crie o repositório vazio, clique em "uploading an existing
> file" e arraste a pasta inteira do projeto.

---

## 🎮 Sobre a jogabilidade

- **3 caminhos iniciais diferentes** (Estrada do Mercador × Floresta
  Sombria, depois Cristal × Rio × Torre) que mudam o restante da
  aventura.
- **Atributos que reagem às escolhas do jogador**: vida, coragem e
  sabedoria, além de um inventário de itens.
- **6 finais possíveis**, todos alcançáveis dependendo das escolhas:
  1. 🏆 **Herói de Eldareth** — coragem + confiança conquistada
  2. 📖 **Sábio Silencioso** — venceu pela reflexão, não pela força
  3. 🌑 **Chama Amarga** — venceu, mas pagou um preço alto
  4. ❄️ **Inverno Eterno** — não se arriscou o suficiente
  5. ✨ **Final secreto: O Verdadeiro Guardião** — só para quem ajudou
     e refletiu em (quase) todas as cenas
  6. 💀 **As Cinzas do Viajante** — a jornada pode matar quem for
     imprudente demais

## ✍️ Sobre a organização do código (para a apresentação)

- `utils.py` → nada de história, só ferramentas (imprimir com efeito de
  digitação, validar escolhas, limpar tela).
- `player.py` → só o estado do jogador, isolado do resto.
- `scenes.py` → só a história, uma função por cena, sem se preocupar em
  saber qual é a cena anterior ou seguinte (isso é papel do `main.py`).
- `main.py` → só o "motor" do jogo: decide qual função chamar a partir
  do nome que a cena anterior retornou.
- `data/itens.json` → as descrições dos itens ficam fora do código,
  como um pequeno dataset, exatamente como sugerido pela atividade.

Essa separação foi pensada para deixar claro, na apresentação, **onde**
mexer se quisesse adicionar uma cena nova, um item novo ou um final
novo — sem precisar reescrever o jogo inteiro.
