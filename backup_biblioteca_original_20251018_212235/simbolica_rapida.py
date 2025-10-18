# lib/funcoes_analiticas/simbolica_rapida.py
try:
    import symengine as se
    from symengine import symbols, sin, cos, exp, log, diff, series
    SYMENGINE_AVAILABLE = True
except ImportError:
    SYMENGINE_AVAILABLE = False
from typing import List, Dict

def symengine_fast_symbolic(seq: List[float]) -> Dict:
    """Matemática simbólica de alta performance com SymEngine."""
    if not SYMENGINE_AVAILABLE:
        return {'symengine_analysis': 'symengine_not_available'}
    
    x = symbols('x')
    n = symbols('n', integer=True)
    
    # Cria expressão simbólica da sequência
    terms = [seq[i] * x**i for i in range(min(8, len(seq)))]
    symbolic_sum = sum(terms)
    
    # Operações simbólicas otimizadas
    operations = {
        'derivative': str(diff(symbolic_sum, x)),
        'taylor_series': str(series(symbolic_sum, x, 0, 6)),
        'integral': _symengine_integrate(symbolic_sum, x),
        'function_roots': _symengine_find_roots(symbolic_sum, x)
    }
    
    return {
        'symengine_results': operations,
        'performance_characteristics': ['C++_backend', 'fast_symbolic', 'lambdification'],
        'expression_complexity': len(str(symbolic_sum))
    }

def _symengine_integrate(expr, x):
    """Integração simbólica."""
    try:
        from symengine import integrate
        return str(integrate(expr, x))
    except:
        return "integration_failed"

def _symengine_find_roots(expr, x):
    """Encontra raízes simbólicas."""
    try:
        # Tenta encontrar raízes para polinômios simples
        from symengine import solve
        solutions = solve(expr, x)
        return [float(sol) for sol in solutions if sol.is_real]
    except:
        return "root_finding_failed"
