# lib/auxiliares/manipulacao_dados.py
import numpy as np
import pandas as pd
from typing import List, Union

# ============================================================
# Preenchimento de valores ausentes
# ============================================================
def fill_missing_values(lst: List[float], strategy: str = 'mean') -> List[float]:
    """
    Preenche valores ausentes (np.nan) em uma lista usando uma estratégia específica.
    
    Args:
        lst (List[float]): Lista de números com valores ausentes.
        strategy (str): 'mean', 'median' ou 'mode'.
        
    Returns:
        List[float]: Lista com valores ausentes preenchidos.
    """
    series = pd.Series(lst)
    if strategy == 'mean':
        filled_series = series.fillna(series.mean())
    elif strategy == 'median':
        filled_series = series.fillna(series.median())
    elif strategy == 'mode':
        filled_series = series.fillna(series.mode()[0])
    else:
        raise ValueError("Estratégia inválida. Escolha entre 'mean', 'median' ou 'mode'.")
    return filled_series.tolist()

# ============================================================
# Normalização e padronização
# ============================================================
def normalize_data(lst: List[float]) -> List[float]:
    """
    Normaliza os dados para o intervalo [0, 1].
    
    Retorna 0 para todos os valores se todos forem iguais.
    """
    arr = np.array(lst, dtype=float)
    if arr.max() == arr.min():
        return [0 for _ in arr]
    return ((arr - arr.min()) / (arr.max() - arr.min())).tolist()

def standardize_data(lst: List[float]) -> List[float]:
    """
    Padroniza os dados (média 0, desvio padrão 1).
    
    Retorna 0 para todos os valores se o desvio padrão for 0.
    """
    arr = np.array(lst, dtype=float)
    mean_val = arr.mean()
    std_val = arr.std(ddof=1)
    if std_val == 0:
        return [0 for _ in arr]
    return ((arr - mean_val) / std_val).tolist()

# ============================================================
# Codificação de variáveis categóricas
# ============================================================
def get_dummies(lst: List[Union[str, int]]) -> pd.DataFrame:
    """
    Converte uma lista de valores categóricos em variáveis dummy.
    
    Args:
        lst (List[Union[str,int]]): Lista de valores categóricos.
        
    Returns:
        pd.DataFrame: DataFrame com colunas dummy.
    """
    return pd.get_dummies(pd.Series(lst))
