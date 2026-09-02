"""
main.py
--------
Ponto de entrada da aventura "A Última Chama de Eldareth".

Organização do projeto:
    main.py     -> laço principal do jogo (este arquivo)
    player.py   -> classe Jogador (estado: vida, itens, atributos)
    scenes.py   -> uma função por cena da história
    utils.py    -> funções auxiliares de texto e entrada
    data/       -> dataset com as descrições dos itens (JSON)

O jogo funciona como uma máquina de estados simples: cada cena é uma
função que recebe o jogador, narra o que acontece e devolve o nome
(string) da próxima cena. Quando uma função devolve None, a história
chegou a um dos finais.
"""

import scenes
from player import Jogador
from utils import digitar, limpar_tela, pausa

# Mapa de cenas: nome (string) -> função responsável por narrá-la.
# Adicionar uma cena nova ao jogo é só escrever a função em scenes.py
# e registrá-la aqui — o laço principal não precisa mudar.
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


def jogar():
    limpar_tela()
    print("=" * 46)
    print("   A ÚLTIMA CHAMA DE ELDARETH — uma aventura em texto")
    print("=" * 46)
    nome = input("\nDigite o nome do seu personagem: ").strip()

    jogador = Jogador(nome)
    cena_atual = "introducao"

    while cena_atual is not None:
        funcao_da_cena = MAPA_DE_CENAS.get(cena_atual)
        if funcao_da_cena is None:
            print(f"[erro interno] cena '{cena_atual}' não existe.")
            break
        cena_atual = funcao_da_cena(jogador)

    print("\n" + "=" * 46)
    digitar("Obrigado por jogar A Última Chama de Eldareth!")
    print("=" * 46)


def main():
    jogando = True
    while jogando:
        jogar()
        resposta = input("\nJogar novamente? (s/n): ").strip().lower()
        jogando = resposta.startswith("s")
    print("\nAté a próxima jornada, viajante.")


if __name__ == "__main__":
    main()
