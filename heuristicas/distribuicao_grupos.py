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
        padrao_ideal = estatisticas.get('distribuicao_dezenas', (0, 0, 0, 0, 0))
        frequencia = estatisticas.get('frequencia_total', {})
        
        if not frequencia:
            return []

        grupos_por_frequencia = {
            'grupo_1_10': sorted([num for num in range(1, 11)], key=lambda x: frequencia.get(x, 0), reverse=True),
            'grupo_11_20': sorted([num for num in range(11, 21)], key=lambda x: frequencia.get(x, 0), reverse=True),
            'grupo_21_30': sorted([num for num in range(21, 31)], key=lambda x: frequencia.get(x, 0), reverse=True),
            'grupo_31_40': sorted([num for num in range(31, 41)], key=lambda x: frequencia.get(x, 0), reverse=True),
            'grupo_41_49': sorted([num for num in range(41, 50)], key=lambda x: frequencia.get(x, 0), reverse=True)
        }

        sugeridos = []
        
        for i in range(len(padrao_ideal)):
            num_a_pegar = padrao_ideal[i]
            
            grupo_chave = list(grupos_por_frequencia.keys())[i]
            grupo_lista = grupos_por_frequencia[grupo_chave]

            for _ in range(num_a_pegar):
                if grupo_lista:
                    num = grupo_lista.pop(0)
                    if num not in sugeridos:
                        sugeridos.append(num)
        
        if len(sugeridos) < n:
            todos_mais_frequentes = [num for num, _ in Counter(frequencia).most_common(len(frequencia))]
            for num in todos_mais_frequentes:
                if num not in sugeridos:
                    sugeridos.append(num)
                if len(sugeridos) >= n:
                    break
        
        return sorted(sugeridos)
