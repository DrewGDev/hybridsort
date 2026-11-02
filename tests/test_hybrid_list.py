import pytest
from src.hybridsort.services.hybrid_list import HybridList

def test_geracao_reprodutivel_e_ordenada():
    """Valida se a região ordenada possui 1.024 elementos únicos, ordenados e reprodutivos via semente."""
    lista1 = HybridList(seed=42)
    lista2 = HybridList(seed=42)

    # Garante quantidade exata de 1.024 elementos
    assert len(lista1.ordered_region) == 1024

    # Garante reprodutibilidade com a mesma semente
    assert lista1.ordered_region == lista2.ordered_region

    # Garante que os elementos iniciais estão ordenados
    assert lista1.ordered_region == sorted(lista1.ordered_region)

    # Garante que não há elementos duplicados na região inicial
    assert len(set(lista1.ordered_region)) == len(lista1.ordered_region)

def test_rejeicao_chaves_repetidas():
    """Valida se a classe rejeita chaves repetidas na região ordenada ou na cauda."""
    lista = HybridList(seed=42)

    # Tenta inserir chave existente na região ordenada (deve ser rejeitada)
    chave_existente = lista.ordered_region[0]
    assert lista.insert_key(chave_existente) is False
    assert len(lista.tail) == 0  # A cauda não deve ter sido alterada

    # Insere uma nova chave na cauda com sucesso
    assert lista.insert_key(999999) is True
    assert len(lista.tail) == 1  # A cauda deve ter um elemento agora

    # Tenta inserir a mesma chave que acabou de entrar na cauda (deve ser rejeitada)
    assert lista.insert_key(999999) is False
    assert len(lista.tail) == 1  # A cauda não deve ter sido alterada

def test_insercao_na_cauda_sem_ordenar():
    """Valida se a cauda armazena as chaves na ordem de chegada sem ordená-las antecipadamente."""
    lista = HybridList(seed=42)

    chaves_teste = [88888, 11111, 55555, 33333]

    for chave in chaves_teste:
        assert lista.insert_key(chave) is True
    
    # A cauda deve manter rigorosamente a sequência de inserção
    assert lista.tail == chaves_teste

def test_intercalacao_e_esvaziamento_na_decima_insercao():
    """Valida se na 10ª inserção a cauda é intercalada à região ordenada e esvaziada."""
    lista = HybridList()

    # Realiza 9 inserções válidas
    for i in range(1, 10):
        assert lista.insert_key(200000 + i) is True

    assert len(lista.tail) == 9  # A cauda deve ter 9 elementos
    assert len(lista.ordered_region) == 1024  # A região ordenada deve permanecer com 1.024 elementos

    # Realiza a 10ª inserção, que deve disparar a intercalação
    assert lista.insert_key(200000 + 10) is True

    # A cauda deve ficar vazia após a intercalação
    assert lista.tail == []

    # A região ordenada deve agora conter os 10 novos elementos (1.024 + 10 = 1.034 elementos)
    assert len(lista.ordered_region) == 1034

    # A nova região ordenada deve estar em ordem crescente
    assert lista.ordered_region == sorted(lista.ordered_region)

def test_novas_insercoes_apos_intercalacao():
    """Valida se novas inserções após a intercalação continuam funcionando corretamente."""
    lista = HybridList()

    # Preenche a cauda até intercalar (10 inserções)
    for i in range(10):
        lista.insert_key(300000 + i)

    assert len(lista.tail) == 0  # A cauda deve estar vazia após a intercalação

    # Permite nova inserção normal após a intercalação
    assert lista.insert_key(400000) is True
    assert len(lista.tail) == 1  # A cauda deve ter um elemento agora
    assert lista.tail == [400000]  # A cauda deve conter a nova chave inserida