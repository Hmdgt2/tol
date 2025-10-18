
try:
    import symengine as se
    from symengine import symbols, sin, cos, exp, log, diff, series
    SYMENGINE_AVAILABLE = True
except ImportError:
    SYMENGINE_AVAILABLE = False
from typing import List, Dict


def _symengine_integrate(expr, x):
    'Integração simbólica.'
    try:
        from symengine import integrate
        return str(integrate(expr, x))
    except:
        return 'integration_failed'


def _symengine_find_roots(expr, x):
    'Encontra raízes simbólicas.'
    try:
        from symengine import solve
        solutions = solve(expr, x)
        return [float(sol) for sol in solutions if sol.is_real]
    except:
        return 'root_finding_failed'

