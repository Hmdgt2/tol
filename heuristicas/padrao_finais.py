# heuristicas/padrao_finais.py
from typing import Dict, Any, List
from collections import Counter

class PadraoFinais:
    # --- Metadados da Heurística ---
    NOME = "padrao_finais"
    DESCRICAO = "Sugere números com terminações semelhantes ao último sorteio."
    DEPENDENCIAS = ["frequencia_terminacoes_padrao", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base nas terminações mais prováveis após o último sorteio.
        """
        frequencia_padrao = estatisticas.get('frequencia_terminacoes_padrao', {})
        frequencia_total = estatisticas.get('frequencia_total', {})
        
        if not frequencia_padrao or not frequencia_total:
            return []

        terminacoes_sorteio_atual = estatisticas.get('terminacoes_sorteio_atual', [])
        if not terminacoes_sorteio_atual:
            return []

        contador_terminacoes_sugeridas = Counter()
        for term_atual in terminacoes_sorteio_atual:
            if term_atual in frequencia_padrao:
                contador_terminacoes_sugeridas.update(frequencia_padrao[term_atual])
        
        terminacoes_comuns = [t for t, _ in contador_terminacoes_sugeridas.most_common(2)]
        
        candidatos = []
        frequencia_ordenada = sorted(frequencia_total.items(), key=lambda item: item[1], reverse=True)
        
        for num, _ in frequencia_ordenada:
            if (num % 10) in terminacoes_comuns:
                candidatos.append(num)
                if len(candidatos) >= n:
                    break
        
        if len(candidatos) < n:
            sugeridos = [num for num, _ in frequencia_ordenada[:n]]
        else:
            sugeridos = candidatos
        
        return sorted(list(set(sugeridos)))
