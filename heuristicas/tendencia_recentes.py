# heuristicas/tendencia_recentes.py
from collections import Counter

def prever(sorteios_historico, n=5, janela=10):
    """
    Prevê números com base na sua frequência nos sorteios mais recentes.

    Args:
        sorteios_historico (list): Lista dos sorteios históricos para análise.
        n (int): O número de sugestões a retornar.
        janela (int): O número de sorteios recentes para considerar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    if len(sorteios_historico) < janela:
        janela = len(sorteios_historico)
        
    if not sorteios_historico:
        return {
            "nome": "tendencia_recentes",
            "numeros": []
        }

    ultimos = sorteios_historico[-janela:]
    
    contador = Counter()
    for s in ultimos:
        contador.update(s.get('numeros', []))

    sugeridos = [num for num, _ in contador.most_common(n)]

    return {
        "nome": "tendencia_recentes",
        "numeros": sorted(list(set(sugeridos)))
    }
