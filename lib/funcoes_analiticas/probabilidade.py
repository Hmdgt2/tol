# lib/funcoes_analiticas/probabilidade.py
from scipy.stats import poisson, binom, norm, uniform, expon, bernoulli, geom
from typing import List, Union

def poisson_pmf(k: int, mu: float) -> float:
    """Calcula a função de massa de probabilidade (PMF) de uma distribuição de Poisson."""
    return poisson.pmf(k, mu)

def poisson_cdf(k: int, mu: float) -> float:
    """Calcula a função de distribuição cumulativa (CDF) de uma distribuição de Poisson."""
    return poisson.cdf(k, mu)

def binomial_pmf(k: int, n: int, p: float) -> float:
    """Calcula a PMF de uma distribuição binomial."""
    return binom.pmf(k, n, p)

def binomial_cdf(k: int, n: int, p: float) -> float:
    """Calcula a CDF de uma distribuição binomial."""
    return binom.cdf(k, n, p)

def normal_pdf(x: float, mu: float, sigma: float) -> float:
    """Calcula a função densidade de probabilidade (PDF) de uma distribuição normal."""
    return norm.pdf(x, mu, sigma)

def normal_cdf(x: float, mu: float, sigma: float) -> float:
    """Calcula a CDF de uma distribuição normal."""
    return norm.cdf(x, mu, sigma)

def uniform_pdf(x: float, a: float, b: float) -> float:
    """Calcula a PDF de uma distribuição uniforme."""
    return uniform.pdf(x, a, b)

def poisson_pmf(k: int, mu: float) -> float:
    """Calcula a PMF da distribuição de Poisson."""
    return poisson.pmf(k, mu)

def poisson_cdf(k: int, mu: float) -> float:
    """Calcula a CDF da distribuição de Poisson."""
    return poisson.cdf(k, mu)

def binomial_pmf(k: int, n: int, p: float) -> float:
    """Calcula a PMF da distribuição binomial."""
    return binom.pmf(k, n, p)

def binomial_cdf(k: int, n: int, p: float) -> float:
    """Calcula a CDF da distribuição binomial."""
    return binom.cdf(k, n, p)

def normal_pdf(x: float, mu: float, sigma: float) -> float:
    """Calcula a PDF da distribuição normal."""
    return norm.pdf(x, mu, sigma)

def normal_cdf(x: float, mu: float, sigma: float) -> float:
    """Calcula a CDF da distribuição normal."""
    return norm.cdf(x, mu, sigma)

def exponential_pdf(x: float, lmbda: float) -> float:
    """Calcula a PDF da distribuição exponencial."""
    return expon.pdf(x, scale=1 / lmbda)
