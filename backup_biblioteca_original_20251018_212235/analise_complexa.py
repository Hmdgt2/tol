# lib/funcoes_analiticas/analise_complexa.py
import numpy as np
from typing import List, Callable
from scipy import integrate

def cauchy_integral_formula(f: Callable[[complex], complex], 
                           z0: complex, 
                           radius: float = 1.0) -> complex:
    """Fórmula integral de Cauchy."""
    def integrand(theta):
        z = z0 + radius * np.exp(1j * theta)
        return f(z) / (z - z0)
    
    result, _ = integrate.quad(lambda theta: integrand(theta), 0, 2*np.pi)
    return result / (2j * np.pi)

def residue_theorem(f: Callable[[complex], complex], 
                   poles: List[complex], 
                   domain: List[float]) -> complex:
    """Teorema dos resíduos simplificado."""
    total_residue = 0.0
    for pole in poles:
        # Aproximação do resíduo
        epsilon = 1e-6
        circle_points = [pole + epsilon * np.exp(1j * theta) 
                        for theta in np.linspace(0, 2*np.pi, 8)]
        residue_approx = sum(f(z) for z in circle_points) / len(circle_points)
        total_residue += residue_approx
    
    return total_residue

def conformal_mapping_distortion(z_points: List[complex], 
                                f: Callable[[complex], complex]) -> List[float]:
    """Distorção de mapeamento conforme."""
    distortions = []
    for z in z_points:
        # Derivada complexa aproximada
        h = 1e-8
        df_dz = (f(z + h) - f(z - h)) / (2 * h)
        distortions.append(abs(df_dz))
    return distortions

def mandelbrot_set_membership(c: complex, max_iter: int = 100) -> int:
    """Verifica se ponto pertence ao conjunto de Mandelbrot."""
    z = 0
    for i in range(max_iter):
        z = z * z + c
        if abs(z) > 2:
            return i
    return max_iter

def riemann_zeta_zeros_approx(t_values: List[float]) -> List[float]:
    """Aproximação de zeros da função zeta de Riemann."""
    zeros = []
    for t in t_values:
        # Fórmula aproximada para zeros não triviais
        zero_approx = t / (2 * np.pi) * np.log(t / (2 * np.pi * np.e))
        zeros.append(zero_approx)
    return zeros
