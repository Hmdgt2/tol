# heuristicas/distribuicao_grupos.py
from typing import Dict, Any, List
from collections import Counter

class DistribuicaoGrupos:
    NOME = "distribuicao_grupos"
    DESCRICAO = "Sugere números seguindo a distribuição mais comum por grupos de dezenas."
    DEPENDENCIAS = ["distribuicao_dezenas", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na distribuição mais frequente por grupos (dezenas).
        """
        frequencia = estatisticas.get('frequencia_total', {})
        
        if not frequencia:
            return []

        # Agrupamos os números por frequência
        grupos_por_frequencia = {
            'grupo_1_10': sorted([num for num in range(1, 11)], key=lambda x: frequencia.get(x, 0), reverse=True),
            'grupo_11_20': sorted([num for num in range(11, 21)], key=lambda x: frequencia.get(x, 0), reverse=True),
            'grupo_21_30': sorted([num for num in range(21, 31)], key=lambda x: frequencia.get(x, 0), reverse=True),
            'grupo_31_40': sorted([num for num in range(31, 41)], key=lambda x: frequencia.get(x, 0), reverse=True),
            'grupo_41_49': sorted([num for num in range(41, 50)], key=lambda x: frequencia.get(x, 0), reverse=True)
        }

        sugeridos = []
        
        # Itera sobre os grupos, adicionando o número mais frequente de cada um
        # até que a lista de sugeridos atinja o tamanho n.
        
        lista_de_grupos = list(grupos_por_frequencia.values())
        
        # Itera sobre os grupos, pegando um número de cada, até atingir o total desejado.
        grupo_idx = 0
        while len(sugeridos) < n and grupo_idx < 50: # Evita loop infinito por segurança
            grupo_atual = lista_de_grupos[grupo_idx % len(lista_de_grupos)]
            if grupo_atual:
                num = grupo_atual.pop(0)
                if num not in sugeridos:
                    sugeridos.append(num)
            
            grupo_idx += 1
            
        return sorted(sugeridos)
