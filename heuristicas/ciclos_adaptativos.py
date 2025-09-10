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
        """
        frequencia_por_ciclo = estatisticas.get('frequencia_por_ciclo', {})
        
        if not frequencia_por_ciclo:
            print("Aviso: A estatística 'frequencia_por_ciclo' não está disponível. A retornar lista vazia.")
            return []

        # CORREÇÃO: Usar a chave correta 'ultimos_10'
        # A chave 'recentes' não existe na estatística.
        numeros_do_ciclo_recente = frequencia_por_ciclo.get('ultimos_10', Counter())
        
        if not numeros_do_ciclo_recente:
            return []
        
        # A variável 'numeros_do_ciclo_recente' já é um Counter,
        # por isso não precisamos de a converter novamente.
        sugeridos = [num for num, _ in numeros_do_ciclo_recente.most_common(n)]
        
        return sorted(sugeridos)
