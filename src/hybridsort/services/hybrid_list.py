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

    def search_key_with_trace(self, key: int) -> dict[str, object]:
        """Procura uma chave e também devolve cada comparação feita.

        Este método é usado pela interface para explicar visualmente o caminho
        da busca. O método search_key continua disponível para quem precisa
        somente do resultado e das métricas.
        """
        return busca_hibrida_com_rastro(self.ordered_region, self.tail, key)

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
    """Procura uma chave na lista ordenada e retorna posição e iterações."""
    indice, iteracoes, _ = _busca_binaria_com_rastro(lista, chave)
    return indice, iteracoes


def _busca_binaria_com_rastro(
    lista: list[int], chave: int
) -> tuple[int, int, list[dict[str, int | str]]]:
    """Executa a busca binária e registra os limites e a comparação de cada etapa."""
    inicio = 0
    fim = len(lista) - 1
    iteracoes = 0
    passos: list[dict[str, int | str]] = []

    while inicio <= fim:
        iteracoes += 1
        inicio_anterior = inicio
        fim_anterior = fim
        meio = (inicio + fim) // 2
        valor_examinado = lista[meio]

        if valor_examinado == chave:
            decisao = "encontrada"
        elif valor_examinado < chave:
            decisao = "menor"
            inicio = meio + 1
        else:
            decisao = "maior"
            fim = meio - 1

        # Cada registro permite mostrar o trecho antes e depois da comparação.
        passos.append(
            {
                "fase": "binaria",
                "inicio": inicio_anterior,
                "fim": fim_anterior,
                "meio": meio,
                "valor": valor_examinado,
                "decisao": decisao,
                "novo_inicio": inicio,
                "novo_fim": fim,
            }
        )

        if decisao == "encontrada":
            return meio, iteracoes, passos

    return -1, iteracoes, passos


def busca_sequencial(lista: list[int], chave: int) -> tuple[int, int]:
    """Procura uma chave item por item e retorna posição e iterações."""
    indice, iteracoes, _ = _busca_sequencial_com_rastro(lista, chave)
    return indice, iteracoes


def _busca_sequencial_com_rastro(
    lista: list[int], chave: int
) -> tuple[int, int, list[dict[str, int | str]]]:
    """Percorre a lista em ordem e registra cada valor examinado."""
    passos: list[dict[str, int | str]] = []

    for indice, numero in enumerate(lista):
        decisao = "encontrada" if numero == chave else "diferente"
        passos.append(
            {
                "fase": "sequencial",
                "indice": indice,
                "valor": numero,
                "decisao": decisao,
            }
        )

        if decisao == "encontrada":
            return indice, len(passos), passos

    return -1, len(passos), passos


def busca_hibrida(
    regiao_ordenada: list[int], cauda: list[int], chave: int
) -> dict[str, bool | str | int]:
    """Procura a chave nas duas partes e devolve somente o resumo da busca."""
    resultado, _ = _busca_hibrida_com_rastro(regiao_ordenada, cauda, chave)
    return resultado


def busca_hibrida_com_rastro(
    regiao_ordenada: list[int], cauda: list[int], chave: int
) -> dict[str, object]:
    """Devolve o resumo da busca híbrida junto com todas as etapas examinadas."""
    resultado, passos = _busca_hibrida_com_rastro(
        regiao_ordenada, cauda, chave
    )
    return {**resultado, "passos": passos}


def _busca_hibrida_com_rastro(
    regiao_ordenada: list[int], cauda: list[int], chave: int
) -> tuple[dict[str, bool | str | int], list[dict[str, int | str]]]:
    """Combina as duas estratégias e preserva a ordem real das comparações."""
    posicao_binaria, iteracoes_binarias, passos_binarios = (
        _busca_binaria_com_rastro(regiao_ordenada, chave)
    )
    passos = list(passos_binarios)
    iteracoes_sequenciais = 0

    if posicao_binaria != -1:
        regiao = "Região ordenada"
        indice_global = posicao_binaria
    else:
        posicao_sequencial, iteracoes_sequenciais, passos_sequenciais = (
            _busca_sequencial_com_rastro(cauda, chave)
        )
        passos.extend(passos_sequenciais)

        if posicao_sequencial != -1:
            regiao = "Cauda"
            indice_global = len(regiao_ordenada) + posicao_sequencial
        else:
            regiao = "Não encontrado"
            indice_global = -1

    resultado = {
        "encontrado": indice_global != -1,
        "regiao": regiao,
        "indice_global": indice_global,
        "iteracoes_binarias": iteracoes_binarias,
        "iteracoes_sequenciais": iteracoes_sequenciais,
        "total_iteracoes": iteracoes_binarias + iteracoes_sequenciais,
    }
    return resultado, passos
