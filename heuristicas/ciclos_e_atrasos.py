# heuristicas/ciclos_e_atrasos.py
from typing import Dict, Any, List

class CiclosEAtrasos:
    # --- Metadados da Heurística ---
    NOME = "ciclos_e_atrasos"
    DESCRICAO = "Sugere números cuja ausência atual é um múltiplo do seu intervalo médio histórico."
    DEPENDENCIAS = ["ausencia_atual", "gaps_medios"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números que estão no final do seu ciclo histórico, ou seja,
        a sua ausência atual é um múltiplo próximo do seu gap médio.
        """
        ausencia = estatisticas.get('ausencia_atual', {})
        gaps_medios = estatisticas.get('gaps_medios', {})

        if not ausencia or not gaps_medios:
            return []

        pontuacoes = {}
        for num, atraso in ausencia.items():
            gap = gaps_medios.get(num, 0)
            if gap > 0 and atraso > gap:
                # Calcula a distância do atraso para o múltiplo mais próximo do gap.
                # Um valor próximo de 0 indica que o número está "no final do seu ciclo".
                proximidade = atraso % gap
                # Usamos o inverso para que a ordem seja do mais próximo para o mais distante.
                pontuacoes[num] = 1 / (proximidade + 1) # Adicionamos 1 para evitar divisão por 0

        sugeridos = sorted(pontuacoes, key=pontuacoes.get, reverse=True)[:n]

        # Fallback para o caso de não haver números suficientes.
        if len(sugeridos) < n:
            frequencia_total = estatisticas.get('frequencia_total', {})
            freq_ordenada = sorted(frequencia_total.items(), key=lambda x: x[1], reverse=True)
            for num, _ in freq_ordenada:
                if len(sugeridos) == n:
                    break
                if num not in sugeridos:
                    sugeridos.append(num)

        return sorted(sugeridos)
