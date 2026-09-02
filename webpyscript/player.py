"""
player.py
----------
Define a classe Jogador, responsável por guardar o estado do herói
durante a aventura: vida, atributos (coragem/sabedoria), inventário
e nome. É esse estado que as cenas vão consultar para decidir os
rumos da história e, no fim, qual final o jogador merece.
"""


class Jogador:
    def __init__(self, nome: str):
        self.nome = nome or "Viajante"
        self.vida = 100
        self.coragem = 0
        self.sabedoria = 0
        self.inventario = []

    # ---------- inventário ----------
    def adicionar_item(self, item: str) -> None:
        if item not in self.inventario:
            self.inventario.append(item)
            print(f"\n   ✦ Você obteve: {item}")

    def tem_item(self, item: str) -> bool:
        return item in self.inventario

    # ---------- atributos ----------
    def alterar_vida(self, valor: int) -> None:
        self.vida = max(0, min(100, self.vida + valor))
        if valor < 0:
            print(f"\n   ✖ Você perdeu {abs(valor)} de vida. (Vida atual: {self.vida})")
        elif valor > 0:
            print(f"\n   ✚ Você recuperou {valor} de vida. (Vida atual: {self.vida})")

    def ganhar_coragem(self, valor: int = 1) -> None:
        self.coragem += valor

    def ganhar_sabedoria(self, valor: int = 1) -> None:
        self.sabedoria += valor

    def esta_vivo(self) -> bool:
        return self.vida > 0

    # ---------- exibição ----------
    def status(self) -> None:
        itens = ", ".join(self.inventario) if self.inventario else "nenhum"
        print("\n┌──────────── STATUS ────────────┐")
        print(f"  Nome:      {self.nome}")
        print(f"  Vida:      {self.vida}/100")
        print(f"  Coragem:   {self.coragem}")
        print(f"  Sabedoria: {self.sabedoria}")
        print(f"  Itens:     {itens}")
        print("└─────────────────────────────────┘")
