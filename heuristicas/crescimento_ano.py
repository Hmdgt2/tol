# heuristicas/crescimento_ano.py
from lib.dados import calcular_frequencia_por_ano

def prever(sorteios, n=2):
    freq_ano = calcular_frequencia_por_ano(sorteios)
    anos = sorted(freq_ano.keys())
    pontos = {}
    for num in range(1, 50):
        crescimentos = 0
        for i in range(1, len(anos)):
            antes = freq_ano[anos[i - 1]].get(num, 0)
            depois = freq_ano[anos[i]].get(num, 0)
            if depois > antes:
                crescimentos += 1
        if crescimentos:
            pontos[num] = crescimentos * 3
    sugeridos = [num for num, _ in sorted(pontos.items(), key=lambda x: x[1], reverse=True)[:n]]
    return {
        "nome": "crescimento_ano",
        "numeros": sugeridos
    }
