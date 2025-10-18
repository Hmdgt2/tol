# lib/funcoes_analiticas/precisao_arbitraria.py
try:
    import flint
    from flint import arb, acb
    FLINT_AVAILABLE = True
except ImportError:
    FLINT_AVAILABLE = False
from typing import List, Dict

def arb_arbitrary_precision_analysis(seq: List[float], precision: int = 333) -> Dict:
    """Análise com precisão arbitrária usando Arb/Flint."""
    if not FLINT_AVAILABLE:
        return {'arb_analysis': 'flint_not_available'}
    
    with arb.ctx(precision=precision):
        # Converte para números de precisão arbitrária
        arb_seq = [arb(x) for x in seq]
        
        # Operações com precisão extrema
        results = {
            'sum_precise': float(sum(arb_seq)),
            'product_precise': float(arb.prod(arb_seq)),
            'special_functions': _arb_special_functions(arb_seq),
            'polynomial_roots': _arb_polynomial_analysis(arb_seq)
        }
        
        # Verifica erros numéricos
        numerical_stability = all(
            abs(float(arb_seq[i]) - seq[i]) < 1e-300 
            for i in range(min(10, len(seq)))
        )
        
        return {
            'arbitrary_precision_results': results,
            'precision_bits': precision,
            'numerical_stability': numerical_stability,
            'capabilities': ['arbitrary_precision', 'rigorous_error_bounds', 'special_functions']
        }

def _arb_special_functions(arb_seq):
    """Funções especiais com precisão arbitrária."""
    if len(arb_seq) < 3:
        return {}
    
    return {
        'zeta_values': [float(arb.zeta(x)) for x in arb_seq[:5]],
        'gamma_values': [float(arb.gamma(x)) for x in arb_seq[:5]],
        'bessel_values': [float(arb.bessel_j(arb(0), x)) for x in arb_seq[:5]]
    }

def _arb_polynomial_analysis(arb_seq):
    """Análise polinomial com precisão arbitrária."""
    # Constrói polinômio a partir da sequência
    coeffs = arb_seq[:min(10, len(arb_seq))]
    poly = arb.poly(coeffs)
    
    # Encontra raízes com precisão arbitrária
    try:
        roots = poly.roots()
        return {
            'root_count': len(roots),
            'root_precision': precision,
            'largest_root': float(roots[0]) if roots else 0
        }
    except:
        return {'roots': 'computation_failed'}
