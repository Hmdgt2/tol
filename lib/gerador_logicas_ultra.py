"""
GERADOR DE LÓGICAS ESCALÁVEL ULTRA - Para 800+ Funções com UniversalWrapper
Sistema inteligente para compor sequências de funções matemáticas avançadas
"""

import random
import numpy as np
from typing import List, Dict, Any, Tuple, Set, Optional, Callable
import json
import logging
import inspect
import time
from functools import lru_cache
from universal_wrapper import UniversalWrapper

# Configurar logging avançado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gerador_logicas.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AnalisadorTiposFuncoesAvancado:
    """
    Analisador avançado para mapear tipos e compatibilidades das 506+ funções
    """
    
    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.mapeamento_tipos = self._construir_mapeamento_completo()
        self.grafo_compatibilidade = self._construir_grafo_compatibilidade()
    
    def _construir_mapeamento_completo(self) -> Dict[str, Dict[str, Any]]:
        """
        Mapeamento completo das 506+ funções com tipos de entrada/saída
        """
        return {
            # === FUNÇÕES MATEMÁTICAS BÁSICAS ===
            'abs_val': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'matematica_basica'},
            'add': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'matematica_basica'},
            'sub': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'matematica_basica'},
            'mul': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'matematica_basica'},
            'div': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'matematica_basica'},
            'pow_func': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'matematica_basica'},
            'sqrt': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'matematica_basica'},
            'cbrt': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'matematica_basica'},
            'exp_func': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'matematica_basica'},
            'log_func': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'matematica_basica'},
            'log10_transform': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'matematica_basica'},
            
            # === FUNÇÕES TRIGONOMÉTRICAS ===
            'sin_transform': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'trigonometria'},
            'cos_transform': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'trigonometria'},
            'tan_transform': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'trigonometria'},
            'arcsin_transform': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'trigonometria'},
            'arccos_transform': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'trigonometria'},
            'arctan_transform': {'entrada': 'numerico', 'saida': 'numerico', 'categoria': 'trigonometria'},
            
            # === FUNÇÕES ESTATÍSTICAS ===
            'mean_combinations2': {'entrada': 'vetor', 'saida': 'escalar', 'categoria': 'estatistica'},
            'std_degree': {'entrada': 'vetor', 'saida': 'escalar', 'categoria': 'estatistica'},
            'higher_order_moments': {'entrada': 'vetor', 'saida': 'vetor', 'categoria': 'estatistica'},
            'shannon_entropy': {'entrada': 'vetor', 'saida': 'escalar', 'categoria': 'estatistica'},
            'gini_index': {'entrada': 'vetor', 'saida': 'escalar', 'categoria': 'estatistica'},
            'normalized_entropy': {'entrada': 'vetor', 'saida': 'escalar', 'categoria': 'estatistica'},
            
            # === FUNÇÕES DE TRANSFORMADA ===
            'fft_magnitude': {'entrada': 'vetor', 'saida': 'espectro', 'categoria': 'transformada'},
            'fft_phase': {'entrada': 'vetor', 'saida': 'espectro', 'categoria': 'transformada'},
            'fft_real': {'entrada': 'vetor', 'saida': 'espectro', 'categoria': 'transformada'},
            'ifft_real': {'entrada': 'espectro', 'saida': 'vetor', 'categoria': 'transformada'},
            'dwt_approx': {'entrada': 'vetor', 'saida': 'wavelet', 'categoria': 'transformada'},
            'wavelet_energy': {'entrada': 'wavelet', 'saida': 'escalar', 'categoria': 'transformada'},
            
            # === FUNÇÕES DE TEORIA DE NÚMEROS ===
            'check_prime': {'entrada': 'inteiro', 'saida': 'booleano', 'categoria': 'teoria_numeros'},
            'prime_factors': {'entrada': 'inteiro', 'saida': 'vetor', 'categoria': 'teoria_numeros'},
            'gcd_list': {'entrada': 'vetor', 'saida': 'inteiro', 'categoria': 'teoria_numeros'},
            'lcm_list': {'entrada': 'vetor', 'saida': 'inteiro', 'categoria': 'teoria_numeros'},
            'euler_phi': {'entrada': 'inteiro', 'saida': 'inteiro', 'categoria': 'teoria_numeros'},
            'mobius_function': {'entrada': 'inteiro', 'saida': 'inteiro', 'categoria': 'teoria_numeros'},
            
            # === FUNÇÕES DE ANÁLISE COMPLEXA ===
            'gamma_func': {'entrada': 'complexo', 'saida': 'complexo', 'categoria': 'analise_complexa'},
            'beta_func': {'entrada': 'complexo', 'saida': 'complexo', 'categoria': 'analise_complexa'},
            'zeta_func': {'entrada': 'complexo', 'saida': 'complexo', 'categoria': 'analise_complexa'},
            'bessel_j': {'entrada': 'complexo', 'saida': 'complexo', 'categoria': 'analise_complexa'},
            'bessel_y': {'entrada': 'complexo', 'saida': 'complexo', 'categoria': 'analise_complexa'},
            
            # === FUNÇÕES DE SISTEMAS DINÂMICOS ===
            'lyapunov_exponent': {'entrada': 'sistema', 'saida': 'escalar', 'categoria': 'sistemas_dinamicos'},
            'mandelbrot_set_membership': {'entrada': 'complexo', 'saida': 'booleano', 'categoria': 'sistemas_dinamicos'},
            'rossler_attractor': {'entrada': 'vetor', 'saida': 'vetor', 'categoria': 'sistemas_dinamicos'},
            
            # === FUNÇÕES DE GEOMETRIA DIFERENCIAL ===
            'gaussian_curvature': {'entrada': 'superficie', 'saida': 'escalar', 'categoria': 'geometria_diferencial'},
            'riemann_metric_tensor': {'entrada': 'variedade', 'saida': 'tensor', 'categoria': 'geometria_diferencial'},
            'geodesic_distance': {'entrada': 'variedade', 'saida': 'escalar', 'categoria': 'geometria_diferencial'},
            
            # === FUNÇÕES DE MECÂNICA QUÂNTICA ===
            'density_matrix_purity': {'entrada': 'matriz_quantica', 'saida': 'escalar', 'categoria': 'quantica'},
            'quantum_fidelity': {'entrada': 'estado_quantico', 'saida': 'escalar', 'categoria': 'quantica'},
            'von_neumann_entropy': {'entrada': 'matriz_densidade', 'saida': 'escalar', 'categoria': 'quantica'},
            'concurrence_entanglement': {'entrada': 'estado_quantico', 'saida': 'escalar', 'categoria': 'quantica'},
            
            # === FUNÇÕES DE TEORIA DA INFORMAÇÃO ===
            'mutual_info': {'entrada': 'distribuicao', 'saida': 'escalar', 'categoria': 'teoria_informacao'},
            'kl_divergence': {'entrada': 'distribuicao', 'saida': 'escalar', 'categoria': 'teoria_informacao'},
            'jensen_shannon': {'entrada': 'distribuicao', 'saida': 'escalar', 'categoria': 'teoria_informacao'},
            
            # === FUNÇÕES DE PROCESSAMENTO DE SINAIS ===
            'hilbert_transform': {'entrada': 'sinal', 'saida': 'analitico', 'categoria': 'processamento_sinais'},
            'teager_kaiser_energy': {'entrada': 'sinal', 'saida': 'energia', 'categoria': 'processamento_sinais'},
            'empirical_mode_decomposition': {'entrada': 'sinal', 'saida': 'modos', 'categoria': 'processamento_sinais'},
            
            # === FUNÇÕES DE ANÁLISE FRACTAL ===
            'higuchi_fractal_dimension': {'entrada': 'serie_temporal', 'saida': 'escalar', 'categoria': 'fractal'},
            'multifractal_spectrum': {'entrada': 'serie_temporal', 'saida': 'espectro', 'categoria': 'fractal'},
            'lacunarity_analysis': {'entrada': 'padrao', 'saida': 'escalar', 'categoria': 'fractal'},
            
            # === FUNÇÕES DE TEORIA DE GRUPOS ===
            'group_character_table': {'entrada': 'grupo', 'saida': 'tabela', 'categoria': 'algebra_abstrata'},
            'young_tableaux_count': {'entrada': 'particao', 'saida': 'inteiro', 'categoria': 'algebra_abstrata'},
            
            # === FUNÇÕES DE OTIMIZAÇÃO ===
            'genetic_algorithm': {'entrada': 'funcao_objetivo', 'saida': 'otimo', 'categoria': 'otimizacao'},
            'particle_swarm_optimization': {'entrada': 'funcao_objetivo', 'saida': 'otimo', 'categoria': 'otimizacao'},
            'simulated_annealing': {'entrada': 'funcao_objetivo', 'saida': 'otimo', 'categoria': 'otimizacao'},
            
            # === FUNÇÕES DE CRIPTOGRAFIA ===
            'rsa_factorization': {'entrada': 'inteiro_grande', 'saida': 'fatores', 'categoria': 'criptografia'},
            'elliptic_curve_discrete_log': {'entrada': 'ponto_curva', 'saida': 'inteiro', 'categoria': 'criptografia'},
            
            # Adicione mais funções conforme necessário...
        }
    
    def _construir_grafo_compatibilidade(self) -> Dict[str, List[str]]:
        """
        Constrói grafo de compatibilidade entre tipos
        """
        return {
            'numerico': ['numerico', 'vetor', 'matriz', 'complexo', 'escalar'],
            'vetor': ['vetor', 'numerico', 'escalar', 'espectro', 'wavelet'],
            'escalar': ['escalar', 'numerico', 'vetor'],
            'espectro': ['espectro', 'vetor', 'numerico'],
            'complexo': ['complexo', 'numerico'],
            'matriz': ['matriz', 'vetor', 'escalar'],
            'wavelet': ['wavelet', 'vetor', 'escalar'],
            'inteiro': ['inteiro', 'numerico'],
            'booleano': ['booleano', 'inteiro'],
            'sistema': ['sistema', 'vetor'],
            'superficie': ['superficie', 'vetor'],
            'variedade': ['variedade', 'tensor'],
            'tensor': ['tensor', 'matriz'],
            'matriz_quantica': ['matriz_quantica', 'matriz'],
            'estado_quantico': ['estado_quantico', 'vetor'],
            'matriz_densidade': ['matriz_densidade', 'matriz'],
            'distribuicao': ['distribuicao', 'vetor'],
            'sinal': ['sinal', 'vetor'],
            'analitico': ['analitico', 'complexo'],
            'energia': ['energia', 'escalar'],
            'modos': ['modos', 'vetor'],
            'serie_temporal': ['serie_temporal', 'vetor'],
            'padrao': ['padrao', 'matriz'],
            'grupo': ['grupo', 'estrutura_algebrica'],
            'tabela': ['tabela', 'matriz'],
            'particao': ['particao', 'vetor'],
            'funcao_objetivo': ['funcao_objetivo', 'funcao'],
            'otimo': ['otimo', 'vetor'],
            'inteiro_grande': ['inteiro_grande', 'inteiro'],
            'fatores': ['fatores', 'vetor'],
            'ponto_curva': ['ponto_curva', 'vetor'],
            'estrutura_algebrica': ['estrutura_algebrica', 'grupo'],
            'funcao': ['funcao', 'numerico']
        }
    
    def categorizar_funcao(self, nome_funcao: str) -> str:
        """Categoriza uma função baseada no mapeamento"""
        if nome_funcao in self.mapeamento_tipos:
            return self.mapeamento_tipos[nome_funcao]['categoria']
        
        # Categorização heurística baseada no nome
        if any(term in nome_funcao for term in ['prime', 'factor', 'gcd', 'lcm']):
            return 'teoria_numeros'
        elif any(term in nome_funcao for term in ['fft', 'dwt', 'wavelet', 'transform']):
            return 'transformada'
        elif any(term in nome_funcao for term in ['lyapunov', 'attractor', 'chaos']):
            return 'sistemas_dinamicos'
        elif any(term in nome_funcao for term in ['quantum', 'entanglement', 'fidelity']):
            return 'quantica'
        elif any(term in nome_funcao for term in ['fractal', 'dimension', 'lacunarity']):
            return 'fractal'
        elif any(term in nome_funcao for term in ['entropy', 'divergence', 'mutual']):
            return 'teoria_informacao'
        elif any(term in nome_funcao for term in ['matrix', 'eigen', 'determinant']):
            return 'algebra_linear'
        elif any(term in nome_funcao for term in ['graph', 'node', 'edge']):
            return 'teoria_grafos'
        else:
            return 'matematica_basica'
    
    def obter_tipo_saida(self, nome_funcao: str) -> str:
        """Obtém o tipo de saída de uma função"""
        if nome_funcao in self.mapeamento_tipos:
            return self.mapeamento_tipos[nome_funcao]['saida']
        return 'numerico'  # Fallback padrão
    
    def obter_tipo_entrada(self, nome_funcao: str) -> str:
        """Obtém o tipo de entrada de uma função"""
        if nome_funcao in self.mapeamento_tipos:
            return self.mapeamento_tipos[nome_funcao]['entrada']
        return 'numerico'  # Fallback padrão
    
    def sao_compatíveis(self, tipo_saida: str, nome_funcao_destino: str) -> bool:
        """Verifica se dois tipos são compatíveis"""
        tipo_entrada_destino = self.obter_tipo_entrada(nome_funcao_destino)
        
        if tipo_saida in self.grafo_compatibilidade:
            return tipo_entrada_destino in self.grafo_compatibilidade[tipo_saida]
        
        return tipo_saida == tipo_entrada_destino

