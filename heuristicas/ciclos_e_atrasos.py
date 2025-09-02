# heuristicas/ciclos_e_atrasos.py

from typing import Dict, Any, List
from collections import Counter
import numpy as np

class CiclosEAtrasos:
    """
    Heurística de Ciclos e Atrasos.
    Sugere números com base na sua frequência e no tempo que não são sorteados.
    """
    # --- Metadados da Heurística ---
    NOME = "ciclos_e_atrasos"
    DESCRICAO = "Sugere os números mais 'atrasados' ou que estão em um ciclo."
    DEPENDENCIAS = ["frequencia_atrasos"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base nos que estão mais atrasados (não foram sorteados por mais tempo).

        Args:
            estatisticas (Dict[str, Any]): Dicionário de estatísticas dos sorteios.
            n (int): O número de sugestões a serem retornadas.

        Returns:
            List[int]: Uma lista de números inteiros sugeridos.
        """
        # Obter os dados de atraso de cada número a partir das estatísticas
        frequencia_atrasos = estatisticas.get('frequencia_atrasos', {})
        
        # Se os dados de atraso não existirem, não há como prever
        if not frequencia_atrasos:
            return []
            
        # Ordenar os números com base no tempo de atraso, do maior para o menor
        # Usamos uma lista de tuplas para manter a relação entre o número e o atraso
        numeros_por_atraso = sorted(frequencia_atrasos.items(), key=lambda item: item[1], reverse=True)
        
        # Selecionar os 'n' números com o maior atraso
        sugeridos = [num for num, atraso in numeros_por_atraso[:n]]
        
        # Retornar a lista de números sugeridos, ordenada em ordem crescente
        return sorted(sugeridos)
