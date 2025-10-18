
try:
    import jax
    import jax.numpy as jnp
    from jax import grad, jit, vmap
    from jax.config import config
    config.update('jax_enable_x64', True)
    JAX_AVAILABLE = True
except ImportError:
    JAX_AVAILABLE = False
from typing import List, Dict, Callable

