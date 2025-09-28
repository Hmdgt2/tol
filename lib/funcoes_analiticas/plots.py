import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from itertools import combinations
from typing import List

# ============================================================
# Funções de visualização
# ============================================================

def plot_histogram(data: List[float], title: str = 'Histograma', bins: int = 10, color: str = 'skyblue') -> None:
    """Plota um histograma de uma lista de dados."""
    plt.figure(figsize=(8, 6))
    sns.histplot(data, bins=bins, color=color, kde=True)
    plt.title(title)
    plt.xlabel('Valores')
    plt.ylabel('Frequência')
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def plot_scatter(x: List[float], y: List[float], title: str = 'Gráfico de Dispersão', color: str = 'green') -> None:
    """Plota um gráfico de dispersão de dois conjuntos de dados."""
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color=color)
    plt.title(title)
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.grid(True)
    plt.show()

def plot_boxplot(data: List[float], title: str = 'Boxplot') -> None:
    """Plota um boxplot para visualizar a distribuição e outliers."""
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=data)
    plt.title(title)
    plt.ylabel('Valores')
    plt.grid(True)
    plt.show()

def plot_time_series(series: List[float], title: str = 'Série Temporal', color: str = 'blue') -> None:
    """Plota uma série temporal."""
    plt.figure(figsize=(12, 6))
    plt.plot(series, color=color, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel('Tempo')
    plt.ylabel('Valores')
    plt.grid(True)
    plt.show()

# ============================================================
# Visualizações adicionais (vindas de exploracao.py)
# ============================================================

def rolling_mean_plot(lst: List[float], window: int = 3) -> None:
    """Plota a média móvel de uma lista."""
    pd.Series(lst).rolling(window=window).mean().plot(title="Média Móvel")
    plt.show()

def cumulative_sum_plot(lst: List[float]) -> None:
    """Plota a soma cumulativa de uma lista."""
    pd.Series(lst).cumsum().plot(title="Soma Cumulativa")
    plt.show()

def heatmap_pairs(lst: List[int]) -> None:
    """Cria um mapa de calor para a frequência de pares."""
    pairs = [tuple(sorted(c)) for c in combinations(lst, 2)]
    df = pd.DataFrame(pairs, columns=["Num1", "Num2"])
    pivot_table = df.groupby(["Num1", "Num2"]).size().unstack(fill_value=0)
    sns.heatmap(pivot_table, annot=True, fmt="d", cmap="YlGnBu")
    plt.title("Frequência de Pares")
    plt.show()
