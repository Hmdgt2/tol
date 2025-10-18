
try:
    import pymc3 as pm
    import arviz as az
    PYMC3_AVAILABLE = True
except ImportError:
    PYMC3_AVAILABLE = False
from typing import List, Dict


def pymc3_gaussian_process(seq: List[float]) -> Dict:
    'Processos gaussianos com PyMC3.'
    if (not PYMC3_AVAILABLE):
        return {}
    x = np.arange(len(seq))
    y = np.array(seq)
    with pm.Model() as gp_model:
        cov_func = pm.gp.cov.ExpQuad(1, ls=0.1)
        gp = pm.gp.Latent(cov_func=cov_func)
        f = gp.prior('f', X=x[(:, None)])
        likelihood = pm.Normal('y', mu=f, sigma=0.1, observed=y)
    return {'gaussian_process': {'kernel': 'ExponentiatedQuadratic', 'latent_process': True, 'applicable': (len(seq) > 10)}}

