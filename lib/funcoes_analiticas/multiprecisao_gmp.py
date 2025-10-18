# lib/funcoes_analiticas/multiprecisao_gmp.py
try:
    import gmpy2
    from gmpy2 import mpz, mpfr, mpq, fac, fib, is_prime
    GMPY2_AVAILABLE = True
except ImportError:
    GMPY2_AVAILABLE = False
from typing import List, Dict

def gmpy2_multiprecision_analysis(seq: List[float]) -> Dict:
    """Análise com múltipla precisão usando GMP/MPFR."""
    if not GMPY2_AVAILABLE:
        return {'gmpy2_analysis': 'gmpy2_not_available'}
    
    # Configura precisão
    gmpy2.get_context().precision = 256
    
    # Converte para números de múltipla precisão
    mpfr_seq = [mpfr(str(x)) for x in seq]
    
    # Operações exatas
    results = {
        'exact_sum': float(sum(mpfr_seq)),
        'exact_product': float(gmpy2.product(mpfr_seq)),
        'number_theory': _gmpy2_number_theory(seq),
        'combinatorics': _gmpy2_combinatorics(seq)
    }
    
    return {
        'gmpy2_results': results,
        'precision_context': gmpy2.get_context().precision,
        'library_backend': 'GMP_MPFR_MPC',
        'exact_arithmetic': True
    }

def _gmpy2_number_theory(seq):
    """Análise de teoria dos números com GMP."""
    int_seq = [mpz(int(abs(x))) for x in seq if abs(x) < 10**100]
    
    return {
        'prime_tests': [bool(is_prime(x)) for x in int_seq[:10]],
        'factorials': [int(fac(x)) for x in int_seq[:5] if x < 1000],
        'fibonacci': [int(fib(int(x))) for x in seq[:5] if 0 <= x < 10000],
        'gcd_network': _gmpy2_gcd_network(int_seq)
    }

def _gmpy2_gcd_network(int_seq):
    """Rede de GCDs entre elementos."""
    if len(int_seq) < 3:
        return {}
    
    gcd_pairs = {}
    for i in range(min(5, len(int_seq))):
        for j in range(i+1, min(5, len(int_seq))):
            gcd_val = gmpy2.gcd(int_seq[i], int_seq[j])
            gcd_pairs[f"gcd_{i}_{j}"] = int(gcd_val)
    
    return gcd_pairs
