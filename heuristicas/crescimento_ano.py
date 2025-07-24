from lib.dados import carregar_sorteios, calcular_frequencia_por_ano

def numeros_crescimento_ano(min_crescimentos=2):
    """
    Retorna os números cuja frequência aumentou em pelo menos `min_crescimentos` anos.
    """
    sorteios = carregar_sorteios()
    freq_ano = calcular_frequencia_por_ano(sorteios)
    anos = sorted(freq_ano.keys())

    pontos = {}
    for num in range(1, 50):
        crescimentos = 0
        for i in range(1, len(anos)):
            freq_antes = freq_ano[anos[i - 1]].get(num, 0)
            freq_depois = freq_ano[anos[i]].get(num, 0)
            if freq_depois > freq_antes:
                crescimentos += 1
        if crescimentos >= min_crescimentos:
            pontos[num] = crescimentos * 3
    return pontos


if __name__ == '__main__':
    crescimento = numeros_crescimento_ano()
    print("Números com crescimento anual significativo:")
    for num, score in sorted(crescimento.items(), key=lambda x: x[1], reverse=True):
        print(f"Número {num}: score {score}")
