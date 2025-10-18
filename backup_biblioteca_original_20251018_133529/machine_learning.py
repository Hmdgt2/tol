# lib/funcoes_analiticas/machine_learning.py
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, f1_score, precision_score, recall_score
from typing import List

def mse(y_true: list, y_pred: list) -> float:
    """Calcula o Erro Quadrático Médio (MSE)."""
    return mean_squared_error(y_true, y_pred)

def rmse(y_true: list, y_pred: list) -> float:
    """Calcula a Raiz do Erro Quadrático Médio (RMSE)."""
    return np.sqrt(mean_squared_error(y_true, y_pred))

def mae(y_true: list, y_pred: list) -> float:
    """Calcula o Erro Absoluto Médio (MAE)."""
    return mean_absolute_error(y_true, y_pred)

def r2(y_true: list, y_pred: list) -> float:
    """Calcula o coeficiente de determinação R²."""
    return r2_score(y_true, y_pred)

def accuracy(y_true: list, y_pred: list) -> float:
    """Calcula a acurácia para tarefas de classificação."""
    return accuracy_score(y_true, y_pred)

def f1(y_true: list, y_pred: list) -> float:
    """Calcula a pontuação F1 (macro-média)."""
    return f1_score(y_true, y_pred, average="macro")

def precision(y_true: list, y_pred: list) -> float:
    """Calcula a precisão (macro-média)."""
    return precision_score(y_true, y_pred, average="macro")

def recall(y_true: list, y_pred: list) -> float:
    """Calcula o recall (macro-média)."""
    return recall_score(y_true, y_pred, average="macro")
