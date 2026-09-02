"""
scenes.py
----------
Cada cena da aventura é modelada como uma função independente.
Toda função de cena:
    1. Recebe o objeto `jogador` (player.Jogador);
    2. Narra o que acontece;
    3. Eventualmente apresenta uma escolha com utils.escolher();
    4. Retorna uma STRING com o nome da próxima cena
       (ou None quando a história chega a um final).

Esse "mapa de cenas -> função" é montado em main.py, então este
arquivo cuida apenas da histórinha, sem se preocupar com o laço
principal do jogo (organização em partes).
"""

import json
import os

from utils import digitar, linha, pausa, escolher, limpar_tela

CAMINHO_ITENS = os.path.join(os.path.dirname(__file__), "data", "itens.json")

with open(CAMINHO_ITENS, encoding="utf-8") as arquivo:
    DESCRICOES_ITENS = json.load(arquivo)


def _mostrar_item(item: str) -> None:
    descricao = DESCRICOES_ITENS.get(item, "")
    if descricao:
        print(f"     \"{descricao}\"")


# ------------------------------------------------------------------ #
#  INÍCIO
# ------------------------------------------------------------------ #
def introducao(jogador):
    limpar_tela()
    linha("═")
    digitar("           A ÚLTIMA CHAMA DE ELDARETH")
    linha("═")
    digitar(
        f"\nHá sete invernos o sol não aquece mais o vale de Eldareth. "
        f"A neve cobre os telhados até as portas e as colheitas apodrecem "
        f"sob o gelo. Diz a lenda que uma Chama viva, guardada nas "
        f"profundezas do vale, é a única coisa capaz de devolver o "
        f"calor à terra."
    )
    digitar(
        f"\nVocê, {jogador.nome}, é o único viajante disposto a atravessar "
        f"o vale amaldiçoado para encontrá-la. Antes de partir, o velho "
        f"guarda do portão da última cidade livre lhe mostra dois caminhos "
        f"no mapa gasto."
    )
    pausa()

    print("\nQual caminho você escolhe?")
    escolha = escolher({
        "1": "A Estrada do Mercador — mais longa, mas ainda usada por viajantes",
        "2": "A Floresta Sombria — um atalho perigoso que ninguém mais atravessa",
    })

    if escolha == "1":
        return "estrada_do_mercador"
    return "floresta_sombria"


# ------------------------------------------------------------------ #
#  CAMINHO A — ESTRADA DO MERCADOR
# ------------------------------------------------------------------ #
def estrada_do_mercador(jogador):
    limpar_tela()
    digitar(
        "A estrada é longa, mas segura. Ao entardecer, você encontra "
        "Bilo, um mercador de carroça quebrada, tentando consertar uma "
        "roda presa no gelo."
    )
    digitar(
        "\nEm troca de ajuda para empurrar a carroça, ele oferece um "
        "presente de sua bagagem — o que restou depois de anos vendendo "
        "relíquias por vilarejos esquecidos."
    )
    pausa()

    print("\nBilo estende dois objetos. Qual você aceita?")
    escolha = escolher({
        "1": "Uma lanterna de vidro com um vaga-lume eterno preso dentro",
        "2": "Uma adaga enferrujada, mas ainda afiada",
    })

    if escolha == "1":
        jogador.adicionar_item("lanterna_de_vaga-lume")
        _mostrar_item("lanterna_de_vaga-lume")
    else:
        jogador.adicionar_item("adaga_enferrujada")
        _mostrar_item("adaga_enferrujada")

    digitar(
        "\nBilo aponta para o horizonte: \"A vila de Cinza-Alta fica logo "
        "depois daquela colina. Cuidado — dizem que lá só restaram cinzas "
        "e memórias.\""
    )
    pausa()
    return "vila_abandonada"


