
try:
    import gmpy2
    from gmpy2 import mpz, mpfr, mpq, fac, fib, is_prime
    GMPY2_AVAILABLE = True
except ImportError:
    GMPY2_AVAILABLE = False
from typing import List, Dict


def _gmpy2_number_theory(seq):
    'Análise de teoria dos números com GMP.'
    int_seq = [mpz(int(abs(x))) for x in seq if (abs(x) < (10 ** 100))]
    return {'prime_tests': [bool(is_prime(x)) for x in int_seq[:10]], 'factorials': [int(fac(x)) for x in int_seq[:5] if (x < 1000)], 'fibonacci': [int(fib(int(x))) for x in seq[:5] if (0 <= x < 10000)], 'gcd_network': _gmpy2_gcd_network(int_seq)}


def _gmpy2_gcd_network(int_seq):
    'Rede de GCDs entre elementos.'
    if (len(int_seq) < 3):
        return {}
    gcd_pairs = {}
    for i in range(min(5, len(int_seq))):
        for j in range((i + 1), min(5, len(int_seq))):
            gcd_val = gmpy2.gcd(int_seq[i], int_seq[j])
            gcd_pairs[f'gcd_{i}_{j}'] = int(gcd_val)
    return gcd_pairs

