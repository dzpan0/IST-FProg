# int_to_char: int → str
def int_para_letra(n):
    """Converte um inteiro para uma letra maiúscula.

    :param n: Inteiro correspondente à posição de uma letra no alfabeto

    :return: Letra correspondente ao inteiro
    """
    salto = ord("A")
    return chr(n + salto - 1)


# obtem_col_lin: intersecao → tuplo
def obtem_col_lin(inter):
    """Recebe uma interseção e devolve um tuplo que contém a coluna e linha da interseção."""
    return obtem_col(inter), obtem_lin(inter)


# lista_letras_col: goban → tuplo
def lista_letras_col(goban):
    """Devolve um tuplo contendo todas as letras das colunas do goban."""
    lim_inter = obtem_ultima_intersecao(goban)
    return [int_para_letra(col) for col in range(1, obtem_lin(lim_inter) + 1)]


# eh_coluna_goban: goban × str → booleano
def eh_coluna_goban(goban, col):
    """Verifica se uma coluna existe no goban."""
    lim_inter = obtem_ultima_intersecao(goban)
    return "A" <= col <= obtem_col(lim_inter)


# eh_linha_goban: goban × int → booleano
def eh_linha_goban(goban, lin):
    """Verifica se uma linha existe no goban."""
    lim_inter = obtem_ultima_intersecao(goban)
    return 1 <= lin <= obtem_lin(lim_inter)


# eh_numero: str → booleano
def eh_str_numero(str_num):
    """Verifica se uma cadeia de caracteres é formado por números.

    :param str_num: String a ser verificada

    :return: True se str_num corresponder a apenas números, False caso contrário
    """
    try:
        int(str_num)
        return True
    except ValueError:
        return False


# obtem_intersecoes: goban → tuplo
def obtem_intersecoes(goban):
    """Recebe um goban e devolve um tuplo, ordenado, com todas as interseções do goban."""
    cols = lista_letras_col(goban)
    inters = [cria_intersecao(col, lin) for col in cols for lin in range(1, len(cols) + 1)]

    return ordena_intersecoes(inters)
#----------------------------------------------------------------------------------------------------------------------#


# TAD interseção -> tuplo: (coluna, linha)
# cria_intersecao: str × int → intersecao
def cria_intersecao(col, lin):
    """Cria uma interseção.

    :param col: String contendo a letra da coluna da interseção
    :param lin: Inteiro correspondente à linha da interseção

    :return: Um tuplo que representa a interseção
    :raise ValueError: Se algum dos argumentos dados for inválido
    """
    if (not (type(col) is str and type(lin) is int) or len(col) != 1
            or not ("A" <= col <= "Z" and 1 <= lin <= 19)):
        raise ValueError("cria_intersecao: argumentos invalidos")
    return col, lin


# obtem_col: intersecao → str
def obtem_col(inter):
    """Recebe uma interseção e devolve a coluna da interseção."""
    return inter[0]


# obtem_lin: intersecao → int
def obtem_lin(inter):
    """Recebe uma interseção e devolve a linha da interseção."""
    return inter[1]


# eh_intersecao: universal → booleano
def eh_intersecao(arg):
    """Recebe um argumento de qualquer tipo e avalia se corresponde a uma interseção."""
    if isinstance(arg, tuple):
        return (len(arg) == 2 and isinstance(arg[0], str) and isinstance(arg[1], int) and len(arg[0]) == 1
                and "A" <= arg[0] <= "S" and 1 <= arg[1] <= 19)
    return False


# intersecoes_iguais: universal × universal → booleano
def intersecoes_iguais(inter1, inter2):
    """Verifica se duas interseções são iguais.

    :return: True se os dois argumentos são interseções e são iguais, e False caso contrário
    """
    if eh_intersecao(inter1) and eh_intersecao(inter2):
        return obtem_col(inter1) == obtem_col(inter2) and obtem_lin(inter1) == obtem_lin(inter2)
    return False


# intersecao_para str: intersecao → str
def intersecao_para_str(inter):
    """Cria uma cadeia de caracteres correspondente à representação de uma interseção.

    :return: String que representa a interseção
    """
    return f"{obtem_col(inter)}{obtem_lin(inter)}"