# ------------------------------------------------------------------ #
#  CAMINHO B — FLORESTA SOMBRIA
# ------------------------------------------------------------------ #
def floresta_sombria(jogador):
    limpar_tela()
    digitar(
        "As árvores da Floresta Sombria não têm folhas há anos. Seus "
        "galhos se entrelaçam como dedos ossudos sobre sua cabeça, "
        "bloqueando o pouco sol que ainda insiste em nascer."
    )
    digitar(
        "\nUm rosnado corta o silêncio. Entre as sombras, dois olhos "
        "amarelos brilham: é Uivante, o último lobo do vale, magro e "
        "faminto, bloqueando o caminho."
    )
    pausa()

    print("\nO que você faz?")
    escolha = escolher({
        "1": "Enfrentar o lobo de frente",
        "2": "Ficar imóvel e observar, esperando que ele se afaste",
    })

    if escolha == "1":
        jogador.ganhar_coragem(1)
        if jogador.tem_item("adaga_enferrujada"):
            digitar(
                "\nVocê saca a adaga de Bilo. A lâmina enferrujada ainda "
                "corta o suficiente para afastar o animal, que foge "
                "mancando entre as árvores."
            )
            jogador.alterar_vida(-8)
        else:
            digitar(
                "\nSem arma alguma, você luta com as próprias mãos. O "
                "lobo crava os dentes em seu braço antes de finalmente "
                "recuar, ganindo de dor. O ferimento é sério."
            )
            jogador.alterar_vida(-55)
    else:
        jogador.ganhar_sabedoria(1)
        digitar(
            "\nVocê prende a respiração e não se move um centímetro. "
            "Uivante fareja o ar, hesita, e por fim se afasta — talvez "
            "reconhecendo em você algo que não vale o risco de atacar."
        )

    if not jogador.esta_vivo():
        return "final_tragico"

    digitar(
        "\nMais à frente, a floresta se abre e você avista os telhados "
        "cobertos de cinzas de uma vila."
    )
    pausa()
    return "vila_abandonada"


# ------------------------------------------------------------------ #
#  PONTO DE ENCONTRO
# ------------------------------------------------------------------ #
def vila_abandonada(jogador):
    limpar_tela()
    digitar(
        "Cinza-Alta já foi um vilarejo próspero. Agora, apenas casas "
        "vazias e um silêncio pesado, quebrado só pelo vento entre as "
        "vigas quebradas."
    )
    digitar(
        "\nNuma das poucas casas com fumaça saindo da chaminé, uma "
        "anciã chamada Ovena tenta, sozinha, empilhar lenha para "
        "sobreviver mais uma noite."
    )
    pausa()

    print("\nComo você reage?")
    escolha = escolher({
        "1": "Parar e ajudá-la a carregar a lenha",
        "2": "Acenar de longe e seguir viagem — o tempo é curto",
    })

    if escolha == "1":
        jogador.ganhar_sabedoria(1)
        digitar(
            "\nVocês trabalham em silêncio até o anoitecer. Antes de "
            "você partir, Ovena tira do pescoço um amuleto de osso e "
            "prata e o coloca em suas mãos."
        )
        jogador.adicionar_item("amuleto_da_anciã")
        _mostrar_item("amuleto_da_anciã")
        digitar(
            "\n\"Ele pertenceu ao meu marido\", ela diz. \"Carregue-o "
            "até a Chama. Talvez o medo o abandone no caminho, como "
            "abandonou a ele.\""
        )
    else:
        digitar(
            "\nVocê segue em frente. Ao longe, ainda ouve Ovena "
            "arrastando a lenha sozinha pela neve — um peso que talvez "
            "volte a incomodar sua consciência mais tarde."
        )

    pausa()
    digitar(
        "\nNo fim da vila, o caminho se divide em três trilhas marcadas "
        "por pedras antigas."
    )
    return "encruzilhada"


# ------------------------------------------------------------------ #
#  ENCRUZILHADA — três rotas possíveis
# ------------------------------------------------------------------ #
def encruzilhada(jogador):
    limpar_tela()
    digitar(
        "Cada trilha tem uma pedra entalhada com um símbolo diferente: "
        "um cristal, uma onda e uma torre."
    )
    pausa()

    print("\nQual trilha você segue?")
    escolha = escolher({
        "1": "A trilha do cristal, rumo à Caverna de Cristal",
        "2": "A trilha da onda, rumo ao Rio Encantado",
        "3": "A trilha da torre, rumo à Torre do Feiticeiro",
    })

    if escolha == "1":
        return "caverna_cristal"
    if escolha == "2":
        return "rio_encantado"
    return "torre_do_feiticeiro"


