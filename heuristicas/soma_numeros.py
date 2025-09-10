# heuristicas/soma_numeros.py
from typing import Dict, Any, List
from collections import Counter

class SomaNumeros:
    # --- Metadados da Heurística ---
    NOME = "soma_numeros"
    DESCRICAO = "Sugere os números menos frequentes que saíram em sorteios com a soma mais comum, promovendo uma maior diversidade."
    DEPENDENCIAS = ["numeros_soma_mais_frequente", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na sua baixa frequência dentro do subconjunto de números que
        historicamente contribuem para a soma mais frequente dos sorteios.
        
        Args:
            estatisticas (dict): Dicionário com as estatísticas. Espera 'numeros_soma_mais_frequente'.
            n (int): O número de sugestões a retornar.
            
        Returns:
            list: Uma lista de números sugeridos.
        """
        numeros_soma = estatisticas.get('numeros_soma_mais_frequente', [])
        
        if not numeros_soma:
            frequencia_total = estatisticas.get('frequencia_total', {})
            return sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)[:n]

        frequencia_subconjunto = Counter(numeros_soma)
        
        # Seleciona os números menos comuns desse subconjunto
        sugeridos_brutos = frequencia_subconjunto.most_common()
        sugeridos = [num for num, _ in reversed(sugeridos_brutos)]
        
        # Pega os 'n' primeiros números
        sugeridos = sugeridos[:n]
        
        # A lista final deve ter exatamente 'n' números
        if len(sugeridos) < n:
            candidatos_restantes = [num for num, _ in sorted(frequencia_subconjunto.items(), key=lambda item: item[1])]
            for num in candidatos_restantes:
                if len(sugeridos) >= n:
                    break
                if num not in sugeridos:
                    sugeridos.append(num)
        
        return sorted(sugeridos)
