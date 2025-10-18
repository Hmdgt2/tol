


def evolutionary_fractal_dimension(seq: List[float], window_sizes: List[int]=[10, 20, 50]) -> Dict:
    'Dimensão fractal evolutiva em múltiplas escalas temporais.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    results = {}
    for window in window_sizes:
        if (len(seq) >= (window * 2)):
            segments = [seq[i:(i + window)] for i in range(0, ((len(seq) - window) + 1), (window // 2))]
            fractal_dims = []
            for segment in segments:
                if (len(segment) > 1):
                    L = []
                    for k in range(1, min(10, (len(segment) // 2))):
                        Lk = 0
                        for m in range(k):
                            idx = np.arange(m, len(segment), k)
                            if (len(idx) > 1):
                                Lkm = np.sum(np.abs(np.diff([segment[i] for i in idx])))
                                Lkm = ((Lkm * (len(segment) - 1)) / (len(idx) * k))
                                Lk += Lkm
                        L.append(np.log((Lk / k)))
                    if (len(L) > 1):
                        x = np.log(np.arange(1, (len(L) + 1)))
                        slope = np.polyfit(x, L, 1)[0]
                        fractal_dims.append(slope)
            results[f'fractal_window_{window}'] = {'mean': (np.mean(fractal_dims) if fractal_dims else 0), 'trend': (np.polyfit(range(len(fractal_dims)), fractal_dims, 1)[0] if (len(fractal_dims) > 1) else 0)}
    return results


def temporal_pattern_entropy(seq: List[float], time_scales: List[int]=[1, 7, 30, 365]) -> Dict:
    'Entropia de padrões em diferentes escalas temporais (dias, semanas, meses, anos).\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    entropy_results = {}
    for scale in time_scales:
        if (len(seq) >= (scale * 3)):
            aggregated = []
            for i in range(0, ((len(seq) - scale) + 1), scale):
                segment = seq[i:(i + scale)]
                aggregated.append({'mean': np.mean(segment), 'std': np.std(segment), 'range': (max(segment) - min(segment))})
            patterns = []
            for i in range((len(aggregated) - 1)):
                pattern = (('up' if (aggregated[(i + 1)]['mean'] > aggregated[i]['mean']) else 'down'), ('volatile' if (aggregated[(i + 1)]['std'] > aggregated[i]['std']) else 'stable'))
                patterns.append(pattern)
            pattern_counts = {}
            for pattern in patterns:
                pattern_counts[pattern] = (pattern_counts.get(pattern, 0) + 1)
            total = len(patterns)
            entropy = (- sum((((count / total) * np.log((count / total))) for count in pattern_counts.values() if (count > 0))))
            entropy_results[f'temporal_entropy_scale_{scale}'] = entropy
    return entropy_results


def phase_transition_detector(seq: List[float], sensitivity: float=2.0) -> Dict:
    'Detecta transições de fase em séries temporais longas.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    if (len(seq) < 50):
        return {}
    window_size = max(10, (len(seq) // 20))
    regimes = []
    for i in range(0, ((len(seq) - window_size) + 1), (window_size // 2)):
        window = seq[i:(i + window_size)]
        regimes.append({'mean': np.mean(window), 'std': np.std(window), 'start': i, 'end': (i + window_size)})
    transitions = []
    for i in range(1, len(regimes)):
        prev = regimes[(i - 1)]
        curr = regimes[i]
        mean_change = (abs((curr['mean'] - prev['mean'])) / (prev['std'] + 1e-10))
        std_change = (abs((curr['std'] - prev['std'])) / (prev['std'] + 1e-10))
        if ((mean_change > sensitivity) or (std_change > sensitivity)):
            transitions.append({'position': curr['start'], 'mean_change': mean_change, 'std_change': std_change, 'type': ('volatility' if (std_change > mean_change) else 'level')})
    return {'transition_count': len(transitions), 'transitions': transitions, 'regime_stability': ((len(transitions) / (len(regimes) - 1)) if (len(regimes) > 1) else 0)}


def critical_slowdown_analysis(seq: List[float]) -> Dict:
    'Análise de desaceleração crítica antes de transições de fase.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    if (len(seq) < 100):
        return {}
    window_size = (len(seq) // 10)
    autocorrs = []
    variances = []
    for i in range(0, ((len(seq) - window_size) + 1), (window_size // 5)):
        window = seq[i:(i + window_size)]
        if (len(window) > 1):
            autocorr = (np.corrcoef(window[:(- 1)], window[1:])[(0, 1)] if (np.std(window) > 0) else 0)
            autocorrs.append((autocorr if (not np.isnan(autocorr)) else 0))
            variances.append(np.var(window))
    critical_signals = []
    for i in range(5, len(autocorrs)):
        recent_autocorr = np.mean(autocorrs[max(0, (i - 5)):i])
        if (recent_autocorr > (np.mean(autocorrs[:i]) + (2 * np.std(autocorrs[:i])))):
            critical_signals.append({'position': (i * (window_size // 5)), 'autocorrelation': recent_autocorr, 'variance': variances[i]})
    return {'critical_slowdown_detected': (len(critical_signals) > 0), 'slowdown_signals': critical_signals, 'autocorrelation_trend': (np.polyfit(range(len(autocorrs)), autocorrs, 1)[0] if autocorrs else 0)}


def sequence_autocorrelation_pattern(seq: List[float], max_lag: int=10) -> Dict:
    'Padrão de autocorrelação multi-lag para detectar periodicidades complexas.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    patterns = {}
    for lag in range(1, min(max_lag, (len(seq) // 2))):
        if (len(seq) > lag):
            corr = np.corrcoef(seq[:(- lag)], seq[lag:])[(0, 1)]
            patterns[f'lag_{lag}'] = (corr if (not np.isnan(corr)) else 0)
    return patterns


def number_theory_pattern_detector(seq: List[int]) -> Dict:
    'Detecta padrões baseados em teoria dos números.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    primes = [x for x in seq if ((x > 1) and all((((x % i) != 0) for i in range(2, (int((x ** 0.5)) + 1)))))]
    evens = [x for x in seq if ((x % 2) == 0)]
    squares = [x for x in seq if ((int((x ** 0.5)) ** 2) == x)]
    cubes = [x for x in seq if ((round((x ** (1 / 3))) ** 3) == x)]
    return {'prime_ratio': ((len(primes) / len(seq)) if seq else 0), 'even_odd_ratio': ((len(evens) / len(seq)) if seq else 0), 'perfect_squares': ((len(squares) / len(seq)) if seq else 0), 'perfect_cubes': ((len(cubes) / len(seq)) if seq else 0), 'modular_patterns': {f'mod_{i}': (len([x for x in seq if ((x % 5) == i)]) / len(seq)) for i in range(5)}}


def recursive_sequence_analyzer(seq: List[float]) -> Dict:
    'Analisa relações recursivas na sequência.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    if (len(seq) < 3):
        return {}
    X = np.column_stack([seq[1:(- 1)], seq[:(- 2)]])
    y = seq[2:]
    try:
        (coeffs, _, _, _) = np.linalg.lstsq(X, y, rcond=None)
        predicted = (X @ coeffs)
        mse = np.mean(((y - predicted) ** 2))
        return {'recursive_coeffs': coeffs.tolist(), 'recursive_mse': mse, 'is_linear_recursive': (mse < (0.1 * np.var(seq)))}
    except:
        return {}

