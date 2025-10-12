"""
GERADOR DE LÓGICAS ESCALÁVEL - Para 800+ funções
Sistema inteligente para compor sequências de funções do UniversalWrapper
"""

import random
import numpy as np
from typing import List, Dict, Any, Tuple, Set, Optional
import json
import logging
import inspect
import time
from functools import lru_cache
from universal_wrapper import UniversalWrapper

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnalisadorTiposFuncoes:
    """
    Analisa automaticamente tipos de entrada e saída das funções
    """
    
    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.cache_tipos = {}
        
        # Mapeamento de padrões de nome para tipos
        self.padroes_tipo = {
            # Processamento de Sinal
            'fft_': 'espectro', 'dct_': 'espectro', 'fourier_': 'espectro',
            'spectral_': 'espectro', 'frequency_': 'espectro', 'wavelet_': 'espectro',
            
            # Álgebra Linear
            'matrix_': 'matriz', 'vector_': 'vetor', 'eigen': 'autovalor',
            'determinant': 'escalar', 'inverse': 'matriz', 'transpose': 'matriz',
            
            # Estatística
            'mean': 'escalar', 'median': 'escalar', 'std_': 'escalar', 'variance': 'escalar',
            'skewness': 'escalar', 'kurtosis': 'escalar', 'quantile': 'escalar',
            'correlation': 'correlacao', 'covariance': 'covariancia',
            
            # Teoria dos Números
            'prime_': 'inteiro', 'gcd': 'inteiro', 'lcm': 'inteiro', 
            'count_': 'inteiro', 'is_': 'booleano',
            
            # Similaridade e Distância
            'similarity': 'similaridade', 'distance': 'distancia', 
            'cosine_': 'similaridade', 'euclidean': 'distancia',
            
            # Transformações
            'normalize': 'vetor', 'standardize': 'vetor', 'transform': 'vetor',
            'log_': 'vetor', 'exp_': 'vetor',
            
            # Análise de Sequências
            'sequence_': 'sequencia', 'subsequence': 'sequencia',
            'longest_': 'sequencia', 'count_': 'inteiro',
            
            # 🌀 SISTEMAS DINÂMICOS E CAOS
            'lyapunov': 'expoente_caos', 'attractor': 'atrator', 'chaos': 'caos',
            'bifurcation': 'bifurcacao', 'entropy_': 'entropia', 'hurst': 'expoente_hurst',
            
            # 📐 GEOMETRIA DIFERENCIAL
            'curvature': 'curvatura', 'riemann': 'metric_riemann', 'metric_': 'metrica',
            'manifold': 'variedade', 'tensor': 'tensor', 'christoffel': 'simbolo_christoffel',
            
            # 🧮 ÁLGEBRA CATEGÓRICA
            'functor': 'funtor', 'monoid': 'monoide', 'category': 'categoria',
            'natural_transformation': 'transformacao_natural', 'morphism': 'morfismo',
            
            # 📏 TEORIA DA MEDIDA
            'lebesgue': 'medida_lebesgue', 'radon': 'derivada_radon', 'hausdorff': 'dimensao_hausdorff',
            'measure': 'medida', 'borel': 'conjunto_borel', 'sigma': 'algebra_sigma',
            
            # 🔬 ANÁLISE FUNCIONAL
            'sobolev': 'norma_sobolev', 'spectral_radius': 'raio_espectral', 'operator': 'operador',
            'banach': 'espaco_banach', 'hilbert': 'espaco_hilbert', 'functional': 'funcional',
            
            # ⚛️ INFORMAÇÃO QUÂNTICA
            'quantum_entropy': 'entropia_quantica', 'von_neumann': 'entropia_von_neumann',
            'entanglement': 'emaranhamento', 'quantum': 'quantico', 'qubit': 'qubit',
            
            # 🎯 TEORIA DOS NÚMEROS COMPUTACIONAL
            'factorization': 'fatoracao', 'pollard': 'pollard_rho', 'elliptic_curve': 'curva_eliptica',
            'prime_test': 'teste_primalidade', 'discrete_log': 'logaritmo_discreto',
            
            # 📊 SINAIS NÃO-LINEARES
            'teager': 'energia_teager', 'higher_moment': 'momento_superior', 'bispectrum': 'bispectro',
            'nonlinear': 'nao_linear', 'higher_order': 'ordem_superior',
            
            # ❄️ GEOMETRIA FRACTAL
            'fractal_dimension': 'dimensao_fractal', 'multifractal': 'multifractal',
            'lacunarity': 'lacunaridade', 'hurst_exponent': 'expoente_hurst',
            'box_counting': 'contagem_caixas'
        }
        
        # Matriz de compatibilidade entre tipos
        self.compatibilidade = {
            'vetor': ['vetor', 'espectro', 'matriz', 'sequencia', 'escalar'],
            'espectro': ['espectro', 'vetor', 'escalar'],
            'matriz': ['matriz', 'vetor', 'escalar', 'autovalor'],
            'sequencia': ['sequencia', 'vetor', 'escalar'],
            'escalar': ['escalar', 'vetor', 'inteiro', 'float'],
            'inteiro': ['inteiro', 'escalar', 'float'],
            'float': ['float', 'escalar', 'inteiro'],
            'booleano': ['booleano', 'inteiro'],
            'correlacao': ['correlacao', 'escalar'],
            'similaridade': ['similaridade', 'escalar'],
            'distancia': ['distancia', 'escalar'],
            'autovalor': ['autovalor', 'vetor', 'escalar'],
            
            # 🆕 COMPATIBILIDADES AVANÇADAS
            'expoente_caos': ['expoente_caos', 'escalar', 'float'],
            'atrator': ['atrator', 'vetor', 'matriz'],
            'curvatura': ['curvatura', 'escalar', 'tensor'],
            'metric_riemann': ['metric_riemann', 'matriz', 'tensor'],
            'funtor': ['funtor', 'transformacao', 'categoria'],
            'monoide': ['monoide', 'algebra', 'estrutura'],
            'medida_lebesgue': ['medida_lebesgue', 'escalar', 'funcao'],
            'dimensao_hausdorff': ['dimensao_hausdorff', 'escalar', 'fractal'],
            'norma_sobolev': ['norma_sobolev', 'escalar', 'funcao'],
            'raio_espectral': ['raio_espectral', 'escalar', 'autovalor'],
            'entropia_quantica': ['entropia_quantica', 'escalar', 'quantico'],
            'emaranhamento': ['emaranhamento', 'escalar', 'quantico'],
            'fatoracao': ['fatoracao', 'inteiro', 'lista_inteiros'],
            'energia_teager': ['energia_teager', 'escalar', 'vetor'],
            'dimensao_fractal': ['dimensao_fractal', 'escalar', 'fractal'],
            'multifractal': ['multifractal', 'espectro', 'fractal']
        }
    
    def categorizar_funcao(self, nome_funcao: str) -> str:
        """
        Categoriza função baseada no nome e assinatura
        """
        # Primeiro verificar categorias avançadas
        categorias_avancadas = {
            'sistemas_dinamicos': ['lyapunov', 'attractor', 'chaos', 'bifurcation', 'hurst'],
            'geometria_diferencial': ['curvature', 'riemann', 'christoffel', 'manifold', 'tensor'],
            'algebra_categórica': ['functor', 'monoid', 'category', 'morphism', 'natural'],
            'teoria_medida': ['lebesgue', 'radon', 'hausdorff', 'measure', 'borel'],
            'analise_funcional': ['sobolev', 'spectral_radius', 'operator', 'banach', 'hilbert'],
            'informacao_quantica': ['quantum_entropy', 'von_neumann', 'entanglement', 'qubit'],
            'teoria_numeros_computacional': ['factorization', 'pollard', 'elliptic_curve', 'prime_test'],
            'sinais_nao_lineares': ['teager', 'higher_moment', 'bispectrum', 'nonlinear'],
            'geometria_fractal': ['fractal_dimension', 'multifractal', 'lacunarity', 'box_counting']
        }
        
        for categoria, palavras_chave in categorias_avancadas.items():
            if any(palavra in nome_funcao.lower() for palavra in palavras_chave):
                return categoria
        
        # Depois tentar por padrões de nome básicos
        for padrao, categoria in self.padroes_tipo.items():
            if nome_funcao.startswith(padrao) or padrao in nome_funcao:
                return categoria
        
        # Tentar inferir pela assinatura
        try:
            if hasattr(self.wrapper, nome_funcao):
                metodo = getattr(self.wrapper, nome_funcao)
                assinatura = inspect.signature(metodo)
                parametros = list(assinatura.parameters.values())
                
                # Nova lógica para detectar funções avançadas
                param_names = [p.name.lower() for p in parametros]
                
                if any(name in param_names for name in ['quantum', 'qubit', 'entanglement']):
                    return 'informacao_quantica'
                elif any(name in param_names for name in ['manifold', 'curvature', 'metric']):
                    return 'geometria_diferencial'
                elif any(name in param_names for name in ['fractal', 'dimension', 'hurst']):
                    return 'geometria_fractal'
                elif any(name in param_names for name in ['lyapunov', 'attractor', 'chaos']):
                    return 'sistemas_dinamicos'
                elif any(name in param_names for name in ['measure', 'lebesgue', 'borel']):
                    return 'teoria_medida'
                
                # Lógica original para categorias básicas
                if len(parametros) == 0:
                    return 'constante'
                elif len(parametros) == 1:
                    param_name = parametros[0].name.lower()
                    if any(word in param_name for word in ['matrix', 'mat']):
                        return 'matriz'
                    elif any(word in param_name for word in ['vector', 'vec', 'array']):
                        return 'vetor'
                    elif any(word in param_name for word in ['seq', 'series', 'time']):
                        return 'sequencia'
                    else:
                        return 'transformacao_simples'
                else:
                    return 'operacao'
                    
        except (ValueError, TypeError) as e:
            logger.debug(f"Erro ao analisar assinatura de {nome_funcao}: {e}")
        
        # Fallback
        return 'geral'
    
    def obter_tipo_saida(self, nome_funcao: str) -> str:
        """
        Inferir tipo de saída baseado no nome e comportamento
        """
        if nome_funcao in self.cache_tipos:
            return self.cache_tipos[nome_funcao]
        
        # Inferir do nome usando padrões
        for padrao, tipo in self.padroes_tipo.items():
            if nome_funcao.startswith(padrao) or padrao in nome_funcao:
                self.cache_tipos[nome_funcao] = tipo
                return tipo
        
        # Padrões específicos por sufixo/palavras-chave
        if any(palavra in nome_funcao for palavra in ['count', 'length', 'size', 'num', 'total']):
            tipo = 'inteiro'
        elif any(palavra in nome_funcao for palavra in ['mean', 'average', 'std', 'variance', 'skew', 'kurtosis']):
            tipo = 'escalar'
        elif any(palavra in nome_funcao for palavra in ['matrix', 'mat']):
            tipo = 'matriz'
        elif any(palavra in nome_funcao for palavra in ['vector', 'array']):
            tipo = 'vetor'
        elif nome_funcao.startswith('is_') or nome_funcao.startswith('has_'):
            tipo = 'booleano'
        elif any(palavra in nome_funcao for palavra in ['ratio', 'rate', 'probability']):
            tipo = 'float'
        else:
            tipo = 'escalar'  # Fallback mais comum
        
        self.cache_tipos[nome_funcao] = tipo
        return tipo
    
    def obter_tipo_entrada(self, nome_funcao: str) -> str:
        """
        Inferir tipo de entrada necessário
        """
        # Padrões baseados no nome
        if any(palavra in nome_funcao for palavra in ['matrix', 'mat_']):
            return 'matriz'
        elif any(palavra in nome_funcao for palavra in ['vector', 'array']):
            return 'vetor'
        elif any(palavra in nome_funcao for palavra in ['fft', 'dct', 'fourier', 'spectral']):
            return 'vetor'
        elif any(palavra in nome_funcao for palavra in ['correlation', 'covariance', 'similarity']):
            return 'vetor'
        elif any(palavra in nome_funcao for palavra in ['sequence', 'subsequence', 'series']):
            return 'sequencia'
        elif any(palavra in nome_funcao for palavra in ['prime', 'gcd', 'lcm']):
            return 'inteiro'
        else:
            return 'vetor'  # Fallback mais comum
    
    def sao_compatíveis(self, tipo_saida: str, nome_funcao_destino: str) -> bool:
        """
        Verifica se o tipo de saída é compatível com a função destino
        """
        tipo_entrada_necessario = self.obter_tipo_entrada(nome_funcao_destino)
        
        # Verificar compatibilidade direta
        if tipo_entrada_necessario in self.compatibilidade.get(tipo_saida, []):
            return True
        
        # Verificar compatibilidade reversa
        if tipo_saida in self.compatibilidade.get(tipo_entrada_necessario, []):
            return True
        
        # Compatibilidades especiais
        compatibilidades_especiais = {
            ('escalar', 'vetor'): True,    # Escalar pode ser aplicado a vetor
            ('inteiro', 'vetor'): True,    # Inteiro pode ser usado como índice
            ('float', 'vetor'): True,      # Float pode ser aplicado a vetor
            ('booleano', 'vetor'): True,   # Booleano para filtragem
        }
        
        return compatibilidades_especiais.get((tipo_saida, tipo_entrada_necessario), False)


