from gplearn.genetic import SymbolicRegressor

def get_model():
    """
    Retorna uma instância do modelo de regressão simbólica.
    """
    return SymbolicRegressor(population_size=500, generations=20, stopping_criteria=0.01,
                             p_crossover=0.7, p_subtree_mutation=0.1, p_hoist_mutation=0.05,
                             p_point_mutation=0.1, max_samples=0.9, verbose=1,
                             parsimony_coefficient=0.01, random_state=42)
