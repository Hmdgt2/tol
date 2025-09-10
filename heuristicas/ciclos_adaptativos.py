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
    DEPENDENCIAS = ["frequencia_por_ciclo"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na frequência dos mais recentes ciclos.
        """
        frequencia_por_ciclo = estatisticas.get('frequencia_por_ciclo', {})
        
        if not frequencia_por_ciclo:
            print("Aviso: A estatística 'frequencia_por_ciclo' não está disponível. A retornar lista vazia.")
            return []

        # CORREÇÃO: Usar a chave correta e obter a lista de contadores
        blocos_de_frequencia = frequencia_por_ciclo.get('blocos_de_10', [])

        # Se a lista de blocos estiver vazia, não há dados para prever
        if not blocos_de_frequencia:
            return []

        # Usar o contador do bloco mais recente (o último da lista)
        ultimo_bloco_frequencia = blocos_de_frequencia[-1]

        sugeridos = [num for num, _ in ultimo_bloco_frequencia.most_common(n)]
        
        return sorted(sugeridos)
