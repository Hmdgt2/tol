


def simulated_annealing(objective: Callable, bounds: List[Tuple], max_iter: int=1000, temp: float=100.0) -> Tuple:
    'Algoritmo de simulated annealing para otimização.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    best_solution = [random.uniform(b[0], b[1]) for b in bounds]
    best_score = objective(best_solution)
    (current_solution, current_score) = (best_solution, best_score)
    for i in range(max_iter):
        candidate = []
        for j in range(len(bounds)):
            candidate.append((current_solution[j] + random.gauss(0, 1)))
            candidate[j] = max(bounds[j][0], min(bounds[j][1], candidate[j]))
        candidate_score = objective(candidate)
        if (candidate_score < current_score):
            (current_solution, current_score) = (candidate, candidate_score)
            if (candidate_score < best_score):
                (best_solution, best_score) = (candidate, candidate_score)
        else:
            acceptance_prob = np.exp(((- (candidate_score - current_score)) / temp))
            if (random.random() < acceptance_prob):
                (current_solution, current_score) = (candidate, candidate_score)
        temp *= 0.95
    return (best_solution, best_score)


def particle_swarm_optimization(objective: Callable, bounds: List[Tuple], n_particles: int=30, max_iter: int=100) -> Tuple:
    'Otimização por enxame de partículas.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    particles = []
    velocities = []
    personal_best = []
    personal_best_scores = []
    for _ in range(n_particles):
        particle = [random.uniform(b[0], b[1]) for b in bounds]
        particles.append(particle)
        velocities.append([random.uniform((- 1), 1) for _ in bounds])
        personal_best.append(particle.copy())
        personal_best_scores.append(objective(particle))
    global_best_idx = np.argmin(personal_best_scores)
    global_best = personal_best[global_best_idx].copy()
    global_best_score = personal_best_scores[global_best_idx]
    w = 0.729
    c1 = 1.494
    c2 = 1.494
    for _ in range(max_iter):
        for i in range(n_particles):
            for j in range(len(bounds)):
                (r1, r2) = (random.random(), random.random())
                cognitive = ((c1 * r1) * (personal_best[i][j] - particles[i][j]))
                social = ((c2 * r2) * (global_best[j] - particles[i][j]))
                velocities[i][j] = (((w * velocities[i][j]) + cognitive) + social)
            for j in range(len(bounds)):
                particles[i][j] += velocities[i][j]
                particles[i][j] = max(bounds[j][0], min(bounds[j][1], particles[i][j]))
            score = objective(particles[i])
            if (score < personal_best_scores[i]):
                personal_best[i] = particles[i].copy()
                personal_best_scores[i] = score
                if (score < global_best_score):
                    global_best = particles[i].copy()
                    global_best_score = score
    return (global_best, global_best_score)


def genetic_algorithm(objective: Callable, bounds: List[Tuple], pop_size: int=50, generations: int=100) -> Tuple:
    'Algoritmo genético simples.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    population = []
    for _ in range(pop_size):
        individual = [random.uniform(b[0], b[1]) for b in bounds]
        population.append(individual)
    fitness = [objective(ind) for ind in population]
    best_idx = np.argmin(fitness)
    best_individual = population[best_idx].copy()
    best_fitness = fitness[best_idx]
    for gen in range(generations):
        new_population = []
        for _ in range(pop_size):
            contestants = random.sample(range(pop_size), 3)
            winner = min(contestants, key=(lambda x: fitness[x]))
            new_population.append(population[winner].copy())
        children = []
        for i in range(0, pop_size, 2):
            if ((i + 1) < pop_size):
                (parent1, parent2) = (new_population[i], new_population[(i + 1)])
                (child1, child2) = ([], [])
                for j in range(len(bounds)):
                    alpha = random.random()
                    child1.append(((alpha * parent1[j]) + ((1 - alpha) * parent2[j])))
                    child2.append(((alpha * parent2[j]) + ((1 - alpha) * parent1[j])))
                children.extend([child1, child2])
        for child in children:
            for j in range(len(bounds)):
                if (random.random() < 0.1):
                    child[j] += random.gauss(0, 0.1)
                    child[j] = max(bounds[j][0], min(bounds[j][1], child[j]))
        population = (new_population + children)
        population = population[:pop_size]
        fitness = [objective(ind) for ind in population]
        current_best_idx = np.argmin(fitness)
        if (fitness[current_best_idx] < best_fitness):
            best_individual = population[current_best_idx].copy()
            best_fitness = fitness[current_best_idx]
    return (best_individual, best_fitness)