# str_para_intersecao: str → intersecao
def str_para_intersecao(str_inter):
    """Cria uma interseção representada pelo argumento.

    :param str_inter: String que representa uma interseção

    :return: Interseção criada
    """
    return cria_intersecao(str_inter[0], int(str_inter[1:]))


# obtem_intersecoes_adjacentes: intersecao × intersecao → tuplo
def obtem_intersecoes_adjacentes(inter, lim_inter):
    """Determina todas as interseções adjacentes à interseção inters.

    :param inter: Uma interseção
    :param lim_inter: Interseção superior direita do tabuleiro de Go

    :return: Tuplo contendo as interseções adjacentes ordenado à ordem de leitura do tabuleiro
    """
    col = obtem_col(inter)
    lin = obtem_lin(inter)

    # Obter os limites do tabuleiro
    max_col = obtem_col(lim_inter)
    max_lin = obtem_lin(lim_inter)

    # Possibilidades de interseções adjacentes por ordem
    passos = (lin - 1, chr(ord(col) - 1), chr(ord(col) + 1), lin + 1)

    inters_adj = ()
    for act, passo in enumerate(passos):
        if (act == 0 or act == 3) and 1 <= passo <= max_lin:  # Adjacentes na mesma coluna
            inters_adj += ((cria_intersecao(col, passo)),)
        elif (act == 1 or act == 2) and "A" <= passo <= max_col:  # Adjacentes na mesma linha
            inters_adj += ((cria_intersecao(passo, lin)),)

    return inters_adj


# ordena_intersecoes: tuplo → tuplo
def ordena_intersecoes(intersecoes):
    """Ordena um tuplo de interseções de acordo com a ordem de leitura do tabuleiro."""
    return tuple(sorted(intersecoes, key=lambda x: (obtem_lin(x), obtem_col(x))))


# TAD pedra -> str: "X", "O", "."
# cria_pedra_branca: {} → pedra
def cria_pedra_branca():
    """Cria uma pedra branca."""
    return "O"


# cria_pedra_preta: {} → pedra
def cria_pedra_preta():
    """Cria uma pedra preta."""
    return "X"


# cria_pedra_neutra: {} → pedra
def cria_pedra_neutra():
    """Cria uma pedra neutra."""
    return "."


# eh_pedra: universal → booleano
def eh_pedra(arg):
    """Recebe um argumento de qualquer tipo e avalia se corresponde a uma pedra."""
    return arg == "O" or arg == "X" or arg == "."


# eh_pedra_branca: pedra → booleano
def eh_pedra_branca(pedra):
    """Recebe uma pedra e verifica se corresponde a uma pedra branca."""
    return pedra == "O"


# eh_pedra_preta: pedra → booleano
def eh_pedra_preta(pedra):
    """Recebe uma pedra e verifica se corresponde a uma pedra preta."""
    return pedra == "X"


# pedras_iguais: universal × universal → boolean
def pedras_iguais(pedra1, pedra2):
    """Verifica se duas pedras são iguais.

    :return: True se os dois argumentos são pedras e são iguais, e False caso contrário
    """
    if eh_pedra(pedra1) and eh_pedra(pedra2):
        return pedra1 == pedra2
    return False


# pedra_para_str: pedra → str
def pedra_para_str(pedra):
    """Recebe uma pedra e devolve a cadeia de caracteres que representa o jogador dono da pedra."""
    return pedra


# eh_pedra_jogador: pedra → booleano
def eh_pedra_jogador(pedra):
    """Recebe uma pedra e avalia se é ou não de um jogador."""
    return eh_pedra_preta(pedra) or eh_pedra_branca(pedra)


# TAD goban -> dict: {coluna: {linha: pedra}}
# cria_goban_vazio: int → goban
def cria_goban_vazio(n):
    """Cria um goban de tamanho n×n, sem interseções ocupadas.

    :param n: Inteiro correspondente à dimensão do goban: 9, 13 ou 19

    :return: Um goban vazio
    :raise ValueError: Se o argumento dado for inválido
    """
    if not (isinstance(n, int) and n in (9, 13, 19)):
        raise ValueError("cria_goban_vazio: argumento invalido")

    goban = dict()
    for i in range(1, n + 1):
        col = int_para_letra(i)
        lin = {j: None for j in range(1, n + 1)}
        goban[col] = lin

    return goban


