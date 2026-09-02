"""
main_web.py
------------
Esta é a versão PyScript de main.py. A ideia é idêntica: um dicionário
que mapeia nome-da-cena -> função, e um laço que vai chamando a função
certa até chegar a um final (quando a função retorna None).

A única mudança é que o laço `while` do terminal, que rodava
instantaneamente do início ao fim, aqui vira um laço assíncrono que
"espera" (`await`) cada cena terminar de coletar a escolha do jogador
antes de continuar — porque no navegador as escolhas chegam por clique,
não por um input() que já vem pronto.
"""

import asyncio

import scenes_web as scenes
from player import Jogador
from utils_web import pedir_texto, pausa, limpar_tela, definir_jogador, digitar

MAPA_DE_CENAS = {
    "introducao": scenes.introducao,
    "estrada_do_mercador": scenes.estrada_do_mercador,
    "floresta_sombria": scenes.floresta_sombria,
    "vila_abandonada": scenes.vila_abandonada,
    "encruzilhada": scenes.encruzilhada,
    "caverna_cristal": scenes.caverna_cristal,
    "rio_encantado": scenes.rio_encantado,
    "torre_do_feiticeiro": scenes.torre_do_feiticeiro,
    "confronto_final": scenes.confronto_final,
    "final_heroico": scenes.final_heroico,
    "final_sabio": scenes.final_sabio,
    "final_sombrio": scenes.final_sombrio,
    "final_covarde": scenes.final_covarde,
    "final_secreto": scenes.final_secreto,
    "final_tragico": scenes.final_tragico,
}


async def jogar():
    while True:
        limpar_tela()
        nome = await pedir_texto("Iniciar jornada")
        jogador = Jogador(nome)
        definir_jogador(jogador)

        cena_atual = "introducao"
        while cena_atual is not None:
            funcao_da_cena = MAPA_DE_CENAS.get(cena_atual)
            if funcao_da_cena is None:
                digitar(f"[erro interno] cena '{cena_atual}' não existe.")
                break
            cena_atual = await funcao_da_cena(jogador)

        await pausa("Jogar novamente")


# PyScript executa o módulo inteiro de forma síncrona; para "iniciar"
# uma função async a partir do topo do arquivo, agendamos ela na
# própria fila de eventos do navegador com create_task — é o mesmo
# princípio de asyncio.run(), só que sem bloquear a aba do navegador.
asyncio.ensure_future(jogar())
