# heuristicas/soma_numeros.py
import numpy as np
from collections import Counter

def prever(estatisticas, sorteios_historico, n=5, **kwargs):
    """
    Prevê números com base na soma mais provável dos sorteios, usando uma abordagem mais eficiente.

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

    # 1. Calcular as somas de todos os sorteios e o intervalo mais comum
    somas = [sum(s['numeros']) for s in sorteios_historico if s.get('numeros')]
    
    if not somas:
        return {
            "nome": "soma_numeros",
            "numeros": []
        }

    soma_media = np.mean(somas)
    soma_desvio = np.std(somas)
    soma_minima = int(soma_media - soma_desvio)
    soma_maxima = int(soma_media + soma_desvio)
    
    print(f"Soma mais provável: {soma_minima} a {soma_maxima}")
    
    # 2. Encontrar os sorteios no histórico que se encaixam no intervalo de soma
    sorteios_dentro_intervalo = [s['numeros'] for s in sorteios_historico if soma_minima <= sum(s.get('numeros', [])) <= soma_maxima]

    if not sorteios_dentro_intervalo:
        # Fallback para os números quentes se nenhum sorteio se encaixar
        numeros_quentes = estatisticas.get('numeros_quentes', [])
        return {
            "nome": "soma_numeros",
            "numeros": numeros_quentes[:n]
        }

    # 3. Contar a frequência de cada número nesses sorteios
    frequencia_intervalo = Counter()
    for numeros in sorteios_dentro_intervalo:
        frequencia_intervalo.update(numeros)

    # 4. Sugerir os números mais frequentes
    sugeridos = [num for num, _ in frequencia_intervalo.most_common(n)]

    return {
        "nome": "soma_numeros",
        "numeros": sorted(list(set(sugeridos)))
    }
