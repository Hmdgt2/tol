
import numpy as np
from typing import List, Callable
from scipy import integrate, special
import mpmath


def takens_embedding(seq: List[float], dimension: int=3, delay: int=1) -> List[List[float]]:
    'Embedding de Takens para reconstrução de espaço de estados.'
    embedded = []
    for i in range((len(seq) - ((dimension - 1) * delay))):
        point = [seq[(i + (j * delay))] for j in range(dimension)]
        embedded.append(point)
    return embedded

