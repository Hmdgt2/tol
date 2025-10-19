# lib/funcoes_analiticas/teoria_jogos.py
import numpy as np
from typing import List, Dict, Tuple
import itertools

# ============================================================
# Equilíbrios e Estratégias
# ============================================================

def nash_equilibrium_finder(payoff_matrix: List[List[Tuple[float, float]]]) -> Dict:
    """Encontra equilíbrios de Nash aproximados em jogos 2x2."""
    if not payoff_matrix or len(payoff_matrix) != 2 or len(payoff_matrix[0]) != 2:
        return {"error": "Matriz de payoff deve ser 2x2"}
    
    equilibria = []
    
    # Verifica estratégias puras
    for i, j in itertools.product([0, 1], repeat=2):
        row_best = all(payoff_matrix[i][j][0] >= payoff_matrix[1-i][j][0] for i2 in [0, 1])
        col_best = all(payoff_matrix[i][j][1] >= payoff_matrix[i][1-j][1] for j2 in [0, 1])
        
        if row_best and col_best:
            equilibria.append({
                "type": "pure",
                "strategies": (i, j),
                "payoffs": payoff_matrix[i][j],
                "confidence": 1.0
            })
    
    # Verifica estratégias mistas (simplificado)
    try:
        A = np.array([[p[0] for p in row] for row in payoff_matrix])
        B = np.array([[p[1] for p in row] for row in payoff_matrix])
        
        # Solução aproximada para equilíbrio misto
        det_A = np.linalg.det(A)
        if abs(det_A) > 1e-10:
            p_mixed = (A[1,1] - A[1,0]) / (A[0,0] + A[1,1] - A[0,1] - A[1,0])
            q_mixed = (A[1,1] - A[0,1]) / (A[0,0] + A[1,1] - A[0,1] - A[1,0])
            
            if 0 <= p_mixed <= 1 and 0 <= q_mixed <= 1:
                equilibria.append({
                    "type": "mixed",
                    "probabilities": (float(p_mixed), float(q_mixed)),
                    "expected_payoffs": (
                        float(p_mixed * q_mixed * A[0,0] + p_mixed * (1-q_mixed) * A[0,1] + 
                              (1-p_mixed) * q_mixed * A[1,0] + (1-p_mixed) * (1-q_mixed) * A[1,1]),
                        float(p_mixed * q_mixed * B[0,0] + p_mixed * (1-q_mixed) * B[0,1] + 
                              (1-p_mixed) * q_mixed * B[1,0] + (1-p_mixed) * (1-q_mixed) * B[1,1])
                    ),
                    "confidence": 0.8
                })
    except:
        pass
    
    return {
        "equilibria": equilibria,
        "num_equilibria": len(equilibria),
        "game_type": "cooperative" if len(equilibria) > 1 else "competitive"
    }

def shapley_value_calculation(coalitions: Dict[Tuple, float]) -> Dict:
    """Calcula valores de Shapley para sequências cooperativas."""
    if not coalitions:
        return {"error": "Dicionário de coalizões vazio"}
    
    players = set()
    for coalition in coalitions.keys():
        players.update(coalition)
    players = sorted(players)
    
    shapley_values = {player: 0.0 for player in players}
    n = len(players)
    
    # Calcula valor de Shapley para cada jogador
    for player in players:
        for coalition_size in range(n):
            # Peso das coalizões deste tamanho
            weight = math.factorial(coalition_size) * math.factorial(n - coalition_size - 1) / math.factorial(n)
            
            # Todas as coalizões sem o jogador
            other_players = [p for p in players if p != player]
            for sub_coalition in itertools.combinations(other_players, coalition_size):
                coalition_with = tuple(sorted(sub_coalition + (player,)))
                coalition_without = tuple(sorted(sub_coalition))
                
                value_with = coalitions.get(coalition_with, 0)
                value_without = coalitions.get(coalition_without, 0)
                
                marginal_contribution = value_with - value_without
                shapley_values[player] += weight * marginal_contribution
    
    return {
        "shapley_values": shapley_values,
        "efficiency": sum(shapley_values.values()) - coalitions.get(tuple(players), 0),
        "symmetry_score": np.std(list(shapley_values.values())),
        "most_powerful_player": max(shapley_values.items(), key=lambda x: x[1])[0] if shapley_values else None
    }

def prisoner_dilemma_simulation(seq: List[int], rounds: int = 100) -> Dict:
    """Simula dilema do prisioneiro baseado em padrões da sequência."""
    if len(seq) < 4:
        return {"error": "Sequência muito curta para simulação"}
    
    # Estratégias baseadas na sequência
    def tit_for_tat(history):
        return history[-1] if history else 0
    
    def always_cooperate(history):
        return 0
    
    def always_defect(history):
        return 1
    
    def sequence_based(history, seq_pattern):
        if not history:
            return seq_pattern[0] % 2
        recent_trend = sum(history[-3:]) / min(3, len(history))
        return 1 if recent_trend > 0.6 else 0
    
    # Payoffs: (Cooperar, Cooperar) = (3,3), (Defect, Cooperar) = (5,0), etc.
    payoff_matrix = {
        (0, 0): (3, 3),    # Ambos cooperam
        (0, 1): (0, 5),    # A coopera, B deserta
        (1, 0): (5, 0),    # A deserta, B coopera
        (1, 1): (1, 1)     # Ambos desertam
    }
    
    # Simulação
    history_a, history_b = [], []
    scores_a, scores_b = 0, 0
    
    for i in range(rounds):
        move_a = sequence_based(history_b, seq)
        move_b = tit_for_tat(history_a)
        
        payoff = payoff_matrix[(move_a, move_b)]
        scores_a += payoff[0]
        scores_b += payoff[1]
        
        history_a.append(move_a)
        history_b.append(move_b)
    
    cooperation_rate_a = 1 - sum(history_a) / len(history_a)
    cooperation_rate_b = 1 - sum(history_b) / len(history_b)
    
    return {
        "final_scores": (scores_a, scores_b),
        "cooperation_rates": (cooperation_rate_a, cooperation_rate_b),
        "strategy_efficiency": (scores_a / rounds, scores_b / rounds),
        "dominant_strategy": "A" if scores_a > scores_b else "B" if scores_b > scores_a else "Tie",
        "mutual_cooperation_ratio": sum(1 for a, b in zip(history_a, history_b) if a == 0 and b == 0) / rounds
    }
