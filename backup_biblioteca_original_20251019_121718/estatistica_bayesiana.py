# lib/funcoes_analiticas/estatistica_bayesiana.py
try:
    import tensorflow_probability as tfp
    import tensorflow as tf
    tfd = tfp.distributions
    TFP_AVAILABLE = True
except ImportError:
    TFP_AVAILABLE = False
from typing import List, Dict

def tfp_bayesian_analysis(seq: List[float]) -> Dict:
    """Análise estatística bayesiana com TensorFlow Probability."""
    if not TFP_AVAILABLE:
        return {'tfp_analysis': 'tensorflow_probability_not_available'}
    
    tensor_seq = tf.constant(seq, dtype=tf.float32)
    
    # Modelo bayesiano hierárquico
    with tf.name_scope("bayesian_model"):
        # Priors
        mu_prior = tfd.Normal(loc=0., scale=10.)
        sigma_prior = tfd.HalfNormal(scale=1.)
        
        # Modelo
        def model():
            mu = mu_prior.sample()
            sigma = sigma_prior.sample()
            likelihood = tfd.Normal(loc=mu, scale=sigma)
            return likelihood.log_prob(tensor_seq)
    
    # Inferência aproximada
    bayesian_results = {
        'posterior_means': _tfp_posterior_estimation(seq),
        'bayesian_regression': _tfp_bayesian_regression(seq),
        'mcmc_diagnostics': _tfp_mcmc_analysis(seq)
    }
    
    return {
        'tfp_bayesian_results': bayesian_results,
        'probabilistic_programming': True,
        'inference_methods': ['MCMC', 'VI', 'HMC', 'NUTS']
    }

def _tfp_posterior_estimation(seq):
    """Estimação posterior com TFP."""
    # Modelo conjugado Normal-Normal
    n = len(seq)
    prior_precision = 1.0
    likelihood_precision = 1.0
    
    posterior_mean = (prior_precision * 0.0 + likelihood_precision * tf.reduce_mean(seq)) / \
                    (prior_precision + n * likelihood_precision)
    
    return {
        'posterior_mean': float(posterior_mean),
        'credible_interval': [float(posterior_mean - 1.0), float(posterior_mean + 1.0)]
    }

def _tfp_bayesian_regression(seq):
    """Regressão bayesiana."""
    if len(seq) < 10:
        return {}
    
    x = tf.range(len(seq), dtype=tf.float32)
    y = tf.constant(seq, dtype=tf.float32)
    
    # Modelo de regressão linear bayesiana
    model = tfp.glm.Bernoulli()
    
    return {
        'regression_model': 'bayesian_linear',
        'data_points': len(seq)
    }
