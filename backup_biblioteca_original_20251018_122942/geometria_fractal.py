# lib/funcoes_analiticas/geometria_fractal.py
import numpy as np
from typing import List

def multifractal_spectrum(points: List[List[float]], 
                         q_values: List[float] = None) -> List[float]:
    """Espectro multifractal f(α)."""
    if q_values is None:
        q_values = np.linspace(-5, 5, 11)
    
    # Converter pontos para grade 2D
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    
    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)
    
    # Criar grade
    grid_size = 32
    grid = np.zeros((grid_size, grid_size))
    
    for x, y in points:
        i = int((x - x_min) / (x_max - x_min) * (grid_size - 1))
        j = int((y - y_min) / (y_max - y_min) * (grid_size - 1))
        if 0 <= i < grid_size and 0 <= j < grid_size:
            grid[i, j] += 1
    
    # Medidas normalizadas
    total = np.sum(grid)
    if total > 0:
        measures = grid / total
    else:
        measures = grid
    
    # Função de partição
    spectrum = []
    scales = [2, 4, 8, 16]
    
    for q in q_values:
        tau_q = 0.0
        for scale in scales:
            if scale >= grid_size:
                continue
                
            # Agregar medidas
            aggregated = 0.0
            for i in range(0, grid_size, scale):
                for j in range(0, grid_size, scale):
                    block = measures[i:min(i+scale, grid_size), j:min(j+scale, grid_size)]
                    if np.sum(block) > 0:
                        if q == 1:
                            aggregated += np.sum(block) * np.log(np.sum(block))
                        else:
                            aggregated += np.sum(block) ** q
            
            if scale > 0:
                if q == 1:
                    tau_q += aggregated / np.log(1/scale)
                else:
                    tau_q += np.log(aggregated + 1e-10) / np.log(1/scale)
        
        spectrum.append(tau_q / len(scales) if len(scales) > 0 else 0.0)
    
    return spectrum

def lacunarity_analysis(points: List[List[float]], 
                       box_sizes: List[int] = None) -> List[float]:
    """Análise de lacunaridade para conjuntos fractais."""
    if box_sizes is None:
        box_sizes = [2, 4, 8, 16, 32]
    
    lacunarities = []
    
    for box_size in box_sizes:
        # Criar grade
        x_vals = [p[0] for p in points]
        y_vals = [p[1] for p in points]
        
        x_min, x_max = min(x_vals), max(x_vals)
        y_min, y_max = min(y_vals), max(y_vals)
        
        num_boxes_x = int((x_max - x_min) / box_size) + 1
        num_boxes_y = int((y_max - y_min) / box_size) + 1
        
        box_counts = np.zeros((num_boxes_x, num_boxes_y))
        
        # Contar pontos em cada caixa
        for x, y in points:
            i = int((x - x_min) / box_size)
            j = int((y - y_min) / box_size)
            if 0 <= i < num_boxes_x and 0 <= j < num_boxes_y:
                box_counts[i, j] += 1
        
        # Calcular lacunaridade
        if np.sum(box_counts) > 0:
            mean = np.mean(box_counts)
            std = np.std(box_counts)
            lacunarity = (std / mean) ** 2 if mean > 0 else 0.0
        else:
            lacunarity = 0.0
        
        lacunarities.append(lacunarity)
    
    return lacunarities
