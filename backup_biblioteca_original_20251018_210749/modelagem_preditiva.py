# lib/funcoes_analiticas/modelagem_preditiva.py
import numpy as np
from typing import List, Tuple
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# ============================================================
# Regressão Linear e Polinomial
# ============================================================
def linear_regression_predict(lst: List[float], steps: int = 1) -> float:
    """Prediz o próximo valor de uma lista usando regressão linear."""
    n = len(lst)
    if n < 2:
        return 0.0
    X = np.arange(n).reshape(-1, 1)
    y = np.array(lst)
    model = LinearRegression().fit(X, y)
    return float(model.predict(np.array([[n + steps - 1]]))[0])

def poly_regression_predict(lst: List[float], degree: int = 2, steps: int = 1) -> float:
    """Prediz o próximo valor de uma lista usando regressão polinomial."""
    n = len(lst)
    if n < degree:
        return 0.0
    X = np.arange(n).reshape(-1, 1)
    y = np.array(lst)
    poly = PolynomialFeatures(degree)
    X_poly = poly.fit_transform(X)
    model = LinearRegression().fit(X_poly, y)
    return float(model.predict(poly.transform([[n + steps - 1]]))[0])

# ============================================================
# Regressão baseada em frequência
# ============================================================
def regression_on_frequency(lst: List[int], steps: int = 1) -> float:
    """Aplica regressão linear na frequência cumulativa de uma lista."""
    counts = {}
    for x in lst:
        counts[x] = counts.get(x, 0) + 1
    freq = [counts[k] for k in sorted(counts.keys())]
    n = len(freq)
    if n < 2:
        return 0.0
    X = np.arange(n).reshape(-1, 1)
    y = np.array(freq)
    model = LinearRegression().fit(X, y)
    return float(model.predict(np.array([[n + steps - 1]]))[0])

# ============================================================
# Utilitários de regressão linear
# ============================================================
def linear_regression_coeffs(x: List[float], y: List[float]) -> Tuple[float, float]:
    """Calcula os coeficientes de regressão linear (inclinação e interceptação)."""
    X = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(X, y, rcond=None)[0]
    return float(m), float(c)

def predict_linear(x: List[float], m: float, c: float) -> List[float]:
    """Prediz valores usando uma equação de regressão linear."""
    return [m * xi + c for xi in x]

def regression_score(x: List[float], y: List[float]) -> float:
    """Calcula a pontuação de ajuste de regressão linear (negativo do MSE)."""
    m, c = linear_regression_coeffs(x, y)
    y_pred = predict_linear(x, m, c)
    return -float(np.mean((np.array(y) - np.array(y_pred)) ** 2))