# cria_goban: int × tuplo × tuplo → goban
def cria_goban(n, inters_b, inters_p):
    """Cria um goban de tamanho n×n.

    :param n: Inteiro correspondente à dimensão do goban: 9, 13 ou 19
    :param inters_b: Tuplo contendo as interseções ocupadas por pedras brancas
    :param inters_p: Tuplo contendo as interseções ocupadas por pedras pretas

    :return: Um goban com interseções em inters_b e inters_p ocupadas por pedras brancas e pretas, respetivamente
    :raise ValueError: Se algum dos argumentos dados for inválido
    """
    if not (isinstance(n, int) and n in (9, 13, 19) and isinstance(inters_b, tuple) and isinstance(inters_p, tuple)
            and all(eh_intersecao(ib) and eh_intersecao_valida(cria_goban_vazio(n), ib) and ib not in inters_p
                    and inters_b.count(ib) == 1 for ib in inters_b)
            and all(eh_intersecao(ip) and eh_intersecao_valida(cria_goban_vazio(n), ip)
                    and inters_p.count(ip) == 1 for ip in inters_p)):
        raise ValueError("cria_goban: argumentos invalidos")

    goban = cria_goban_vazio(n)

    for inter in inters_b:
        col, lin = obtem_col_lin(inter)
        goban[col][lin] = cria_pedra_branca()

    for inter in inters_p:
        col, lin = obtem_col_lin(inter)
        goban[col][lin] = cria_pedra_preta()

    return goban


# cria_copia_goban: goban → goban
def cria_copia_goban(goban):
    """Cria uma cópia do goban passado como argumento.

    :param goban: O goban a ser copiado

    :return: Uma cópia do goban
    """
    copia = dict()

    for col, linhas in goban.items():
        copia[col] = {lin: cria_pedra_branca() if eh_pedra_branca(pedra) else cria_pedra_preta()
                      if pedra is not None else None for lin, pedra in linhas.items()}

    return copia


# obtem_ultima_intersecao: goban → intersecao
def obtem_ultima_intersecao(goban):
    """Devolve a última interseção do goban."""
    n = len(goban)  # Obtem o número de linhas e colunas do tabuleiro
    ultima_coluna = int_para_letra(n)
    ultima_linha = n

    return cria_intersecao(ultima_coluna, ultima_linha)


# obtem_pedra: goban × intersecao → pedra
def obtem_pedra(goban, inter):
    """Devolve a pedra na interseção dada.

    :param goban: Um goban
    :param inter: Uma interseção do goban

    :return: A pedra que ocupa a interseção inter ou uma pedra neutra se não estiver ocupada
    """
    col, lin = obtem_col_lin(inter)
    pedra = goban[col][lin]

    if eh_pedra_branca(pedra):
        return cria_pedra_branca()
    elif eh_pedra_preta(pedra):
        return cria_pedra_preta()
    else:
        return cria_pedra_neutra()


# obtem_cadeia: goban × intersecao → tuplo
def obtem_cadeia(goban, inter):
    """Encontra todas as interseções que estão conectadas à interseção recebida.

    :param goban: Um goban
    :param inter: Uma interseção pertencente ao goban

    :return: Tuplo contendo interseções conectadas, ordenado à ordem de leitura
    :raise ValueError: Se algum dos argumentos for inválido
    """

    def add_adj(inter, cadeia):
        cadeia.add(inter)
        inters_adj = obtem_intersecoes_adjacentes(inter, ultima_inter)

        for adjacente in inters_adj:
            if adjacente not in cadeia and pedras_iguais(obtem_pedra(goban, adjacente), pedra_cadeia):
                add_adj(adjacente, cadeia)

    cadeia = set()
    ultima_inter = obtem_ultima_intersecao(goban)
    pedra_cadeia = obtem_pedra(goban, inter)

    add_adj(inter, cadeia)

    return ordena_intersecoes(cadeia)


# coloca_pedra: goban × intersecao × pedra → goban
def coloca_pedra(goban, inter, pedra):
    """Modifica destrutivamente um goban, colocando uma pedra na interseção dada.

    :param goban: Um goban
    :param inter: Uma interseção do goban
    :param pedra: Uma pedra de um jogador que irá ser colocada na interseção inter

    :return: O próprio goban após a colocação da pedra
    """
    col, lin = obtem_col_lin(inter)
    goban[col][lin] = pedra
    return goban


