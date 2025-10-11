# Wrappers automáticos para funções analíticas
# Cada wrapper inclui objetivo e finalidade, facilitando integração universal

class GenericFeatureWrapper:
    """
    Objetivo: Genérico
    Finalidade no pipeline: Transformação genérica para integração universal
    """

    @staticmethod
    def apply_function(func, data, *args, **kwargs):
        """
        Aplica função a dados, adaptando tipo de retorno para integração universal.
        """
        result = func(data, *args, **kwargs)
        if isinstance(result, list):
            return result[:5] if len(result) > 5 else result
        elif isinstance(result, dict):
            return list(result.values())[:5]
        elif isinstance(result, (int, float)):
            return [result]
        elif hasattr(result, 'shape'):
            try:
                return result.flatten().tolist()[:5]
            except Exception:
                return [float(result)]
        return result

    @staticmethod
    def kendall_tau(x, y):
        """Calcula o coeficiente de correlação de Kendall.
        
        Args:
            x (List[float]): Primeira amostra.
            y (List[float]): Segunda amostra.
        
        Returns:
            float: Coeficiente de Kendall tau."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_nao_parametrica import kendall_tau
        return GenericFeatureWrapper.apply_function(kendall_tau, x, y)

    @staticmethod
    def spearman_corr(x, y):
        """Calcula o coeficiente de correlação de Spearman.
        
        Args:
            x (List[float]): Primeira amostra.
            y (List[float]): Segunda amostra.
        
        Returns:
            float: Coeficiente de Spearman."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_nao_parametrica import spearman_corr
        return GenericFeatureWrapper.apply_function(spearman_corr, x, y)

    @staticmethod
    def mann_whitney(x, y):
        """Realiza o teste de soma de postos de Mann-Whitney U.
        
        Args:
            x (List[float]): Primeira amostra.
            y (List[float]): Segunda amostra.
        
        Returns:
            float: Estatística U."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_nao_parametrica import mann_whitney
        return GenericFeatureWrapper.apply_function(mann_whitney, x, y)

    @staticmethod
    def kruskal_test():
        """Realiza o teste de Kruskal-Wallis H para múltiplos grupos.
        
        Args:
            *groups (List[float]): Um ou mais grupos de amostras.
        
        Returns:
            float: Estatística H."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_nao_parametrica import kruskal_test
        return GenericFeatureWrapper.apply_function(kruskal_test, )

    @staticmethod
    def wilcoxon_test(x, y):
        """Realiza o teste de soma de postos de Wilcoxon para amostras pareadas.
        
        Args:
            x (List[float]): Primeira amostra.
            y (List[float]): Segunda amostra.
        
        Returns:
            float: Estatística W."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_nao_parametrica import wilcoxon_test
        return GenericFeatureWrapper.apply_function(wilcoxon_test, x, y)

    @staticmethod
    def median_test(x, y):
        """Calcula a diferença entre as medianas de duas amostras.
        
        Args:
            x (List[float]): Primeira amostra.
            y (List[float]): Segunda amostra.
        
        Returns:
            float: Diferença entre as medianas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_nao_parametrica import median_test
        return GenericFeatureWrapper.apply_function(median_test, x, y)

    @staticmethod
    def range_stat(lst):
        """Calcula a amplitude (range) de uma amostra.
        
        Args:
            lst (List[float]): Lista de valores.
        
        Returns:
            float: Valor máximo menos mínimo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_nao_parametrica import range_stat
        return GenericFeatureWrapper.apply_function(range_stat, lst)

    @staticmethod
    def factorial_func(a):
        """Calcula o fatorial de um número inteiro não negativo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria import factorial_func
        return GenericFeatureWrapper.apply_function(factorial_func, a)

    @staticmethod
    def comb_func(n, k):
        """Calcula as combinações de n elementos em grupos de k."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria import comb_func
        return GenericFeatureWrapper.apply_function(comb_func, n, k)

    @staticmethod
    def perm_func(n, k):
        """Calcula as permutações de n elementos em grupos de k."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria import perm_func
        return GenericFeatureWrapper.apply_function(perm_func, n, k)

    @staticmethod
    def multinomial_coef(lst):
        """Calcula o coeficiente multinomial de uma lista de números."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria import multinomial_coef
        return GenericFeatureWrapper.apply_function(multinomial_coef, lst)

    @staticmethod
    def simulate_multinomial_prob(lst, probabilities, trials):
        """Simula uma distribuição multinomial."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade_distribuicoes import simulate_multinomial_prob
        return GenericFeatureWrapper.apply_function(simulate_multinomial_prob, lst, probabilities, trials)

    @staticmethod
    def simulate_dirichlet(alpha, size):
        """Simula uma distribuição de Dirichlet."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade_distribuicoes import simulate_dirichlet
        return GenericFeatureWrapper.apply_function(simulate_dirichlet, alpha, size)

    @staticmethod
    def simulate_multivariate_wishart(df, scale, size):
        """Simula uma distribuição de Wishart multivariada (avançada)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade_distribuicoes import simulate_multivariate_wishart
        return GenericFeatureWrapper.apply_function(simulate_multivariate_wishart, df, scale, size)

    @staticmethod
    def mpmath_sqrt(x):
        """Calcula a raiz quadrada de x com alta precisão."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.precisao import mpmath_sqrt
        return GenericFeatureWrapper.apply_function(mpmath_sqrt, x)

    @staticmethod
    def mpmath_log(x):
        """Calcula o logaritmo natural de x com alta precisão.
        
        Retorna None se x <= 0."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.precisao import mpmath_log
        return GenericFeatureWrapper.apply_function(mpmath_log, x)

    @staticmethod
    def mpmath_sin(x):
        """Calcula o seno de x com alta precisão."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.precisao import mpmath_sin
        return GenericFeatureWrapper.apply_function(mpmath_sin, x)

    @staticmethod
    def mpmath_prod_list(lst):
        """Calcula o produto dos elementos de uma lista com alta precisão."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.precisao import mpmath_prod_list
        return GenericFeatureWrapper.apply_function(mpmath_prod_list, lst)

    @staticmethod
    def mpmath_sum_list(lst):
        """Calcula a soma dos elementos de uma lista com alta precisão."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.precisao import mpmath_sum_list
        return GenericFeatureWrapper.apply_function(mpmath_sum_list, lst)

    @staticmethod
    def sum_of_pairs(lst):
        """Calcula a soma de todas as combinações de pares."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_padroes import sum_of_pairs
        return GenericFeatureWrapper.apply_function(sum_of_pairs, lst)

    @staticmethod
    def sum_of_triples(lst):
        """Calcula a soma de todas as combinações de trios."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_padroes import sum_of_triples
        return GenericFeatureWrapper.apply_function(sum_of_triples, lst)

    @staticmethod
    def diff_of_pairs(lst):
        """Calcula a diferença absoluta de todos os pares."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_padroes import diff_of_pairs
        return GenericFeatureWrapper.apply_function(diff_of_pairs, lst)

    @staticmethod
    def count_pair_sums_equal(lst, value):
        """Conta os pares cuja soma é igual a um valor."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_padroes import count_pair_sums_equal
        return GenericFeatureWrapper.apply_function(count_pair_sums_equal, lst, value)

    @staticmethod
    def score_even_odd(lst):
        """Pontua a lista com base na paridade dos elementos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_padroes import score_even_odd
        return GenericFeatureWrapper.apply_function(score_even_odd, lst)

    @staticmethod
    def score_prime(lst):
        """Pontua a lista com base na presença de números primos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_padroes import score_prime
        return GenericFeatureWrapper.apply_function(score_prime, lst)

    @staticmethod
    def score_pairs_sum_mod(lst, k):
        """Pontua a lista com base na soma dos pares módulo k."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_padroes import score_pairs_sum_mod
        return GenericFeatureWrapper.apply_function(score_pairs_sum_mod, lst, k)

    @staticmethod
    def score_cumulative_diff(lst):
        """Pontua a lista com base na soma das diferenças absolutas consecutivas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_padroes import score_cumulative_diff
        return GenericFeatureWrapper.apply_function(score_cumulative_diff, lst)

    @staticmethod
    def most_frequent_pairs(lst):
        """Encontra os pares mais frequentes na lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_padroes import most_frequent_pairs
        return GenericFeatureWrapper.apply_function(most_frequent_pairs, lst)

    @staticmethod
    def cluster_by_diff(lst, max_diff):
        """Agrupa números que estão próximos uns dos outros."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_padroes import cluster_by_diff
        return GenericFeatureWrapper.apply_function(cluster_by_diff, lst, max_diff)

    @staticmethod
    def unique_count(lst):
        """Conta o número de elementos únicos em uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatisticas import unique_count
        return GenericFeatureWrapper.apply_function(unique_count, lst)

    @staticmethod
    def intersection(lst1, lst2):
        """Retorna os elementos em comum entre duas listas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatisticas import intersection
        return GenericFeatureWrapper.apply_function(intersection, lst1, lst2)

    @staticmethod
    def union(lst1, lst2):
        """Retorna a união de elementos de duas listas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatisticas import union
        return GenericFeatureWrapper.apply_function(union, lst1, lst2)

    @staticmethod
    def difference(lst1, lst2):
        """Retorna os elementos de lst1 que não estão em lst2."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatisticas import difference
        return GenericFeatureWrapper.apply_function(difference, lst1, lst2)

    @staticmethod
    def symmetric_difference(lst1, lst2):
        """Retorna os elementos que estão em lst1 ou lst2, mas não em ambos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatisticas import symmetric_difference
        return GenericFeatureWrapper.apply_function(symmetric_difference, lst1, lst2)

    @staticmethod
    def mirror_count(lst, total):
        """Conta os números que têm um 'espelho' na lista (e.g., total - x)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatisticas import mirror_count
        return GenericFeatureWrapper.apply_function(mirror_count, lst, total)

    @staticmethod
    def pair_sum_count(lst, target):
        """Conta os pares de números que somam um valor alvo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatisticas import pair_sum_count
        return GenericFeatureWrapper.apply_function(pair_sum_count, lst, target)

    @staticmethod
    def pair_product_count(lst, target):
        """Conta os pares de números que multiplicados dão um valor alvo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatisticas import pair_product_count
        return GenericFeatureWrapper.apply_function(pair_product_count, lst, target)

    @staticmethod
    def count_even(lst):
        """Conta números pares na lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatisticas import count_even
        return GenericFeatureWrapper.apply_function(count_even, lst)

    @staticmethod
    def count_odd(lst):
        """Conta números ímpares na lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatisticas import count_odd
        return GenericFeatureWrapper.apply_function(count_odd, lst)

    @staticmethod
    def diff(lst):
        """Diferença entre elementos consecutivos (x₂ - x₁)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.sequencias import diff
        return GenericFeatureWrapper.apply_function(diff, lst)

    @staticmethod
    def diff_abs(lst):
        """Diferença absoluta entre elementos consecutivos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.sequencias import diff_abs
        return GenericFeatureWrapper.apply_function(diff_abs, lst)

    @staticmethod
    def ratio_consecutive(lst):
        """Razão simples entre elementos consecutivos (x₂ / x₁)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.sequencias import ratio_consecutive
        return GenericFeatureWrapper.apply_function(ratio_consecutive, lst)

    @staticmethod
    def rolling_sum(lst, window):
        """Soma em janela deslizante."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.sequencias import rolling_sum
        return GenericFeatureWrapper.apply_function(rolling_sum, lst, window)

    @staticmethod
    def rolling_mean(lst, window):
        """Média em janela deslizante."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.sequencias import rolling_mean
        return GenericFeatureWrapper.apply_function(rolling_mean, lst, window)

    @staticmethod
    def rolling_std(lst, window):
        """Desvio padrão em janela deslizante."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.sequencias import rolling_std
        return GenericFeatureWrapper.apply_function(rolling_std, lst, window)

    @staticmethod
    def rank_array(lst):
        """Ranking dos elementos de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.sequencias import rank_array
        return GenericFeatureWrapper.apply_function(rank_array, lst)

    @staticmethod
    def sym_derivative(expr):
        """Calcula a derivada de uma expressão simbólica."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_simbolica import sym_derivative
        return GenericFeatureWrapper.apply_function(sym_derivative, expr)

    @staticmethod
    def sym_integral(expr):
        """Calcula a integral indefinida de uma expressão simbólica."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_simbolica import sym_integral
        return GenericFeatureWrapper.apply_function(sym_integral, expr)

    @staticmethod
    def sym_series_expansion(expr, n):
        """Expande uma expressão em série de Taylor em torno de 0."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_simbolica import sym_series_expansion
        return GenericFeatureWrapper.apply_function(sym_series_expansion, expr, n)

    @staticmethod
    def sym_limit(expr, point):
        """Calcula o limite de uma expressão no ponto dado."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_simbolica import sym_limit
        return GenericFeatureWrapper.apply_function(sym_limit, expr, point)

    @staticmethod
    def sym_roots(expr):
        """Encontra as raízes de uma expressão."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_simbolica import sym_roots
        return GenericFeatureWrapper.apply_function(sym_roots, expr)

    @staticmethod
    def sym_simplify(expr):
        """Simplifica uma expressão."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_simbolica import sym_simplify
        return GenericFeatureWrapper.apply_function(sym_simplify, expr)

    @staticmethod
    def sym_expand(expr):
        """Expande uma expressão."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_simbolica import sym_expand
        return GenericFeatureWrapper.apply_function(sym_expand, expr)

    @staticmethod
    def sym_factor(expr):
        """Fatora uma expressão."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_simbolica import sym_factor
        return GenericFeatureWrapper.apply_function(sym_factor, expr)

    @staticmethod
    def fill_missing_values(lst, strategy):
        """Preenche valores ausentes (np.nan) em uma lista usando uma estratégia específica.
        
        Args:
            lst (List[float]): Lista de números com valores ausentes.
            strategy (str): 'mean', 'median' ou 'mode'.
            
        Returns:
            List[float]: Lista com valores ausentes preenchidos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.manipulacao_dados import fill_missing_values
        return GenericFeatureWrapper.apply_function(fill_missing_values, lst, strategy)

    @staticmethod
    def normalize_data(lst):
        """Normaliza os dados para o intervalo [0, 1].
        
        Retorna 0 para todos os valores se todos forem iguais."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.manipulacao_dados import normalize_data
        return GenericFeatureWrapper.apply_function(normalize_data, lst)

    @staticmethod
    def standardize_data(lst):
        """Padroniza os dados (média 0, desvio padrão 1).
        
        Retorna 0 para todos os valores se o desvio padrão for 0."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.manipulacao_dados import standardize_data
        return GenericFeatureWrapper.apply_function(standardize_data, lst)

    @staticmethod
    def get_dummies(lst):
        """Converte uma lista de valores categóricos em variáveis dummy.
        
        Args:
            lst (List[Union[str,int]]): Lista de valores categóricos.
            
        Returns:
            pd.DataFrame: DataFrame com colunas dummy."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.manipulacao_dados import get_dummies
        return GenericFeatureWrapper.apply_function(get_dummies, lst)

    @staticmethod
    def fibonacci(n):
        """Retorna o n-ésimo número de Fibonacci."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.numeros_especiais import fibonacci
        return GenericFeatureWrapper.apply_function(fibonacci, n)

    @staticmethod
    def lucas(n):
        """Retorna o n-ésimo número de Lucas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.numeros_especiais import lucas
        return GenericFeatureWrapper.apply_function(lucas, n)

    @staticmethod
    def catalan_number(n):
        """Retorna o n-ésimo número de Catalan."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.numeros_especiais import catalan_number
        return GenericFeatureWrapper.apply_function(catalan_number, n)

    @staticmethod
    def bell_number(n):
        """Retorna o n-ésimo número de Bell."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.numeros_especiais import bell_number
        return GenericFeatureWrapper.apply_function(bell_number, n)

    @staticmethod
    def partition_number(n):
        """Retorna o número de partições de n."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.numeros_especiais import partition_number
        return GenericFeatureWrapper.apply_function(partition_number, n)

    @staticmethod
    def stirling2(n, k):
        """Retorna o número de Stirling de segunda espécie S(n, k)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.numeros_especiais import stirling2
        return GenericFeatureWrapper.apply_function(stirling2, n, k)

    @staticmethod
    def stirling1(n, k):
        """Retorna o número de Stirling de primeira espécie s(n, k)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.numeros_especiais import stirling1
        return GenericFeatureWrapper.apply_function(stirling1, n, k)

    @staticmethod
    def bernoulli_number(n):
        """Retorna o n-ésimo número de Bernoulli."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.numeros_especiais import bernoulli_number
        return GenericFeatureWrapper.apply_function(bernoulli_number, n)

    @staticmethod
    def floor_div(a, b):
        """Calcula a divisão inteira de dois números (floor division)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import floor_div
        return GenericFeatureWrapper.apply_function(floor_div, a, b)

    @staticmethod
    def ceil_div(a, b):
        """Calcula a divisão inteira arredondada para cima (ceil division)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import ceil_div
        return GenericFeatureWrapper.apply_function(ceil_div, a, b)

    @staticmethod
    def mod_inverse(a, k):
        """Calcula o inverso modular de 'a' mod 'k' (se existir)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import mod_inverse
        return GenericFeatureWrapper.apply_function(mod_inverse, a, k)

    @staticmethod
    def floor_val(a):
        """Retorna o maior inteiro menor ou igual a 'a'."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import floor_val
        return GenericFeatureWrapper.apply_function(floor_val, a)

    @staticmethod
    def ceil_val(a):
        """Retorna o menor inteiro maior ou igual a 'a'."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import ceil_val
        return GenericFeatureWrapper.apply_function(ceil_val, a)

    @staticmethod
    def sqrt_transform(lst):
        """Transformação de raiz quadrada."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import sqrt_transform
        return GenericFeatureWrapper.apply_function(sqrt_transform, lst)

    @staticmethod
    def cbrt_transform(lst):
        """Transformação de raiz cúbica."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import cbrt_transform
        return GenericFeatureWrapper.apply_function(cbrt_transform, lst)

    @staticmethod
    def square_transform(lst):
        """Transformação de potência ao quadrado."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import square_transform
        return GenericFeatureWrapper.apply_function(square_transform, lst)

    @staticmethod
    def cube_transform(lst):
        """Transformação de potência ao cubo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import cube_transform
        return GenericFeatureWrapper.apply_function(cube_transform, lst)

    @staticmethod
    def exp_transform(lst):
        """Transformação exponencial."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import exp_transform
        return GenericFeatureWrapper.apply_function(exp_transform, lst)

    @staticmethod
    def reciprocal_transform(lst):
        """Transformação recíproca (1/x)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import reciprocal_transform
        return GenericFeatureWrapper.apply_function(reciprocal_transform, lst)

    @staticmethod
    def log_transform(lst):
        """Transformação logarítmica (base e)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import log_transform
        return GenericFeatureWrapper.apply_function(log_transform, lst)

    @staticmethod
    def log10_transform(lst):
        """Transformação logarítmica (base 10)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import log10_transform
        return GenericFeatureWrapper.apply_function(log10_transform, lst)

    @staticmethod
    def log_normalize(lst):
        """Normalização com transformação logarítmica."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import log_normalize
        return GenericFeatureWrapper.apply_function(log_normalize, lst)

    @staticmethod
    def sqrt_log_transform(lst):
        """Transformação combinada: raiz da transformação logarítmica."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import sqrt_log_transform
        return GenericFeatureWrapper.apply_function(sqrt_log_transform, lst)

    @staticmethod
    def sin_transform(lst):
        """Transformação seno."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import sin_transform
        return GenericFeatureWrapper.apply_function(sin_transform, lst)

    @staticmethod
    def cos_transform(lst):
        """Transformação cosseno."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import cos_transform
        return GenericFeatureWrapper.apply_function(cos_transform, lst)

    @staticmethod
    def tan_transform(lst):
        """Transformação tangente."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import tan_transform
        return GenericFeatureWrapper.apply_function(tan_transform, lst)

    @staticmethod
    def arcsin_transform(lst):
        """Transformação arcoseno (normalizada pelo valor máximo)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import arcsin_transform
        return GenericFeatureWrapper.apply_function(arcsin_transform, lst)

    @staticmethod
    def arccos_transform(lst):
        """Transformação arccoseno (normalizada pelo valor máximo)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import arccos_transform
        return GenericFeatureWrapper.apply_function(arccos_transform, lst)

    @staticmethod
    def arctan_transform(lst):
        """Transformação arctangente."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import arctan_transform
        return GenericFeatureWrapper.apply_function(arctan_transform, lst)

    @staticmethod
    def centered_sin(lst):
        """Transformação seno centrada na média."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import centered_sin
        return GenericFeatureWrapper.apply_function(centered_sin, lst)

    @staticmethod
    def mod_transform(lst, m):
        """Transformação de módulo (x % m)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import mod_transform
        return GenericFeatureWrapper.apply_function(mod_transform, lst, m)

    @staticmethod
    def minmax_normalize(lst):
        """Normalização Min-Max."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import minmax_normalize
        return GenericFeatureWrapper.apply_function(minmax_normalize, lst)

    @staticmethod
    def zscore_normalize(lst):
        """Normalização Z-Score."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.transformacoes import zscore_normalize
        return GenericFeatureWrapper.apply_function(zscore_normalize, lst)

    @staticmethod
    def z_score_outliers(lst, threshold):
        """Detecta outliers usando o método de Z-score.
        
        Args:
            lst (List[float]): Lista de valores.
            threshold (float): Limite de desvio padrão para considerar outlier.
        
        Returns:
            List[float]: Lista de valores considerados outliers."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.deteccao_anomalias import z_score_outliers
        return GenericFeatureWrapper.apply_function(z_score_outliers, lst, threshold)

    @staticmethod
    def iqr_outliers(lst):
        """Detecta outliers usando o método do Intervalo Interquartil (IQR).
        
        Args:
            lst (List[float]): Lista de valores.
        
        Returns:
            List[float]: Lista de valores considerados outliers."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.deteccao_anomalias import iqr_outliers
        return GenericFeatureWrapper.apply_function(iqr_outliers, lst)

    @staticmethod
    def rolling_z_score(lst, window, threshold):
        """Detecta outliers usando um Z-score móvel.
        
        Args:
            lst (List[float]): Lista de valores.
            window (int): Tamanho da janela móvel.
            threshold (float): Limite de desvio padrão para considerar outlier.
        
        Returns:
            List[float]: Lista de valores considerados outliers, sem duplicados."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.deteccao_anomalias import rolling_z_score
        return GenericFeatureWrapper.apply_function(rolling_z_score, lst, window, threshold)

    @staticmethod
    def create_graph(lst):
        """Cria um grafo completo a partir de uma lista de nós."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import create_graph
        return GenericFeatureWrapper.apply_function(create_graph, lst)

    @staticmethod
    def num_nodes(lst):
        """Retorna o número de nós de um grafo criado a partir de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import num_nodes
        return GenericFeatureWrapper.apply_function(num_nodes, lst)

    @staticmethod
    def num_edges(lst):
        """Retorna o número de arestas de um grafo completo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import num_edges
        return GenericFeatureWrapper.apply_function(num_edges, lst)

    @staticmethod
    def node_degrees(lst):
        """Calcula os graus de cada nó em um grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import node_degrees
        return GenericFeatureWrapper.apply_function(node_degrees, lst)

    @staticmethod
    def graph_degree(lst):
        """Calcula o grau (número de conexões) de cada nó no grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import graph_degree
        return GenericFeatureWrapper.apply_function(graph_degree, lst)

    @staticmethod
    def graph_avg_degree(lst):
        """Calcula o grau médio de todos os nós do grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import graph_avg_degree
        return GenericFeatureWrapper.apply_function(graph_avg_degree, lst)

    @staticmethod
    def mean_degree(lst):
        """Calcula o grau médio de um grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import mean_degree
        return GenericFeatureWrapper.apply_function(mean_degree, lst)

    @staticmethod
    def std_degree(lst):
        """Calcula o desvio padrão dos graus de um grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import std_degree
        return GenericFeatureWrapper.apply_function(std_degree, lst)

    @staticmethod
    def is_complete(lst):
        """Verifica se um grafo criado a partir da lista é completo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import is_complete
        return GenericFeatureWrapper.apply_function(is_complete, lst)

    @staticmethod
    def graph_density(lst):
        """Calcula a densidade do grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import graph_density
        return GenericFeatureWrapper.apply_function(graph_density, lst)

    @staticmethod
    def graph_diameter(lst):
        """Calcula o diâmetro do grafo (maior caminho mais curto)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import graph_diameter
        return GenericFeatureWrapper.apply_function(graph_diameter, lst)

    @staticmethod
    def graph_connected_components_count(lst):
        """Conta o número de componentes conectados no grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import graph_connected_components_count
        return GenericFeatureWrapper.apply_function(graph_connected_components_count, lst)

    @staticmethod
    def graph_connected_components(G):
        """Retorna os componentes conectados de um grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import graph_connected_components
        return GenericFeatureWrapper.apply_function(graph_connected_components, G)

    @staticmethod
    def graph_triangle_count(lst):
        """Conta o número de triângulos no grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import graph_triangle_count
        return GenericFeatureWrapper.apply_function(graph_triangle_count, lst)

    @staticmethod
    def degree_centrality(lst):
        """Calcula a centralidade de grau de cada nó."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import degree_centrality
        return GenericFeatureWrapper.apply_function(degree_centrality, lst)

    @staticmethod
    def closeness_centrality_from_graph(G):
        """Calcula a centralidade de proximidade de um grafo existente."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import closeness_centrality_from_graph
        return GenericFeatureWrapper.apply_function(closeness_centrality_from_graph, G)

    @staticmethod
    def closeness_centrality_from_list(lst):
        """Calcula a centralidade de proximidade de cada nó (grafo criado a partir da lista)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import closeness_centrality_from_list
        return GenericFeatureWrapper.apply_function(closeness_centrality_from_list, lst)

    @staticmethod
    def betweenness_centrality(G):
        """Calcula a centralidade de intermediação de um grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import betweenness_centrality
        return GenericFeatureWrapper.apply_function(betweenness_centrality, G)

    @staticmethod
    def eigenvector_centrality(G):
        """Calcula a centralidade de autovetor de um grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import eigenvector_centrality
        return GenericFeatureWrapper.apply_function(eigenvector_centrality, G)

    @staticmethod
    def pagerank_scores(G, alpha):
        """Calcula os scores de PageRank de um grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import pagerank_scores
        return GenericFeatureWrapper.apply_function(pagerank_scores, G, alpha)

    @staticmethod
    def shortest_paths_length(G):
        """Calcula os comprimentos dos caminhos mais curtos entre todos os pares de nós."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import shortest_paths_length
        return GenericFeatureWrapper.apply_function(shortest_paths_length, G)

    @staticmethod
    def graph_eigenvalues(G):
        """Calcula os autovalores da matriz de adjacência de um grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import graph_eigenvalues
        return GenericFeatureWrapper.apply_function(graph_eigenvalues, G)

    @staticmethod
    def graph_laplacian_spectrum(G):
        """Calcula o espectro Laplaciano de um grafo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.grafos import graph_laplacian_spectrum
        return GenericFeatureWrapper.apply_function(graph_laplacian_spectrum, G)

    @staticmethod
    def arima_predict(lst, order, steps):
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.series_temporais import arima_predict
        return GenericFeatureWrapper.apply_function(arima_predict, lst, order, steps)

    @staticmethod
    def centered_moving_average(lst, window):
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.series_temporais import centered_moving_average
        return GenericFeatureWrapper.apply_function(centered_moving_average, lst, window)

    @staticmethod
    def ewma(lst, span):
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.series_temporais import ewma
        return GenericFeatureWrapper.apply_function(ewma, lst, span)

    @staticmethod
    def exp_weighted_mean(lst, alpha):
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.series_temporais import exp_weighted_mean
        return GenericFeatureWrapper.apply_function(exp_weighted_mean, lst, alpha)

    @staticmethod
    def cumulative_sum(lst):
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.series_temporais import cumulative_sum
        return GenericFeatureWrapper.apply_function(cumulative_sum, lst)

    @staticmethod
    def cumulative_product(lst):
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.series_temporais import cumulative_product
        return GenericFeatureWrapper.apply_function(cumulative_product, lst)

    @staticmethod
    def normalized_cumsum(lst):
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.series_temporais import normalized_cumsum
        return GenericFeatureWrapper.apply_function(normalized_cumsum, lst)

    @staticmethod
    def cumulative_max(lst):
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.series_temporais import cumulative_max
        return GenericFeatureWrapper.apply_function(cumulative_max, lst)

    @staticmethod
    def cumulative_min(lst):
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.series_temporais import cumulative_min
        return GenericFeatureWrapper.apply_function(cumulative_min, lst)

    @staticmethod
    def poisson_pmf(k, mu):
        """Calcula a PMF da distribuição de Poisson."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import poisson_pmf
        return GenericFeatureWrapper.apply_function(poisson_pmf, k, mu)

    @staticmethod
    def poisson_cdf(k, mu):
        """Calcula a CDF da distribuição de Poisson."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import poisson_cdf
        return GenericFeatureWrapper.apply_function(poisson_cdf, k, mu)

    @staticmethod
    def poisson_var(mu):
        """Calcula a variância da distribuição de Poisson."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import poisson_var
        return GenericFeatureWrapper.apply_function(poisson_var, mu)

    @staticmethod
    def poisson_entropy(mu):
        """Calcula a entropia da distribuição de Poisson."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import poisson_entropy
        return GenericFeatureWrapper.apply_function(poisson_entropy, mu)

    @staticmethod
    def binomial_pmf(k, n, p):
        """Calcula a PMF da distribuição binomial."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import binomial_pmf
        return GenericFeatureWrapper.apply_function(binomial_pmf, k, n, p)

    @staticmethod
    def binomial_cdf(k, n, p):
        """Calcula a CDF da distribuição binomial."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import binomial_cdf
        return GenericFeatureWrapper.apply_function(binomial_cdf, k, n, p)

    @staticmethod
    def binomial_var(n, p):
        """Calcula a variância da distribuição binomial."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import binomial_var
        return GenericFeatureWrapper.apply_function(binomial_var, n, p)

    @staticmethod
    def binomial_entropy(n, p):
        """Calcula a entropia da distribuição binomial."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import binomial_entropy
        return GenericFeatureWrapper.apply_function(binomial_entropy, n, p)

    @staticmethod
    def normal_pdf(x, mu, sigma):
        """Calcula a PDF da distribuição normal."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import normal_pdf
        return GenericFeatureWrapper.apply_function(normal_pdf, x, mu, sigma)

    @staticmethod
    def normal_cdf(x, mu, sigma):
        """Calcula a CDF da distribuição normal."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import normal_cdf
        return GenericFeatureWrapper.apply_function(normal_cdf, x, mu, sigma)

    @staticmethod
    def normal_var(sigma):
        """Calcula a variância da distribuição normal."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import normal_var
        return GenericFeatureWrapper.apply_function(normal_var, sigma)

    @staticmethod
    def normal_entropy(mu, sigma):
        """Calcula a entropia da distribuição normal."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import normal_entropy
        return GenericFeatureWrapper.apply_function(normal_entropy, mu, sigma)

    @staticmethod
    def exponential_pdf(x, lmbda):
        """Calcula a PDF da distribuição exponencial."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import exponential_pdf
        return GenericFeatureWrapper.apply_function(exponential_pdf, x, lmbda)

    @staticmethod
    def uniform_pdf(x, a, b):
        """Calcula a PDF da distribuição uniforme."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.probabilidade import uniform_pdf
        return GenericFeatureWrapper.apply_function(uniform_pdf, x, a, b)

    @staticmethod
    def add(a, b):
        """Calcula a soma de dois números."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import add
        return GenericFeatureWrapper.apply_function(add, a, b)

    @staticmethod
    def sub(a, b):
        """Calcula a subtração de dois números."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import sub
        return GenericFeatureWrapper.apply_function(sub, a, b)

    @staticmethod
    def mul(a, b):
        """Calcula a multiplicação de dois números."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import mul
        return GenericFeatureWrapper.apply_function(mul, a, b)

    @staticmethod
    def div(a, b):
        """Calcula a divisão de dois números, evitando divisão por zero."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import div
        return GenericFeatureWrapper.apply_function(div, a, b)

    @staticmethod
    def mod(a, b):
        """Calcula o resto da divisão de dois números, evitando divisão por zero."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import mod
        return GenericFeatureWrapper.apply_function(mod, a, b)

    @staticmethod
    def pow_func(a, b):
        """Calcula a potência de um número."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import pow_func
        return GenericFeatureWrapper.apply_function(pow_func, a, b)

    @staticmethod
    def sqrt(a):
        """Calcula a raiz quadrada de um número."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import sqrt
        return GenericFeatureWrapper.apply_function(sqrt, a)

    @staticmethod
    def cbrt(a):
        """Calcula a raiz cúbica de um número."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import cbrt
        return GenericFeatureWrapper.apply_function(cbrt, a)

    @staticmethod
    def log_func(a):
        """Calcula o logaritmo natural de um número, se for positivo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import log_func
        return GenericFeatureWrapper.apply_function(log_func, a)

    @staticmethod
    def exp_func(a):
        """Calcula o exponencial de um número."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import exp_func
        return GenericFeatureWrapper.apply_function(exp_func, a)

    @staticmethod
    def neg(a):
        """Retorna o negativo de um número."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import neg
        return GenericFeatureWrapper.apply_function(neg, a)

    @staticmethod
    def inv(a):
        """Calcula o inverso de um número, se não for zero."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import inv
        return GenericFeatureWrapper.apply_function(inv, a)

    @staticmethod
    def abs_val(a):
        """Calcula o valor absoluto de um número."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.aritmetica import abs_val
        return GenericFeatureWrapper.apply_function(abs_val, a)

    @staticmethod
    def gamma_func(x):
        """Calcula a função Gamma."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.funcoes_especiais import gamma_func
        return GenericFeatureWrapper.apply_function(gamma_func, x)

    @staticmethod
    def beta_func(a, b):
        """Calcula a função Beta."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.funcoes_especiais import beta_func
        return GenericFeatureWrapper.apply_function(beta_func, a, b)

    @staticmethod
    def zeta_func(s):
        """Calcula a função Zeta de Riemann."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.funcoes_especiais import zeta_func
        return GenericFeatureWrapper.apply_function(zeta_func, s)

    @staticmethod
    def bessel_j(n, x):
        """Calcula a função de Bessel de primeira espécie."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.funcoes_especiais import bessel_j
        return GenericFeatureWrapper.apply_function(bessel_j, n, x)

    @staticmethod
    def legendre_poly(n, x):
        """Calcula o polinómio de Legendre."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.funcoes_especiais import legendre_poly
        return GenericFeatureWrapper.apply_function(legendre_poly, n, x)

    @staticmethod
    def chebyshev_T(n, x):
        """Calcula o polinómio de Chebyshev de primeira espécie."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.funcoes_especiais import chebyshev_T
        return GenericFeatureWrapper.apply_function(chebyshev_T, n, x)

    @staticmethod
    def chebyshev_U(n, x):
        """Calcula o polinómio de Chebyshev de segunda espécie."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.funcoes_especiais import chebyshev_U
        return GenericFeatureWrapper.apply_function(chebyshev_U, n, x)

    @staticmethod
    def hermite_poly(n, x):
        """Calcula o polinómio de Hermite."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.funcoes_especiais import hermite_poly
        return GenericFeatureWrapper.apply_function(hermite_poly, n, x)

    @staticmethod
    def laguerre_poly(n, x):
        """Calcula o polinómio de Laguerre."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.funcoes_especiais import laguerre_poly
        return GenericFeatureWrapper.apply_function(laguerre_poly, n, x)

    @staticmethod
    def discrete_convolution(lst1, lst2):
        """Calcula a convolução discreta de duas listas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.funcoes_especiais import discrete_convolution
        return GenericFeatureWrapper.apply_function(discrete_convolution, lst1, lst2)

    @staticmethod
    def cross_correlation(lst1, lst2):
        """Calcula a correlação cruzada de duas listas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.funcoes_especiais import cross_correlation
        return GenericFeatureWrapper.apply_function(cross_correlation, lst1, lst2)

    @staticmethod
    def primes_in_list(lst):
        """Filtra e retorna os números primos de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import primes_in_list
        return GenericFeatureWrapper.apply_function(primes_in_list, lst)

    @staticmethod
    def count_primes(lst):
        """Conta a quantidade de números primos em uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import count_primes
        return GenericFeatureWrapper.apply_function(count_primes, lst)

    @staticmethod
    def count_primes_below(lst, limit):
        """Conta os primos abaixo de um limite."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import count_primes_below
        return GenericFeatureWrapper.apply_function(count_primes_below, lst, limit)

    @staticmethod
    def count_primes_above(lst, limit):
        """Conta os primos acima de um limite."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import count_primes_above
        return GenericFeatureWrapper.apply_function(count_primes_above, lst, limit)

    @staticmethod
    def sum_primes(lst):
        """Calcula a soma dos números primos em uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import sum_primes
        return GenericFeatureWrapper.apply_function(sum_primes, lst)

    @staticmethod
    def mean_primes(lst):
        """Calcula a média dos números primos em uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import mean_primes
        return GenericFeatureWrapper.apply_function(mean_primes, lst)

    @staticmethod
    def median_primes(lst):
        """Calcula a mediana dos números primos em uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import median_primes
        return GenericFeatureWrapper.apply_function(median_primes, lst)

    @staticmethod
    def max_prime(lst):
        """Retorna o maior número primo em uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import max_prime
        return GenericFeatureWrapper.apply_function(max_prime, lst)

    @staticmethod
    def min_prime(lst):
        """Retorna o menor número primo em uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import min_prime
        return GenericFeatureWrapper.apply_function(min_prime, lst)

    @staticmethod
    def range_primes(lst):
        """Calcula a diferença entre o maior e o menor primo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import range_primes
        return GenericFeatureWrapper.apply_function(range_primes, lst)

    @staticmethod
    def prime_near_mean(lst):
        """Retorna o número primo mais próximo da média da lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import prime_near_mean
        return GenericFeatureWrapper.apply_function(prime_near_mean, lst)

    @staticmethod
    def next_primes(lst):
        """Retorna o próximo número primo de cada elemento."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import next_primes
        return GenericFeatureWrapper.apply_function(next_primes, lst)

    @staticmethod
    def prime_gaps(lst):
        """Calcula os gaps (diferenças) entre números primos consecutivos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import prime_gaps
        return GenericFeatureWrapper.apply_function(prime_gaps, lst)

    @staticmethod
    def sum_prime_gaps(lst):
        """Calcula a soma dos gaps entre números primos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import sum_prime_gaps
        return GenericFeatureWrapper.apply_function(sum_prime_gaps, lst)

    @staticmethod
    def odd_primes(lst):
        """Retorna os números primos ímpares de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import odd_primes
        return GenericFeatureWrapper.apply_function(odd_primes, lst)

    @staticmethod
    def square_primes(lst):
        """Retorna o quadrado de cada número primo em uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import square_primes
        return GenericFeatureWrapper.apply_function(square_primes, lst)

    @staticmethod
    def prime_binary(lst):
        """Cria uma representação binária (1=primo, 0=não primo)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_primos import prime_binary
        return GenericFeatureWrapper.apply_function(prime_binary, lst)

    @staticmethod
    def wavelet_dwt(data, wavelet):
        """Aplica a Transformada Discreta de Wavelet (DWT) de nível 1."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.wavelets import wavelet_dwt
        return GenericFeatureWrapper.apply_function(wavelet_dwt, data, wavelet)

    @staticmethod
    def wavelet_idwt(cA, cD, wavelet):
        """Aplica a Transformada Discreta de Wavelet Inversa (IDWT) de nível 1."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.wavelets import wavelet_idwt
        return GenericFeatureWrapper.apply_function(wavelet_idwt, cA, cD, wavelet)

    @staticmethod
    def wavelet_wavedec(data, level, wavelet):
        """Aplica a decomposição de wavelet multinível."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.wavelets import wavelet_wavedec
        return GenericFeatureWrapper.apply_function(wavelet_wavedec, data, level, wavelet)

    @staticmethod
    def wavelet_waverec(coeffs, wavelet):
        """Reconstrói um sinal a partir dos coeficientes de wavelet."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.wavelets import wavelet_waverec
        return GenericFeatureWrapper.apply_function(wavelet_waverec, coeffs, wavelet)

    @staticmethod
    def wavelet_energy(data, wavelet):
        """Calcula a energia total de um sinal em diferentes níveis de wavelet."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.wavelets import wavelet_energy
        return GenericFeatureWrapper.apply_function(wavelet_energy, data, wavelet)

    @staticmethod
    def euler_totient(n):
        """Calcula a função totiente de Euler."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import euler_totient
        return GenericFeatureWrapper.apply_function(euler_totient, n)

    @staticmethod
    def factor_integer(n):
        """Fatora um número em seus fatores primos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import factor_integer
        return GenericFeatureWrapper.apply_function(factor_integer, n)

    @staticmethod
    def prime_factors(n):
        """Retorna os fatores primos únicos de um número."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import prime_factors
        return GenericFeatureWrapper.apply_function(prime_factors, n)

    @staticmethod
    def prime_factor_count(n):
        """Retorna o número de fatores primos únicos de um número."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import prime_factor_count
        return GenericFeatureWrapper.apply_function(prime_factor_count, n)

    @staticmethod
    def largest_prime_factor(n):
        """Retorna o maior fator primo de um número."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import largest_prime_factor
        return GenericFeatureWrapper.apply_function(largest_prime_factor, n)

    @staticmethod
    def smallest_prime_factor(n):
        """Retorna o menor fator primo de um número."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import smallest_prime_factor
        return GenericFeatureWrapper.apply_function(smallest_prime_factor, n)

    @staticmethod
    def gcd_list(lst):
        """Calcula o Máximo Divisor Comum (MDC) de uma lista de números."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import gcd_list
        return GenericFeatureWrapper.apply_function(gcd_list, lst)

    @staticmethod
    def lcm_list(lst):
        """Calcula o Mínimo Múltiplo Comum (MMC) de uma lista de números."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import lcm_list
        return GenericFeatureWrapper.apply_function(lcm_list, lst)

    @staticmethod
    def check_prime(n):
        """Verifica se um número é primo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import check_prime
        return GenericFeatureWrapper.apply_function(check_prime, n)

    @staticmethod
    def count_primes_upto(n):
        """Conta o número de primos até n."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import count_primes_upto
        return GenericFeatureWrapper.apply_function(count_primes_upto, n)

    @staticmethod
    def next_prime_num(n):
        """Encontra o próximo número primo após n."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import next_prime_num
        return GenericFeatureWrapper.apply_function(next_prime_num, n)

    @staticmethod
    def prev_prime_num(n):
        """Encontra o número primo anterior a n."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import prev_prime_num
        return GenericFeatureWrapper.apply_function(prev_prime_num, n)

    @staticmethod
    def generate_primes(n):
        """Gera uma lista de primos até n."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import generate_primes
        return GenericFeatureWrapper.apply_function(generate_primes, n)

    @staticmethod
    def fibonacci_num(n):
        """Retorna o n-ésimo número de Fibonacci."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import fibonacci_num
        return GenericFeatureWrapper.apply_function(fibonacci_num, n)

    @staticmethod
    def lucas_num(n):
        """Retorna o n-ésimo número de Lucas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import lucas_num
        return GenericFeatureWrapper.apply_function(lucas_num, n)

    @staticmethod
    def catalan_num(n):
        """Retorna o n-ésimo número de Catalan."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import catalan_num
        return GenericFeatureWrapper.apply_function(catalan_num, n)

    @staticmethod
    def bell_number(n):
        """Retorna o n-ésimo número de Bell."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import bell_number
        return GenericFeatureWrapper.apply_function(bell_number, n)

    @staticmethod
    def partition_number(n):
        """Retorna o número de partições de n."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import partition_number
        return GenericFeatureWrapper.apply_function(partition_number, n)

    @staticmethod
    def bernoulli_number(n):
        """Retorna o n-ésimo número de Bernoulli."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_numeros import bernoulli_number
        return GenericFeatureWrapper.apply_function(bernoulli_number, n)

    @staticmethod
    def generate_key():
        """Gera uma chave de criptografia Fernet e armazena globalmente.
        
        Returns:
            str: Chave gerada como string."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.criptografia import generate_key
        return GenericFeatureWrapper.apply_function(generate_key, )

    @staticmethod
    def encrypt_data(data):
        """Criptografa dados usando a chave Fernet armazenada.
        
        Args:
            data (str | bytes): Dados a criptografar.
        
        Returns:
            bytes: Dados criptografados.
        
        Raises:
            RuntimeError: Se a chave não foi gerada."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.criptografia import encrypt_data
        return GenericFeatureWrapper.apply_function(encrypt_data, data)

    @staticmethod
    def decrypt_data(token):
        """Descriptografa dados usando a chave Fernet armazenada.
        
        Args:
            token (bytes): Dados criptografados.
        
        Returns:
            str: Dados descriptografados.
        
        Raises:
            RuntimeError: Se a chave não foi gerada."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.criptografia import decrypt_data
        return GenericFeatureWrapper.apply_function(decrypt_data, token)

    @staticmethod
    def lag_series(lst, lag):
        """Calcula a diferença entre elementos com um certo atraso (lag)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.temporais import lag_series
        return GenericFeatureWrapper.apply_function(lag_series, lst, lag)

    @staticmethod
    def fft_magnitude(lst):
        """Calcula a magnitude da Transformada Rápida de Fourier (FFT)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.temporais import fft_magnitude
        return GenericFeatureWrapper.apply_function(fft_magnitude, lst)

    @staticmethod
    def fft_phase(lst):
        """Calcula a fase da Transformada Rápida de Fourier (FFT)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.temporais import fft_phase
        return GenericFeatureWrapper.apply_function(fft_phase, lst)

    @staticmethod
    def ifft_real(lst):
        """Calcula a Transformada Inversa de Fourier (IFFT) e retorna a parte real."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.temporais import ifft_real
        return GenericFeatureWrapper.apply_function(ifft_real, lst)

    @staticmethod
    def dominant_frequency(lst):
        """Encontra o índice da frequência dominante em uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.temporais import dominant_frequency
        return GenericFeatureWrapper.apply_function(dominant_frequency, lst)

    @staticmethod
    def autocorr(lst, lag):
        """Calcula a autocorrelação de uma lista em um determinado atraso."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.temporais import autocorr
        return GenericFeatureWrapper.apply_function(autocorr, lst, lag)

    @staticmethod
    def autocorr_series(lst, max_lag):
        """Calcula a série de autocorrelação para múltiplos atrasos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.temporais import autocorr_series
        return GenericFeatureWrapper.apply_function(autocorr_series, lst, max_lag)

    @staticmethod
    def euclidean_dist(a, b):
        """Calcula a distância euclidiana entre dois pontos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.geometria import euclidean_dist
        return GenericFeatureWrapper.apply_function(euclidean_dist, a, b)

    @staticmethod
    def manhattan_dist(a, b):
        """Calcula a distância de Manhattan entre dois pontos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.geometria import manhattan_dist
        return GenericFeatureWrapper.apply_function(manhattan_dist, a, b)

    @staticmethod
    def chebyshev_dist(a, b):
        """Calcula a distância de Chebyshev entre dois pontos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.geometria import chebyshev_dist
        return GenericFeatureWrapper.apply_function(chebyshev_dist, a, b)

    @staticmethod
    def cosine_dist(a, b):
        """Calcula a distância do cosseno entre dois vetores."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.geometria import cosine_dist
        return GenericFeatureWrapper.apply_function(cosine_dist, a, b)

    @staticmethod
    def hamming_dist_str(a, b):
        """Calcula a distância de Hamming entre duas strings."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.geometria import hamming_dist_str
        return GenericFeatureWrapper.apply_function(hamming_dist_str, a, b)

    @staticmethod
    def levenshtein_dist(a, b):
        """Calcula a distância de Levenshtein entre duas strings."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.geometria import levenshtein_dist
        return GenericFeatureWrapper.apply_function(levenshtein_dist, a, b)

    @staticmethod
    def jaccard_index(a, b):
        """Calcula o índice de Jaccard entre dois conjuntos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.geometria import jaccard_index
        return GenericFeatureWrapper.apply_function(jaccard_index, a, b)

    @staticmethod
    def centroid(points):
        """Calcula o centroide de um conjunto de pontos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.geometria import centroid
        return GenericFeatureWrapper.apply_function(centroid, points)

    @staticmethod
    def sample_binomial(n, p, size):
        """Gera uma amostra de uma distribuição Binomial."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.simulacao import sample_binomial
        return GenericFeatureWrapper.apply_function(sample_binomial, n, p, size)

    @staticmethod
    def sample_poisson(lam, size):
        """Gera uma amostra de uma distribuição de Poisson."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.simulacao import sample_poisson
        return GenericFeatureWrapper.apply_function(sample_poisson, lam, size)

    @staticmethod
    def sample_normal(mu, sigma, size):
        """Gera uma amostra de uma distribuição Normal."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.simulacao import sample_normal
        return GenericFeatureWrapper.apply_function(sample_normal, mu, sigma, size)

    @staticmethod
    def monte_carlo_sum(target_sum, trials):
        """Calcula a probabilidade de atingir uma soma alvo em amostras aleatórias."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.simulacao import monte_carlo_sum
        return GenericFeatureWrapper.apply_function(monte_carlo_sum, target_sum, trials)

    @staticmethod
    def monte_carlo_even_ratio(trials):
        """Simula a proporção média de números pares em amostras aleatórias."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.simulacao import monte_carlo_even_ratio
        return GenericFeatureWrapper.apply_function(monte_carlo_even_ratio, trials)

    @staticmethod
    def monte_carlo_prime_ratio(trials):
        """Simula a proporção média de números primos em amostras aleatórias."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.simulacao import monte_carlo_prime_ratio
        return GenericFeatureWrapper.apply_function(monte_carlo_prime_ratio, trials)

    @staticmethod
    def monte_carlo_max(trials):
        """Simula os valores máximos de amostras aleatórias."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.simulacao import monte_carlo_max
        return GenericFeatureWrapper.apply_function(monte_carlo_max, trials)

    @staticmethod
    def monte_carlo_min(trials):
        """Simula os valores mínimos de amostras aleatórias."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.simulacao import monte_carlo_min
        return GenericFeatureWrapper.apply_function(monte_carlo_min, trials)

    @staticmethod
    def monte_carlo_multistep(lst, steps, trials):
        """Simulação Monte Carlo multi-passos, selecionando elementos aleatórios."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.simulacao import monte_carlo_multistep
        return GenericFeatureWrapper.apply_function(monte_carlo_multistep, lst, steps, trials)

    @staticmethod
    def metropolis_hastings(target_func, start, iterations, proposal_std):
        """Geração de amostras MCMC usando o algoritmo Metropolis-Hastings."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.simulacao import metropolis_hastings
        return GenericFeatureWrapper.apply_function(metropolis_hastings, target_func, start, iterations, proposal_std)

    @staticmethod
    def plot_histogram(data, title, bins, color):
        """Plota um histograma de uma lista de dados."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.plots import plot_histogram
        return GenericFeatureWrapper.apply_function(plot_histogram, data, title, bins, color)

    @staticmethod
    def plot_scatter(x, y, title, color):
        """Plota um gráfico de dispersão de dois conjuntos de dados."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.plots import plot_scatter
        return GenericFeatureWrapper.apply_function(plot_scatter, x, y, title, color)

    @staticmethod
    def plot_boxplot(data, title):
        """Plota um boxplot para visualizar a distribuição e outliers."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.plots import plot_boxplot
        return GenericFeatureWrapper.apply_function(plot_boxplot, data, title)

    @staticmethod
    def plot_time_series(series, title, color):
        """Plota uma série temporal."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.plots import plot_time_series
        return GenericFeatureWrapper.apply_function(plot_time_series, series, title, color)

    @staticmethod
    def rolling_mean_plot(lst, window):
        """Plota a média móvel de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.plots import rolling_mean_plot
        return GenericFeatureWrapper.apply_function(rolling_mean_plot, lst, window)

    @staticmethod
    def cumulative_sum_plot(lst):
        """Plota a soma cumulativa de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.plots import cumulative_sum_plot
        return GenericFeatureWrapper.apply_function(cumulative_sum_plot, lst)

    @staticmethod
    def heatmap_pairs(lst):
        """Cria um mapa de calor para a frequência de pares."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.plots import heatmap_pairs
        return GenericFeatureWrapper.apply_function(heatmap_pairs, lst)

    @staticmethod
    def linear_regression_predict(lst, steps):
        """Prediz o próximo valor de uma lista usando regressão linear."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.modelagem_preditiva import linear_regression_predict
        return GenericFeatureWrapper.apply_function(linear_regression_predict, lst, steps)

    @staticmethod
    def poly_regression_predict(lst, degree, steps):
        """Prediz o próximo valor de uma lista usando regressão polinomial."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.modelagem_preditiva import poly_regression_predict
        return GenericFeatureWrapper.apply_function(poly_regression_predict, lst, degree, steps)

    @staticmethod
    def regression_on_frequency(lst, steps):
        """Aplica regressão linear na frequência cumulativa de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.modelagem_preditiva import regression_on_frequency
        return GenericFeatureWrapper.apply_function(regression_on_frequency, lst, steps)

    @staticmethod
    def linear_regression_coeffs(x, y):
        """Calcula os coeficientes de regressão linear (inclinação e interceptação)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.modelagem_preditiva import linear_regression_coeffs
        return GenericFeatureWrapper.apply_function(linear_regression_coeffs, x, y)

    @staticmethod
    def predict_linear(x, m, c):
        """Prediz valores usando uma equação de regressão linear."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.modelagem_preditiva import predict_linear
        return GenericFeatureWrapper.apply_function(predict_linear, x, m, c)

    @staticmethod
    def regression_score(x, y):
        """Calcula a pontuação de ajuste de regressão linear (negativo do MSE)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.modelagem_preditiva import regression_score
        return GenericFeatureWrapper.apply_function(regression_score, x, y)

    @staticmethod
    def shannon_entropy(lst):
        """Calcula a entropia de Shannon de uma distribuição de probabilidade."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_informacao import shannon_entropy
        return GenericFeatureWrapper.apply_function(shannon_entropy, lst)

    @staticmethod
    def normalized_entropy(lst):
        """Calcula a entropia de Shannon normalizada."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_informacao import normalized_entropy
        return GenericFeatureWrapper.apply_function(normalized_entropy, lst)

    @staticmethod
    def mutual_info(x, y):
        """Calcula a informação mútua entre duas listas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_informacao import mutual_info
        return GenericFeatureWrapper.apply_function(mutual_info, x, y)

    @staticmethod
    def normalized_mutual_info(x, y):
        """Calcula a informação mútua normalizada."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_informacao import normalized_mutual_info
        return GenericFeatureWrapper.apply_function(normalized_mutual_info, x, y)

    @staticmethod
    def kl_divergence(p, q):
        """Calcula a divergência de Kullback-Leibler entre duas distribuições."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_informacao import kl_divergence
        return GenericFeatureWrapper.apply_function(kl_divergence, p, q)

    @staticmethod
    def jensen_shannon(p, q):
        """Calcula a divergência de Jensen-Shannon entre duas distribuições."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_informacao import jensen_shannon
        return GenericFeatureWrapper.apply_function(jensen_shannon, p, q)

    @staticmethod
    def gini_impurity(lst):
        """Calcula a impureza de Gini de uma distribuição."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.teoria_informacao import gini_impurity
        return GenericFeatureWrapper.apply_function(gini_impurity, lst)

    @staticmethod
    def fft_real(lst):
        """Calcula a magnitude da FFT de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import fft_real
        return GenericFeatureWrapper.apply_function(fft_real, lst)

    @staticmethod
    def fft_phase(lst):
        """Calcula a fase da FFT de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import fft_phase
        return GenericFeatureWrapper.apply_function(fft_phase, lst)

    @staticmethod
    def fft_log(lst):
        """Calcula a FFT da lista transformada em log."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import fft_log
        return GenericFeatureWrapper.apply_function(fft_log, lst)

    @staticmethod
    def fft_sqrt(lst):
        """Calcula a FFT da raiz quadrada da lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import fft_sqrt
        return GenericFeatureWrapper.apply_function(fft_sqrt, lst)

    @staticmethod
    def fft_normalized(lst):
        """Calcula a FFT normalizada da lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import fft_normalized
        return GenericFeatureWrapper.apply_function(fft_normalized, lst)

    @staticmethod
    def ifft_real(lst):
        """Calcula a parte real da IFFT."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import ifft_real
        return GenericFeatureWrapper.apply_function(ifft_real, lst)

    @staticmethod
    def fft_frequencies(n, sample_rate):
        """Retorna as frequências correspondentes à FFT."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import fft_frequencies
        return GenericFeatureWrapper.apply_function(fft_frequencies, n, sample_rate)

    @staticmethod
    def apply_lowpass(lst, cutoff, order):
        """Aplica um filtro passa-baixa Butterworth."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import apply_lowpass
        return GenericFeatureWrapper.apply_function(apply_lowpass, lst, cutoff, order)

    @staticmethod
    def apply_highpass(lst, cutoff, order):
        """Aplica um filtro passa-alta Butterworth."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import apply_highpass
        return GenericFeatureWrapper.apply_function(apply_highpass, lst, cutoff, order)

    @staticmethod
    def apply_bandpass(lst, low, high, order):
        """Aplica um filtro passa-faixa Butterworth."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import apply_bandpass
        return GenericFeatureWrapper.apply_function(apply_bandpass, lst, low, high, order)

    @staticmethod
    def wavelet_decompose(lst, wavelet, level):
        """Decompõe uma lista em coeficientes de Wavelet (DWT)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import wavelet_decompose
        return GenericFeatureWrapper.apply_function(wavelet_decompose, lst, wavelet, level)

    @staticmethod
    def wavelet_reconstruct(coeffs, wavelet):
        """Reconstrói uma lista a partir de coeficientes de Wavelet."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import wavelet_reconstruct
        return GenericFeatureWrapper.apply_function(wavelet_reconstruct, coeffs, wavelet)

    @staticmethod
    def dwt_approx(lst, wavelet):
        """Retorna apenas os coeficientes de aproximação da DWT."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import dwt_approx
        return GenericFeatureWrapper.apply_function(dwt_approx, lst, wavelet)

    @staticmethod
    def dwt_detail(lst, wavelet):
        """Retorna os coeficientes de detalhe da DWT."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import dwt_detail
        return GenericFeatureWrapper.apply_function(dwt_detail, lst, wavelet)

    @staticmethod
    def hilbert_transform(lst):
        """Calcula a Transformada de Hilbert (magnitude)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import hilbert_transform
        return GenericFeatureWrapper.apply_function(hilbert_transform, lst)

    @staticmethod
    def savgol_smooth(lst, window, poly):
        """Aplica filtro de Savitzky-Golay para suavização."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import savgol_smooth
        return GenericFeatureWrapper.apply_function(savgol_smooth, lst, window, poly)

    @staticmethod
    def stft_transform(lst, fs):
        """Aplica a Transformada de Fourier de Curto Prazo (STFT)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import stft_transform
        return GenericFeatureWrapper.apply_function(stft_transform, lst, fs)

    @staticmethod
    def istft_transform(Z, fs):
        """Reconstrói sinal a partir da STFT (ISTFT)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import istft_transform
        return GenericFeatureWrapper.apply_function(istft_transform, Z, fs)

    @staticmethod
    def welch_psd(lst, fs):
        """Calcula o Power Spectral Density pelo método de Welch."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import welch_psd
        return GenericFeatureWrapper.apply_function(welch_psd, lst, fs)

    @staticmethod
    def periodogram_psd(lst, fs):
        """Calcula o Power Spectral Density pelo periodograma."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import periodogram_psd
        return GenericFeatureWrapper.apply_function(periodogram_psd, lst, fs)

    @staticmethod
    def spectral_energy(lst):
        """Calcula a energia total do espectro."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import spectral_energy
        return GenericFeatureWrapper.apply_function(spectral_energy, lst)

    @staticmethod
    def spectral_entropy(lst):
        """Calcula a entropia espectral do sinal."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import spectral_entropy
        return GenericFeatureWrapper.apply_function(spectral_entropy, lst)

    @staticmethod
    def find_signal_peaks(lst):
        """Encontra os índices dos picos no sinal."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import find_signal_peaks
        return GenericFeatureWrapper.apply_function(find_signal_peaks, lst)

    @staticmethod
    def detect_cycle_length(lst):
        """Detecta o comprimento do ciclo repetitivo mais curto."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import detect_cycle_length
        return GenericFeatureWrapper.apply_function(detect_cycle_length, lst)

    @staticmethod
    def butter_lowpass(cutoff, fs, order):
        """Retorna coeficientes de filtro Butterworth passa-baixa."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import butter_lowpass
        return GenericFeatureWrapper.apply_function(butter_lowpass, cutoff, fs, order)

    @staticmethod
    def filter_signal(b, a, x):
        """Filtra um sinal usando os coeficientes b e a."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.processamento_sinal import filter_signal
        return GenericFeatureWrapper.apply_function(filter_signal, b, a, x)

    @staticmethod
    def covariance_matrix(X):
        """Calcula a matriz de covariância de um conjunto de dados.
        
        Args:
            X (List[List[float]]): Matriz de dados, linhas = amostras, colunas = variáveis.
        
        Returns:
            List[List[float]]: Matriz de covariância."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_multivariada import covariance_matrix
        return GenericFeatureWrapper.apply_function(covariance_matrix, X)

    @staticmethod
    def correlation_matrix(X):
        """Calcula a matriz de correlação de um conjunto de dados.
        
        Args:
            X (List[List[float]]): Matriz de dados, linhas = amostras, colunas = variáveis.
        
        Returns:
            List[List[float]]: Matriz de correlação."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_multivariada import correlation_matrix
        return GenericFeatureWrapper.apply_function(correlation_matrix, X)

    @staticmethod
    def mutual_info(x, y):
        """Calcula a informação mútua entre duas variáveis discretas.
        
        Args:
            x (List[int]): Primeira variável discreta.
            y (List[int]): Segunda variável discreta.
        
        Returns:
            float: Informação mútua."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_multivariada import mutual_info
        return GenericFeatureWrapper.apply_function(mutual_info, x, y)

    @staticmethod
    def normalized_mutual_info(x, y):
        """Calcula a informação mútua normalizada entre duas variáveis discretas.
        
        Args:
            x (List[int]): Primeira variável discreta.
            y (List[int]): Segunda variável discreta.
        
        Returns:
            float: Informação mútua normalizada."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_multivariada import normalized_mutual_info
        return GenericFeatureWrapper.apply_function(normalized_mutual_info, x, y)

    @staticmethod
    def silhouette(X, labels):
        """Calcula o coeficiente de silhueta para avaliar a qualidade de um agrupamento.
        
        Args:
            X (List[List[float]]): Matriz de dados.
            labels (List[int]): Rótulos de cluster para cada ponto.
        
        Returns:
            float: Coeficiente de silhueta."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_multivariada import silhouette
        return GenericFeatureWrapper.apply_function(silhouette, X, labels)

    @staticmethod
    def pca_eigenvalues(X):
        """Calcula os autovalores da matriz de covariância para a Análise de Componentes Principais (PCA).
        
        Args:
            X (List[List[float]]): Matriz de dados.
        
        Returns:
            List[float]: Autovalores da matriz de covariância."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_multivariada import pca_eigenvalues
        return GenericFeatureWrapper.apply_function(pca_eigenvalues, X)

    @staticmethod
    def gini_index(values):
        """Calcula o índice de Gini para medir a desigualdade.
        
        Args:
            values (List[float]): Lista de valores.
        
        Returns:
            float: Índice de Gini (0 = igualdade perfeita, 1 = desigualdade máxima)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.estatistica_multivariada import gini_index
        return GenericFeatureWrapper.apply_function(gini_index, values)

    @staticmethod
    def gamma_transform(lst):
        """Aplica a função Gamma a cada elemento positivo da lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import gamma_transform
        return GenericFeatureWrapper.apply_function(gamma_transform, lst)

    @staticmethod
    def bessel_j_list(lst, n):
        """Calcula a função de Bessel de primeira espécie para uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import bessel_j_list
        return GenericFeatureWrapper.apply_function(bessel_j_list, lst, n)

    @staticmethod
    def euler_totient(lst):
        """Calcula a função totiente de Euler para cada elemento positivo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import euler_totient
        return GenericFeatureWrapper.apply_function(euler_totient, lst)

    @staticmethod
    def sum_divisors(lst):
        """Calcula a soma dos divisores de cada elemento."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import sum_divisors
        return GenericFeatureWrapper.apply_function(sum_divisors, lst)

    @staticmethod
    def gamma_func(x):
        """Calcula a função Gamma."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import gamma_func
        return GenericFeatureWrapper.apply_function(gamma_func, x)

    @staticmethod
    def loggamma_func(x):
        """Calcula o logaritmo da função Gamma."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import loggamma_func
        return GenericFeatureWrapper.apply_function(loggamma_func, x)

    @staticmethod
    def digamma_func(x):
        """Calcula a função Digamma."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import digamma_func
        return GenericFeatureWrapper.apply_function(digamma_func, x)

    @staticmethod
    def beta_func(x, y):
        """Calcula a função Beta."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import beta_func
        return GenericFeatureWrapper.apply_function(beta_func, x, y)

    @staticmethod
    def bessel_j(n, x):
        """Calcula a função de Bessel de primeira espécie."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import bessel_j
        return GenericFeatureWrapper.apply_function(bessel_j, n, x)

    @staticmethod
    def bessel_y(n, x):
        """Calcula a função de Bessel de segunda espécie."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import bessel_y
        return GenericFeatureWrapper.apply_function(bessel_y, n, x)

    @staticmethod
    def bessel_j0(x):
        """Função de Bessel de primeira espécie de ordem 0."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import bessel_j0
        return GenericFeatureWrapper.apply_function(bessel_j0, x)

    @staticmethod
    def bessel_y0(x):
        """Função de Bessel de segunda espécie de ordem 0."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import bessel_y0
        return GenericFeatureWrapper.apply_function(bessel_y0, x)

    @staticmethod
    def error_func(x):
        """Função de erro (erf)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import error_func
        return GenericFeatureWrapper.apply_function(error_func, x)

    @staticmethod
    def error_func_c(x):
        """Função de erro complementar (erfc)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import error_func_c
        return GenericFeatureWrapper.apply_function(error_func_c, x)

    @staticmethod
    def elliptic_j(u, m):
        """Funções elípticas de Jacobi (sn, cn, dn)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import elliptic_j
        return GenericFeatureWrapper.apply_function(elliptic_j, u, m)

    @staticmethod
    def legendre_p(n, x):
        """Polinômio de Legendre de ordem n."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import legendre_p
        return GenericFeatureWrapper.apply_function(legendre_p, n, x)

    @staticmethod
    def chebyshev_t(n, x):
        """Polinômio de Chebyshev de primeira espécie de ordem n."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import chebyshev_t
        return GenericFeatureWrapper.apply_function(chebyshev_t, n, x)

    @staticmethod
    def airy_ai(x):
        """Função Airy Ai."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import airy_ai
        return GenericFeatureWrapper.apply_function(airy_ai, x)

    @staticmethod
    def airy_bi(x):
        """Função Airy Bi."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.matematica_especial import airy_bi
        return GenericFeatureWrapper.apply_function(airy_bi, x)

    @staticmethod
    def linear_trend_slope(lst):
        """Calcula a inclinação da tendência linear de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.exploracao import linear_trend_slope
        return GenericFeatureWrapper.apply_function(linear_trend_slope, lst)

    @staticmethod
    def successive_diff(lst):
        """Calcula a diferença entre elementos sucessivos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.exploracao import successive_diff
        return GenericFeatureWrapper.apply_function(successive_diff, lst)

    @staticmethod
    def mutate_list(lst, mutation_rate, max_val):
        """Aplica mutação a uma lista, trocando elementos aleatoriamente."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import mutate_list
        return GenericFeatureWrapper.apply_function(mutate_list, lst, mutation_rate, max_val)

    @staticmethod
    def crossover_lists(lst1, lst2):
        """Combina duas listas em um ponto de cruzamento."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import crossover_lists
        return GenericFeatureWrapper.apply_function(crossover_lists, lst1, lst2)

    @staticmethod
    def fitness_sum(lst, target):
        """Calcula o 'fitness' de uma lista com base em sua soma."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import fitness_sum
        return GenericFeatureWrapper.apply_function(fitness_sum, lst, target)

    @staticmethod
    def fitness_even_ratio(lst, target_ratio):
        """Calcula o 'fitness' com base na proporção de números pares."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import fitness_even_ratio
        return GenericFeatureWrapper.apply_function(fitness_even_ratio, lst, target_ratio)

    @staticmethod
    def select_best_population(population, fitness_func, k):
        """Seleciona a melhor parte de uma população com base em uma função de fitness."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import select_best_population
        return GenericFeatureWrapper.apply_function(select_best_population, population, fitness_func, k)

    @staticmethod
    def combined_score(lst, heuristics):
        """Combina o score de múltiplas heurísticas para uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import combined_score
        return GenericFeatureWrapper.apply_function(combined_score, lst, heuristics)

    @staticmethod
    def weighted_score(lst, heuristics, weights):
        """Calcula o score combinado de heurísticas com pesos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import weighted_score
        return GenericFeatureWrapper.apply_function(weighted_score, lst, heuristics, weights)

    @staticmethod
    def rank_heuristics(lst, heuristics):
        """Classifica heurísticas com base em seu desempenho em uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import rank_heuristics
        return GenericFeatureWrapper.apply_function(rank_heuristics, lst, heuristics)

    @staticmethod
    def generate_heuristic_from_library(lst, funcs):
        """Executa uma heurística aleatória da biblioteca."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import generate_heuristic_from_library
        return GenericFeatureWrapper.apply_function(generate_heuristic_from_library, lst, funcs)

    @staticmethod
    def integrated_heuristic_test(lst, heuristics):
        """Testa e retorna heurísticas ordenadas por score."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import integrated_heuristic_test
        return GenericFeatureWrapper.apply_function(integrated_heuristic_test, lst, heuristics)

    @staticmethod
    def top_k_integrated(lst, heuristics, k):
        """Retorna as top K heurísticas integradas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import top_k_integrated
        return GenericFeatureWrapper.apply_function(top_k_integrated, lst, heuristics, k)

    @staticmethod
    def generate_new_combined_heuristic(heuristics, transforms):
        """Gera uma nova heurística combinando uma função com uma transformação."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import generate_new_combined_heuristic
        return GenericFeatureWrapper.apply_function(generate_new_combined_heuristic, heuristics, transforms)

    @staticmethod
    def stochastic_score(lst, heuristics, trials):
        """Calcula o score estocástico de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import stochastic_score
        return GenericFeatureWrapper.apply_function(stochastic_score, lst, heuristics, trials)

    @staticmethod
    def combined_stochastic_score(lst, heuristics, weights, trials):
        """Calcula o score estocástico combinado com pesos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import combined_stochastic_score
        return GenericFeatureWrapper.apply_function(combined_stochastic_score, lst, heuristics, weights, trials)

    @staticmethod
    def random_selection(lst, k):
        """Seleciona k elementos aleatórios de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import random_selection
        return GenericFeatureWrapper.apply_function(random_selection, lst, k)

    @staticmethod
    def weighted_choice(lst, weights):
        """Faz uma escolha aleatória de um elemento com base em pesos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import weighted_choice
        return GenericFeatureWrapper.apply_function(weighted_choice, lst, weights)

    @staticmethod
    def shuffle_sum(lst):
        """Embaralha a lista e retorna a soma de seus elementos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import shuffle_sum
        return GenericFeatureWrapper.apply_function(shuffle_sum, lst)

    @staticmethod
    def shuffle_product(lst):
        """Embaralha a lista e retorna o produto de seus elementos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import shuffle_product
        return GenericFeatureWrapper.apply_function(shuffle_product, lst)

    @staticmethod
    def random_mean(lst, k, trials):
        """Calcula a média de múltiplas seleções aleatórias de k elementos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import random_mean
        return GenericFeatureWrapper.apply_function(random_mean, lst, k, trials)

    @staticmethod
    def random_cumsum(lst, k, trials):
        """Calcula a soma de k elementos selecionados aleatoriamente, repetindo por N testes."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.ia_heuristica import random_cumsum
        return GenericFeatureWrapper.apply_function(random_cumsum, lst, k, trials)

    @staticmethod
    def mse(y_true, y_pred):
        """Calcula o Erro Quadrático Médio (MSE)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.machine_learning import mse
        return GenericFeatureWrapper.apply_function(mse, y_true, y_pred)

    @staticmethod
    def rmse(y_true, y_pred):
        """Calcula a Raiz do Erro Quadrático Médio (RMSE)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.machine_learning import rmse
        return GenericFeatureWrapper.apply_function(rmse, y_true, y_pred)

    @staticmethod
    def mae(y_true, y_pred):
        """Calcula o Erro Absoluto Médio (MAE)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.machine_learning import mae
        return GenericFeatureWrapper.apply_function(mae, y_true, y_pred)

    @staticmethod
    def r2(y_true, y_pred):
        """Calcula o coeficiente de determinação R²."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.machine_learning import r2
        return GenericFeatureWrapper.apply_function(r2, y_true, y_pred)

    @staticmethod
    def accuracy(y_true, y_pred):
        """Calcula a acurácia para tarefas de classificação."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.machine_learning import accuracy
        return GenericFeatureWrapper.apply_function(accuracy, y_true, y_pred)

    @staticmethod
    def f1(y_true, y_pred):
        """Calcula a pontuação F1 (macro-média)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.machine_learning import f1
        return GenericFeatureWrapper.apply_function(f1, y_true, y_pred)

    @staticmethod
    def precision(y_true, y_pred):
        """Calcula a precisão (macro-média)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.machine_learning import precision
        return GenericFeatureWrapper.apply_function(precision, y_true, y_pred)

    @staticmethod
    def recall(y_true, y_pred):
        """Calcula o recall (macro-média)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.machine_learning import recall
        return GenericFeatureWrapper.apply_function(recall, y_true, y_pred)

    @staticmethod
    def matrix_determinant(mat):
        """Calcula o determinante de uma matriz."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import matrix_determinant
        return GenericFeatureWrapper.apply_function(matrix_determinant, mat)

    @staticmethod
    def matrix_rank(mat):
        """Calcula o posto de uma matriz."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import matrix_rank
        return GenericFeatureWrapper.apply_function(matrix_rank, mat)

    @staticmethod
    def matrix_inverse(mat):
        """Calcula a inversa de uma matriz."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import matrix_inverse
        return GenericFeatureWrapper.apply_function(matrix_inverse, mat)

    @staticmethod
    def matrix_trace(mat):
        """Calcula o traço de uma matriz."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import matrix_trace
        return GenericFeatureWrapper.apply_function(matrix_trace, mat)

    @staticmethod
    def matrix_condition_number(mat):
        """Calcula o número de condição de uma matriz."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import matrix_condition_number
        return GenericFeatureWrapper.apply_function(matrix_condition_number, mat)

    @staticmethod
    def matrix_norm_fro(mat):
        """Calcula a norma de Frobenius de uma matriz."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import matrix_norm_fro
        return GenericFeatureWrapper.apply_function(matrix_norm_fro, mat)

    @staticmethod
    def matrix_norm_inf(mat):
        """Calcula a norma do infinito de uma matriz."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import matrix_norm_inf
        return GenericFeatureWrapper.apply_function(matrix_norm_inf, mat)

    @staticmethod
    def matrix_eigenvalues(mat):
        """Calcula os autovalores de uma matriz."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import matrix_eigenvalues
        return GenericFeatureWrapper.apply_function(matrix_eigenvalues, mat)

    @staticmethod
    def matrix_eigenvectors(mat):
        """Calcula os autovetores de uma matriz."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import matrix_eigenvectors
        return GenericFeatureWrapper.apply_function(matrix_eigenvectors, mat)

    @staticmethod
    def solve_linear_system(A, b):
        """Resolve um sistema de equações lineares Ax=b."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import solve_linear_system
        return GenericFeatureWrapper.apply_function(solve_linear_system, A, b)

    @staticmethod
    def cholesky_decomposition(mat):
        """Realiza a decomposição de Cholesky."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import cholesky_decomposition
        return GenericFeatureWrapper.apply_function(cholesky_decomposition, mat)

    @staticmethod
    def qr_decomposition(mat):
        """Realiza a decomposição QR."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import qr_decomposition
        return GenericFeatureWrapper.apply_function(qr_decomposition, mat)

    @staticmethod
    def svd_u(mat):
        """Retorna a matriz U da SVD."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import svd_u
        return GenericFeatureWrapper.apply_function(svd_u, mat)

    @staticmethod
    def svd_s(mat):
        """Retorna os valores singulares da SVD."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import svd_s
        return GenericFeatureWrapper.apply_function(svd_s, mat)

    @staticmethod
    def matrix_pinv(mat):
        """Calcula a pseudoinversa de uma matriz."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algebra_linear import matrix_pinv
        return GenericFeatureWrapper.apply_function(matrix_pinv, mat)

    @staticmethod
    def laplace_transform(f, a):
        """Calcula a transformada de Laplace de uma função."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_numerica import laplace_transform
        return GenericFeatureWrapper.apply_function(laplace_transform, f, a)

    @staticmethod
    def z_transform(lst):
        """Calcula a transformada Z de uma sequência discreta."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_numerica import z_transform
        return GenericFeatureWrapper.apply_function(z_transform, lst)

    @staticmethod
    def airy_func(x):
        """Calcula a função Airy."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_numerica import airy_func
        return GenericFeatureWrapper.apply_function(airy_func, x)

    @staticmethod
    def product_primes(lst):
        """Calcula o produto dos números primos numa lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_numerica import product_primes
        return GenericFeatureWrapper.apply_function(product_primes, lst)

    @staticmethod
    def product_prime_gaps(lst):
        """Calcula o produto dos gaps entre primos numa lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.analise_numerica import product_prime_gaps
        return GenericFeatureWrapper.apply_function(product_prime_gaps, lst)

    @staticmethod
    def combinations_sum(lst, r):
        """Soma todas as combinações de r elementos da lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import combinations_sum
        return GenericFeatureWrapper.apply_function(combinations_sum, lst, r)

    @staticmethod
    def permutations_sum(lst, r):
        """Soma todas as permutações de r elementos da lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import permutations_sum
        return GenericFeatureWrapper.apply_function(permutations_sum, lst, r)

    @staticmethod
    def sum_combinations2(lst):
        """Soma de todas as combinações de 2 elementos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import sum_combinations2
        return GenericFeatureWrapper.apply_function(sum_combinations2, lst)

    @staticmethod
    def sum_combinations3(lst):
        """Soma de todas as combinações de 3 elementos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import sum_combinations3
        return GenericFeatureWrapper.apply_function(sum_combinations3, lst)

    @staticmethod
    def sum_permutations2(lst):
        """Soma de todas as permutações de 2 elementos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import sum_permutations2
        return GenericFeatureWrapper.apply_function(sum_permutations2, lst)

    @staticmethod
    def prod_combinations2(lst):
        """Produto das somas de todas as combinações de 2 elementos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import prod_combinations2
        return GenericFeatureWrapper.apply_function(prod_combinations2, lst)

    @staticmethod
    def prod_permutations2(lst):
        """Produto das somas de todas as permutações de 2 elementos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import prod_permutations2
        return GenericFeatureWrapper.apply_function(prod_permutations2, lst)

    @staticmethod
    def max_diff_combinations(lst, k):
        """Diferença entre a soma máxima e mínima das combinações."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import max_diff_combinations
        return GenericFeatureWrapper.apply_function(max_diff_combinations, lst, k)

    @staticmethod
    def mean_combinations2(lst):
        """Média das somas de todas as combinações de 2 elementos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import mean_combinations2
        return GenericFeatureWrapper.apply_function(mean_combinations2, lst)

    @staticmethod
    def reduce_sum(lst):
        """Soma de uma lista usando reduce."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import reduce_sum
        return GenericFeatureWrapper.apply_function(reduce_sum, lst)

    @staticmethod
    def reduce_prod(lst):
        """Produto de uma lista usando reduce."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import reduce_prod
        return GenericFeatureWrapper.apply_function(reduce_prod, lst)

    @staticmethod
    def reduce_max(lst):
        """Máximo de uma lista usando reduce."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import reduce_max
        return GenericFeatureWrapper.apply_function(reduce_max, lst)

    @staticmethod
    def prod_ratio(lst):
        """Produto das proporções entre elementos consecutivos."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import prod_ratio
        return GenericFeatureWrapper.apply_function(prod_ratio, lst)

    @staticmethod
    def conditional_permutations(lst, condition):
        """Permutações que satisfazem uma condição."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import conditional_permutations
        return GenericFeatureWrapper.apply_function(conditional_permutations, lst, condition)

    @staticmethod
    def combinations_with_sum(lst, target):
        """Combinações cuja soma é igual ao valor alvo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import combinations_with_sum
        return GenericFeatureWrapper.apply_function(combinations_with_sum, lst, target)

    @staticmethod
    def count_combinations_with_sum(lst, target):
        """Conta combinações cuja soma é igual ao valor alvo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import count_combinations_with_sum
        return GenericFeatureWrapper.apply_function(count_combinations_with_sum, lst, target)

    @staticmethod
    def product_sum(lst1, lst2):
        """Soma dos pares do produto cartesiano de duas listas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import product_sum
        return GenericFeatureWrapper.apply_function(product_sum, lst1, lst2)

    @staticmethod
    def product_prod(lst1, lst2):
        """Produto dos pares do produto cartesiano de duas listas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import product_prod
        return GenericFeatureWrapper.apply_function(product_prod, lst1, lst2)

    @staticmethod
    def product_sum_square(lst1, lst2):
        """Quadrado da soma de cada par do produto cartesiano."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import product_sum_square
        return GenericFeatureWrapper.apply_function(product_sum_square, lst1, lst2)

    @staticmethod
    def product_prod_square(lst1, lst2):
        """Quadrado do produto de cada par do produto cartesiano."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import product_prod_square
        return GenericFeatureWrapper.apply_function(product_prod_square, lst1, lst2)

    @staticmethod
    def combination_count(n, k):
        """Número exato de combinações."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import combination_count
        return GenericFeatureWrapper.apply_function(combination_count, n, k)

    @staticmethod
    def permutation_count(n, k):
        """Número exato de permutações."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import permutation_count
        return GenericFeatureWrapper.apply_function(permutation_count, n, k)

    @staticmethod
    def factorial_list(lst):
        """Fatorial de cada elemento de uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.combinatoria_avancada import factorial_list
        return GenericFeatureWrapper.apply_function(factorial_list, lst)

    @staticmethod
    def dijkstra_path(G, source, target, weight):
        """Encontra o caminho mais curto entre origem e destino (Dijkstra)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algoritmos_grafos import dijkstra_path
        return GenericFeatureWrapper.apply_function(dijkstra_path, G, source, target, weight)

    @staticmethod
    def dijkstra_length(G, source, target, weight):
        """Calcula o comprimento do caminho mais curto entre origem e destino (Dijkstra)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algoritmos_grafos import dijkstra_length
        return GenericFeatureWrapper.apply_function(dijkstra_length, G, source, target, weight)

    @staticmethod
    def shortest_path_all_pairs(G):
        """Encontra o comprimento do caminho mais curto entre todos os pares de nós."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algoritmos_grafos import shortest_path_all_pairs
        return GenericFeatureWrapper.apply_function(shortest_path_all_pairs, G)

    @staticmethod
    def is_connected(G):
        """Verifica se o grafo é conexo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algoritmos_grafos import is_connected
        return GenericFeatureWrapper.apply_function(is_connected, G)

    @staticmethod
    def has_cycle(G):
        """Verifica se o grafo contém pelo menos um ciclo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.algoritmos_grafos import has_cycle
        return GenericFeatureWrapper.apply_function(has_cycle, G)

    @staticmethod
    def unique_count(lst):
        """Conta o número de elementos únicos em uma lista."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.conjuntos import unique_count
        return GenericFeatureWrapper.apply_function(unique_count, lst)

    @staticmethod
    def intersection(lst1, lst2):
        """Retorna os elementos em comum entre duas listas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.conjuntos import intersection
        return GenericFeatureWrapper.apply_function(intersection, lst1, lst2)

    @staticmethod
    def union(lst1, lst2):
        """Retorna a união de elementos de duas listas."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.conjuntos import union
        return GenericFeatureWrapper.apply_function(union, lst1, lst2)

    @staticmethod
    def mirror_count(lst, total):
        """Conta os números que têm um 'espelho' na lista (e.g., total - x)."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.conjuntos import mirror_count
        return GenericFeatureWrapper.apply_function(mirror_count, lst, total)

    @staticmethod
    def pair_sum_count(lst, target):
        """Conta os pares de números que somam um valor alvo."""
        # Chamada original + adaptação universal
        from lib.funcoes_analiticas.conjuntos import pair_sum_count
        return GenericFeatureWrapper.apply_function(pair_sum_count, lst, target)


