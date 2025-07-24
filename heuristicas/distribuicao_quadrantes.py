# heuristicas/distribuicao_quadrantes.py
from lib.dados import analisar_distribuicao_quadrantes
from collections import Counter
import random

def prever(sorteios, n=2):
    padrao_ideal_quadrantes = analisar_distribuicao_quadrantes(sorteios)
    
    # Identificar quais quadrantes o padrão ideal 'prefere'
    # Ex: se padrao_ideal_quadrantes é (2, 1, 1, 1), significa 2 números no Q1, 1 no Q2, etc.
    
    # Gerar uma lista de todos os números e as suas frequências
    frequencia_geral = Counter()
    for s in sorteios:
        frequencia_geral.update(s.get('numeros', []))

    # Vamos sugerir os 'n' números mais frequentes que ajudem a atingir o padrão ideal de quadrantes.
    # Para n=2, é um pouco difícil, pois a heurística é mais sobre a composição de 5 números.
    # No entanto, podemos priorizar os números de quadrantes que, historicamente, são mais representados
    # ou que precisam de mais números de acordo com o padrão ideal.

    # Abordagem simplificada para n=2:
    # Pegar os 2 quadrantes com a maior representação no padrao_ideal_quadrantes
    # e sugerir os números mais frequentes desses quadrantes.

    quadrantes_ordenados = sorted(
        enumerate(padrao_ideal_quadrantes), 
        key=lambda item: item[1], 
        reverse=True
    ) # (índice_quadrante, contagem_ideal)

    sugeridos = []
    tamanho_quadrante = 49 // 4 # Assumindo 4 quadrantes
    
    # Para cada um dos top 'X' quadrantes do padrão ideal (vamos pegar nos 2 primeiros)
    for idx_quadrante, _ in quadrantes_ordenados[:min(2, len(quadrantes_ordenados))]:
        limite_inferior = idx_quadrante * tamanho_quadrante + 1
        limite_superior = (idx_quadrante + 1) * tamanho_quadrante
        if idx_quadrante == 3: # Último quadrante
            limite_superior = 49

        # Filtrar os números mais frequentes que estão neste quadrante
        candidatos_no_quadrante = [
            num for num, _ in frequencia_geral.most_common(len(frequencia_geral)) 
            if limite_inferior <= num <= limite_superior
        ]
        
        # Adicionar o número mais frequente deste quadrante, se houver, até atingir n
        if candidatos_no_quadrante and len(sugeridos) < n:
            sugeridos.append(candidatos_no_quadrante[0])
            
    # Se ainda não tivermos n números, complementar com os mais frequentes
    if len(sugeridos) < n:
        todos_mais_frequentes = [num for num, _ in frequencia_geral.most_common(len(frequencia_geral))]
        for num in todos_mais_frequentes:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)

    return {
        "nome": "distribuicao_quadrantes",
        "numeros": sorted(sugeridos)[:n] # Garante n números únicos e ordenados
    }
