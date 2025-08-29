# heuristicas/frequencia_terminacoes.py
from collections import Counter

DESCRICAO = "Sugere números com terminações mais frequentes."

# Nota: analisa o último dígito dos números sorteados e escolhe os mais comuns.

def prever(estatisticas, n=5):
    """
    Prevê números com base na frequência das terminações (último dígito).

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        n (int): O número de sugestões a retornar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    frequencia_total = estatisticas.get('frequencia_total', {})

    if not frequencia_total:
        return {
            "nome": "frequencia_terminacoes",
            "numeros": []
        }
    
    # Deriva a frequência das terminações a partir da frequência total pré-calculada
    contador_terminacoes = Counter()
    for num, freq in frequencia_total.items():
        terminacao = num % 10
        contador_terminacoes[terminacao] += freq

    terminacoes_mais_frequentes = [t for t, _ in contador_terminacoes.most_common(3)]
    
    # Encontra os candidatos que terminam nos dígitos mais frequentes
    candidatos = []
    frequencia_ordenada = sorted(frequencia_total.items(), key=lambda item: item[1], reverse=True)
    
    for num, _ in frequencia_ordenada:
        if (num % 10) in terminacoes_mais_frequentes:
            candidatos.append(num)
            if len(candidatos) >= n:
                break

    sugeridos = candidatos[:n]
    
    return {
        "nome": "frequencia_terminacoes",
        "numeros": sorted(list(set(sugeridos)))
    }