class GeradorLogicasEscalavel:
    def __init__(self, wrapper=None):
        self.wrapper = wrapper or UniversalWrapper()
        self.analisador_tipos = AnalisadorTiposFuncoes(self.wrapper)
        self.categorias_dinamicas = self._categorizar_funcoes_dinamicamente()
        self.logicas_avaliadas = []
        self.cache_validacao = {}
        
        logger.info(f"✅ Gerador inicializado com {len(self._obter_todas_funcoes())} funções disponíveis")
    
    def _obter_todas_funcoes(self) -> List[str]:
        """
        Obtém automaticamente todas as funções do wrapper
        """
        funcoes = []
        for attr_name in dir(self.wrapper):
            if not attr_name.startswith('_') and callable(getattr(self.wrapper, attr_name)):
                funcoes.append(attr_name)
        return funcoes
    
    def _categorizar_funcoes_dinamicamente(self) -> Dict[str, List[str]]:
        """
        Categoriza automaticamente todas as funções disponíveis
        """
        todas_funcoes = self._obter_todas_funcoes()
        categorias = {}
        
        for funcao in todas_funcoes:
            categoria = self.analisador_tipos.categorizar_funcao(funcao)
            
            if categoria not in categorias:
                categorias[categoria] = []
            
            categorias[categoria].append(funcao)
        
        # Log estatísticas
        for cat, funcoes in categorias.items():
            logger.info(f"📁 Categoria '{cat}': {len(funcoes)} funções")
        
        logger.info(f"📊 Total: {len(todas_funcoes)} funções em {len(categorias)} categorias")
        return categorias
    
    def _gerar_dados_teste(self, tipo: str = "vetor", tamanho: int = 100) -> Any:
        """
        Gera dados de teste para validação das lógicas
        """
        if tipo == "vetor":
            return [random.uniform(-10, 10) for _ in range(tamanho)]
        elif tipo == "inteiro":
            return [random.randint(1, 100) for _ in range(tamanho)]
        elif tipo == "matriz":
            size = int(np.sqrt(tamanho)) if tamanho > 9 else 3
            return [[random.uniform(-5, 5) for _ in range(size)] for _ in range(size)]
        elif tipo == "sequencia_temporal":
            tendencia = [i * 0.1 for i in range(tamanho)]
            ruido = [random.gauss(0, 0.5) for _ in range(tamanho)]
            return [t + r for t, r in zip(tendencia, ruido)]
        elif tipo == "escalar":
            return random.uniform(-100, 100)
        elif tipo == "quantico":  # 🆕 Dados quânticos simulados
            return [complex(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(tamanho)]
        elif tipo == "fractal":   # 🆕 Dados fractais simulados
            return self._gerar_sequencia_fractal(tamanho)
        else:
            return [random.random() for _ in range(tamanho)]
    
    def _gerar_sequencia_fractal(self, tamanho: int) -> List[float]:
        """Gera uma sequência com propriedades fractais"""
        # Sequência simples com auto-similaridade
        sequencia = [random.uniform(-1, 1)]
        for i in range(1, tamanho):
            # Adicionar dependência fractal
            prev = sequencia[i-1]
            sequencia.append(prev * 0.7 + random.gauss(0, 0.3))
        return sequencia
    
    def gerar_logica_inteligente(self, 
                               objetivo: str = None,
                               comprimento: Tuple[int, int] = (3, 7)) -> List[str]:
        """
        Gera lógicas inteligentes baseadas em objetivo e compatibilidade
        """
        comprimento_alvo = random.randint(comprimento[0], comprimento[1])
        
        if objetivo:
            return self._gerar_logica_orientada_objetivo(objetivo, comprimento_alvo)
        else:
            return self._gerar_logica_por_compatibilidade(comprimento_alvo)
    
    def _gerar_logica_por_compatibilidade(self, comprimento: int) -> List[str]:
        """
        Gera lógica baseada em compatibilidade de tipos entre funções
        """
        tentativas_max = 50
        for tentativa in range(tentativas_max):
            try:
                logica = []
                
                # Começar com função aleatória
                funcao_inicial = self._escolher_funcao_inicial()
                logica.append(funcao_inicial)
                
                tipo_atual = self.analisador_tipos.obter_tipo_saida(funcao_inicial)
                
                # Construir cadeia compatível
                while len(logica) < comprimento and len(logica) < 10:  # Limite de segurança
                    proxima_funcao = self._encontrar_funcao_compativel(tipo_atual, logica)
                    
                    if proxima_funcao:
                        logica.append(proxima_funcao)
                        tipo_atual = self.analisador_tipos.obter_tipo_saida(proxima_funcao)
                    else:
                        # Tentar quebrar a cadeia com nova função
                        nova_funcao = self._escolher_funcao_inicial()
                        if nova_funcao not in logica:
                            logica.append(nova_funcao)
                            tipo_atual = self.analisador_tipos.obter_tipo_saida(nova_funcao)
                
                if len(logica) >= 3:  # Mínimo para ser útil
                    logger.info(f"🔗 Lógica compatível gerada ({len(logica)} funções): {' → '.join(logica[:5])}{'...' if len(logica) > 5 else ''}")
                    return logica
                    
            except Exception as e:
                logger.debug(f"Tentativa {tentativa + 1} falhou: {e}")
                continue
        
        # Fallback: lógica aleatória simples
        return self._gerar_logica_aleatoria_fallback(comprimento)
    
    def _escolher_funcao_inicial(self) -> str:
        """Escolhe uma função inicial com boa probabilidade de sucesso"""
        categorias_iniciais = ['vetor', 'espectro', 'sequencia', 'transformacao_simples']
        candidatas = []
        
        for cat in categorias_iniciais:
            if cat in self.categorias_dinamicas:
                candidatas.extend(self.categorias_dinamicas[cat])
        
        return random.choice(candidatas) if candidatas else random.choice(self._obter_todas_funcoes())
    
    def _encontrar_funcao_compativel(self, tipo_entrada: str, logica_existente: List[str]) -> Optional[str]:
        """
        Encontra função compatível com o tipo de entrada atual
        """
        candidatas = []
        
        # Priorizar funções da mesma "família" avançada
        familias_avancadas = {
            'sistemas_dinamicos': ['sistemas_dinamicos', 'geometria_fractal', 'caos'],
            'geometria_diferencial': ['geometria_diferencial', 'algebra_categórica', 'tensor'],
            'informacao_quantica': ['informacao_quantica', 'entropia', 'quantico'],
            'teoria_medida': ['teoria_medida', 'analise_funcional', 'medida']
        }
        
        # Primeiro tentar funções da mesma família
        for familia, categorias in familias_avancadas.items():
            if any(cat in tipo_entrada for cat in categorias):
                for cat in categorias:
                    if cat in self.categorias_dinamicas:
                        for funcao in self.categorias_dinamicas[cat]:
                            if (funcao not in logica_existente and 
                                hasattr(self.wrapper, funcao) and
                                self.analisador_tipos.sao_compatíveis(tipo_entrada, funcao)):
                                candidatas.append(funcao)
        
        # Se não encontrou na mesma família, buscar em todas
        if not candidatas:
            for categoria, funcoes in self.categorias_dinamicas.items():
                for funcao in funcoes:
                    if (funcao not in logica_existente and 
                        hasattr(self.wrapper, funcao) and
                        self.analisador_tipos.sao_compatíveis(tipo_entrada, funcao)):
                        candidatas.append(funcao)
        
        return random.choice(candidatas) if candidatas else None
    
    def _gerar_logica_orientada_objetivo(self, objetivo: str, comprimento: int) -> List[str]:
        """
        Gera lógica específica para um objetivo
        """
        objetivos_predefinidos = {
            # Objetivos básicos
            'analise_series_temporais': {
                'categorias_prioritarias': ['espectro', 'sequencia', 'escalar'],
                'funcoes_obrigatorias': ['fft_magnitude', 'mean', 'std_dev'],
            },
            'processamento_imagem': {
                'categorias_prioritarias': ['matriz', 'vetor', 'transformacao'],
                'funcoes_obrigatorias': ['matrix_determinant', 'vector_norm'],
            },
            'analise_estatistica': {
                'categorias_prioritarias': ['escalar', 'correlacao', 'similaridade'],
                'funcoes_obrigatorias': ['mean', 'std_dev', 'pearson_correlation'],
            },
            'mineracao_texto': {
                'categorias_prioritarias': ['vetor', 'similaridade', 'sequencia'],
                'funcoes_obrigatorias': ['cosine_similarity', 'vector_norm'],
            },
            
            # 🆕 OBJETIVOS AVANÇADOS
            'sistemas_caoticos': {
                'categorias_prioritarias': ['sistemas_dinamicos', 'geometria_fractal', 'escalar'],
                'funcoes_obrigatorias': ['lyapunov_exponent', 'correlation_dimension', 'hurst_exponent'],
            },
            'geometria_avancada': {
                'categorias_prioritarias': ['geometria_diferencial', 'algebra_categórica', 'tensor'],
                'funcoes_obrigatorias': ['riemann_curvature', 'manifold_distance', 'tensor_contract'],
            },
            'analise_funcional': {
                'categorias_prioritarias': ['analise_funcional', 'teoria_medida', 'operador'],
                'funcoes_obrigatorias': ['sobolev_norm', 'spectral_radius', 'operator_norm'],
            },
            'informacao_quantica': {
                'categorias_prioritarias': ['informacao_quantica', 'entropia', 'emaranhamento'],
                'funcoes_obrigatorias': ['von_neumann_entropy', 'quantum_fidelity', 'entanglement_measure'],
            },
            'criptografia_avancada': {
                'categorias_prioritarias': ['teoria_numeros_computacional', 'algebra', 'primalidade'],
                'funcoes_obrigatorias': ['rsa_factorization', 'elliptic_curve_discrete_log', 'prime_test'],
            },
            'processamento_nao_linear': {
                'categorias_prioritarias': ['sinais_nao_lineares', 'estatistica_avancada', 'espectro'],
                'funcoes_obrigatorias': ['teager_energy', 'higher_order_moments', 'bispectral_analysis'],
            },
            'analise_fractal': {
                'categorias_prioritarias': ['geometria_fractal', 'dimensao', 'multifractal'],
                'funcoes_obrigatorias': ['fractal_dimension', 'multifractal_spectrum', 'lacunarity_measure'],
            }
        }
        
        config = objetivos_predefinidos.get(objetivo, {})
        categorias_prioritarias = config.get('categorias_prioritarias', [])
        funcoes_obrigatorias = [f for f in config.get('funcoes_obrigatorias', []) 
                               if hasattr(self.wrapper, f)]
        
        logica = funcoes_obrigatorias.copy()
        
        # Preencher com funções das categorias prioritárias
        while len(logica) < comprimento and len(logica) < 15:
            if categorias_prioritarias:
                categoria = random.choice(categorias_prioritarias)
                if categoria in self.categorias_dinamicas:
                    # Escolher função que existe no wrapper
                    funcoes_validas = [f for f in self.categorias_dinamicas[categoria] 
                                     if hasattr(self.wrapper, f)]
                    if funcoes_validas:
                        funcao = random.choice(funcoes_validas)
                        if funcao not in logica:
                            logica.append(funcao)
            else:
                # Fallback para função aleatória existente
                todas_funcoes = [f for f in self._obter_todas_funcoes() if hasattr(self.wrapper, f)]
                if todas_funcoes:
                    funcao = random.choice(todas_funcoes)
                    if funcao not in logica:
                        logica.append(funcao)
        
        logger.info(f"🎯 Lógica para '{objetivo}': {' → '.join(logica[:5])}{'...' if len(logica) > 5 else ''}")
        return logica
    
    def _gerar_logica_aleatoria_fallback(self, comprimento: int) -> List[str]:
        """Fallback para geração de lógica aleatória"""
        todas_funcoes = self._obter_todas_funcoes()
        logica = random.sample(todas_funcoes, min(comprimento, len(todas_funcoes)))
        logger.info(f"🎲 Lógica aleatória fallback: {' → '.join(logica[:5])}...")
        return logica
    
    def executar_logica(self, logica: List[str], dados: Any) -> Any:
        """
        Executa uma sequência de funções nos dados
        """
        if not logica:
            return dados
        
        resultado = dados
        
        for i, funcao in enumerate(logica):
            try:
                if hasattr(self.wrapper, funcao):
                    metodo = getattr(self.wrapper, funcao)
                    
                    # Executar função
                    if isinstance(resultado, (list, tuple)) and len(resultado) > 0:
                        resultado = metodo(resultado)
                    else:
                        resultado = metodo([resultado]) if isinstance(resultado, (int, float)) else metodo(resultado)
                        
                else:
                    logger.warning(f"⚠️ Função {funcao} não encontrada")
                    return None
                    
            except Exception as e:
                logger.error(f"❌ Erro em {funcao} (posição {i+1}): {e}")
                return None
        
        return resultado
    
    def avaliar_logica(self, logica: List[str], num_testes: int = 5) -> Dict[str, Any]:
        """
        Avalia a performance de uma lógica
        """
        cache_key = tuple(logica)
        if cache_key in self.cache_validacao:
            return self.cache_validacao[cache_key]
        
        # Gerar dados de teste variados
        dados_teste = [
            self._gerar_dados_teste("vetor", 50),
            self._gerar_dados_teste("sequencia_temporal", 30),
            self._gerar_dados_teste("matriz", 16),
            self._gerar_dados_teste("inteiro", 20),
            self._gerar_dados_teste("escalar")
        ][:num_testes]
        
        resultados = []
        tempos_execucao = []
        sucessos = 0
        
        for dados in dados_teste:
            try:
                inicio = time.time()
                resultado = self.executar_logica(logica, dados)
                fim = time.time()
                
                if resultado is not None:
                    resultados.append(resultado)
                    tempos_execucao.append(fim - inicio)
                    sucessos += 1
                    
            except Exception as e:
                logger.debug(f"Teste falhou: {e}")
                continue
        
        # Métricas de avaliação
        taxa_sucesso = sucessos / len(dados_teste) if dados_teste else 0
        tempo_medio = np.mean(tempos_execucao) if tempos_execucao else float('inf')
        
        # Diversidade de resultados
        if resultados:
            try:
                resultados_flat = []
                for r in resultados:
                    if isinstance(r, (list, tuple)):
                        resultados_flat.extend(r)
                    else:
                        resultados_flat.append(r)
                diversidade = np.std(resultados_flat) if len(resultados_flat) > 1 else 0
            except:
                diversidade = 0
        else:
            diversidade = 0
        
        # Score composto
        score = (
            taxa_sucesso * 0.5 +
            (1 / (1 + min(tempo_medio, 10))) * 0.3 +
            min(diversidade / 10, 1) * 0.2
        )
        
        avaliacao = {
            'logica': logica,
            'score': float(score),
            'taxa_sucesso': float(taxa_sucesso),
            'tempo_medio': float(tempo_medio),
            'diversidade_resultados': float(diversidade),
            'num_funcoes': len(logica),
            'resultados_amostra': str(resultados[:2]) if resultados else "Nenhum"
        }
        
        self.cache_validacao[cache_key] = avaliacao
        return avaliacao
    
    def evoluir_logicas(self, 
                       tamanho_populacao: int = 30,
                       geracoes: int = 20,
                       taxa_mutacao: float = 0.15) -> List[Dict[str, Any]]:
        """
        Algoritmo genético para evoluir lógicas performantes (otimizado)
        """
        logger.info(f"🧬 Iniciando evolução: {tamanho_populacao} lógicas, {geracoes} gerações")
        
        # População inicial diversificada
        populacao = []
        while len(populacao) < tamanho_populacao:
            logica = self.gerar_logica_inteligente()
            if logica and logica not in [p['logica'] for p in populacao]:
                avaliacao = self.avaliar_logica(logica)
                populacao.append(avaliacao)
        
        for geracao in range(geracoes):
            # Ordenar por score
            populacao.sort(key=lambda x: x['score'], reverse=True)
            
            # Log do progresso
            if geracao % 5 == 0:
                logger.info(f"📈 Geração {geracao}: Melhor score = {populacao[0]['score']:.3f}")
            
            # Nova população (elitismo + offspring)
            nova_populacao = populacao[:max(5, tamanho_populacao // 6)]
            
            while len(nova_populacao) < tamanho_populacao:
                # Seleção por torneio
                pai1 = self._torneio_selecao(populacao)
                pai2 = self._torneio_selecao(populacao)
                
                # Crossover
                filho_logica = self._crossover(pai1['logica'], pai2['logica'])
                
                # Mutação
                if random.random() < taxa_mutacao:
                    filho_logica = self._mutar(filho_logica)
                
                # Avaliar e adicionar
                if filho_logica:
                    avaliacao_filho = self.avaliar_logica(filho_logica)
                    nova_populacao.append(avaliacao_filho)
            
            populacao = nova_populacao
        
        # Retornar as melhores
        populacao.sort(key=lambda x: x['score'], reverse=True)
        logger.info(f"🏆 Evolução completa. Melhor score final: {populacao[0]['score']:.3f}")
        
        return populacao[:10]
    
    def _torneio_selecao(self, populacao: List[Dict], tamanho_torneio: int = 3) -> Dict:
        """Seleção por torneio"""
        participantes = random.sample(populacao, min(tamanho_torneio, len(populacao)))
        return max(participantes, key=lambda x: x['score'])
    
    def _crossover(self, logica1: List[str], logica2: List[str]) -> List[str]:
        """Combina duas lógicas"""
        if len(logica1) < 2 or len(logica2) < 2:
            return logica1 or logica2
        
        ponto = random.randint(1, min(len(logica1), len(logica2)) - 1)
        filho = logica1[:ponto] + logica2[ponto:]
        
        # Remover duplicados mantendo ordem
        seen = set()
        return [x for x in filho if not (x in seen or seen.add(x))]
    
    def _mutar(self, logica: List[str]) -> List[str]:
        """Aplica mutação em uma lógica"""
        if len(logica) < 2:
            return logica
        
        operacao = random.choice(['adicionar', 'remover', 'substituir', 'reordenar'])
        
        if operacao == 'adicionar' and len(logica) < 8:
            nova_funcao = self._escolher_funcao_inicial()
            if nova_funcao not in logica:
                logica.insert(random.randint(0, len(logica)), nova_funcao)
                
        elif operacao == 'remover' and len(logica) > 2:
            logica.pop(random.randint(0, len(logica) - 1))
            
        elif operacao == 'substituir':
            idx = random.randint(0, len(logica) - 1)
            nova_funcao = self._escolher_funcao_inicial()
            if nova_funcao not in logica:
                logica[idx] = nova_funcao
                
        elif operacao == 'reordenar' and len(logica) > 2:
            random.shuffle(logica)
        
        return logica
    
    def salvar_logicas(self, arquivo: str = "logicas_otimizadas.json"):
        """Salva as lógicas avaliadas"""
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.logicas_avaliadas, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 {len(self.logicas_avaliadas)} lógicas salvas em {arquivo}")
    
    def carregar_logicas(self, arquivo: str = "logicas_otimizadas.json"):
        """Carrega lógicas de arquivo"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                self.logicas_avaliadas = json.load(f)
            logger.info(f"📂 {len(self.logicas_avaliadas)} lógicas carregadas")
        except FileNotFoundError:
            logger.warning(f"Arquivo {arquivo} não encontrado")


# Funções de demonstração
def demonstrar_escalabilidade():
    print("🚀 GERADOR DE LÓGICAS ESCALÁVEL - DEMONSTRAÇÃO")
    print("=" * 50)
    
    try:
        gerador = GeradorLogicasEscalavel()
        
        print(f"📊 Sistema inicializado com {len(gerador._obter_todas_funcoes())} funções")
        print(f"🎯 {len(gerador.categorias_dinamicas)} categorias dinâmicas detectadas")
        
        # Testar diferentes tipos de geração
        print("\n1. 🔧 GERANDO LÓGICAS INTELIGENTES:")
        
        # Lógica por compatibilidade
        logica_auto = gerador.gerar_logica_inteligente()
        print(f"   🤖 Automática: {' → '.join(logica_auto)}")
        
        # Lógica orientada a objetivo
        objetivos = ['analise_series_temporais', 'analise_estatistica']
        for objetivo in objetivos:
            logica_obj = gerador.gerar_logica_inteligente(objetivo=objetivo)
            print(f"   🎯 {objetivo}: {' → '.join(logica_obj[:5])}...")
        
        print("\n2. 🧪 TESTANDO EXECUÇÃO:")
        dados_teste = gerador._gerar_dados_teste("vetor", 10)
        resultado = gerador.executar_logica(logica_auto[:3], dados_teste)  # Testar com 3 funções
        print(f"   Dados: {dados_teste[:5]}...")
        print(f"   Resultado: {resultado}")
        
        print("\n3. 📈 AVALIANDO LÓGICA:")
        avaliacao = gerador.avaliar_logica(logica_auto[:4])  # Avaliar com 4 funções
        print(f"   Score: {avaliacao['score']:.3f}")
        print(f"   Sucesso: {avaliacao['taxa_sucesso']:.1%}")
        print(f"   Tempo: {avaliacao['tempo_medio']:.4f}s")
        
        print("\n4. 🧬 EVOLUÇÃO RÁPIDA (mini-demo):")
        melhores = gerador.evoluir_logicas(tamanho_populacao=8, geracoes=3)
        
        print("\n🏆 MELHORES LÓGICAS:")
        for i, logica_av in enumerate(melhores[:2]):
            print(f"   {i+1}. Score {logica_av['score']:.3f}: {' → '.join(logica_av['logica'][:4])}...")
        
        print(f"\n✅ DEMONSTRAÇÃO CONCLUÍDA!")
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()

def demonstrar_dominios_avancados():
    """
    Demonstra o gerador com as novas categorias avançadas
    """
    print("🧠 GERADOR AVANÇADO - DOMÍNIOS COMPLEXOS")
    print("=" * 55)
    
    try:
        gerador = GeradorLogicasEscalavel()
        
        print("🎯 OBJETIVOS AVANÇADOS DISPONÍVEIS:")
        objetivos_avancados = [
            'sistemas_caoticos',
            'geometria_avancada', 
            'analise_funcional',
            'informacao_quantica',
            'criptografia_avancada',
            'processamento_nao_linear',
            'analise_fractal'
        ]
        
        for objetivo in objetivos_avancados:
            print(f"\n🔬 {objetivo.upper().replace('_', ' ')}:")
            logica = gerador.gerar_logica_inteligente(objetivo=objetivo)
            
            if logica:
                # Agrupar por categoria para análise
                categorias_na_logica = {}
                for funcao in logica:
                    cat = gerador.analisador_tipos.categorizar_funcao(funcao)
                    if cat not in categorias_na_logica:
                        categorias_na_logica[cat] = []
                    categorias_na_logica[cat].append(funcao)
                
                print(f"   📋 Lógica ({len(logica)} funções):")
                for cat, funcoes in categorias_na_logica.items():
                    print(f"      {cat}: {', '.join(funcoes[:3])}{'...' if len(funcoes) > 3 else ''}")
                
                # Avaliação rápida
                avaliacao = gerador.avaliar_logica(logica[:4])  # Testar com primeiras 4
                print(f"   📊 Score: {avaliacao['score']:.3f} | Sucesso: {avaliacao['taxa_sucesso']:.1%}")
            else:
                print("   ⚠️ Não foi possível gerar lógica para este objetivo")
        
        print(f"\n✅ Demonstração de domínios avançados concluída!")
        
    except Exception as e:
        print(f"❌ Erro na demonstração avançada: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 GERADOR DE LÓGICAS - VERSÃO AVANÇADA")
    print("Escalável para 800+ funções com domínios complexos")
    print("=" * 60)
    
    # Executar demonstrações
    demonstrar_escalabilidade()
    print("\n" + "="*60)
    demonstrar_dominios_avancados()
