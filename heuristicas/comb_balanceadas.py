# heuristicas/comb_balanceadas.py
from typing import Dict, Any, List

class CombBalanceadas:
    NOME = "comb_balanceadas"
    DESCRICAO = "Sugere combinações que equilibram números pares e ímpares, altos e baixos, com base em padrões históricos."
    DEPENDENCIAS = ["frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base em combinações balanceadas de paridade e posição.
        """
        frequencia_total = estatisticas.get('frequencia_total', {})
        
        if not frequencia_total:
            return []

        pares = sorted([num for num in frequencia_total if num % 2 == 0], key=lambda x: frequencia_total[x], reverse=True)
        impares = sorted([num for num in frequencia_total if num % 2 != 0], key=lambda x: frequencia_total[x], reverse=True)

        baixos = sorted([num for num in frequencia_total if num <= 24], key=lambda x: frequencia_total[x], reverse=True)
        altos = sorted([num for num in frequencia_total if num >= 25], key=lambda x: frequencia_total[x], reverse=True)
        
        sugeridos = []
        grupos = [pares, impares, baixos, altos]
        
        num_por_grupo = n // len(grupos)
        
        for grupo in grupos:
            for _ in range(num_por_grupo):
                if grupo:
                    sugeridos.append(grupo.pop(0))

        # CORREÇÃO: Remove duplicados da lista inicial de sugestões
        sugeridos = list(set(sugeridos))

        # O resto do código (fallback) já é robusto e verifica duplicados
        frequencia_ordenada = sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)
        for num in frequencia_ordenada:
            if len(sugeridos) >= n:
                break
            if num not in sugeridos:
                sugeridos.append(num)

        return sorted(sugeridos)
