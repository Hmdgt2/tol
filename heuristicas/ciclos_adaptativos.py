# heuristicas/ciclos_adaptativos.py

import importlib
from typing import Dict, Any, List
from collections import Counter

class CiclosAdaptativos:
    """
    Heurística de Ciclos Adaptativos.
    Sugere números com base na sua performance em ciclos de tempo recentes
    (como meses, trimestres ou anos).
    """
    # --- Metadados da Heurística ---
    NOME = "ciclos_adaptativos"
    DESCRICAO = "Sugere números com base na sua frequência e precisão em ciclos de tempo recentes."
    # Esta heurística dependerá de uma nova estatística, a 'frequencia_por_ciclo'.
    DEPENDENCIAS = ["frequencia_por_ciclo"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na frequência dos mais recentes ciclos.

        Args:
            estatisticas (Dict[str, Any]): Dicionário de estatísticas dos sorteios.
            n (int): O número de sugestões a serem retornadas.

        Returns:
            List[int]: Uma lista de números inteiros sugeridos.
        """
        frequencia_por_ciclo = estatisticas.get('frequencia_por_ciclo', {})
        
        if not frequencia_por_ciclo:
            # Caso a estatística ainda não tenha sido calculada, retorna uma lista vazia.
            print("Aviso: A estatística 'frequencia_por_ciclo' não está disponível. A retornar lista vazia.")
            return []

        # Para esta versão, usaremos apenas o ciclo mais recente.
        # A chave 'recentes' conterá os números mais frequentes do último ciclo.
        numeros_do_ciclo_recente = frequencia_por_ciclo.get('recentes', {})
        
        # Encontra os números mais frequentes neste ciclo
        if not numeros_do_ciclo_recente:
            return []
            
        # Ordena os números por frequência em ordem decrescente
        sugeridos = [num for num, _ in Counter(numeros_do_ciclo_recente).most_common(n)]
        
        # Retorna a lista de números sugeridos, ordenada em ordem crescente
        return sorted(sugeridos)
