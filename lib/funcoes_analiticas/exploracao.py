# lib/funcoes_analiticas/exploracao.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List

def plot_histogram(lst: list, bins: int = 10) -> None:
    """Cria e exibe um histograma de uma lista de números."""
    plt.hist(lst, bins=bins)
    plt.title("Histograma")
    plt.show()

def rolling_mean_plot(lst: list, window: int = 3) -> None:
    """Plota a média móvel de uma lista."""
    pd.Series(lst).rolling(window=window).mean().plot(title="Média Móvel")
    plt.show()

def cumulative_sum_plot(lst: list) -> None:
    """Plota a soma cumulativa de uma lista."""
    pd.Series(lst).cumsum().plot(title="Soma Cumulativa")
    plt.show()

def heatmap_pairs(lst: list) -> None:
    """Cria um mapa de calor para a frequência de pares."""
    pairs = [tuple(sorted(c)) for c in combinations(lst, 2)]
    df = pd.DataFrame(pairs, columns=['Num1', 'Num2'])
    pivot_table = df.groupby(['Num1', 'Num2']).size().unstack(fill_value=0)
    sns.heatmap(pivot_table, annot=True, fmt="d", cmap="YlGnBu")
    plt.title("Frequência de Pares")
    plt.show()

def linear_trend_slope(lst: list) -> float:
    """Calcula a inclinação da tendência linear de uma lista."""
    n = len(lst)
    x = np.arange(n)
    y = np.array(lst)
    if n < 2: return 0
    slope = np.polyfit(x, y, 1)[0]
    return float(slope)

def successive_diff(lst: list) -> list:
    """Calcula a diferença entre elementos sucessivos."""
    return [lst[i] - lst[i-1] for i in range(1, len(lst))]
