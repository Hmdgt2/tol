# heuristicas/frequencia_soma.py

from typing import Dict, Any, List
from collections import Counter

class FrequenciaSoma:
    NOME = "frequencia_soma"
    DESCRICAO = "Sugere os números mais frequentes que saíram em sorteios com a soma mais comum, preenchendo a lista com os menos frequentes desse subconjunto para garantir uma previsão completa."
    DEPENDENCIAS = ["numeros_soma_mais_frequente"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na sua frequência dentro do subconjunto de números que
        historicamente contribuem para a soma mais frequente dos sorteios.
        
        Args:
            estatisticas (dict): Dicionário com as estatísticas. Espera 'numeros_soma_mais_frequente'.
            n (int): O número de sugestões a retornar.
            
        Returns:
            list: Uma lista de números sugeridos.
        """
        numeros_soma = estatisticas.get('numeros_soma_mais_frequente', [])
        
        if not numeros_soma:
            # Se a lista estiver vazia, significa que os dados são insuficientes.
            return []
            
        # Conta a frequência dos números no subconjunto de 'numeros_soma_mais_frequente'
        frequencia_subconjunto = Counter(numeros_soma)
        
        # Seleciona os 'n' números mais comuns desse subconjunto
        sugeridos_brutos = frequencia_subconjunto.most_common(n)
        sugeridos = [num for num, _ in sugeridos_brutos]
        
        # A lista final deve ter exatamente 'n' números
        if len(sugeridos) < n:
            # Se houver menos de 'n' números, preenche com os números menos frequentes do subconjunto
            # (que ainda não foram sugeridos) para garantir 5 sugestões.
            candidatos_restantes = [num for num, _ in sorted(frequencia_subconjunto.items(), key=lambda item: item[1])]
            for num in candidatos_restantes:
                if len(sugeridos) >= n:
                    break
                if num not in sugeridos:
                    sugeridos.append(num)

        return sorted(sugeridos)