def caverna_cristal(jogador):
    limpar_tela()
    digitar(
        "Dentro da caverna, milhares de cristais cobrem as paredes e "
        "emitem um som quase musical, como se cantassem em uníssono. "
        "No centro, um enigma está gravado na pedra:"
    )
    digitar(
        "\n   \"Não tenho voz, mas canto. Não tenho corpo, mas corto. "
        "O que sou?\""
    )
    pausa()

    print("\nComo você lida com o enigma?")
    escolha = escolher({
        "1": "Ignorar o enigma e arrancar um cristal à força",
        "2": "Pensar com calma e responder: \"o vento\"",
    })

    if escolha == "1":
        jogador.ganhar_coragem(1)
        digitar(
            "\nOs cristais vibram furiosamente. Lascas afiadas se "
            "desprendem da parede e cortam profundamente seus braços "
            "antes que você consiga fugir com um fragmento nas mãos."
        )
        jogador.alterar_vida(-50)
        jogador.adicionar_item("fragmento_de_cristal")
    else:
        jogador.ganhar_sabedoria(1)
        digitar(
            "\nO canto dos cristais muda de tom, quase como um "
            "suspiro de aprovação. Um fragmento se solta sozinho e "
            "cai suavemente em sua mão."
        )
        jogador.adicionar_item("fragmento_de_cristal")

    if not jogador.esta_vivo():
        return "final_tragico"

    pausa()
    return "confronto_final"


def rio_encantado(jogador):
    limpar_tela()
    digitar(
        "O Rio Encantado brilha com uma luz própria, mesmo sob o céu "
        "cinzento. Da água emerge uma figura translúcida — o espírito "
        "guardião do rio, feito de luz e neblina."
    )
    digitar(
        "\n\"Ninguém atravessa sem oferecer algo em troca\", sussurra "
        "a figura, com uma voz que soa como água correndo sobre pedras."
    )
    pausa()

    print("\nO que você faz?")
    escolha = escolher({
        "1": "Oferecer um item que carrega consigo",
        "2": "Tentar atravessar à força pela correnteza",
    })

    if escolha == "1" and jogador.inventario:
        jogador.ganhar_sabedoria(1)
        item_oferecido = jogador.inventario[0]
        digitar(
            f"\nVocê entrega {item_oferecido.replace('_', ' ')} ao "
            f"espírito, que o segura com reverência antes de dissolvê-lo "
            f"em luz. Em troca, ele lhe entrega um frasco de água que "
            f"brilha sob a lua."
        )
        jogador.adicionar_item("essencia_do_rio")
    elif escolha == "1":
        digitar(
            "\nVocê procura algo para oferecer, mas suas mãos estão "
            "vazias. O espírito balança a cabeça, desapontado, e afunda "
            "de volta na água sem lhe dar passagem fácil."
        )
        jogador.alterar_vida(-18)
    else:
        jogador.ganhar_coragem(1)
        digitar(
            "\nVocê avança pela correnteza gelada. A água é mais forte "
            "do que parece, e você é jogado contra as pedras antes de "
            "conseguir alcançar a outra margem, exausto e ferido."
        )
        jogador.alterar_vida(-40)

    if not jogador.esta_vivo():
        return "final_tragico"

    pausa()
    return "confronto_final"


def torre_do_feiticeiro(jogador):
    limpar_tela()
    digitar(
        "A Torre do Feiticeiro se ergue torta entre as rochas, como se "
        "tivesse sido construída por mãos distraídas. No topo, Aurelin, "
        "o último feiticeiro do vale, observa você chegar sem surpresa."
    )
    digitar(
        "\n\"Muitos vêm até aqui buscando poder\", ele diz. \"Vou saber "
        "em um instante o que você busca de verdade.\""
    )
    pausa()

    print("\nAurelin propõe um teste. O que você faz?")
    escolha = escolher({
        "1": "Aceitar o teste de Aurelin com calma",
        "2": "Recusar o teste e seguir seu caminho",
    })

    if escolha == "1":
        jogador.ganhar_sabedoria(1)
        digitar(
            "\nAurelin faz apenas uma pergunta: \"O que pesa mais, o "
            "medo de falhar ou o arrependimento de nunca tentar?\" "
            "Sua resposta, sincera e sem pressa, parece satisfazê-lo."
        )
        digitar(
            "\nEle lhe entrega um pergaminho com símbolos antigos. "
            "\"Isso vai lhe mostrar o caminho certo quando a escuridão "
            "tentar confundir seus olhos.\""
        )
        jogador.adicionar_item("pergaminho_do_feiticeiro")
    else:
        digitar(
            "\nVocê recusa educadamente. Aurelin dá de ombros e volta "
            "a observar o horizonte, sem insistir. Você segue sem "
            "ganhar nada, mas também sem perder nada."
        )

    pausa()
    return "confronto_final"


