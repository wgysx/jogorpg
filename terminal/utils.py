"""
utils.py
---------
Funções utilitárias usadas em todo o jogo: efeito de digitação,
limpeza de tela, pausas e validação de escolhas do jogador.

Mantemos essas funções separadas das cenas para que o código fique
organizado em partes (uma responsabilidade por arquivo).
"""

import os
import sys
import time


def digitar(texto: str, delay: float = 0.018) -> None:
    """Imprime um texto letra por letra, criando um efeito de narrativa."""
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def linha(caractere: str = "─", tamanho: int = 46) -> None:
    print(caractere * tamanho)


def pausa(mensagem: str = "\n(pressione ENTER para continuar...)") -> None:
    input(mensagem)


def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def escolher(opcoes: dict) -> str:
    """
    Recebe um dicionário {"1": "texto da opção", "2": "..."} e mostra
    as opções numeradas na tela, validando a entrada do jogador até
    que ele digite uma opção existente.
    """
    for chave, texto in opcoes.items():
        print(f"  [{chave}] {texto}")

    while True:
        escolha = input("\n> Sua escolha: ").strip()
        if escolha in opcoes:
            return escolha
        print("✗ Opção inválida. Digite um dos números listados acima.")
