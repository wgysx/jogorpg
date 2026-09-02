# A Última Chama de Eldareth 🔥❄️

Jogo de aventura em texto, criado para a atividade de **modelagem de
cenas com funções, escolhas e múltiplos finais**.

O projeto agora tem **três versões**, todas com a mesma história:

| Versão | Onde roda | Como abrir |
|---|---|---|
| 🖥️ **Terminal** (o que a atividade pede) | Terminal / VS Code / Jupyter | `python3 main.py` (ou `terminal/main.py`, o backup) |
| 🌐 **Navegador — JavaScript** | Qualquer navegador, offline | `web-js/index.html` |
| 🐍 **Navegador — PyScript** | Qualquer navegador, com internet na 1ª carga | `web-pyscript/index.html` (via servidor local, veja abaixo) |

> A versão **PyScript** é a mais nova: em vez de reescrever o jogo em
> JavaScript, ela roda **o próprio código Python** (`scenes.py` /
> `player.py`) dentro do navegador, usando o framework
> [PyScript](https://pyscript.net). É a forma mais fiel de "colocar o
> jogo Python no navegador" — o código que decide a história é
> literalmente o mesmo, só a forma de mostrar texto e receber cliques
> muda.

---

## 🗂 Estrutura do projeto

```
eldareth-aventura/
├── main.py, player.py, scenes.py, utils.py   # jogo original de terminal
├── data/itens.json
│
├── terminal/                # 🔒 BACKUP do jogo de terminal, feito antes
│   ├── main.py               #    de mexer em qualquer coisa para aplicar
│   ├── player.py             #    o framework PyScript. Se algo quebrar
│   ├── scenes.py             #    nas outras versões, o jogo original
│   ├── utils.py              #    inteiro está intacto aqui.
│   └── data/itens.json
│
├── web-js/                  # versão navegador em JavaScript puro
│   ├── index.html
│   ├── style.css
│   └── game.js               #    história reescrita em JS (funciona 100% offline)
│
├── web-pyscript/            # versão navegador rodando Python de verdade
│   ├── index.html             #  carrega o PyScript + o Python abaixo
│   ├── style.css
│   ├── pyscript.toml           #  diz ao PyScript quais arquivos .py buscar
│   ├── main_web.py              #  = main.py, mas assíncrono (await)
│   ├── scenes_web.py            #  = scenes.py, mesma história, com async/await
│   ├── utils_web.py             #  = utils.py, só que usando botões em vez de input()
│   ├── player.py                 #  IDÊNTICO ao player.py original (sem nenhuma mudança!)
│   └── data/itens.json           #  IDÊNTICO ao dataset original
│
└── README.md
```

---

## 🔒 Sobre o backup (terminal/)

Antes de aplicar o framework PyScript, foi feita uma cópia fiel de
todo o jogo de terminal funcional para a pasta `terminal/`. Isso
garante que, aconteça o que acontecer nas versões web, sempre existe
uma versão 100% funcional e testada para apresentar ou entregar.

A pasta raiz (`main.py`, `player.py`, `scenes.py`, `utils.py`) continua
sendo a mesma versão de sempre — o backup em `terminal/` é uma
segurança extra, não uma substituição.

---

## 🐍 Como o PyScript foi aplicado (o que mudou e o que NÃO mudou)

O grande objetivo ao aplicar o framework foi mudar **o mínimo possível**
do código já pronto — só a "camada de interface" precisou de ajuste:

| Arquivo original | O que fazia | Versão PyScript | O que mudou |
|---|---|---|---|
| `player.py` | Guarda vida, coragem, sabedoria, itens | `player.py` (idêntico) | **Nada.** Não tem I/O, então não precisa mudar. |
| `utils.py` | `input()` para escolher, `print()` para narrar | `utils_web.py` | `escolher()`/`pausa()` viraram `async def` e passaram a esperar (`await`) o clique de um botão em vez de uma tecla ENTER |
| `scenes.py` | Uma função por cena, retorna o nome da próxima | `scenes_web.py` | Cada `def cena(jogador):` virou `async def cena(jogador):`, e cada chamada a `escolher()`/`pausa()` ganhou um `await` na frente. A história, os itens, os atributos e os 6 finais são **exatamente os mesmos**. |
| `main.py` | Laço `while` síncrono com um dicionário de cenas | `main_web.py` | O mesmo dicionário de cenas, só que o laço agora é `async` e é iniciado com `asyncio.ensure_future()` em vez de rodar direto |

Ou seja: a **árvore da história** (o que faz a atividade valer nota —
modelar cenas com funções, criar escolhas e finais) não mudou uma
vírgula. Só a forma de "entregar" cada cena para a pessoa jogando é
diferente.

### Por que precisa de `async`/`await`?

No terminal, `input()` literalmente **trava** o programa até alguém
digitar e apertar ENTER. No navegador isso não existe — travar a aba
inteira esperando um clique deixaria a página congelada. A solução do
Python para "esperar sem travar" é `asyncio`: a função para no `await`,
devolve o controle para o navegador, e só continua quando o clique no
botão resolve uma `Future` (isso acontece dentro de `utils_web.py`).

---

## ▶️ Como rodar cada versão

### Inicialização rápida no Windows

Com o Python instalado, dê duplo clique em `iniciar_jogo.bat` na pasta
do projeto. O arquivo inicia o servidor local, abre a versão PyScript no
navegador e mantém o servidor ativo enquanto esta janela estiver aberta.

### 1. Terminal (Python puro)

```bash
python3 main.py
# ou, para rodar o backup:
python3 terminal/main.py
```

### 2. Navegador — JavaScript (`web-js/`)

Basta abrir `web-js/index.html` com duplo clique. Funciona 100%
offline, sem precisar de servidor nem internet.

### 3. Navegador — PyScript (`web-pyscript/`)

Essa versão **precisa** ser aberta por um servidor local (não funciona
com duplo clique / `file://`), porque o navegador bloqueia o PyScript
de buscar os arquivos `.py` diretamente do disco por segurança. Além
disso, a primeira vez que a página abre, o navegador baixa o
interpretador Python (Pyodide) da internet — depois disso ele fica em
cache.

**Opção mais simples — VS Code:**
1. Instale a extensão **Live Server**.
2. Clique com o botão direito em `web-pyscript/index.html`.
3. Escolha **"Open with Live Server"**.

**Opção sem VS Code — terminal:**
```bash
cd web-pyscript
python3 -m http.server 8000
```
Depois abra `http://localhost:8000` no navegador.

> Se você abrir `web-pyscript/index.html` direto pelo `file://`, vai
> aparecer erro de CORS/"failed to fetch" no console — isso é o
> navegador protegendo o disco, não um bug do jogo. É só usar um dos
> dois métodos acima.

---

## 🌐 Publicando no GitHub / GitHub Pages

```bash
cd eldareth-aventura
git init
git add .
git commit -m "A Última Chama de Eldareth — terminal, web-js e web-pyscript"
git remote add origin https://github.com/SEU-USUARIO/eldareth-aventura.git
git branch -M main
git push -u origin main
```

No repositório, vá em **Settings → Pages**, selecione a branch `main`
e a pasta que você quer publicar:
- `/web-js` para a versão 100% offline; ou
- `/web-pyscript` para a versão que roda o Python de verdade (o
  GitHub Pages já serve os arquivos por `https://`, então o problema
  de CORS do `file://` não acontece lá).

---

## 🎮 Sobre a jogabilidade (vale para as três versões)

- **3 caminhos iniciais diferentes** (Estrada do Mercador × Floresta
  Sombria, depois Cristal × Rio × Torre).
- **Atributos que reagem às escolhas**: vida, coragem, sabedoria e um
  inventário de itens.
- **6 finais possíveis**:
  1. 🏆 Herói de Eldareth — coragem + confiança conquistada
  2. 📖 Sábio Silencioso — venceu pela reflexão, não pela força
  3. 🌑 Chama Amarga — venceu, mas pagou um preço alto
  4. ❄️ Inverno Eterno — não se arriscou o suficiente
  5. ✨ Final secreto: O Verdadeiro Guardião — só para quem ajudou e
     refletiu em quase todas as cenas
  6. 💀 As Cinzas do Viajante — dá pra morrer se for imprudente demais

## ✍️ Organização do código (para a apresentação)

- `utils.py` / `utils_web.py` → só ferramentas de interface, sem
  história nenhuma dentro.
- `player.py` → só o estado do jogador, isolado de tudo (por isso não
  precisou mudar uma linha para rodar no navegador).
- `scenes.py` / `scenes_web.py` → só a história, uma função por cena.
- `main.py` / `main_web.py` → só o "motor": decide qual função chamar
  a partir do nome que a cena anterior devolveu.
- `data/itens.json` → descrições dos itens fora do código, como um
  dataset — usado sem nenhuma alteração pelas três versões.

Essa separação em camadas foi o que permitiu trocar terminal por
navegador (duas vezes, inclusive) sem tocar na história em si — é o
ponto mais forte para destacar na apresentação de 15 minutos.