# ------------------------------------------------------------------ #
#  CONFRONTO FINAL — decide qual final o jogador alcança
# ------------------------------------------------------------------ #
def confronto_final(jogador):
    limpar_tela()
    linha("═")
    digitar("           O SALÃO DA ÚLTIMA CHAMA")
    linha("═")
    digitar(
        "\nApós dias de jornada, você encontra a caverna final: um "
        "salão de gelo onde a Última Chama de Eldareth queima, "
        "pequena, azul e solitária, no centro de um altar de pedra."
    )
    digitar(
        "\nDiante dela, um Guardião das Cinzas — uma armadura vazia "
        "movida por brasas antigas — barra sua passagem, esperando "
        "para ver quem realmente é você."
    )
    jogador.status()
    pausa()

    tem_amuleto = jogador.tem_item("amuleto_da_anciã")
    tem_cristal = jogador.tem_item("fragmento_de_cristal")
    tem_essencia = jogador.tem_item("essencia_do_rio")
    tem_pergaminho = jogador.tem_item("pergaminho_do_feiticeiro")

    itens_dos_três_caminhos = sum([tem_cristal, tem_essencia, tem_pergaminho])

    # A ordem importa: do final mais completo ao mais neutro.
    if tem_amuleto and itens_dos_três_caminhos >= 1 and jogador.sabedoria >= 3:
        return "final_secreto"       # ajudou, refletiu e persistiu em todas as frentes
    if tem_amuleto and jogador.coragem >= 1:
        return "final_heroico"       # confiança da anciã + um ato real de coragem
    if jogador.sabedoria >= 2:
        return "final_sabio"         # venceu pela cautela e pela reflexão, não pela força
    if jogador.vida <= 60:
        return "final_sombrio"       # sobreviveu, mas pagando um preço alto pelo caminho
    return "final_covarde"           # chegou inteiro, mas sem ter provado nada de si mesmo


# ------------------------------------------------------------------ #
#  FINAIS
# ------------------------------------------------------------------ #
def final_heroico(jogador):
    limpar_tela()
    linha("═")
    digitar("   FINAL: O HERÓI DE ELDARETH")
    linha("═")
    digitar(
        f"\nO Guardião das Cinzas ergue sua lâmina de brasa, mas o "
        f"amuleto da anciã Ovena brilha em seu peito, afastando o "
        f"medo. Com passos firmes, {jogador.nome} avança e retira a "
        f"Chama do altar sem hesitar."
    )
    jogador.adicionar_item("chama_de_eldareth")
    digitar(
        "\nO Guardião se desfaz em cinzas, como se apenas esperasse "
        "por alguém corajoso o bastante. Quando você retorna a "
        "Cinza-Alta com a Chama nas mãos, o gelo dos telhados começa "
        "a derreter pela primeira vez em sete invernos."
    )
    digitar(
        f"\nOvena chora ao ver a luz voltar ao vale. Os moradores que "
        f"restaram passam a chamar {jogador.nome} de 'o herói que "
        f"devolveu o verão'. Fim."
    )
    return None


