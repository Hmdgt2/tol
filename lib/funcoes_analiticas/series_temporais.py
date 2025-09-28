import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf, adfuller, kpss
from typing import List, Tuple
from .sequencias import diff, ratio_consecutive, rolling_mean, rolling_std

# ===================== ARIMA =====================
def arima_predict(lst: List[float], order: Tuple[int, int, int] = (1, 0, 0), steps: int = 1) -> List[float]:
    model = ARIMA(lst, order=order)
    fitted = model.fit()
    return fitted.forecast(steps=steps).tolist()

arima_forecast = arima_predict  # alias

# ===================== Médias móveis =====================
def centered_moving_average(lst: List[float], window: int = 3) -> List[float]:
    half = window // 2
    return [np.mean(lst[max(0, i-half):i+half+1]) for i in range(len(lst))]

def ewma(lst: List[float], span: int = 3) -> List[float]:
    return pd.Series(lst).ewm(span=span).mean().tolist()

def exp_weighted_mean(lst: List[float], alpha: float = 0.3) -> List[float]:
    result, prev = [], lst[0]
    for x in lst:
        prev = alpha * x + (1 - alpha) * prev
        result.append(prev)
    return result

# ===================== Cumulativos =====================
def cumulative_sum(lst: List[float]) -> List[float]:
    return np.cumsum(lst).tolist()

def cumulative_product(lst: List[float]) -> List[float]:
    return np.cumprod(lst).tolist()

def normalized_cumsum(lst: List[float]) -> List[float]:
    cs = np.cumsum(lst)
    return (cs / cs[-1]).tolist() if cs[-1] != 0 else cs.tolist()

def cumulative_max(lst: List[float]) -> List[float]:
    res, current = [], -float('inf')
    for x in lst:
        current = max(current, x)
        res.append(current)
    return res

def cumulative_min(lst: List[float]) -> List[float]:
    res, current = [], float('inf')
    for x in lst:
        current = min(current, x)
        res.append(current)
    return res

# ===================== Diferenças =====================
consecutive_diff = diff  # alias
diff_series = diff       # alias
relative_diff = ratio_consecutive  # mantém coerência
