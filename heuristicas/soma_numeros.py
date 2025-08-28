# heuristicas/soma_numeros.py
import numpy as np
from itertools import combinations
from collections import Counter

def prever(estatisticas, sorteios_historico, n=5):
    """
    Prevê números com base na soma mais provável dos sorteios.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        sorteios_historico (list): Lista dos sorteios históricos para análise.
        n (int): O número de sugestões a retornar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """

    if not sorteios_historico:
        return {
            "nome": "soma_numeros",
            "numeros": []
        }

    # 1. Calcular as somas de todos os sorteios
    somas = [sum(s['numeros']) for s in sorteios_historico if s.get('numeros')]
    
    if not somas:
        return {
            "nome": "soma_numeros",
            "numeros": []
        }

    # 2. Determinar a soma mais comum (intervalo)
    soma_media = np.mean(somas)
    soma_desvio = np.std(somas)
    soma_minima = int(soma_media - soma_desvio)
    soma_maxima = int(soma_media + soma_desvio)
    
    print(f"Soma mais provável: {soma_minima} a {soma_maxima}")
    
    # 3. Gerar combinações de 6 números
    numeros_possiveis = range(1, 50)
    combinacoes_validas = []

    # Otimização: A soma dos 6 menores números (1+2+3+4+5+6 = 21)
    # A soma dos 6 maiores números (49+48+47+46+45+44 = 279)
    # Podemos limitar as combinações para melhorar o desempenho
    
    # 4. Selecionar combinações com a soma no intervalo
    # Esta parte do código pode ser computacionalmente intensiva.
    # Usaremos uma amostra aleatória para evitar tempos de execução muito longos.
    frequencia_combinacoes = Counter()
    
    # Limitar o número de combinações para um tempo de execução razoável
    numero_combinacoes_a_testar = 50000 
    
    for i in range(numero_combinacoes_a_testar):
        c = np.random.choice(numeros_possiveis, 6, replace=False)
        c.sort()
        soma_c = sum(c)
        if soma_minima <= soma_c <= soma_maxima:
            frequencia_combinacoes.update(c)

    if not frequencia_combinacoes:
        return {
            "nome": "soma_numeros",
            "numeros": []
        }

    # 5. Contar a frequência de cada número e selecionar os mais comuns
    sugeridos = [num for num, _ in frequencia_combinacoes.most_common(n)]

    return {
        "nome": "soma_numeros",
        "numeros": sorted(list(set(sugeridos)))
    }