def final_sabio(jogador):
    limpar_tela()
    linha("═")
    digitar("   FINAL: O SÁBIO SILENCIOSO")
    linha("═")
    digitar(
        f"\nO Guardião das Cinzas pergunta, com uma voz de brasa "
        f"crepitante: \"O que você busca de verdade?\" {jogador.nome} "
        f"responde com calma, citando tudo o que aprendeu no caminho "
        f"— o enigma dos cristais, a troca justa do rio, a pergunta "
        f"de Aurelin."
    )
    digitar(
        "\nO Guardião abaixa sua lâmina. \"Poucos chegam até aqui "
        "entendendo mais do que buscando.\" Ele se afasta e permite "
        "que você retire a Chama sem lutar."
    )
    jogador.adicionar_item("chama_de_eldareth")
    digitar(
        "\nVocê retorna ao vale não como um guerreiro, mas como "
        "alguém que ouviu com atenção cada aviso do caminho. O vale "
        "volta a florescer, devagar, mas de forma duradoura. Fim."
    )
    return None


def final_sombrio(jogador):
    limpar_tela()
    linha("═")
    digitar("   FINAL: A CHAMA AMARGA")
    linha("═")
    digitar(
        f"\nFerido e exausto, {jogador.nome} enfrenta o Guardião das "
        f"Cinzas com o que resta de forças. A luta é dura, e você "
        f"consegue arrancar a Chama do altar por pouco, caindo de "
        f"joelhos logo em seguida."
    )
    jogador.adicionar_item("chama_de_eldareth")
    digitar(
        "\nVocê sobrevive, mas as cicatrizes da jornada nunca "
        "desaparecem de verdade. O vale volta a aquecer, e as "
        "pessoas comemoram — mas você observa tudo de longe, sabendo "
        "o preço real que pagou por essa vitória. Fim."
    )
    return None


def final_covarde(jogador):
    limpar_tela()
    linha("═")
    digitar("   FINAL: O INVERNO ETERNO")
    linha("═")
    digitar(
        f"\nDiante do Guardião das Cinzas, {jogador.nome} hesita um "
        f"segundo a mais do que deveria. Sem amuleto, sem sabedoria "
        f"suficiente, sem coragem provada, o Guardião empurra você "
        f"para fora do salão antes que a Chama sequer seja tocada."
    )
    digitar(
        "\nVocê volta para Cinza-Alta de mãos vazias. O inverno "
        "continua, e talvez outro viajante, mais preparado, precise "
        "tentar o que você não conseguiu terminar. Fim."
    )
    return None


def final_secreto(jogador):
    limpar_tela()
    linha("═")
    digitar("   FINAL SECRETO: O VERDADEIRO GUARDIÃO")
    linha("═")
    digitar(
        f"\nO Guardião das Cinzas para no meio do movimento. Ele "
        f"reconhece o amuleto de Ovena, o brilho da essência do rio, "
        f"o fragmento de cristal que ainda canta baixinho em seu "
        f"bolso — sinais de alguém que percorreu o vale inteiro, "
        f"ajudando e aprendendo em cada trilha."
    )
    digitar(
        "\n\"Você não veio apenas buscar a Chama\", diz o Guardião, "
        "sua voz de brasa suavizando pela primeira vez em séculos. "
        "\"Você veio cuidar do vale.\""
    )
    digitar(
        f"\nA armadura se abre como uma porta, revelando que dentro "
        f"dela não havia nada além de cinzas guardando um segredo: "
        f"a própria Chama já reconhecia {jogador.nome} havia tempo."
    )
    jogador.adicionar_item("chama_de_eldareth")
    digitar(
        "\nQuando você retorna ao vale, a neve derrete em um único "
        "dia. Não é apenas o calor que volta a Eldareth — é a "
        "confiança das pessoas em dias melhores. Você se torna parte "
        "da lenda que um dia alguém mais vai contar a outro viajante "
        "perdido. Fim verdadeiro."
    )
    return None


def final_tragico(jogador):
    limpar_tela()
    linha("═")
    digitar("   FINAL: AS CINZAS DO VIAJANTE")
    linha("═")
    digitar(
        f"\nOs ferimentos acumulados ao longo do caminho são demais "
        f"para {jogador.nome} suportar. Em algum ponto da jornada, "
        f"suas forças se esvaem antes que a Chama de Eldareth possa "
        f"ser alcançada."
    )
    digitar(
        "\nO vale permanece congelado, e seu nome se junta à lista de "
        "viajantes que tentaram e não voltaram. Talvez a próxima "
        "pessoa a tentar aprenda com os seus erros. Fim."
    )
    return None
