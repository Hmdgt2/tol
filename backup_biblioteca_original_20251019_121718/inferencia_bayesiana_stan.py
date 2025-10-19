# lib/funcoes_analiticas/inferencia_bayesiana_stan.py
try:
    import cmdstanpy
    import stan
    STAN_AVAILABLE = True
except ImportError:
    STAN_AVAILABLE = False
from typing import List, Dict

def stan_bayesian_inference(seq: List[float]) -> Dict:
    """Inferência bayesiana com Stan."""
    if not STAN_AVAILABLE:
        return {'stan_analysis': 'cmdstanpy_not_available'}
    
    stan_code = """
    data {
        int<lower=0> N;
        vector[N] y;
    }
    parameters {
        real mu;
        real<lower=0> sigma;
    }
    model {
        mu ~ normal(0, 10);
        sigma ~ cauchy(0, 5);
        y ~ normal(mu, sigma);
    }
    """
    
    stan_data = {
        'N': len(seq),
        'y': seq
    }
    
    try:
        posterior = stan.build(stan_code, data=stan_data)
        fit = posterior.sample(num_chains=4, num_samples=1000)
        
        return {
            'stan_results': {
                'mu_mean': float(np.mean(fit['mu'])),
                'sigma_mean': float(np.mean(fit['sigma'])),
                'divergences': fit.diagnose().count('divergence')
            },
            'stan_features': ['HMC', 'NUTS', 'compiled_C++', 'autodiff']
        }
    except Exception as e:
        return {'stan_sampling': f'failed: {str(e)}'}
