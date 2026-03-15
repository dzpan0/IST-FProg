# char_to_ind: inteiro → string
def ind_to_char(n):
    """Converte index para letra

    :param n: Inteiro correspondente ao index do caminho vertical no tuplo do território
    :return: String correspondente à letra
    """
    salto = ord("A")
    return chr(n + salto)


# char_to_ind: string → inteiro
def char_to_ind(letra):
    """Converte letra para index

    :param letra: String contendo a letra correspondente ao caminho vertical
    :return: Inteiro correspondente ao index no tuplo do território
    """
    salto = ord("A")
    return ord(letra) - salto


# obtem_montanha: territorio → tuplo
def obtem_montanhas(terr):
    """Obtem todas as interseções ocupadas por montanhas do território

    :param terr: Tuplo correspondente ao território onde será efetuado a procura
    :return: Tuplo contendo todas as interseções ocupadas por montanhas do território,
    ordenado à ordem de leitura de um território
    """
    montanhas = ()

    for ind_vert, c_vert in enumerate(terr):
        if c_vert.count(1) == 0:  # Salta a iteração se o caminho vertical não conter montanhas
            continue

        letra_vert = ind_to_char(ind_vert)

        for ind_horiz, c_horiz in enumerate(c_vert):
            if c_horiz == 1:
                montanhas += ((letra_vert, ind_horiz + 1),)

    return ordena_intersecoes(montanhas)
# ----------------------------------------------------------------------------------------------------------------------#


# eh_territorio: universal → booleano
def eh_territorio(arg):
    """Recebe um argumento de qualquer tipo e avalia se corresponde a um território"""
    if isinstance(arg, tuple) and 1 <= len(arg) <= 26:
        for c_verti in arg:
            if (not isinstance(c_verti, tuple) or not 1 <= len(c_verti) <= 99 or len(c_verti) != len(arg[0])
                    or any((c_horiz != 0 and c_horiz != 1) or not isinstance(c_horiz, int) for c_horiz in c_verti)):
                break
        else:  # Corre apenas se o loop terminar sem interrupção (sem apanhar exceções)
            return True

    return False


# obtem_ultima_intersecao: territorio → intersecao
def obtem_ultima_intersecao(terr):
    """Devolve a última interseção do território"""
    return ind_to_char(len(terr) - 1), len(terr[-1])


# eh_intersecao: universal → booleano
def eh_intersecao(arg):
    """Recebe um argumento de qualquer tipo e avalia se corresponde a uma interseção"""
    if (isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[0], str) and isinstance(arg[1], int)
            and len(arg[0]) == 1 and 1 <= arg[1] <= 99 and "A" <= arg[0] <= "Z"):
        return True

    return False


# eh_intersecao_valida: territorio × intersecao → booleano
def eh_intersecao_valida(terr, inters):
    """Recebe um território e uma interseção e verifica se a interseção pertence ao território"""
    return 1 <= char_to_ind(inters[0]) + 1 <= len(terr) and 1 <= inters[1] <= len(terr[0])


# eh_intersecao_livre: territorio × intersecao → booleano
def eh_intersecao_livre(terr, inters):
    """Recebe um território e uma interseção e verifica se a interseção é livre"""
    cv = char_to_ind(inters[0])
    ch = inters[1] - 1

    return terr[cv][ch] == 0


# obtem_intersecoes_adjacentes: territorio × intersecao → tuplo
def obtem_intersecoes_adjacentes(terr, inters):
    """Determina todas as interseções adjacentes à interseção dada

    :param terr: Tuplo de um território
    :param inters: Tuplo de uma interseção do território
    :return: Tuplo contendo as interseções adjacentes ordenado à ordem de leitura de um território
    """
    c_vert = char_to_ind(inters[0])
    c_horiz = inters[1]
    passos = (c_horiz - 1, c_vert - 1, c_vert + 1, c_horiz + 1)  # Possibilidades de interseções adjacentes por ordem
    inters_adj = ()

    for act, passo in enumerate(passos):
        if 1 <= passo < len(terr[0]) + 1 and (act == 0 or act == 3):  # Adjacentes na mesma coluna
            inters_adj += ((inters[0], passo),)
        elif 0 <= passo < len(terr) and (act == 1 or act == 2):  # Adjacentes na mesma linha
            inters_adj += ((ind_to_char(passo), c_horiz),)

    return inters_adj


# ordena_intersecoes: tuplo → tuplo
def ordena_intersecoes(intersecoes):
    """Ordena um tuplo de interseções de acordo com a ordem de leitura de um território"""
    return tuple(sorted(intersecoes, key=lambda x: (x[1], x[0])))


# territorio_para_str: territorio → cad. carateres
def territorio_para_str(terr):
    """Cria uma cadeia de caracteres correspondente à representação de um território

    :param terr: Tuplo de um território
    :return: Uma cadeia de caracteres que representa o território
    :raise ValueError: Se argumento dado não corresponder a um território
    """
    if not eh_territorio(terr):
        raise ValueError("territorio_para_str: argumento invalido")

    # Cria uma string com as letras do caminho vertical (separadas por um espaço)
    str_vertical = " ".join([ind_to_char(c_vert) for c_vert in range(len(terr))])

    res = "   " + str_vertical + "\n"

    for passo_ch in range(len(terr[0]) - 1, -1, -1):  # Intera sobre os indices do caminho horizontal decrescentemente
        c_horiz = passo_ch + 1
        res += f"{c_horiz: >2}"

        for i in terr:
            res += f" ." if i[passo_ch] == 0 else f" X"  # Define o tipo de interseção que será adicionado à string res

        res += f"{c_horiz: >3}\n"

    return res + "   " + str_vertical


