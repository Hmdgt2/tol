# lib/funcoes_analiticas/modelagem_preditiva.py
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def linear_regression_predict(lst: list, steps: int = 1) -> float:
    """Prediz o próximo valor de uma lista usando regressão linear."""
    n = len(lst)
    if n < 2: return 0
    X = np.arange(n).reshape(-1, 1)
    y = np.array(lst)
    model = LinearRegression().fit(X, y)
    return model.predict(np.array([[n + steps - 1]]))[0]

def poly_regression_predict(lst: list, degree: int = 2, steps: int = 1) -> float:
    """Prediz o próximo valor de uma lista usando regressão polinomial."""
    n = len(lst)
    if n < degree: return 0
    X = np.arange(n).reshape(-1, 1)
    y = np.array(lst)
    poly = PolynomialFeatures(degree)
    X_poly = poly.fit_transform(X)
    model = LinearRegression().fit(X_poly, y)
    return model.predict(poly.transform([[n + steps - 1]]))[0]

def regression_on_frequency(lst: list, steps: int = 1) -> float:
    """Aplica regressão linear na frequência cumulativa de uma lista."""
    counts = {}
    for x in lst:
        counts[x] = counts.get(x, 0) + 1
    freq = [counts[k] for k in sorted(counts.keys())]
    n = len(freq)
    if n < 2: return 0
    X = np.arange(n).reshape(-1, 1)
    y = np.array(freq)
    model = LinearRegression().fit(X, y)
    return model.predict(np.array([[n + steps - 1]]))[0]
