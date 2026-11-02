import random


class HybridList:
    TAIL_LIMIT = 10

    def __init__(self, seed: int = 42):
        """Cria a região ordenada inicial com 1.024 números inteiros distintos.

        A mesma semente sempre gera os mesmos números. O gerador aleatório é
        local a esta instância, então inicializar a lista não altera a sequência
        aleatória usada pelo restante do programa.
        """
        rng = random.Random(seed)

        # ``sample`` seleciona números sem repetição dentro do intervalo informado.
        initial_keys = rng.sample(range(1, 100_000), 1_024)

        # A busca binária depende de a região principal estar em ordem crescente.
        self.ordered_region: list[int] = sorted(initial_keys)
        # Novas chaves ficam temporariamente aqui, sem precisar manter a ordem.
        self.tail: list[int] = []

    def search_key(self, key: int) -> dict[str, bool | str | int]:
        """Procura uma chave e devolve onde ela está e quantas iterações foram feitas.

        A busca binária é usada em ``ordered_region``. Só se a chave não estiver
        lá, a função percorre ``tail`` sequencialmente. O índice retornado é
        relativo à lista lógica formada por ``ordered_region`` seguida de
        ``tail``. A busca não modifica as listas.
        """
        return busca_hibrida(self.ordered_region, self.tail, key)

    def insert_key(self, key: int) -> bool:
        """Insere uma chave nova na cauda e informa se a inserção foi aceita.

        Chaves já presentes na região ordenada ou na cauda são rejeitadas. Ao
        atingir ``TAIL_LIMIT`` chaves acumuladas, a cauda é incorporada à região ordenada.
        Retorna ``True`` quando insere a chave e ``False`` quando ela é repetida.
        """
        # A lista mantém valores únicos; rejeita a chave se ela já estiver em qualquer parte.
        if key in self.ordered_region or key in self.tail:
            return False

        # A cauda recebe as novas chaves na ordem de chegada; ela não precisa estar ordenada.
        self.tail.append(key)

        # Ao atingir o limite, ordena e incorpora a cauda à região principal.
        if len(self.tail) >= self.TAIL_LIMIT:
            self._intercalate_and_clear_tail()

        return True

    def _intercalate_and_clear_tail(self) -> None:
        """Intercala a cauda à região ordenada e deixa a cauda vazia.

        A função é chamada quando a cauda chega ao limite de dez valores. Como
        as duas partes ficam ordenadas antes da intercalação, basta comparar
        seus próximos elementos para construir uma única região em ordem.
        """
        self.tail.sort()

        # Estes índices apontam para o próximo valor ainda não copiado de cada parte.
        indice_regiao = 0
        indice_cauda = 0
        regiao_intercalada = []

        # Compara os próximos valores e copia o menor, mantendo a ordem crescente.
        while (
            indice_regiao < len(self.ordered_region)
            and indice_cauda < len(self.tail)
        ):
            if self.ordered_region[indice_regiao] <= self.tail[indice_cauda]:
                regiao_intercalada.append(self.ordered_region[indice_regiao])
                indice_regiao += 1
            else:
                regiao_intercalada.append(self.tail[indice_cauda])
                indice_cauda += 1

        # Copia os elementos restantes da parte que ainda não foi totalmente lida.
        regiao_intercalada.extend(self.ordered_region[indice_regiao:])
        regiao_intercalada.extend(self.tail[indice_cauda:])

        # Substitui a região antiga pela combinação ordenada das duas partes.
        self.ordered_region = regiao_intercalada

        # Começa uma cauda vazia para receber as próximas inserções.
        self.tail = []


def busca_binaria(lista: list[int], chave: int) -> tuple[int, int]:
    """Procura uma chave em uma lista ordenada usando busca binária.

    Em cada iteração, examina o elemento do meio do trecho ainda possível.
    Como ``lista`` deve estar ordenada em ordem crescente, o valor desse
    elemento indica qual metade pode ser descartada. Se encontrar a chave,
    devolve seu índice e o número de iterações; se não encontrar, devolve
    ``-1`` e o total de iterações.

    Args:
        lista: Números inteiros em ordem crescente.
        chave: Número inteiro que será procurado.

    Returns:
        Um par ``(indice, iteracoes)``. ``indice`` é a posição da chave ou
        ``-1`` quando ela não aparece na lista. ``iteracoes`` conta quantos
        elementos do meio foram examinados, uma vez por passagem pelo laço.
    """
    # ``inicio`` e ``fim`` delimitam o trecho que ainda pode conter a chave.
    inicio = 0
    fim = len(lista) - 1
    iteracoes = 0

    # Continua enquanto houver pelo menos uma posição candidata entre os limites.
    while inicio <= fim:
        # Uma iteração corresponde a examinar um elemento do meio.
        iteracoes += 1
        meio = (inicio + fim) // 2

        # Se o meio contém a chave, seu índice é a resposta.
        if lista[meio] == chave:
            return meio, iteracoes

        # Se o valor do meio é menor, a chave só pode estar à direita dele.
        elif lista[meio] < chave:
            inicio = meio + 1

        # Caso contrário, a chave só pode estar à esquerda do meio.
        else:
            fim = meio - 1

    # Os limites se cruzaram: não restam posições possíveis para examinar.
    return -1, iteracoes


