# lib/funcoes_analiticas/biologia_matematica.py
import numpy as np
from typing import List, Dict, Tuple
from scipy.integrate import odeint

# ============================================================
# Dinâmica Populacional e Epidemiológica
# ============================================================

def lotka_volterra_dynamics(populations: List[Tuple[float, float]], 
                          parameters: Dict = None) -> Dict:
    """Simula dinâmica de Lotka-Volterra para populações predador-presa."""
    if len(populations) < 2:
        return {"error": "Pelo menos duas populações necessárias"}
    
    if parameters is None:
        parameters = {
            'growth_rate': 0.1,
            'predation_rate': 0.01,
            'predator_death_rate': 0.05,
            'conversion_efficiency': 0.1
        }
    
    # Sistema de equações diferenciais
    def lotka_volterra_eq(y, t, params):
        prey, predator = y
        alpha, beta, delta, gamma = params
        
        dprey_dt = alpha * prey - beta * prey * predator
        dpredator_dt = delta * beta * prey * predator - gamma * predator
        
        return [dprey_dt, dpredator_dt]
    
    # Simulação
    time_points = np.linspace(0, 100, 1000)
    initial_conditions = [populations[0][0], populations[0][1]]
    params = [parameters['growth_rate'], parameters['predation_rate'],
              parameters['conversion_efficiency'], parameters['predator_death_rate']]
    
    solution = odeint(lotka_volterra_eq, initial_conditions, time_points, args=(params,))
    
    # Análise de estabilidade
    stability = analyze_lotka_volterra_stability(solution)
    
    return {
        "time_series": {
            "time": time_points.tolist(),
            "prey_population": solution[:, 0].tolist(),
            "predator_population": solution[:, 1].tolist()
        },
        "equilibrium_points": find_equilibrium_points(params),
        "stability_analysis": stability,
        "oscillation_properties": {
            "period": calculate_oscillation_period(solution),
            "amplitude_prey": np.std(solution[:, 0]),
            "amplitude_predator": np.std(solution[:, 1]),
            "phase_difference": calculate_phase_difference(solution[:, 0], solution[:, 1])
        },
        "bifurcation_analysis": analyze_lotka_volterra_bifurcations(parameters)
    }

def epidemic_spread_model(parameters: Dict) -> Dict:
    """Modela propagação de epidemia usando modelo SIR/SEIR."""
    model_type = parameters.get('model_type', 'SIR')
    population = parameters.get('population', 1000)
    initial_infected = parameters.get('initial_infected', 1)
    
    # Parâmetros epidemiológicos
    beta = parameters.get('infection_rate', 0.3)  # Taxa de infecção
    gamma = parameters.get('recovery_rate', 0.1)  # Taxa de recuperação
    sigma = parameters.get('incubation_rate', 0.2)  # Para SEIR
    
    def sir_model(y, t, beta, gamma):
        S, I, R = y
        dS_dt = -beta * S * I / population
        dI_dt = beta * S * I / population - gamma * I
        dR_dt = gamma * I
        return [dS_dt, dI_dt, dR_dt]
    
    def seir_model(y, t, beta, gamma, sigma):
        S, E, I, R = y
        dS_dt = -beta * S * I / population
        dE_dt = beta * S * I / population - sigma * E
        dI_dt = sigma * E - gamma * I
        dR_dt = gamma * I
        return [dS_dt, dE_dt, dI_dt, dR_dt]
    
    # Condições iniciais e simulação
    time_points = np.linspace(0, 200, 1000)
    
    if model_type == 'SIR':
        initial_conditions = [population - initial_infected, initial_infected, 0]
        solution = odeint(sir_model, initial_conditions, time_points, args=(beta, gamma))
        compartments = ['Susceptible', 'Infected', 'Recovered']
    else:  # SEIR
        initial_conditions = [population - initial_infected, 0, initial_infected, 0]
        solution = odeint(seir_model, initial_conditions, time_points, args=(beta, gamma, sigma))
        compartments = ['Susceptible', 'Exposed', 'Infected', 'Recovered']
    
    # Métricas epidemiológicas
    r0 = beta / gamma  # Número básico de reprodução
    herd_immunity_threshold = 1 - 1/r0 if r0 > 1 else 0
    
    return {
        "model_type": model_type,
        "compartments": compartments,
        "time_series": {
            "time": time_points.tolist(),
            "data": solution.tolist()
        },
        "epidemiological_metrics": {
            "basic_reproduction_number": r0,
            "herd_immunity_threshold": herd_immunity_threshold,
            "peak_infection": np.max(solution[:, 2] if model_type == 'SIR' else solution[:, 3]),
            "final_size": solution[-1, -1] / population  # Fração recuperada final
        },
        "intervention_analysis": analyze_intervention_effects(parameters, solution),
        "stochastic_variability": estimate_stochastic_variability(parameters)
    }

def evolutionary_game_dynamics(strategies: List[str], payoffs: Dict) -> Dict:
    """Analisa dinâmica evolutiva em teoria dos jogos."""
    if len(strategies) < 2:
        return {"error": "Pelo menos duas estratégias necessárias"}
    
    # Matriz de payoff
    payoff_matrix = build_payoff_matrix(strategies, payoffs)
    
    # Equações de replicador
    def replicator_dynamics(x, t, A):
        # x: frequências das estratégias
        # A: matriz de payoff
        fitness = A @ x
        avg_fitness = x @ fitness
        return x * (fitness - avg_fitness)
    
    # Simulação
    time_points = np.linspace(0, 100, 1000)
    initial_frequencies = np.ones(len(strategies)) / len(strategies)
    
    solution = odeint(replicator_dynamics, initial_frequencies, time_points, args=(payoff_matrix,))
    
    # Análise de ESS (Evolutionarily Stable Strategy)
    ess_analysis = find_evolutionarily_stable_strategies(payoff_matrix, strategies)
    
    return {
        "strategies": strategies,
        "payoff_matrix": payoff_matrix.tolist(),
        "strategy_dynamics": {
            "time": time_points.tolist(),
            "frequencies": solution.tolist()
        },
        "evolutionarily_stable_strategies": ess_analysis,
        "nash_equilibria": find_nash_equilibria(payoff_matrix),
        "convergence_analysis": {
            "converged": check_convergence(solution),
            "final_frequencies": solution[-1, :].tolist(),
            "dominant_strategy": strategies[np.argmax(solution[-1, :])] if check_convergence(solution) else None
        }
    }