# remove_pedra: goban × intersecao → goban
def remove_pedra(goban, inter):
    """Modifica destrutivamente um goban, removendo a pedra da interseção dada.

    :param goban: Um goban
    :param inter: Uma interseção do goban

    :return: O próprio goban após a remoção
    """
    col, lin = obtem_col_lin(inter)
    goban[col][lin] = None
    return goban


# remove_cadeia: goban × tuplo → goban
def remove_cadeia(goban, tup):
    """Modifica destrutivamente um goban, removendo todas as pedras nas interseções do tuplo dado.

    :param goban: Um goban
    :param tup: Um tuplo com interseção do goban

    :return: O próprio goban após a remoção
    """
    for inter in tup:
        remove_pedra(goban, inter)
    return goban


# eh_goban: universal → booleano
def eh_goban(arg):
    """Recebe um argumento de qualquer tipo e avalia se corresponde a um goban."""
    if not isinstance(arg, dict) or len(arg) not in (9, 13, 19):
        return False

    n = len(arg)
    for col, linhas in arg.items():
        if not (isinstance(col, str) and len(col) == 1 and "A" <= col <= int_para_letra(n)
                and isinstance(linhas, dict) and len(linhas) == len(arg)
                and all(isinstance(lin, int) and 1 <= lin <= n for lin in linhas)
                and all(eh_pedra_jogador(pedra) or pedra is None for pedra in linhas.values())):
            return False

    return True


# eh_intersecao_valida: goban × intersecao → booleano
def eh_intersecao_valida(goban, inter):
    """Recebe um goban e uma interseção e verifica se a interseção pertence ao goban."""
    return eh_coluna_goban(goban, obtem_col(inter)) and eh_linha_goban(goban, obtem_lin(inter))


# gobans_iguais: universal × universal → booleano
def gobans_iguais(goban1, goban2):
    """Verifica se dois gobans são iguais.

    :return: True se os dois argumentos são gobans e são iguais, e False caso contrário
    """
    if eh_goban(goban1) and eh_goban(goban2):
        inters1 = obtem_intersecoes(goban1)
        inters2 = obtem_intersecoes(goban2)

        if len(inters1) == len(inters2):
            for inter1, inter2 in zip(inters1, inters2):
                pedra1 = obtem_pedra(goban1, inter1)
                pedra2 = obtem_pedra(goban2, inter2)

                if not pedras_iguais(pedra1, pedra2):
                    break
            else:
                return True
    return False


# goban_para_str: goban → str
def goban_para_str(goban):
    """Cria uma cadeia de caracteres correspondente à representação de um goban.

    :param goban: Um goban

    :return: Cadeia de caracteres que representa o goban
    """
    ultima_inter = obtem_ultima_intersecao(goban)
    n = obtem_lin(ultima_inter)  # Tamanho do goban

    list_cols = lista_letras_col(goban)  # Cria uma lista com as letras das colunas
    str_cols = " ".join(list_cols)

    res = "   " + str_cols + "\n"

    for i in range(n, 0, -1):
        res += f"{i: >2}"

        for col in list_cols:
            pedra = obtem_pedra(goban, cria_intersecao(col, i))
            res += f" {pedra_para_str(pedra)}"
        res += f"{i: >3}\n"

    return res + "   " + str_cols


# obtem_territorios: goban → tuplo
def obtem_territorios(goban):
    """Procura todos os territórios de um goban e as interseções que os formam.

    :param goban: Um goban

    :return: Tuplo contendo tuplos de territórios com todas as interseções de cada território,
    ordenado à ordem de leitura
    """
    territorios = []
    livres_analisados = []  # Ratreia as interseções livres que já foram analisadas

    for inter in obtem_intersecoes(goban):
        pedra = obtem_pedra(goban, inter)

        if not (eh_pedra_jogador(pedra) or inter in livres_analisados):
            terr = obtem_cadeia(goban, inter)
            livres_analisados.extend(terr)
            territorios.append(terr)

    return tuple(sorted(territorios, key=lambda x: (obtem_lin(x[0]), obtem_col(x[0]))))