def convex_function_test(f: Callable[([float], float)], domain: List[float], samples: int=100) -> bool:
    'Testa se função é convexa.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    x_vals = np.linspace(domain[0], domain[1], samples)
    for i in range(1, (len(x_vals) - 1)):
        (x1, x2, x3) = (x_vals[(i - 1)], x_vals[i], x_vals[(i + 1)])
        (f1, f2, f3) = (f(x1), f(x2), f(x3))
        if (f2 > (((f1 + f3) / 2) + 1e-06)):
            return False
    return True


def subgradient_method(f: Callable[([List[float]], float)], subgrad: Callable[([List[float]], List[float])], x0: List[float], steps: int=100) -> List[float]:
    'Método do subgradiente para otimização não-suave.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    x = np.array(x0)
    best_x = x.copy()
    best_f = f(x)
    for k in range(steps):
        g = np.array(subgrad(x))
        step_size = (1.0 / (k + 1))
        x = (x - (step_size * g))
        current_f = f(x)
        if (current_f < best_f):
            best_f = current_f
            best_x = x.copy()
    return best_x.tolist()


def lagrange_duality(primal_obj: Callable, constraints: List[Callable], x0: List[float]) -> float:
    'Valor dual de problema de otimização.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'

    def lagrangian(x, lambdas):
        penalty = sum(((lambdas[i] * max(0, constraints[i](x))) for i in range(len(constraints))))
        return (primal_obj(x) + penalty)
    best_dual = (- np.inf)
    for lambda_val in [0.1, 1.0, 10.0]:
        lambdas = ([lambda_val] * len(constraints))
        dual_val = (- lagrangian(x0, lambdas))
        best_dual = max(best_dual, dual_val)
    return best_dual


def barrier_method(f: Callable[([List[float]], float)], constraints: List[Callable], x0: List[float], mu: float=10.0) -> List[float]:
    'Método de barreira para otimização com restrições.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'

    def barrier_function(x):
        barrier = 0.0
        for constr in constraints:
            if (constr(x) >= 0):
                barrier += (- np.log((- constr(x))))
            else:
                barrier += 10000000000.0
        return (f(x) + (mu * barrier))
    result = optimize.minimize(barrier_function, x0, method='BFGS')
    return (result.x.tolist() if result.success else x0)


def polynomial_pattern_fitter(seq: List[float], max_degree: int=5) -> Dict:
    'Encontra o melhor polinômio que se ajusta à sequência.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    x = np.arange(len(seq))
    y = np.array(seq)
    best_fit = {}
    for degree in range(1, min((max_degree + 1), len(seq))):
        try:
            coeffs = np.polyfit(x, y, degree)
            predicted = np.polyval(coeffs, x)
            r_squared = (1 - (np.sum(((y - predicted) ** 2)) / np.sum(((y - np.mean(y)) ** 2))))
            if ((not best_fit) or (r_squared > best_fit.get('r_squared', (- 1)))):
                best_fit = {'degree': degree, 'coefficients': coeffs.tolist(), 'r_squared': r_squared, 'mse': np.mean(((y - predicted) ** 2))}
        except:
            continue
    return best_fit


def exponential_pattern_detector(seq: List[float]) -> Dict:
    'Detecta padrões exponenciais e logarítmicos.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    if ((len(seq) < 3) or any(((x <= 0) for x in seq))):
        return {}
    x = np.arange(len(seq))
    y = np.array(seq)
    patterns = {}
    try:

        def exp_func(x, a, b):
            return (a * np.exp((b * x)))
        (popt, pcov) = curve_fit(exp_func, x, y, p0=[y[0], 0.1])
        predicted = exp_func(x, *popt)
        r_squared = (1 - (np.sum(((y - predicted) ** 2)) / np.sum(((y - np.mean(y)) ** 2))))
        patterns['exponential'] = {'parameters': popt.tolist(), 'r_squared': r_squared}
    except:
        pass
    try:

        def log_func(x, a, b, c):
            return (a * np.log(((b * x) + c)))
        (popt, pcov) = curve_fit(log_func, x, y, p0=[y[0], 1, 1])
        predicted = log_func(x, *popt)
        r_squared = (1 - (np.sum(((y - predicted) ** 2)) / np.sum(((y - np.mean(y)) ** 2))))
        patterns['logarithmic'] = {'parameters': popt.tolist(), 'r_squared': r_squared}
    except:
        pass
    return patterns

