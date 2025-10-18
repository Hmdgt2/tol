
import numpy as np
from typing import List, Callable
from scipy import integrate


def lebesgue_integral_approx(f: Callable[([float], float)], domain: List[float], measure: Callable[([float], float)]=(lambda x: 1.0), partitions: int=1000) -> float:
    'Integral de Lebesgue aproximada.'
    (a, b) = domain
    x_vals = np.linspace(a, b, partitions)
    y_vals = [f(x) for x in x_vals]
    unique_vals = sorted(set(y_vals))
    integral = 0.0
    for y in unique_vals:
        measure_set = 0.0
        for (i, x) in enumerate(x_vals):
            if (abs((f(x) - y)) < 1e-10):
                measure_set += ((measure(x) * (b - a)) / partitions)
        integral += (y * measure_set)
    return integral


def radon_nikodym_derivative_approx(measure1: Callable, measure2: Callable, points: List[float]) -> List[float]:
    'Derivada de Radon-Nikodym aproximada.'
    derivatives = []
    eps = 1e-08
    for x in points:
        interval_measure1 = (measure1((x + eps)) - measure1((x - eps)))
        interval_measure2 = (measure2((x + eps)) - measure2((x - eps)))
        if (abs(interval_measure2) > 1e-12):
            derivative = (interval_measure1 / interval_measure2)
        else:
            derivative = 0.0
        derivatives.append(derivative)
    return derivatives

