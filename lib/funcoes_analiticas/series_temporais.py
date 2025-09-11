# lib/funcoes_analiticas/series_temporais.py
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from typing import List, Tuple

def arima_predict(lst: list, order: Tuple[int, int, int] = (1, 0, 0), steps: int = 1) -> list:
    """Prediz o próximo valor de uma série temporal usando o modelo ARIMA."""
    model = ARIMA(lst, order=order)
    fitted = model.fit()
    forecast = fitted.forecast(steps=steps)
    return forecast.tolist()

def rolling_mean(lst: list, window: int = 3) -> list:
    """Calcula a média móvel de uma lista."""
    return [np.mean(lst[i:i + window]) for i in range(len(lst) - window + 1)]

def rolling_std(lst: list, window: int = 3) -> list:
    """Calcula o desvio padrão móvel de uma lista."""
    return [np.std(lst[i:i + window]) for i in range(len(lst) - window + 1)]

def seasonal_decompose(lst: list, period: int = 5) -> list:
    """Decompõe uma série temporal por período (calcula a média de cada período)."""
    trend = [np.mean(lst[i::period]) for i in range(period)]
    return trend

def consecutive_diff(lst: list) -> list:
    """Calcula a diferença entre elementos consecutivos."""
    return [lst[i + 1] - lst[i] for i in range(len(lst) - 1)]

def moving_average(lst: list, window: int = 3) -> list:
    """Calcula a média móvel de uma lista (sinônimo de rolling_mean)."""
    return [np.mean(lst[i:i + window]) for i in range(len(lst) - window + 1)]

def moving_median(lst: list, window: int = 3) -> list:
    """Calcula a mediana móvel de uma lista."""
    return [np.median(lst[i:i + window]) for i in range(len(lst) - window + 1)]

def moving_variance(lst: list, window: int = 3) -> list:
    """Calcula a variância móvel de uma lista."""
    return [np.var(lst[i:i + window]) for i in range(len(lst) - window + 1)]

def centered_moving_average(lst: list, window: int = 3) -> list:
    """Calcula a média móvel centrada."""
    half = window // 2
    return [np.mean(lst[max(0, i - half):i + half + 1]) for i in range(len(lst))]

def cumulative_sum(lst: list) -> list:
    """Calcula a soma cumulativa de uma lista."""
    return np.cumsum(lst).tolist()

def cumulative_product(lst: list) -> list:
    """Calcula o produto cumulativo de uma lista."""
    return np.cumprod(lst).tolist()

def log_returns(lst: list) -> list:
    """Calcula os retornos logarítmicos de uma lista."""
    return [np.log(lst[i + 1] / lst[i]) for i in range(len(lst) - 1) if lst[i] != 0]

def diff_ratio(lst: list) -> list:
    """Calcula a razão de diferença entre elementos consecutivos."""
    return [(lst[i + 1] - lst[i]) / lst[i] for i in range(len(lst) - 1) if lst[i] != 0]

def normalized_cumsum(lst: list) -> list:
    """Calcula a soma cumulativa normalizada."""
    cs = np.cumsum(lst)
    return (cs / cs[-1]).tolist() if cs[-1] != 0 else cs.tolist()

def cumulative_max(lst: list) -> list:
    """Calcula o máximo cumulativo de uma lista."""
    res = []
    current = -float('inf')
    for x in lst:
        current = max(current, x)
        res.append(current)
    return res

def cumulative_min(lst: list) -> list:
    """Calcula o mínimo cumulativo de uma lista."""
    res = []
    current = float('inf')
    for x in lst:
        current = min(current, x)
        res.append(current)
    return res