# obtem_adjacentes_diferentes: goban × tuplo → tuplo
def obtem_adjacentes_diferentes(goban, tup):
    """Procura todas as interseções adjacentes de tipos diferentes às das interseções do tuplo dado

    :param goban: Um goban
    :param tup: Tuplo formado por interseções

    :return: Tuplo, ordenado, formado pelas interseções adjacentes livres, se as interseções do tuplo tup estão
    ocupadas por pedras de jogador, ou ocupadas por pedras de jogador, se o tuplo tup for formado por interseções livres
    """
    adj_dif = set()
    ultima_inter = obtem_ultima_intersecao(goban)

    for origin in tup:
        # Se True procura as liberdades de uma cadeia de pedras, caso contrário a fronteira de um território
        tipo = eh_pedra_jogador(obtem_pedra(goban, origin))

        for adjacente in obtem_intersecoes_adjacentes(origin, ultima_inter):
            pedra_adj = obtem_pedra(goban, adjacente)

            if adjacente not in adj_dif and eh_pedra_jogador(pedra_adj) != tipo:
                adj_dif.add(adjacente)

    return ordena_intersecoes(adj_dif)


# jogada: goban × intersecao × pedra → goban
def jogada(goban, inter, pedra):
    """Modifica destrutivamente um goban, colocando uma pedra numa interseção e removendo todas as pedras do jogador
    contrário pertencentes a cadeias adjacentes da interseção sem liberdades.

    :param goban: Um goban
    :param inter: Uma interseção do goban onde a pedra irá ser colocada
    :param pedra: Uma pedra de um jogador

    :return: O próprio goban após colocar a pedra e remover as pedras do jogador contrário
    """
    coloca_pedra(goban, inter, pedra)

    for adjacente in obtem_intersecoes_adjacentes(inter, obtem_ultima_intersecao(goban)):
        pedra_adj = obtem_pedra(goban, adjacente)
        cadeia_adj = obtem_cadeia(goban, adjacente)

        # Remove a cadeia de pedras sem liberdades do jogador adversário
        if (eh_pedra_jogador(pedra_adj) and not pedras_iguais(pedra, pedra_adj)
                and len(obtem_adjacentes_diferentes(goban, cadeia_adj)) == 0):
            remove_cadeia(goban, cadeia_adj)

    return goban


# obtem_pedras_jogadores: goban → tuplo
def obtem_pedras_jogadores(goban):
    """Calcula o número de pedras de cada jogador no goban.

    :param goban: Um goban

    :return: Um tuplo de dois inteiros que correspondem ao número de interseções ocupadas por pedras do
    jogador branco e preto, respetivamente.
    """
    pedras_brancas = 0
    pedras_pretas = 0
    inters = obtem_intersecoes(goban)

    for inter in inters:
        aux_pedra = obtem_pedra(goban, inter)

        if pedras_iguais(aux_pedra, cria_pedra_branca()):
            pedras_brancas += 1
        if pedras_iguais(aux_pedra, cria_pedra_preta()):
            pedras_pretas += 1

    return pedras_brancas, pedras_pretas


# calcula_pontos: goban → tuple
def calcula_pontos(goban):
    """Recebe um goban e devolve um tuplo de dois inteiros com a pontuação dos
    jogadores branco e preto, respetivamente."""
    pontuacao_brancas, pontuacao__pretas = obtem_pedras_jogadores(goban)
    all_terr = obtem_territorios(goban)

    for terr in all_terr:
        # Tuplo constituido pelas interseções que formam a fronteiras de um território
        fronteira = obtem_adjacentes_diferentes(goban, terr)
        if len(fronteira) == 0:
            continue

        # Se todas as interseções adjacentes forem ocupadas por pedras brancas ou todas por pedras pretas,
        # adiciona pontos à pontuacao_branca ou pontuacao_preta, respetivamente
        if all(eh_pedra_branca(obtem_pedra(goban, adjacente)) for adjacente in fronteira):
            pontuacao_brancas += len(terr)
        elif all(eh_pedra_preta(obtem_pedra(goban, adjacente)) for adjacente in fronteira):
            pontuacao__pretas += len(terr)

    return pontuacao_brancas, pontuacao__pretas


