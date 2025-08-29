# heuristicas/balanceamento_tipos.py
from collections import Counter

DESCRICAO = "Sugere números equilibrando pares, ímpares e primos conforme o padrão mais comum."

def prever(estatisticas, n=5):
    """
    Prevê números com base no padrão de balanceamento de pares, ímpares e primos.
    A heurística sugere os números mais frequentes que correspondem ao padrão mais comum.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        n (int): O número de sugestões a retornar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    # Acessa diretamente as estatísticas de padrão de tipos e frequência total
    padrao_ideal = estatisticas.get('padrao_tipos_numeros', (0, 0, 0))
    frequencia = estatisticas.get('frequencia_total', {})
    
    if not frequencia:
        return { "nome": "balanceamento_tipos", "numeros": [] }

    frequencia_ordenada = sorted(frequencia.items(), key=lambda item: item[1], reverse=True)

    candidatos_por_tipo = {
        'par': [],
        'impar': [],
        'primo': []
    }

    # Classifica os números mais frequentes por tipo
    for num, freq in frequencia_ordenada:
        if num % 2 == 0:
            candidatos_por_tipo['par'].append(num)
        else:
            candidatos_por_tipo['impar'].append(num)
        if _is_prime(num):
            candidatos_por_tipo['primo'].append(num)
            
    sugeridos = []
    
    # Lógica de seleção simplificada:
    # Se o padrão ideal sugere mais pares do que ímpares, tenta pegar o par mais frequente
    if padrao_ideal[0] > padrao_ideal[1] and candidatos_por_tipo['par']:
        sugeridos.append(candidatos_por_tipo['par'][0])
    # Caso contrário, tenta pegar o ímpar mais frequente
    elif padrao_ideal[1] > padrao_ideal[0] and candidatos_por_tipo['impar']:
        sugeridos.append(candidatos_por_tipo['impar'][0])
    
    # Adiciona o número restante para atingir n, priorizando o mais frequente de qualquer tipo
    while len(sugeridos) < n:
        for num, _ in frequencia_ordenada:
            if num not in sugeridos:
                sugeridos.append(num)
                if len(sugeridos) == n:
                    break
                    
    return {
        "nome": "balanceamento_tipos",
        "numeros": sorted(list(set(sugeridos)))
    }

def _is_prime(n):
    """Verifica se um número é primo (função auxiliar)."""
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True
