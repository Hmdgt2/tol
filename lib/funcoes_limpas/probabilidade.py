# lib/funcoes_analiticas/probabilidade.py
from scipy.stats import poisson, binom, norm, uniform, expon
from typing import List, Union

# ============================================================
# Funções de probabilidade
# ============================================================

# Poisson
def poisson_pmf(k: int, mu: float) -> float:
    """Calcula a PMF da distribuição de Poisson."""
    return poisson.pmf(k, mu)

def poisson_cdf(k: int, mu: float) -> float:
    """Calcula a CDF da distribuição de Poisson."""
    return poisson.cdf(k, mu)

def poisson_var(mu: float) -> float:
    """Calcula a variância da distribuição de Poisson."""
    return poisson.var(mu)

def poisson_entropy(mu: float) -> float:
    """Calcula a entropia da distribuição de Poisson."""
    return poisson.entropy(mu)

# Binomial
def binomial_pmf(k: int, n: int, p: float) -> float:
    """Calcula a PMF da distribuição binomial."""
    return binom.pmf(k, n, p)

def binomial_cdf(k: int, n: int, p: float) -> float:
    """Calcula a CDF da distribuição binomial."""
    return binom.cdf(k, n, p)

def binomial_var(n: int, p: float) -> float:
    """Calcula a variância da distribuição binomial."""
    return binom.var(n, p)

def binomial_entropy(n: int, p: float) -> float:
    """Calcula a entropia da distribuição binomial."""
    return binom.entropy(n, p)

# Normal
def normal_pdf(x: float, mu: float, sigma: float) -> float:
    """Calcula a PDF da distribuição normal."""
    return norm.pdf(x, mu, sigma)

def normal_cdf(x: float, mu: float, sigma: float) -> float:
    """Calcula a CDF da distribuição normal."""
    return norm.cdf(x, mu, sigma)

def normal_var(sigma: float) -> float:
    """Calcula a variância da distribuição normal."""
    return sigma**2

def normal_entropy(mu: float, sigma: float) -> float:
    """Calcula a entropia da distribuição normal."""
    return norm(mu, sigma).entropy()

# Exponencial
def exponential_pdf(x: float, lmbda: float) -> float:
    """Calcula a PDF da distribuição exponencial."""
    return expon.pdf(x, scale=1 / lmbda)

# Uniforme
def uniform_pdf(x: float, a: float, b: float) -> float:
    """Calcula a PDF da distribuição uniforme."""
    return uniform.pdf(x, a, b)