def busca_sequencial(lista: list[int], chave: int) -> tuple[int, int]:
    """Procura uma chave examinando os elementos um por um, do início ao fim.

    Esta busca funciona mesmo quando a lista não está ordenada. Ela para assim
    que encontra a primeira ocorrência da chave; se não encontrar, percorre a
    lista inteira.

    Args:
        lista: Números inteiros em qualquer ordem.
        chave: Número inteiro que será procurado.

    Returns:
        Um par ``(indice, iteracoes)``. ``indice`` é a posição da chave ou
        ``-1`` quando ela não aparece. ``iteracoes`` conta quantos elementos
        foram examinados.
    """
    iteracoes = 0

    # ``enumerate`` fornece, a cada passo, tanto a posição quanto o valor.
    for indice, numero in enumerate(lista):
        # Cada elemento examinado conta como uma iteração.
        iteracoes += 1

        # Ao achar a chave, devolve a posição local e encerra a busca.
        if numero == chave:
            return indice, iteracoes

    # O laço terminou sem encontrar a chave.
    return -1, iteracoes


def busca_hibrida(
    regiao_ordenada: list[int], cauda: list[int], chave: int
) -> dict[str, bool | str | int]:
    """Procura uma chave nas duas partes de uma lista híbrida.

    Primeiro usa busca binária na ``regiao_ordenada``. Se a chave não estiver
    lá, usa busca sequencial na ``cauda``, que pode não estar ordenada. O índice
    da cauda é convertido para um índice global, considerando a lista lógica
    ``regiao_ordenada + cauda``.

    Args:
        regiao_ordenada: Parte inicial da lista, ordenada em ordem crescente.
        cauda: Parte final da lista, mantida sem ordenação.
        chave: Número inteiro que será procurado.

    Returns:
        Um dicionário com:
        - ``encontrado``: ``True`` se a chave estiver em uma das partes.
        - ``regiao``: ``"Região ordenada"``, ``"Cauda"`` ou ``"Não encontrado"``.
        - ``indice_global``: posição na lista lógica completa ou ``-1``.
        - ``iteracoes_binarias`` e ``iteracoes_sequenciais``: trabalho feito
          por cada busca.
        - ``total_iteracoes``: soma das iterações das duas buscas.
    """
    # Pesquisa primeiro a parte ordenada, descartando metade dos candidatos por iteração.
    posicao_binaria, iteracoes_binarias = busca_binaria(regiao_ordenada, chave)

    # A busca sequencial só será executada se a chave não estiver na região ordenada.
    posicao_sequencial = -1
    iteracoes_sequenciais = 0

    if posicao_binaria != -1:
        # O índice local da região ordenada já é o índice global da lista lógica.
        regiao = "Região ordenada"
        indice_global = posicao_binaria
    else:
        # Como a cauda pode estar fora de ordem, examinamos seus elementos em sequência.
        posicao_sequencial, iteracoes_sequenciais = busca_sequencial(cauda, chave)

        if posicao_sequencial != -1:
            # A cauda vem depois da região ordenada; somamos seu tamanho ao índice local.
            regiao = "Cauda"
            indice_global = len(regiao_ordenada) + posicao_sequencial
        else:
            # A chave não apareceu em nenhuma das partes.
            regiao = "Não encontrado"
            indice_global = -1

    # Retorna um resumo consistente, inclusive quantas iterações cada estratégia usou.
    return {
        "encontrado": indice_global != -1,
        "regiao": regiao,
        "indice_global": indice_global,
        "iteracoes_binarias": iteracoes_binarias,
        "iteracoes_sequenciais": iteracoes_sequenciais,
        "total_iteracoes": iteracoes_binarias + iteracoes_sequenciais,
    }
