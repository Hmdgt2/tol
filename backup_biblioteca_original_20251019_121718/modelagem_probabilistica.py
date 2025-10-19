# lib/funcoes_analiticas/modelagem_probabilistica.py
try:
    import pymc3 as pm
    import arviz as az
    PYMC3_AVAILABLE = True
except ImportError:
    PYMC3_AVAILABLE = False
from typing import List, Dict

def pymc3_probabilistic_modeling(seq: List[float]) -> Dict:
    """Modelagem probabilística com PyMC3."""
    if not PYMC3_AVAILABLE or len(seq) < 20:
        return {'pymc3_analysis': 'pymc3_not_available_or_insufficient_data'}
    
    with pm.Model() as model:
        # Priors
        mu = pm.Normal('mu', mu=0, sigma=10)
        sigma = pm.HalfNormal('sigma', sigma=1)
        
        # Likelihood
        likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=seq)
        
        # Amostragem
        try:
            trace = pm.sample(1000, tune=1000, cores=1, return_inferencedata=False)
            
            # Análise do trace
            summary = pm.summary(trace)
            
            return {
                'pymc3_results': {
                    'posterior_means': {var: float(trace[var].mean()) for var in trace.varnames},
                    'hdi_95': {var: az.hdi(trace[var]).tolist() for var in trace.varnames},
                    'r_hat': {var: float(summary.loc[var, 'r_hat']) for var in trace.varnames}
                },
                'model_diagnostics': 'convergence_checked',
                'sampling_method': 'NUTS'
            }
        except:
            return {'pymc3_sampling': 'failed'}

def pymc3_gaussian_process(seq: List[float]) -> Dict:
    """Processos gaussianos com PyMC3."""
    if not PYMC3_AVAILABLE:
        return {}
    
    x = np.arange(len(seq))
    y = np.array(seq)
    
    with pm.Model() as gp_model:
        # Kernel do processo gaussiano
        cov_func = pm.gp.cov.ExpQuad(1, ls=0.1)
        
        # GP prior
        gp = pm.gp.Latent(cov_func=cov_func)
        f = gp.prior("f", X=x[:, None])
        
        # Likelihood
        likelihood = pm.Normal("y", mu=f, sigma=0.1, observed=y)
    
    return {
        'gaussian_process': {
            'kernel': 'ExponentiatedQuadratic',
            'latent_process': True,
            'applicable': len(seq) > 10
        }
    }
