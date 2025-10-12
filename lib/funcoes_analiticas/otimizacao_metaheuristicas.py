# lib/funcoes_analiticas/otimizacao_metaheuristicas.py
import numpy as np
from typing import List, Callable, Tuple
import random

# ============================================================
# Algoritmos de Otimização
# ============================================================

def simulated_annealing(objective: Callable, bounds: List[Tuple], 
                       max_iter: int = 1000, temp: float = 100.0) -> Tuple:
    """Algoritmo de simulated annealing para otimização."""
    # Solução inicial
    best_solution = [random.uniform(b[0], b[1]) for b in bounds]
    best_score = objective(best_solution)
    
    current_solution, current_score = best_solution, best_score
    
    for i in range(max_iter):
        # Gerar solução candidata
        candidate = []
        for j in range(len(bounds)):
            candidate.append(current_solution[j] + random.gauss(0, 1))
            # Manter dentro dos limites
            candidate[j] = max(bounds[j][0], min(bounds[j][1], candidate[j]))
        
        candidate_score = objective(candidate)
        
        # Critério de aceitação
        if candidate_score < current_score:
            current_solution, current_score = candidate, candidate_score
            if candidate_score < best_score:
                best_solution, best_score = candidate, candidate_score
        else:
            # Aceitação probabilística
            acceptance_prob = np.exp(-(candidate_score - current_score) / temp)
            if random.random() < acceptance_prob:
                current_solution, current_score = candidate, candidate_score
        
        # Resfriamento
        temp *= 0.95
    
    return best_solution, best_score

def particle_swarm_optimization(objective: Callable, bounds: List[Tuple], 
                               n_particles: int = 30, max_iter: int = 100) -> Tuple:
    """Otimização por enxame de partículas."""
    # Inicialização
    particles = []
    velocities = []
    personal_best = []
    personal_best_scores = []
    
    for _ in range(n_particles):
        particle = [random.uniform(b[0], b[1]) for b in bounds]
        particles.append(particle)
        velocities.append([random.uniform(-1, 1) for _ in bounds])
        personal_best.append(particle.copy())
        personal_best_scores.append(objective(particle))
    
    # Melhor global
    global_best_idx = np.argmin(personal_best_scores)
    global_best = personal_best[global_best_idx].copy()
    global_best_score = personal_best_scores[global_best_idx]
    
    # Parâmetros PSO
    w = 0.729  # Inércia
    c1 = 1.494  # Cognitivo
    c2 = 1.494  # Social
    
    for _ in range(max_iter):
        for i in range(n_particles):
            # Atualizar velocidade
            for j in range(len(bounds)):
                r1, r2 = random.random(), random.random()
                cognitive = c1 * r1 * (personal_best[i][j] - particles[i][j])
                social = c2 * r2 * (global_best[j] - particles[i][j])
                velocities[i][j] = w * velocities[i][j] + cognitive + social
            
            # Atualizar posição
            for j in range(len(bounds)):
                particles[i][j] += velocities[i][j]
                # Manter dentro dos limites
                particles[i][j] = max(bounds[j][0], min(bounds[j][1], particles[i][j]))
            
            # Avaliar
            score = objective(particles[i])
            
            # Atualizar melhores
            if score < personal_best_scores[i]:
                personal_best[i] = particles[i].copy()
                personal_best_scores[i] = score
                
                if score < global_best_score:
                    global_best = particles[i].copy()
                    global_best_score = score
    
    return global_best, global_best_score

# ============================================================
# Algoritmos Genéticos
# ============================================================

def genetic_algorithm(objective: Callable, bounds: List[Tuple], 
                     pop_size: int = 50, generations: int = 100) -> Tuple:
    """Algoritmo genético simples."""
    # Inicializar população
    population = []
    for _ in range(pop_size):
        individual = [random.uniform(b[0], b[1]) for b in bounds]
        population.append(individual)
    
    # Avaliar população inicial
    fitness = [objective(ind) for ind in population]
    
    best_idx = np.argmin(fitness)
    best_individual = population[best_idx].copy()
    best_fitness = fitness[best_idx]
    
    for gen in range(generations):
        # Seleção por torneio
        new_population = []
        for _ in range(pop_size):
            # Torneio de tamanho 3
            contestants = random.sample(range(pop_size), 3)
            winner = min(contestants, key=lambda x: fitness[x])
            new_population.append(population[winner].copy())
        
        # Cruzamento (crossover)
        children = []
        for i in range(0, pop_size, 2):
            if i + 1 < pop_size:
                parent1, parent2 = new_population[i], new_population[i+1]
                child1, child2 = [], []
                
                for j in range(len(bounds)):
                    # Crossover aritmético
                    alpha = random.random()
                    child1.append(alpha * parent1[j] + (1 - alpha) * parent2[j])
                    child2.append(alpha * parent2[j] + (1 - alpha) * parent1[j])
                
                children.extend([child1, child2])
        
        # Mutação
        for child in children:
            for j in range(len(bounds)):
                if random.random() < 0.1:  # Taxa de mutação
                    child[j] += random.gauss(0, 0.1)
                    child[j] = max(bounds[j][0], min(bounds[j][1], child[j]))
        
        # Nova população
        population = new_population + children
        population = population[:pop_size]  # Manter tamanho
        
        # Avaliar
        fitness = [objective(ind) for ind in population]
        
        # Atualizar melhor
        current_best_idx = np.argmin(fitness)
        if fitness[current_best_idx] < best_fitness:
            best_individual = population[current_best_idx].copy()
            best_fitness = fitness[current_best_idx]
    
    return best_individual, best_fitness
