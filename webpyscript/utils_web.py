"""
utils_web.py
-------------
Esta é a MESMA IDEIA de utils.py (funções auxiliares de interface),
só que reimplementada para rodar dentro do navegador com o PyScript.

No terminal, `input()` PARA o programa até a pessoa digitar algo.
No navegador não existe um `input()` que trava a página assim — em vez
disso, usamos `asyncio`: cada função "espera" (`await`) até que o
jogador clique em um botão, através de uma `asyncio.Future` que é
resolvida dentro do `addEventListener` do botão.

Por isso as funções aqui são `async def` e precisam ser chamadas com
`await` — é a única mudança estrutural necessária em quem as usa
(veja scenes_web.py).
"""

import asyncio
from pyscript import document

_area_texto = document.getElementById("texto-cena")
_area_escolhas = document.getElementById("area-escolhas")

# Referência ao jogador atual, usada só para manter a HUD (barra de
# vida, coragem, sabedoria, itens) sincronizada com o estado real do
# jogador — sem precisar espalhar chamadas de atualização por todo o
# scenes_web.py.
_jogador_atual = None


def definir_jogador(jogador) -> None:
    global _jogador_atual
    _jogador_atual = jogador
    atualizar_hud()


def atualizar_hud() -> None:
    if _jogador_atual is None:
        return
    barra = document.getElementById("barra-vida")
    if barra is not None:
        barra.style.width = f"{_jogador_atual.vida}%"

    valor_coragem = document.getElementById("valor-coragem")
    if valor_coragem is not None:
        valor_coragem.innerText = str(_jogador_atual.coragem)

    valor_sabedoria = document.getElementById("valor-sabedoria")
    if valor_sabedoria is not None:
        valor_sabedoria.innerText = str(_jogador_atual.sabedoria)

    valor_itens = document.getElementById("valor-itens")
    if valor_itens is not None:
        if _jogador_atual.inventario:
            valor_itens.innerText = ", ".join(
                item.replace("_", " ") for item in _jogador_atual.inventario
            )
        else:
            valor_itens.innerText = "nenhum"


def limpar_tela() -> None:
    """No terminal limpava o console. No navegador, limpa a caixa de texto
    e aproveita o momento para sincronizar a HUD com o estado atual."""
    _area_texto.innerHTML = ""
    atualizar_hud()


def digitar(texto: str, delay: float = 0.0) -> None:
    """No terminal, escrevia letra por letra. Aqui, cria um parágrafo na tela."""
    paragrafo = document.createElement("p")
    paragrafo.innerText = texto
    _area_texto.appendChild(paragrafo)
    _area_texto.scrollTop = _area_texto.scrollHeight


def mostrar_destaque(texto: str) -> None:
    """Equivalente ao print() usado para mostrar a descrição de um item."""
    paragrafo = document.createElement("p")
    paragrafo.className = "destaque"
    paragrafo.innerText = texto
    _area_texto.appendChild(paragrafo)


def linha(caractere: str = "─", tamanho: int = 46) -> None:
    """Puramente decorativo no terminal; sem efeito visual necessário aqui."""
    return None


async def pausa(mensagem: str = "Continuar…") -> None:
    """
    Equivalente ao pausa() do terminal (que esperava um ENTER).
    Aqui, mostramos um botão único e esperamos o clique.
    """
    loop = asyncio.get_event_loop()
    futuro = loop.create_future()

    botao = document.createElement("button")
    botao.className = "botao-escolha botao-continuar"
    botao.innerText = mensagem

    def ao_clicar(_evento):
        if not futuro.done():
            futuro.set_result(None)

    botao.addEventListener("click", ao_clicar)
    _area_escolhas.innerHTML = ""
    _area_escolhas.appendChild(botao)

    await futuro
    _area_escolhas.innerHTML = ""


async def escolher(opcoes: dict) -> str:
    """
    Equivalente ao escolher() do terminal (que validava o input()).
    Aqui não existe entrada inválida: cada opção já é um botão, então
    só é possível "digitar" uma opção que exista.
    """
    loop = asyncio.get_event_loop()
    futuro = loop.create_future()

    _area_escolhas.innerHTML = ""
    for chave, texto_opcao in opcoes.items():
        botao = document.createElement("button")
        botao.className = "botao-escolha"
        botao.innerText = texto_opcao

        def gerar_callback(chave_escolhida):
            def ao_clicar(_evento):
                if not futuro.done():
                    futuro.set_result(chave_escolhida)
            return ao_clicar

        botao.addEventListener("click", gerar_callback(chave))
        _area_escolhas.appendChild(botao)

    resultado = await futuro
    _area_escolhas.innerHTML = ""
    return resultado


async def pedir_texto(rotulo_botao: str = "Iniciar jornada", texto_padrao: str = "Viajante") -> str:
    """
    Não existe equivalente disso no utils.py original (lá era só um
    input() simples no main.py). Criamos aqui porque, no navegador,
    pedir o nome do personagem também precisa de um campo + botão em
    vez de um input() de terminal.
    """
    loop = asyncio.get_event_loop()
    futuro = loop.create_future()

    campo = document.createElement("input")
    campo.type = "text"
    campo.placeholder = "Nome do seu personagem"
    campo.maxLength = 24

    botao = document.createElement("button")
    botao.className = "botao-primario"
    botao.innerText = rotulo_botao

    envolucro = document.createElement("div")
    envolucro.className = "campo-nome"
    envolucro.appendChild(campo)
    envolucro.appendChild(botao)

    def enviar(_evento=None):
        if not futuro.done():
            valor = campo.value.strip() or texto_padrao
            futuro.set_result(valor)

    def tecla(evento):
        if evento.key == "Enter":
            enviar()

    botao.addEventListener("click", enviar)
    campo.addEventListener("keydown", tecla)

    _area_escolhas.innerHTML = ""
    _area_escolhas.appendChild(envolucro)
    campo.focus()

    resultado = await futuro
    _area_escolhas.innerHTML = ""
    return resultado
