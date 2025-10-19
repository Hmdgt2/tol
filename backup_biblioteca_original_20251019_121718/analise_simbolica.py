# lib/funcoes_analiticas/analise_simbolica.py
import sympy as sp
from sympy import series, limit, diff, integrate
from typing import List, Dict

def symbolic_sequence_analysis(seq: List[float]) -> Dict:
    """Análise simbólica da sequência usando álgebra computacional."""
    x = sp.symbols('x')
    n = sp.symbols('n', integer=True)
    
    # Tenta encontrar fórmula fechada
    try:
        # Cria função geradora simbólica
        terms = [seq[i] * x**i for i in range(min(10, len(seq)))]
        generating_function = sum(terms)
        
        # Expansão em série
        series_expansion = series(generating_function, x, 0, 10)
        
        # Tenta encontrar relação de recorrência
        recurrence = None
        if len(seq) >= 5:
            # Usa método das diferenças
            differences = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
            if all(abs(diff) < 1e-10 for diff in differences):
                recurrence = "constant"
            else:
                second_diff = [differences[i+1] - differences[i] for i in range(len(differences)-1)]
                if all(abs(diff) < 1e-10 for diff in second_diff):
                    recurrence = "linear"
        
        return {
            'generating_function': str(generating_function),
            'series_expansion': str(series_expansion),
            'recurrence_type': recurrence,
            'symbolic_complexity': sp.count_ops(generating_function)
        }
    except:
        return {'error': 'symbolic_analysis_failed'}

def closed_form_expression_finder(seq: List[float]) -> Dict:
    """Tenta encontrar expressão fechada para a sequência."""
    x = sp.symbols('x')
    
    # Testa diferentes formas fechadas
    candidates = []
    
    # Polinômio
    if len(seq) >= 3:
        try:
            poly_coeffs = sp.poly_from_list(seq[:5], x)
            candidates.append(('polynomial', str(poly_coeffs.as_expr())))
        except:
            pass
    
    # Exponencial
    try:
        if all(seq[i] > 0 for i in range(min(5, len(seq)))):
            log_seq = [sp.log(val) for val in seq[:5]]
            if all(abs(log_seq[i+1] - log_seq[i] - (log_seq[1] - log_seq[0])) < 0.1 
                   for i in range(1, len(log_seq)-1)):
                a = sp.exp(log_seq[0])
                r = sp.exp(log_seq[1] - log_seq[0])
                candidates.append(('exponential', f"{a} * {r}^n"))
    except:
        pass
    
    return {
        'candidate_expressions': candidates,
        'expression_count': len(candidates)
    }
