# lib/funcoes_analiticas/series_temporais.py
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf, adfuller, kpss
from typing import List, Tuple

# ===================== ARIMA =====================
def arima_predict(lst: List[float], order: Tuple[int, int, int] = (1, 0, 0), steps: int = 1) -> List[float]:
    """Prevê os próximos valores de uma série temporal usando ARIMA."""
    model = ARIMA(lst, order=order)
    fitted = model.fit()
    forecast = fitted.forecast(steps=steps)
    return forecast.tolist()

def arima_forecast(lst: List[float], order: Tuple[int, int, int], steps: int) -> List[float]:
    """Sinônimo de arima_predict."""
    return arima_predict(lst, order, steps)

# ===================== Médias móveis =====================
def rolling_mean(lst: List[float], window: int = 3) -> List[float]:
    """Calcula a média móvel."""
    return [np.mean(lst[i:i+window]) for i in range(len(lst) - window + 1)]

def rolling_std(lst: List[float], window: int = 3) -> List[float]:
    """Calcula o desvio padrão móvel."""
    return [np.std(lst[i:i+window], ddof=1) for i in range(len(lst) - window + 1)]

def centered_moving_average(lst: List[float], window: int = 3) -> List[float]:
    """Calcula a média móvel centrada."""
    half = window // 2
    return [np.mean(lst[max(0, i-half):i+half+1]) for i in range(len(lst))]

def ewma(lst: List[float], span: int = 3) -> List[float]:
    """Calcula a média móvel exponencial."""
    return pd.Series(lst).ewm(span=span).mean().tolist()

def exp_weighted_mean(lst: List[float], alpha: float = 0.3) -> List[float]:
    """Calcula a média móvel exponencialmente ponderada manualmente."""
    result = []
    prev = lst[0]
    for x in lst:
        prev = alpha * x + (1 - alpha) * prev
        result.append(prev)
    return result

# ===================== Cumulativos =====================
def cumulative_sum(lst: List[float]) -> List[float]:
    """Calcula a soma cumulativa."""
    return np.cumsum(lst).tolist()

def cumulative_product(lst: List[float]) -> List[float]:
    """Calcula o produto cumulativo."""
    return np.cumprod(lst).tolist()

def normalized_cumsum(lst: List[float]) -> List[float]:
    """Calcula a soma cumulativa normalizada."""
    cs = np.cumsum(lst)
    return (cs / cs[-1]).tolist() if cs[-1] != 0 else cs.tolist()

def cumulative_max(lst: List[float]) -> List[float]:
    """Calcula o máximo cumulativo."""
    res = []
    current = -float('inf')
    for x in lst:
        current = max(current, x)
        res.append(current)
    return res

def cumulative_min(lst: List[float]) -> List[float]:
    """Calcula o mínimo cumulativo."""
    res = []
    current = float('inf')
    for x in lst:
        current = min(current, x)
        res.append(current)
    return res

# ===================== Diferenças =====================
def consecutive_diff(lst: List[float]) -> List[float]:
    """Calcula a diferença entre elementos consecutivos."""
    return [lst[i+1] - lst[i] for i in range(len(lst) - 1)]

def relative_diff(lst: List[float]) -> List[float]:
    """Calcula a diferença relativa entre elementos consecutivos."""
    return [(lst[i+1] - lst[i])/lst[i] if lst[i] != 0 else 0 for i in range(len(lst) - 1)]

def diff_series(lst: List[float]) -> List[float]:
    """Sinônimo de consecutive_diff."""
    return consecutive_diff(lst)

def diff_ratio(lst: List[float]) -> List[float]:
    """Calcula a razão de diferença entre elementos consecutivos."""
    return [(lst[i+1] - lst[i])/lst[i] for i in range(len(lst)-1) if lst[i] != 0]

def log_returns(lst: List[float]) -> List[float]:
    """Calcula retornos logarítmicos."""
    return [np.log(lst[i+1]/lst[i]) for i in range(len(lst)-1) if lst[i] != 0]

# ===================== Blocos e medianas =====================
def non_overlapping_sum(lst: List[float], k: int = 2) -> List[float]:
    """Soma elementos em blocos não sobrepostos."""
    return [sum(lst[i:i+k]) for i in range(0, len(lst), k)]

def moving_median(lst: List[float], window: int = 3) -> List[float]:
    """Calcula a mediana móvel."""
    return [np.median(lst[i:i+window]) for i in range(len(lst) - window + 1)]

def moving_variance(lst: List[float], window: int = 3) -> List[float]:
    """Calcula a variância móvel."""
    return [np.var(lst[i:i+window], ddof=1) for i in range(len(lst) - window + 1)]

# ===================== Testes estatísticos =====================
def adf_test(lst: List[float]) -> float:
    """Retorna o p-valor do teste de Dickey-Fuller aumentado (ADF)."""
    return adfuller(lst)[1]

def kpss_test(lst: List[float]) -> float:
    """Retorna o p-valor do teste KPSS."""
    return kpss(lst, regression='c')[1]

# ===================== Autocorrelação =====================
def autocorr(lst: List[float], lags: int = 10) -> List[float]:
    """Calcula autocorrelação (ACF)."""
    return acf(lst, nlags=lags).tolist()

def partial_autocorr(lst: List[float], lags: int = 10) -> List[float]:
    """Calcula autocorrelação parcial (PACF)."""
    return pacf(lst, nlags=lags).tolist()

# ===================== Transformações =====================
def log_transform(lst: List[float]) -> List[float]:
    """Aplica a transformação logarítmica log(x+1)."""
    return np.log(np.array(lst) + 1).tolist()
