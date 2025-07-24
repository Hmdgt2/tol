# heuristicas/frequencia_total.py

from lib.dados import carregar_sorteios, contar_ocorrencias

def frequencia_total(n=2):
    """
    Retorna os n números mais frequentes ao longo de todos os sorteios.
    """
    sorteios = carregar_sorteios()
    contador = contar_ocorrencias(sorteios)
    return [num for num, _ in contador.most_common(n)]

# Exemplo de teste direto
if __name__ == "__main__":
    print("Números mais frequentes:", frequencia_total(2))
