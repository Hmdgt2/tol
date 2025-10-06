"""
Wrappers automáticos para todas as funções analíticas.
Permite conexão universal e padronização para ML/genético criar heurísticas combinando funções.
Cada wrapper inclui objetivo e finalidade para uso dinâmico.
"""

class UniversalWrapper:
    """
    Objetivo: Adaptar qualquer função para uso em heurísticas evolutivas.
    Finalidade: Padronizar entrada/saída, conectar funções diferentes, permitir recombinação.
    """

    @staticmethod
    def apply_function(func, data, *args, **kwargs):
        """
        Aplica função a dados, adaptando tipo de retorno.
        - Se retorna lista: pega top-N ou estatísticas.
        - Se retorna número: transforma em lista.
        - Se retorna matriz: flatten e pega top-N.
        - Se retorna dict: pega valores.
        - Adapta para o pipeline usar sempre o mesmo formato.
        """
        result = func(data, *args, **kwargs)
        if isinstance(result, list):
            # Exemplo: sempre retorna top 5 elementos ou estatísticas
            return result[:5] if len(result) > 5 else result
        elif isinstance(result, dict):
            return list(result.values())[:5]
        elif isinstance(result, (int, float)):
            return [result]
        elif hasattr(result, 'shape'):  # numpy array or matrix
            try:
                return result.flatten().tolist()[:5]
            except Exception:
                return [float(result)]
        # Qualquer outro tipo retorna como está
        return result

    # Você pode gerar também wrappers por tipo (exemplo):
    @staticmethod
    def fft_magnitude(lst):
        """Detecta padrões cíclicos via FFT."""
        from lib.funcoes_analiticas.processamento_sinal import fft_magnitude
        return UniversalWrapper.apply_function(fft_magnitude, lst)

    @staticmethod
    def count_primes(lst):
        """Conta primos em uma lista."""
        from lib.funcoes_analiticas.teoria_numeros import count_primes
        return UniversalWrapper.apply_function(count_primes, lst)

    # ... gerar para todas as funções automaticamente!
