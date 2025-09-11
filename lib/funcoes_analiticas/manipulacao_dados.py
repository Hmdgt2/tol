# lib/auxiliares/manipulacao_dados.py
import numpy as np
import pandas as pd
from typing import List, Union

def fill_missing_values(lst: list, strategy: str = 'mean') -> list:
    """
    Preenche valores ausentes em uma lista usando uma estratégia específica.
    
    Args:
        lst (list): Lista de números com valores ausentes (np.nan).
        strategy (str): 'mean', 'median', ou 'mode'.
        
    Returns:
        list: Lista com valores ausentes preenchidos.
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

def normalize_data(lst: list) -> list:
    """Normaliza os dados para o intervalo [0, 1]."""
    arr = np.array(lst, dtype=float)
    return ((arr - arr.min()) / (arr.max() - arr.min())).tolist()

def standardize_data(lst: list) -> list:
    """Padroniza os dados (média 0, desvio padrão 1)."""
    arr = np.array(lst, dtype=float)
    return ((arr - arr.mean()) / arr.std()).tolist()

def get_dummies(lst: list) -> pd.DataFrame:
    """Converte uma lista de valores categóricos em variáveis dummy."""
    return pd.get_dummies(pd.Series(lst))
