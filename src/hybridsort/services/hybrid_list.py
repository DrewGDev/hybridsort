import random

class HybridList:
    def __init__(self, seed: int = 42):
        """
        Inicializa a lista híbrida com uma região ordenada de 1.024 números 
        distintos gerados de forma reprodutível através de uma semente.
        """
        random.seed(seed)
        
        # Gera 1024 números inteiros únicos (amostra de um intervalo maior)
        initial_key = random.sample(range(1, 100000), 1024)
        
        self.ordered_region = sorted(initial_key)
        self.tail = []
        
    def insert_key(self, key: int) -> bool:
        """
        Insere uma nova chave no final da cauda, sem ordená-la, 
        rejeitando chaves que já existam.
        Retorna True se inseriu, False se foi rejeitada.
        """
        # Rejeita chaves repetidas
        if key in self.ordered_region or key in self.tail:
            return False
            
        # Insere no final da cauda sem ordenar
        self.tail.append(key)
        
        # Na 10ª inserção, ordena e intercala
        if len(self.tail) == 10:
            self._intercalate_and_clear_tail()
            
        return True
        
    def _intercalate_and_clear_tail(self):
        """
        Ordena as chaves da cauda, intercala à região ordenada e esvazia a cauda.
        """
        self.tail.sort()
        
        # Intercala as duas regiões mantendo a ordenação. 
        # O Timsort nativo do Python (sort) é altamente otimizado para listas parcialmente ordenadas.
        self.ordered_region.extend(self.tail)
        self.ordered_region.sort()
        
        # A cauda fica vazia para permitir novas inserções
        self.tail = []