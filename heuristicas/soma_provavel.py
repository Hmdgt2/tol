# heuristicas/soma_provavel.py
from lib.dados import calcular_somas_sorteios
from collections import Counter
from itertools import combinations

def prever(sorteios, n=2):
    analise_somas = calcular_somas_sorteios(sorteios)
    soma_mais_comum = analise_somas['soma_mais_comum']
    intervalo_inferior = analise_somas['intervalo_inferior']
    intervalo_superior = analise_somas['intervalo_superior']

    # Gerar números candidatos baseados na frequência geral
    frequencia_geral = Counter()
    for s in sorteios:
        frequencia_geral.update(s.get('numeros', []))
    
    # Pegar nos 15-20 números mais frequentes como base para combinações
    candidatos = [num for num, _ in frequencia_geral.most_common(20)] 
    
    melhores_combinacoes_de_5 = []
    
    # Gerar todas as combinações possíveis de 5 números a partir dos candidatos
    for comb in combinations(candidatos, 5):
        current_sum = sum(comb)
        # Se a soma da combinação estiver no intervalo provável, guarda-a
        if intervalo_inferior <= current_sum <= intervalo_superior:
            melhores_combinacoes_de_5.append(sorted(comb))
            # Opcional: limitar o número de combinações para performance
            if len(melhores_combinacoes_de_5) > 1000: # Limite arbitrário
                break 
    
    # Se não houver combinações dentro do intervalo, volta aos números mais frequentes
    if not melhores_combinacoes_de_5:
        sugeridos = [num for num, _ in frequencia_geral.most_common(n)]
    else:
        # Contar a frequência dos números nas combinações que caíram no intervalo
        contador_numeros_nestas_somas = Counter()
        for comb in melhores_combinacoes_de_5:
            contador_numeros_nestas_somas.update(comb)
        
        # Sugerir os 'n' números mais frequentes dentro dessas combinações
        sugeridos = [num for num, _ in contador_numeros_nestas_somas.most_common(n)]

    return {
        "nome": "soma_provavel",
        "numeros": sugeridos
    }