# eh_jogada_legal: goban × intersecao × pedra × goban → booleano
def eh_jogada_legal(goban, inter, pedra, last):
    """Verifica se uma jogada é legal.

    :param goban: Um goban
    :param inter: Uma interseção do goban onde a pedra irá ser colocada
    :param pedra: Uma pedra de um jogador
    :param last: O estado do tabuleiro que não pode ser obtido após a resolução completa da jogada

    :return: True se a jogada for legal e False caso contrário
    """
    if not eh_intersecao_valida(goban, inter) or eh_pedra_jogador(obtem_pedra(goban, inter)):
        return False

    copia = cria_copia_goban(goban)
    jogada(copia, inter, pedra)

    # Liberdades da cadeia de pedras constituída pelas pedras conectadas à pedra colocada na jogada
    liberdades = obtem_adjacentes_diferentes(copia, obtem_cadeia(copia, inter))

    return not gobans_iguais(copia, last) and len(liberdades) != 0


# turno_jogador: goban × pedra × goban → booleano
def turno_jogador(goban, pedra, last):
    """
    Função auxiliar para o turno de um jogador. Se o comando introduzido for uma interseção válida, irá ser realizado a
    jogada.

    :param goban: Um goban
    :param pedra: A pedra do jogador que está a jogar
    :param last: O estado do tabuleiro que não pode ser obtido após a resolução completa da jogada

    :return: True se o jogador realiza uma jogada válida, False se passar o turno
    """
    while True:
        command = input(f"Escreva uma intersecao ou 'P' para passar [{pedra_para_str(pedra)}]:")

        if command == "P":
            return False

        if not (len(command) in (2, 3) and eh_coluna_goban(goban, command[0])
                and eh_str_numero(command[1:]) and eh_linha_goban(goban, int(command[1:]))):
            continue

        inter = str_para_intersecao(command)
        if eh_jogada_legal(goban, inter, pedra, last):
            jogada(goban, inter, pedra)
            return True


# tabuleiro_atual: goban × int × int
def tabuleiro_atual(goban, pontos_b, pontos_p):
    """Mostra a pontuação de cada jogador e o estado do tabuleiro no início do turno."""
    print(f"Branco (O) tem {pontos_b} pontos\nPreto (X) tem {pontos_p} pontos")
    print(goban_para_str(goban))


# go: int × tuple × tuple → booleano
def go(n, inters_b, inters_p):
    """
    Função principal para jogar um jogo completo de Go entre dois jogadores.

    :param n: Inteiro correspondente à dimensão do goban: 9, 13 ou 19
    :param inters_b: Um tuplo com a representação externa das interseções ocupadas por pedras brancas inicialmente
    :param inters_p: Um tuplo com a representação externa das interseções ocupadas por pedras pretas inicialmente

    :return: True se o jogador com pedras brancas ganhar o jogo, False caso contrário
    :raise ValueError: Se algum dos argumentos não for válido
    """
    try:
        if not (n in (9, 13, 19) and isinstance(inters_b, tuple) and isinstance(inters_p, tuple)
                and all(isinstance(ib, str) and "A" <= ib[0] <= int_para_letra(n)
                        and int(ib[1:]) <= n and ib not in inters_p for ib in inters_b)
                and all(isinstance(ip, str) and "A" <= ip[0] <= int_para_letra(n)
                        and int(ip[1:]) <= n for ip in inters_p)):
            raise ValueError("go: argumentos invalidos")
    except ValueError:  # Apanha o erro de conversão int()
        raise ValueError("go: argumentos invalidos")

    inters_b = tuple(str_para_intersecao(ib) for ib in inters_b)
    inters_p = tuple(str_para_intersecao(ip) for ip in inters_p)

    goban = cria_goban(n, inters_b, inters_p)
    pedra = cria_pedra_preta()
    passar = 0
    last_2turnos = cria_goban_vazio(n)   # Estado do tabuleiro que não pode ser obtido após uma jogada

    pontos_branco, pontos_preto = (0, 0) if gobans_iguais(cria_goban_vazio(n), goban) else calcula_pontos(goban)
    tabuleiro_atual(goban, pontos_branco, pontos_preto)

    while passar != 2:
        last_turno = cria_copia_goban(goban)

        if not turno_jogador(goban, pedra, last_2turnos):
            passar += 1
        else:
            passar = 0

        last_2turnos, last_turno = last_turno, cria_copia_goban(goban)
        pontos_branco, pontos_preto = calcula_pontos(goban)
        tabuleiro_atual(goban, pontos_branco, pontos_preto)

        pedra = cria_pedra_branca() if eh_pedra_preta(pedra) else cria_pedra_preta()   # Troca o turno do jogador

    return True if pontos_branco >= pontos_preto else False
