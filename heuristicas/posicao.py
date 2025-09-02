#heuristicas/posicao.py

from typing import Dict, Any, List
from collections import Counter

class Posicao:
    """
    Heurística de Posição.
    Sugere números com base na sua tendência de aparecerem em posições específicas
    do resultado de um sorteio.
    """
    # --- Metadados da Heurística ---
    NOME = "posicao"
    DESCRICAO = "Sugere números com base na sua tendência de aparecerem em posições específicas do sorteio."
    DEPENDENCIAS = ["frequencia_por_posicao"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na frequência de cada número aparecer em cada posição.

        Args:
            estatisticas (Dict[str, Any]): Dicionário de estatísticas dos sorteios.
            n (int): O número de sugestões a serem retornadas.

        Returns:
            List[int]: Uma lista de números inteiros sugeridos.
        """
        frequencia_posicao = estatisticas.get('frequencia_posicao', {})
        
        if not frequencia_posicao:
            return []
            
        # Dicionário para somar as pontuações de cada número
        pontuacao_numeros = Counter()
        
        # Para cada posição no sorteio (de 0 a 4, ou seja, 1ª a 5ª posição)
        for posicao, numeros_por_posicao in frequencia_posicao.items():
            # Encontrar os 3 números mais comuns para essa posição
            numeros_comuns = Counter(numeros_por_posicao).most_common(3)
            for numero, contagem in numeros_comuns:
                # Adicionar a contagem ao número, dando pontos por ser frequente numa posição
                pontuacao_numeros[numero] += contagem
                
        # Selecionar os 'n' números com a maior pontuação total
        sugeridos = [num for num, _ in pontuacao_numeros.most_common(n)]
        
        # Retornar a lista de números sugeridos, ordenada em ordem crescente
        return sorted(sugeridos)