class GeradorLogicasEscalavelUltra:
    """
    Gerador ultra-escalável para 800+ funções com UniversalWrapper
    """
    
    def __init__(self, wrapper=None):
        self.wrapper = wrapper or UniversalWrapper()
        self.analisador_tipos = AnalisadorTiposFuncoesAvancado(self.wrapper)
        self.categorias_dinamicas = self._categorizar_funcoes_dinamicamente()
        self.logicas_avaliadas = []
        self.cache_validacao = {}
        self.estatisticas_execucao = {}
        
        logger.info(f"🚀 GERADOR ULTRA inicializado com {len(self._obter_todas_funcoes())} funções")
        logger.info(f"📊 {len(self.categorias_dinamicas)} categorias dinâmicas detectadas")
    
    def _obter_todas_funcoes(self) -> List[str]:
        """Obtém automaticamente todas as funções do wrapper"""
        return [attr for attr in dir(self.wrapper) 
                if not attr.startswith('_') and callable(getattr(self.wrapper, attr))]
    
    def _categorizar_funcoes_dinamicamente(self) -> Dict[str, List[str]]:
        """Categoriza automaticamente todas as funções disponíveis"""
        todas_funcoes = self._obter_todas_funcoes()
        categorias = {}
        
        for funcao in todas_funcoes:
            categoria = self.analisador_tipos.categorizar_funcao(funcao)
            
            if categoria not in categorias:
                categorias[categoria] = []
            
            categorias[categoria].append(funcao)
        
        # Log estatísticas detalhadas
        for cat, funcoes in sorted(categorias.items(), key=lambda x: len(x[1]), reverse=True):
            logger.info(f"📁 {cat}: {len(funcoes)} funções")
        
        total_funcoes = sum(len(f) for f in categorias.values())
        logger.info(f"📊 TOTAL: {total_funcoes} funções em {len(categorias)} categorias")
        
        return categorias
    
    def _gerar_dados_teste_avancado(self, tipo: str = "vetor", tamanho: int = 100) -> Any:
        """
        Gera dados de teste avançados para validação das lógicas
        """
        geradores = {
            "vetor": lambda: [random.uniform(-10, 10) for _ in range(tamanho)],
            "inteiro": lambda: [random.randint(1, 100) for _ in range(tamanho)],
            "matriz": lambda: [[random.uniform(-5, 5) for _ in range(int(np.sqrt(tamanho)))] 
                             for _ in range(int(np.sqrt(tamanho)))],
            "sequencia_temporal": lambda: self._gerar_serie_temporal(tamanho),
            "escalar": lambda: random.uniform(-100, 100),
            "complexo": lambda: [complex(random.uniform(-1, 1), random.uniform(-1, 1)) 
                               for _ in range(tamanho)],
            "fractal": lambda: self._gerar_sequencia_fractal(tamanho),
            "quantico": lambda: self._gerar_estado_quantico(tamanho),
            "sistema_caotico": lambda: self._gerar_trajetoria_caotica(tamanho),
            "grafo": lambda: self._gerar_grafo_aleatorio(tamanho // 10),
            "distribuicao_probabilidade": lambda: self._gerar_distribuicao(tamanho),
        }
        
        return geradores.get(tipo, geradores["vetor"])()
    
    def _gerar_serie_temporal(self, tamanho: int) -> List[float]:
        """Gera série temporal com tendência e sazonalidade"""
        tempo = np.linspace(0, 4*np.pi, tamanho)
        tendencia = 0.1 * tempo
        sazonalidade = 2 * np.sin(tempo)
        ruido = np.random.normal(0, 0.5, tamanho)
        return list(tendencia + sazonalidade + ruido)
    
    def _gerar_sequencia_fractal(self, tamanho: int) -> List[float]:
        """Gera sequência com propriedades fractais"""
        sequencia = [random.uniform(-1, 1)]
        for i in range(1, tamanho):
            # Processo auto-similar
            prev = sequencia[i-1]
            sequencia.append(prev * 0.7 + random.gauss(0, 0.3) + 0.1 * np.sin(i * 0.1))
        return sequencia
    
    def _gerar_estado_quantico(self, tamanho: int) -> List[complex]:
        """Gera estado quântico normalizado"""
        estado = [complex(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(tamanho)]
        norma = np.sqrt(sum(abs(z)**2 for z in estado))
        return [z/norma for z in estado]
    
    def _gerar_trajetoria_caotica(self, tamanho: int) -> List[float]:
        """Gera trajetória de sistema caótico (logístico)"""
        x = [random.uniform(0, 1)]
        r = 3.9  # Parâmetro caótico
        for _ in range(tamanho-1):
            x.append(r * x[-1] * (1 - x[-1]))
        return x
    
    def _gerar_grafo_aleatorio(self, num_nos: int) -> Dict[str, Any]:
        """Gera grafo aleatório para funções de teoria dos grafos"""
        nos = list(range(num_nos))
        arestas = []
        for i in range(num_nos):
            for j in range(i+1, num_nos):
                if random.random() < 0.3:  # 30% de chance de conexão
                    arestas.append((i, j, random.random()))
        return {'nos': nos, 'arestas': arestas}
    
    def _gerar_distribuicao(self, tamanho: int) -> List[float]:
        """Gera distribuição de probabilidade"""
        dist = np.random.exponential(1, tamanho)
        return list(dist / np.sum(dist))
    
    def gerar_logica_inteligente_avancada(self, 
                                        objetivo: str = None,
                                        comprimento: Tuple[int, int] = (3, 8),
                                        complexidade: str = "media") -> List[str]:
        """
        Gera lógicas inteligentes avançadas com diferentes níveis de complexidade
        """
        comprimento_alvo = random.randint(comprimento[0], comprimento[1])
        
        estrategias = {
            "simples": self._gerar_logica_simples,
            "media": self._gerar_logica_por_compatibilidade,
            "avancada": self._gerar_logica_avancada,
            "especializada": lambda comp: self._gerar_logica_orientada_objetivo(objetivo, comp)
        }
        
        estrategia = estrategias.get(complexidade, estrategias["media"])
        return estrategia(comprimento_alvo)
    
    def _gerar_logica_simples(self, comprimento: int) -> List[str]:
        """Gera lógica simples com funções básicas"""
        categorias_simples = ['matematica_basica', 'estatistica', 'trigonometria']
        funcoes_candidatas = []
        
        for cat in categorias_simples:
            if cat in self.categorias_dinamicas:
                funcoes_candidatas.extend(self.categorias_dinamicas[cat])
        
        return random.sample(funcoes_candidatas, min(comprimento, len(funcoes_candidatas)))
    
    def _gerar_logica_avancada(self, comprimento: int) -> List[str]:
        """Gera lógica avançada com funções complexas"""
        categorias_avancadas = [
            'sistemas_dinamicos', 'quantica', 'fractal', 
            'analise_complexa', 'geometria_diferencial'
        ]
        
        logica = []
        tentativas = 0
        
        while len(logica) < comprimento and tentativas < 20:
            tentativas += 1
            
            if not logica:
                # Escolher função inicial avançada
                cat_inicial = random.choice(categorias_avancadas)
                if cat_inicial in self.categorias_dinamicas:
                    funcao = random.choice(self.categorias_dinamicas[cat_inicial])
                    logica.append(funcao)
                    tipo_atual = self.analisador_tipos.obter_tipo_saida(funcao)
            else:
                # Encontrar função compatível avançada
                funcao_compativel = self._encontrar_funcao_avancada_compativel(tipo_atual, logica)
                if funcao_compativel:
                    logica.append(funcao_compativel)
                    tipo_atual = self.analisador_tipos.obter_tipo_saida(funcao_compativel)
                else:
                    # Reiniciar com nova função
                    cat_inicial = random.choice(categorias_avancadas)
                    if cat_inicial in self.categorias_dinamicas:
                        funcao = random.choice(self.categorias_dinamicas[cat_inicial])
                        if funcao not in logica:
                            logica.append(funcao)
                            tipo_atual = self.analisador_tipos.obter_tipo_saida(funcao)
        
        return logica if len(logica) >= 2 else self._gerar_logica_simples(comprimento)
    
    def _encontrar_funcao_avancada_compativel(self, tipo_entrada: str, logica_existente: List[str]) -> Optional[str]:
        """Encontra função avançada compatível"""
        categorias_avancadas = [
            'sistemas_dinamicos', 'quantica', 'fractal', 
            'analise_complexa', 'geometria_diferencial', 'teoria_informacao'
        ]
        
        candidatas = []
        for cat in categorias_avancadas:
            if cat in self.categorias_dinamicas:
                for funcao in self.categorias_dinamicas[cat]:
                    if (funcao not in logica_existente and 
                        self.analisador_tipos.sao_compatíveis(tipo_entrada, funcao)):
                        candidatas.append(funcao)
        
        return random.choice(candidatas) if candidatas else None
    
    # [Métodos _gerar_logica_por_compatibilidade, _gerar_logica_orientada_objetivo, 
    # _escolher_funcao_inicial, _encontrar_funcao_compativel similares ao anterior...]
    
    def executar_logica_com_monitoramento(self, logica: List[str], dados: Any) -> Dict[str, Any]:
        """
        Executa lógica com monitoramento detalhado de performance
        """
        if not logica:
            return {'resultado': dados, 'estatisticas': {}}
        
        resultado = dados
        estatisticas = {
            'funcoes_executadas': [],
            'tempos_execucao': [],
            'tamanhos_resultados': [],
            'erros': []
        }
        
        for i, funcao in enumerate(logica):
            try:
                if hasattr(self.wrapper, funcao):
                    inicio = time.time()
                    
                    # Executar função com tratamento inteligente de parâmetros
                    if isinstance(resultado, (list, tuple)) and len(resultado) > 0:
                        resultado_execucao = getattr(self.wrapper, funcao)(resultado)
                    elif isinstance(resultado, (int, float)):
                        resultado_execucao = getattr(self.wrapper, funcao)([resultado])
                    elif isinstance(resultado, dict):
                        resultado_execucao = getattr(self.wrapper, funcao)(resultado)
                    else:
                        resultado_execucao = getattr(self.wrapper, funcao)(resultado)
                    
                    fim = time.time()
                    
                    # Atualizar estatísticas
                    estatisticas['funcoes_executadas'].append(funcao)
                    estatisticas['tempos_execucao'].append(fim - inicio)
                    
                    if hasattr(resultado_execucao, '__len__'):
                        estatisticas['tamanhos_resultados'].append(len(resultado_execucao))
                    else:
                        estatisticas['tamanhos_resultados'].append(1)
                    
                    resultado = resultado_execucao
                    
                    # Log de progresso para lógicas longas
                    if len(logica) > 10 and i % 5 == 0:
                        logger.info(f"📈 Progresso: {i+1}/{len(logica)} funções executadas")
                        
                else:
                    estatisticas['erros'].append(f"Função {funcao} não encontrada")
                    logger.warning(f"⚠️ Função {funcao} não encontrada")
                    
            except Exception as e:
                erro_msg = f"Erro em {funcao} (posição {i+1}): {str(e)}"
                estatisticas['erros'].append(erro_msg)
                logger.error(f"❌ {erro_msg}")
                break
        
        return {
            'resultado': resultado,
            'estatisticas': estatisticas,
            'sucesso': len(estatisticas['erros']) == 0
        }
    
    def avaliar_logica_avancada(self, logica: List[str], num_testes: int = 8) -> Dict[str, Any]:
        """
        Avaliação avançada com múltiplas métricas
        """
        cache_key = tuple(logica)
        if cache_key in self.cache_validacao:
            return self.cache_validacao[cache_key]
        
        # Gerar dados de teste diversificados
        tipos_teste = ["vetor", "sequencia_temporal", "matriz", "complexo", "fractal"]
        dados_teste = [self._gerar_dados_teste_avancado(tipo, 50 + i*20) 
                      for i, tipo in enumerate(tipos_teste[:num_testes])]
        
        resultados = []
        metricas = {
            'sucessos': 0,
            'tempos': [],
            'estabilidade': [],
            'diversidade': []
        }
        
        for dados in dados_teste:
            try:
                execucao = self.executar_logica_com_monitoramento(logica, dados)
                
                if execucao['sucesso']:
                    metricas['sucessos'] += 1
                    metricas['tempos'].append(np.mean(execucao['estatisticas']['tempos_execucao']))
                    
                    # Calcular estabilidade numérica
                    resultado = execucao['resultado']
                    if isinstance(resultado, (list, tuple)) and len(resultado) > 1:
                        estabilidade = 1.0 / (1.0 + np.std([float(x) for x in resultado if np.isfinite(x)]))
                        metricas['estabilidade'].append(estabilidade)
                    
                    resultados.append(resultado)
                    
            except Exception as e:
                logger.debug(f"Teste falhou: {e}")
                continue
        
        # Métricas compostas
        taxa_sucesso = metricas['sucessos'] / len(dados_teste)
        tempo_medio = np.mean(metricas['tempos']) if metricas['tempos'] else float('inf')
        estabilidade_media = np.mean(metricas['estabilidade']) if metricas['estabilidade'] else 0.5
        
        # Score avançado
        score = (
            taxa_sucesso * 0.4 +
            (1 / (1 + min(tempo_medio, 10))) * 0.3 +
            estabilidade_media * 0.2 +
            min(len(logica) / 15, 1) * 0.1  # Penalizar lógicas muito longas
        )
        
        avaliacao = {
            'logica': logica,
            'score': float(score),
            'taxa_sucesso': float(taxa_sucesso),
            'tempo_medio': float(tempo_medio),
            'estabilidade': float(estabilidade_media),
            'num_funcoes': len(logica),
            'complexidade_estimada': self._calcular_complexidade_logica(logica),
            'categorias_envolvidas': list(set(self.analisador_tipos.categorizar_funcao(f) for f in logica))
        }
        
        self.cache_validacao[cache_key] = avaliacao
        return avaliacao
    
    def _calcular_complexidade_logica(self, logica: List[str]) -> float:
        """Calcula complexidade estimada da lógica"""
        complexidades = {
            'matematica_basica': 1.0,
            'estatistica': 1.5,
            'trigonometria': 1.2,
            'transformada': 2.0,
            'teoria_numeros': 1.8,
            'analise_complexa': 2.5,
            'sistemas_dinamicos': 3.0,
            'quantica': 3.5,
            'fractal': 2.8,
            'geometria_diferencial': 3.2,
            'teoria_informacao': 2.3,
            'algebra_linear': 2.0,
            'teoria_grafos': 2.2,
            'criptografia': 3.0,
            'otimizacao': 2.7
        }
        
        complexidade_total = 0
        for funcao in logica:
            categoria = self.analisador_tipos.categorizar_funcao(funcao)
            complexidade_total += complexidades.get(categoria, 1.5)
        
        return complexidade_total / len(logica) if logica else 1.0
    
    def evoluir_logicas_avancado(self, 
                               tamanho_populacao: int = 40,
                               geracoes: int = 25,
                               estrategia: str = "balanceada") -> List[Dict[str, Any]]:
        """
        Algoritmo genético avançado para evolução de lógicas
        """
        logger.info(f"🧬 EVOLUÇÃO AVANÇADA: {tamanho_populacao} lógicas, {geracoes} gerações")
        
        # População inicial diversificada
        populacao = []
        while len(populacao) < tamanho_populacao:
            complexidade = random.choice(["simples", "media", "avancada"])
            logica = self.gerar_logica_inteligente_avancada(complexidade=complexidade)
            
            if logica and logica not in [p['logica'] for p in populacao]:
                avaliacao = self.avaliar_logica_avancada(logica)
                populacao.append(avaliacao)
        
        estrategias_evolucao = {
            "exploratoria": self._evolucao_exploratoria,
            "exploratoria": self._evolucao_exploratoria,
            "balanceada": self._evolucao_balanceada
        }
        
        estrategia_fn = estrategias_evolucao.get(estrategia, self._evolucao_balanceada)
        
        for geracao in range(geracoes):
            populacao = estrategia_fn(populacao, tamanho_populacao, geracao)
            
            # Log detalhado
            if geracao % 5 == 0:
                melhor = populacao[0]
                logger.info(
                    f"📈 Geração {geracao}: "
                    f"Melhor = {melhor['score']:.3f}, "
                    f"Funções = {melhor['num_funcoes']}, "
                    f"Categorias = {len(melhor['categorias_envolvidas'])}"
                )
        
        populacao.sort(key=lambda x: x['score'], reverse=True)
        logger.info(f"🏆 EVOLUÇÃO COMPLETA. Melhor score: {populacao[0]['score']:.3f}")
        
        return populacao[:15]
    
    def _evolucao_balanceada(self, populacao: List[Dict], tamanho_populacao: int, geracao: int) -> List[Dict]:
        """Estratégia de evolução balanceada"""
        populacao.sort(key=lambda x: x['score'], reverse=True)
        
        # Elitismo (20% melhores)
        nova_populacao = populacao[:max(8, tamanho_populacao // 5)]
        
        while len(nova_populacao) < tamanho_populacao:
            # Seleção adaptativa baseada na geração
            if geracao < 10:
                # Fase inicial: mais exploração
                pai1, pai2 = random.sample(populacao[:len(populacao)//2], 2)
            else:
                # Fase posterior: mais exploração
                pai1, pai2 = random.sample(populacao[:len(populacao)//3], 2)
            
            # Crossover com taxa adaptativa
            taxa_crossover = 0.7 + 0.2 * (geracao / 25)  # Aumenta com as gerações
            if random.random() < taxa_crossover:
                filho_logica = self._crossover_avancado(pai1['logica'], pai2['logica'])
            else:
                filho_logica = random.choice([pai1['logica'], pai2['logica']])
            
            # Mutação com taxa decrescente
            taxa_mutacao = 0.15 * (1 - geracao / 30)  # Diminui com as gerações
            if random.random() < taxa_mutacao:
                filho_logica = self._mutar_avancado(filho_logica)
            
            # Avaliar e adicionar
            if filho_logica:
                avaliacao_filho = self.avaliar_logica_avancada(filho_logica)
                nova_populacao.append(avaliacao_filho)
        
        return nova_populacao
    
    def _crossover_avancado(self, logica1: List[str], logica2: List[str]) -> List[str]:
        """Crossover avançado que preserva compatibilidade"""
        if len(logica1) < 2 or len(logica2) < 2:
            return logica1 or logica2
        
        # Encontrar pontos de crossover que mantenham compatibilidade
        pontos_validos = []
        for i in range(1, min(len(logica1), len(logica2))):
            tipo_saida_ant = self.analisador_tipos.obter_tipo_saida(logica1[i-1])
            tipo_entrada_prox = self.analisador_tipos.obter_tipo_entrada(logica2[i])
            
            if self.analisador_tipos.sao_compatíveis(tipo_saida_ant, logica2[i]):
                pontos_validos.append(i)
        
        if pontos_validos:
            ponto = random.choice(pontos_validos)
            filho = logica1[:ponto] + logica2[ponto:]
        else:
            # Fallback: crossover simples
            ponto = random.randint(1, min(len(logica1), len(logica2)) - 1)
            filho = logica1[:ponto] + logica2[ponto:]
        
        # Remover duplicados mantendo ordem e compatibilidade
        return self._otimizar_ordem_funcoes(filho)
    
    def _mutar_avancado(self, logica: List[str]) -> List[str]:
        """Mutação avançada que mantém compatibilidade"""
        if len(logica) < 2:
            return logica
        
        operacoes = ['substituir_compativel', 'adicionar_compativel', 'remover', 'reordenar_compativel']
        operacao = random.choice(operacoes)
        
        if operacao == 'substituir_compativel' and len(logica) > 1:
            idx = random.randint(0, len(logica) - 1)
            
            # Encontrar função compatível considerando vizinhança
            tipo_entrada = self.analisador_tipos.obter_tipo_entrada(logica[idx])
            tipo_saida_esperado = self.analisador_tipos.obter_tipo_saida(logica[idx])
            
            candidatas = []
            for funcao in self._obter_todas_funcoes():
                if (funcao not in logica and
                    self.analisador_tipos.obter_tipo_entrada(funcao) == tipo_entrada and
                    self.analisador_tipos.obter_tipo_saida(funcao) == tipo_saida_esperado):
                    candidatas.append(funcao)
            
            if candidatas:
                logica[idx] = random.choice(candidatas)
                
        elif operacao == 'adicionar_compativel' and len(logica) < 12:
            idx = random.randint(0, len(logica))
            
            if idx == 0:
                # Adicionar no início
                nova_funcao = self._escolher_funcao_inicial()
                if nova_funcao not in logica:
                    logica.insert(0, nova_funcao)
            else:
                # Adicionar no meio mantendo compatibilidade
                tipo_anterior = self.analisador_tipos.obter_tipo_saida(logica[idx-1])
                candidatas = []
                
                for funcao in self._obter_todas_funcoes():
                    if (funcao not in logica and
                        self.analisador_tipos.sao_compatíveis(tipo_anterior, funcao)):
                        candidatas.append(funcao)
                
                if candidatas:
                    logica.insert(idx, random.choice(candidatas))
        
        elif operacao == 'remover' and len(logica) > 3:
            # Remover função que não quebre a cadeia
            if len(logica) > 3:
                idx = random.randint(1, len(logica) - 2)  # Não remove extremos
                # Verificar se a remoção mantém compatibilidade
                if (self.analisador_tipos.sao_compatíveis(
                    self.analisador_tipos.obter_tipo_saida(logica[idx-1]),
                    logica[idx+1]
                )):
                    logica.pop(idx)
        
        elif operacao == 'reordenar_compativel' and len(logica) > 2:
            # Reordenar mantendo compatibilidade
            logica_otimizada = self._otimizar_ordem_funcoes(logica)
            if len(logica_otimizada) == len(logica):  # Só aceitar se não perder funções
                logica = logica_otimizada
        
        return logica
    
    def _otimizar_ordem_funcoes(self, logica: List[str]) -> List[str]:
        """Otimiza a ordem das funções para maximizar compatibilidade"""
        if len(logica) <= 1:
            return logica
        
        # Remover duplicados
        logica_unica = []
        for funcao in logica:
            if funcao not in logica_unica:
                logica_unica.append(funcao)
        
        if len(logica_unica) <= 1:
            return logica_unica
        
        # Ordenar por compatibilidade usando algoritmo guloso
        ordenada = [logica_unica[0]]
        restantes = logica_unica[1:]
        
        while restantes:
            # Encontrar a função mais compatível com a última da lista ordenada
            ultimo_tipo = self.analisador_tipos.obter_tipo_saida(ordenada[-1])
            melhor_compatibilidade = -1
            melhor_funcao = None
            melhor_idx = -1
            
            for idx, funcao in enumerate(restantes):
                compatibilidade = self._calcular_compatibilidade(ultimo_tipo, funcao)
                if compatibilidade > melhor_compatibilidade:
                    melhor_compatibilidade = compatibilidade
                    melhor_funcao = funcao
                    melhor_idx = idx
            
            if melhor_funcao:
                ordenada.append(melhor_funcao)
                restantes.pop(melhor_idx)
            else:
                # Se nenhuma é compatível, adicionar aleatoriamente
                ordenada.append(restantes.pop(0))
        
        return ordenada
    
    def _calcular_compatibilidade(self, tipo_saida: str, nome_funcao: str) -> float:
        """Calcula score de compatibilidade entre tipos"""
        tipo_entrada = self.analisador_tipos.obter_tipo_entrada(nome_funcao)
        
        if tipo_saida == tipo_entrada:
            return 1.0
        elif tipo_entrada in self.analisador_tipos.grafo_compatibilidade.get(tipo_saida, []):
            return 0.8
        else:
            return 0.0
    
    def _escolher_funcao_inicial(self) -> str:
        """Escolhe função inicial com boa probabilidade de sucesso"""
        categorias_iniciais = ['matematica_basica', 'estatistica', 'vetor', 'transformada_simples']
        candidatas = []
        
        for cat in categorias_iniciais:
            if cat in self.categorias_dinamicas:
                candidatas.extend(self.categorias_dinamicas[cat])
        
        return random.choice(candidatas) if candidatas else random.choice(self._obter_todas_funcoes())
    
    def salvar_logicas_avancado(self, arquivo: str = "logicas_avancadas.json"):
        """Salva lógicas com metadados avançados"""
        dados_salvar = {
            'logicas': self.logicas_avaliadas,
            'metadata': {
                'total_funcoes': len(self._obter_todas_funcoes()),
                'categorias': list(self.categorias_dinamicas.keys()),
                'timestamp': time.time(),
                'versao': 'ultra_escalavel_1.0'
            }
        }
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_salvar, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 {len(self.logicas_avaliadas)} lógicas salvas em {arquivo}")
    
    def carregar_logicas_avancado(self, arquivo: str = "logicas_avancadas.json"):
        """Carrega lógicas com verificação de compatibilidade"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            self.logicas_avaliadas = dados.get('logicas', [])
            logger.info(f"📂 {len(self.logicas_avaliadas)} lógicas carregadas")
            
        except FileNotFoundError:
            logger.warning(f"Arquivo {arquivo} não encontrado")
        except Exception as e:
            logger.error(f"Erro ao carregar lógicas: {e}")

# Funções de demonstração ultra-escaláveis
def demonstrar_poder_ultra():
    print("🚀 GERADOR ULTRA-ESCALÁVEL - DEMONSTRAÇÃO DE PODER")
    print("=" * 60)
    
    try:
        gerador = GeradorLogicasEscalavelUltra()
        
        print(f"🎯 SISTEMA INICIALIZADO:")
        print(f"   📊 {len(gerador._obter_todas_funcoes())} funções disponíveis")
        print(f"   🗂️  {len(gerador.categorias_dinamicas)} categorias dinâmicas")
        
        # Demonstrar diferentes níveis de complexidade
        print("\n🔧 GERANDO LÓGICAS EM DIFERENTES NÍVEIS:")
        
        niveis = ["simples", "media", "avancada"]
        for nivel in niveis:
            logica = gerador.gerar_logica_inteligente_avancada(complexidade=nivel)
            avaliacao = gerador.avaliar_logica_avancada(logica[:6])  # Testar com 6 funções
            
            print(f"\n   🎯 {nivel.upper()}:")
            print(f"      📋 {len(logica)} funções: {' → '.join(logica[:4])}...")
            print(f"      ⭐ Score: {avaliacao['score']:.3f}")
            print(f"      🎯 Sucesso: {avaliacao['taxa_sucesso']:.1%}")
            print(f"      ⚡ Complexidade: {avaliacao['complexidade_estimada']:.2f}")
        
        print("\n🧪 TESTANDO EXECUÇÃO AVANÇADA:")
        dados_complexos = gerador._gerar_dados_teste_avancado("quantico", 20)
        logica_teste = gerador.gerar_logica_inteligente_avancada(complexidade="media")
        
        resultado = gerador.executar_logica_com_monitoramento(logica_teste[:4], dados_complexos)
        print(f"   ✅ Execução: {resultado['sucesso']}")
        print(f"   ⏱️  Tempo médio: {np.mean(resultado['estatisticas']['tempos_execucao']):.4f}s")
        print(f"   🔢 Funções executadas: {len(resultado['estatisticas']['funcoes_executadas'])}")
        
        print(f"\n✅ DEMONSTRAÇÃO ULTRA CONCLUÍDA!")
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()

def benchmark_escalabilidade():
    """Benchmark de escalabilidade do sistema"""
    print("\n📊 BENCHMARK DE ESCALABILIDADE")
    print("=" * 50)
    
    try:
        gerador = GeradorLogicasEscalavelUltra()
        
        tamanhos_testar = [10, 25, 50, 100]
        resultados = []
        
        for tamanho in tamanhos_testar:
            inicio = time.time()
            
            # Gerar e avaliar múltiplas lógicas
            logicas = []
            for _ in range(min(tamanho, 20)):  # Limitar para não demorar muito
                logica = gerador.gerar_logica_inteligente_avancada(complexidade="media")
                avaliacao = gerador.avaliar_logica_avancada(logica[:5])
                logicas.append(avaliacao)
            
            fim = time.time()
            tempo_total = fim - inicio
            
            resultados.append({
                'tamanho': tamanho,
                'tempo': tempo_total,
                'logicas_geradas': len(logicas),
                'score_medio': np.mean([l['score'] for l in logicas]) if logicas else 0
            })
            
            print(f"   📈 {tamanho} lógicas: {tempo_total:.2f}s "
                  f"(score médio: {resultados[-1]['score_medio']:.3f})")
        
        print(f"\n✅ Benchmark concluído!")
        
    except Exception as e:
        print(f"❌ Erro no benchmark: {e}")

if __name__ == "__main__":
    print("🚀 GERADOR DE LÓGICAS ULTRA-ESCALÁVEL")
    print("Para 800+ funções com UniversalWrapper")
    print("=" * 65)
    
    # Executar demonstrações
    demonstrar_poder_ultra()
    benchmark_escalabilidade()
    
    print(f"\n🎉 SISTEMA PRONTO PARA OPERAÇÃO EM ESCALA!")
