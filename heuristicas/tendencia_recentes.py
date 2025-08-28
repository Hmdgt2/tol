# heuristicas/tendencia_recentes.py
from collections import Counter

def prever(estatisticas, sorteios_historico, n=5, janela=10):
    """
    Prevê números com base na sua frequência nos sorteios mais recentes.
    """
    # Restante da sua lógica, que agora funcionará corretamente
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
