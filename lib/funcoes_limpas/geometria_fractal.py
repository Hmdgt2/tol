
'# Computacao Cientifica'
import numpy as np
pass
'# Outros'
from typing import List
pass


def hausdorff_dimension_approx(points: List[List[float]], scales: List[float]=None) -> float:
    'Dimensão de Hausdorff aproximada de um conjunto.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    if (scales is None):
        scales = np.logspace((- 3), 0, 20)
    counts = []
    for scale in scales:
        covered = set()
        for point in points:
            box_coord = tuple((int((coord / scale)) for coord in point))
            covered.add(box_coord)
        counts.append(len(covered))
    if (len(counts) > 1):
        log_scales = np.log((1 / np.array(scales)))
        log_counts = np.log((np.array(counts) + 1))
        slope = np.polyfit(log_scales, log_counts, 1)[0]
        return slope
    return 0.0

