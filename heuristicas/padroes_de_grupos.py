# heuristicas/padroes_de_grupos

from typing import Dict, Any, List
from collections import Counter

class PadroesDeGrupos:
    """
    Heurística de Padrões de Grupos.
    Sugere números com base nos grupos de números que são frequentemente sorteados juntos.
    """
    # --- Metadados da Heurística ---
    NOME = "padroes_de_grupos"
    DESCRICAO = "Sugere números com base nos grupos de números que são frequentemente sorteados juntos."
    DEPENDENCIAS = ["frequencia_grupos"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na frequência de grupos de números.
        
        Args:
            estatisticas (Dict[str, Any]): Dicionário de estatísticas dos sorteios.
            n (int): O número de sugestões a serem retornadas.

        Returns:
            List[int]: Uma lista de números inteiros sugeridos.
        """
        # Obter a frequência de grupos de números (a ser gerada por lib/dados.py)
        frequencia_grupos = estatisticas.get('frequencia_grupos', {})
        
        # Se os dados não existirem, retornar uma lista vazia
        if not frequencia_grupos:
            return []
            
        # Encontrar os grupos mais frequentes (por exemplo, os 10 mais comuns)
        grupos_mais_frequentes = Counter(frequencia_grupos).most_common(10)
        
        # Contar a frequência de números individuais dentro desses grupos
        contador_numeros = Counter()
        for grupo, _ in grupos_mais_frequentes:
            contador_numeros.update(grupo)
            
        # Selecionar os 'n' números com a maior contagem
        sugeridos = [num for num, _ in contador_numeros.most_common(n)]
        
        # Retornar a lista de números sugeridos, ordenada em ordem crescente
        return sorted(sugeridos)
