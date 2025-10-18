# lib/funcoes_analiticas/evolucao_darwiniana.py
import numpy as np
from typing import List, Dict
from scipy import stats

def evolutionary_fitness_landscape(seq: List[float]) -> Dict:
    """Analisa a sequência como um landscape evolutivo de fitness."""
    if len(seq) < 20:
        return {}
    
    # Identifica "espécies" (regimes estáveis)
    from sklearn.cluster import DBSCAN
    values = np.array(seq).reshape(-1, 1)
    
    # Clusterização para identificar regimes
    clustering = DBSCAN(eps=np.std(seq)*0.5, min_samples=5).fit(values)
    labels = clustering.labels_
    
    regimes = {}
    for label in set(labels):
        if label != -1:  # Ignora outliers
            regime_points = [seq[i] for i in range(len(seq)) if labels[i] == label]
            regimes[f'regime_{label}'] = {
                'size': len(regime_points),
                'mean_fitness': np.mean(regime_points),
                'stability': np.std(regime_points),
                'duration': len(regime_points)
            }
    
    # Análise de transições evolutivas
    transitions = []
    for i in range(1, len(labels)):
        if labels[i] != labels[i-1] and labels[i] != -1 and labels[i-1] != -1:
            fitness_change = seq[i] - seq[i-1]
            transitions.append({
                'position': i,
                'from_regime': labels[i-1],
                'to_regime': labels[i],
                'fitness_change': fitness_change,
                'adaptation': fitness_change > 0
            })
    
    return {
        'evolutionary_regimes': regimes,
        'transitions': transitions,
        'adaptation_rate': len([t for t in transitions if t['adaptation']]) / len(transitions) if transitions else 0,
        'evolutionary_stability': len(regimes) / len(seq),
        'selection_pressure': np.std(seq) / (np.mean(seq) + 1e-10)
    }

def evolutionary_algorithm_simulation(seq: List[float], generations: int = 100) -> Dict:
    """Simula evolução artificial para entender padrões evolutivos."""
    if len(seq) < 10:
        return {}
    
    # Usa a sequência como função de fitness inicial
    population_size = min(50, len(seq))
    population = seq[:population_size]
    
    evolutionary_trajectory = []
    for gen in range(generations):
        # Seleção (roleta viciada)
        fitness = np.array(population)
        fitness = fitness - np.min(fitness) + 1e-10  # Garante positividade
        probabilities = fitness / np.sum(fitness)
        
        selected_indices = np.random.choice(len(population), size=len(population), p=probabilities)
        selected = [population[i] for i in selected_indices]
        
        # Mutação
        mutation_rate = 0.1
        mutated = []
        for individual in selected:
            if np.random.random() < mutation_rate:
                mutated.append(individual + np.random.normal(0, np.std(population)*0.1))
            else:
                mutated.append(individual)
        
        population = mutated
        evolutionary_trajectory.append({
            'generation': gen,
            'mean_fitness': np.mean(population),
            'diversity': np.std(population),
            'max_fitness': np.max(population)
        })
    
    return {
        'evolutionary_trajectory': evolutionary_trajectory,
        'final_adaptation': evolutionary_trajectory[-1]['mean_fitness'] - evolutionary_trajectory[0]['mean_fitness'],
        'evolutionary_convergence': evolutionary_trajectory[-1]['diversity'] / (evolutionary_trajectory[0]['diversity'] + 1e-10),
        'emergent_complexity': len([t for t in evolutionary_trajectory if t['diversity'] > np.std(seq)]) / generations
    }