# obtem_cadeia: territorio × intersecao → tuplo
def obtem_cadeia(terr, inters):
    """Encontra todas as interseções que estão conectadas à interseção recebida

    :param terr: Tuplo de um território
    :param inters: Tuplo de uma interseção pertencente ao território
    :return: Um tuplo contendo interseções conectadas, ordenado à ordem de leitura de um território
    :raise ValueError: Se território ou interseção for inválido
    """
    if not (eh_territorio(terr) and eh_intersecao(inters) and eh_intersecao_valida(terr, inters)):
        raise ValueError("obtem_cadeia: argumentos invalidos")

    # Função recursiva que adiciona todas as interseções conectadas no set cadeia
    def add_adj(terr, inters, cadeia, tipo):
        cadeia.add(inters)
        inters_adj = obtem_intersecoes_adjacentes(terr, inters)

        for adjacente in inters_adj:
            if adjacente not in cadeia and eh_intersecao_livre(terr, adjacente) == tipo:
                add_adj(terr, adjacente, cadeia, tipo)

    cadeia = set()
    tipo = eh_intersecao_livre(terr, inters)   # Define o tipo da cadeia que será formada
    add_adj(terr, inters, cadeia, tipo)

    return ordena_intersecoes(list(cadeia))


# obtem_vale: territorio × intersecao → tuplo
def obtem_vale(terr, inters):
    """Cria um tuplo formado por todas as interseções correspondentes a vales da interseção recebida

    :param terr: Tuplo de um território
    :param inters: Tuplo de uma interseção ocupada por uma montanha pertencente ao território
    :return: Um tuplo com interseções correspondentes a vales ordenado à ordem de leitura de um território
    :raise ValueError: Se território ou interseção for inválido
    """
    if not (eh_territorio(terr) and eh_intersecao_valida(terr, inters)) or eh_intersecao_livre(terr, inters):
        raise ValueError("obtem_vale: argumentos invalidos")

    vales = ()
    cadeia_mont = obtem_cadeia(terr, inters)

    for montanha in cadeia_mont:
        for adjacente in obtem_intersecoes_adjacentes(terr, montanha):
            if eh_intersecao_livre(terr, adjacente) and adjacente not in vales:
                vales += (adjacente,)

    return ordena_intersecoes(vales)


# verifica_conexao: territorio × intersecao × intersecao → booleano
def verifica_conexao(terr, inters1, inters2):
    """Verifica se duas interseções de um mesmo território estão conectadas

    :raise ValueError: Se algum dos argumentos dados for inválido
    """
    if not (eh_territorio(terr) and eh_intersecao_valida(terr, inters1) and eh_intersecao_valida(terr, inters2)):
        raise ValueError("verifica_conexao: argumentos invalidos")

    cadeia = obtem_cadeia(terr, inters1)
    return inters2 in cadeia


# calcula_numero_montanhas: territorio → int
def calcula_numero_montanhas(terr):
    """Calcula o número de interseções ocupadas por montanhas no território

    :return: Inteiro correspondente ao resultado do cálculo
    :raise ValueError: Se argumento dado não corresponder a um território
    """
    if not eh_territorio(terr):
        raise ValueError("calcula_numero_montanhas: argumento invalido")

    return sum(c_vert.count(1) for c_vert in terr)


# calcula_numero_cadeias_montanhas: territorio → int
def calcula_numero_cadeias_montanhas(terr):
    """Calcula o número de cadeias formadas por interseções ocupadas por montanhas no território

    :return: Inteiro correspondente ao resultado do cálculo
    :raise ValueError: Se argumento dado não corresponder a um território
    """
    if not eh_territorio(terr):
        raise ValueError("calcula_numero_cadeias_montanhas: argumento invalido")

    mont_analisadas = []  # Lista que rastreia as montanhas que já foram analisadas
    n_cadeias = 0
    montanhas = obtem_montanhas(terr)

    for montanha in montanhas:
        if montanha not in mont_analisadas:
            mont_analisadas.extend(obtem_cadeia(terr, montanha))
            n_cadeias += 1

    return n_cadeias


# calcula_tamanho_vales: territorio → int
def calcula_tamanho_vales(terr):
    """Calcula o número total de interseções correspondentes a vales no território

    :return: Inteiro correspondente ao resultado do cálculo
    :raise ValueError: Se argumento dado não corresponder a um território
    """
    if not eh_territorio(terr):
        raise ValueError("calcula_tamanho_vales: argumento invalido")

    mont_analisadas = []   # Lista que rastreia as montanhas que já foram analisadas
    vales = []
    montanhas = obtem_montanhas(terr)

    for montanha in montanhas:
        if montanha not in mont_analisadas:
            mont_analisadas.extend(obtem_cadeia(terr, montanha))

            vale_aux = obtem_vale(terr, montanha)
            vales.extend(vale for vale in vale_aux if vale not in vales)

    return len(vales)
