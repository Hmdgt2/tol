# heuristicas/repeticao_por_posicao.py
from typing import Dict, Any, List

class RepeticaoPorPosicao:
    # --- Metadados da Heurística ---
    NOME = "repeticao_por_posicao"
    DESCRICAO = "Sugere números com base na frequência em cada posição do sorteio, aproveitando padrões posicionais."
    DEPENDENCIAS = ["frequencia_por_posicao", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na repetição de números em posições específicas do sorteio.
        """
        frequencia_por_posicao = estatisticas.get('frequencia_por_posicao', {})
        
        if not frequencia_por_posicao:
            return []

        sugeridos = []
        for pos in sorted(frequencia_por_posicao.keys()):
            contador_pos = frequencia_por_posicao[pos]
            if contador_pos:
                num_mais_frequente = sorted(contador_pos.items(), key=lambda item: item[1], reverse=True)[0][0]
                if num_mais_frequente not in sugeridos:
                    sugeridos.append(num_mais_frequente)
            if len(sugeridos) >= n:
                break
            
        if len(sugeridos) < n:
            frequencia_total = estatisticas.get('frequencia_total', {})
            numeros_gerais = sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)
            
            for num in numeros_gerais:
                if num not in sugeridos and len(sugeridos) < n:
                    sugeridos.append(num)

        return sorted(sugeridos)
