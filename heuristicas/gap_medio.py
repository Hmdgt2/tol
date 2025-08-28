# heuristicas/gap_medio.py
def prever(estatisticas, n=5):
    """
    Prevê números com base no seu gap médio (intervalo médio entre saídas),
    sugerindo os números com o gap mais curto.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        n (int): O número de sugestões a retornar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    gaps_medios = estatisticas.get('gaps_medios', {})

    if not gaps_medios:
        return {
            "nome": "gap_medio",
            "numeros": []
        }

    # Ordena os números pelo seu gap médio, do menor para o maior
    melhores = sorted(gaps_medios.items(), key=lambda x: x[1])

    sugeridos = [num for num, _ in melhores[:n]]

    return {
        "nome": "gap_medio",
        "numeros": sugeridos
    }
