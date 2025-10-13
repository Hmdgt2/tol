# lib/gerador_heuristicas_dinamicas.py
"""
SISTEMA DE HEURÍSTICAS DINÂMICAS
Substitui heurísticas fixas por lógicas geradas automaticamente
"""

import os
import sys
import json
import numpy as np
from typing import List, Dict, Any, Set
from collections import Counter
from lib.gerador_logicas_ultra import GeradorLogicasEscalavelUltra
from universal_wrapper import UniversalWrapper

class HeuristicaDinamica:
    """Classe base para heurísticas dinâmicas geradas automaticamente"""
    
    def __init__(self, nome: str, logica: List[str], descricao: str, dependencias: Set[str]):
        self.NOME = nome
        self.DESCRICAO = descricao
        self.DEPENDENCIAS = dependencias
        self.logica = logica
        self.wrapper = UniversalWrapper()
        
    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Executa a lógica dinâmica nas estatísticas para gerar previsões
        """
        try:
            # Converter estatísticas em formato adequado para as funções
            dados_entrada = self._preparar_dados_entrada(estatisticas)
            
            # Executar a cadeia de funções
            resultado = dados_entrada
            for funcao in self.logica:
                if hasattr(self.wrapper, funcao):
                    resultado = getattr(self.wrapper, funcao)(resultado)
                else:
                    # Fallback para funções não encontradas
                    resultado = self._funcao_fallback(funcao, resultado)
            
            # Converter resultado em números de 1-49
            numeros_previstos = self._extrair_numeros_previsao(resultado, n)
            return numeros_previstos
            
        except Exception as e:
            print(f"Erro na heurística {self.NOME}: {e}")
            return []
    
    def _preparar_dados_entrada(self, estatisticas: Dict[str, Any]) -> List[float]:
        """
        Prepara os dados de entrada a partir das estatísticas disponíveis
        """
        dados = []
        
        # Extrair valores numéricos das estatísticas
        for dep in self.DEPENDENCIAS:
            if dep in estatisticas:
                valor = estatisticas[dep]
                dados.extend(self._extrair_valores_numericos(valor))
        
        # Se não encontrou dados suficientes, usar fallback
        if len(dados) < 5:
            dados = list(range(1, 50))  # Todos os números possíveis
            
        return dados[:100]  # Limitar tamanho para performance
    
    def _extrair_valores_numericos(self, obj: Any) -> List[float]:
        """Extrai valores numéricos de diferentes estruturas de dados"""
        valores = []
        
        if isinstance(obj, (int, float)):
            valores.append(float(obj))
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                valores.extend(self._extrair_valores_numericos(item))
        elif isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(key, (int, float)):
                    valores.append(float(key))
                valores.extend(self._extrair_valores_numericos(value))
        elif isinstance(obj, Counter):
            valores.extend([float(k) for k in obj.keys() if isinstance(k, (int, float))])
            valores.extend([float(v) for v in obj.values() if isinstance(v, (int, float))])
        
        return [v for v in valores if 1 <= v <= 49 or 0 < v < 100]
    
    def _funcao_fallback(self, nome_funcao: str, dados: List[float]) -> List[float]:
        """Fallback para funções não implementadas"""
        fallbacks = {
            'mean': lambda x: [np.mean(x)] if x else [0],
            'sum': lambda x: [sum(x)] if x else [0],
            'max': lambda x: [max(x)] if x else [0],
            'min': lambda x: [min(x)] if x else [0],
            'std': lambda x: [np.std(x)] if len(x) > 1 else [0],
        }
        
        if nome_funcao in fallbacks:
            return fallbacks[nome_funcao](dados)
        else:
            return dados  # Retorna os dados sem modificação
    
    def _extrair_numeros_previsao(self, resultado: Any, n: int = 5) -> List[int]:
        """
        Converte o resultado das funções em números de loteria (1-49)
        """
        try:
            numeros = []
            
            # Diferentes tipos de resultado
            if isinstance(resultado, (int, float)):
                num = int(round(resultado))
                if 1 <= num <= 49:
                    numeros.append(num)
                    
            elif isinstance(resultado, (list, tuple)):
                for item in resultado:
                    if isinstance(item, (int, float)):
                        num = int(round(item))
                        if 1 <= num <= 49 and num not in numeros:
                            numeros.append(num)
                    elif isinstance(item, (list, tuple)):
                        numeros.extend(self._extrair_numeros_previsao(item, n))
            
            # Garantir que temos números únicos entre 1-49
            numeros = [n for n in numeros if 1 <= n <= 49]
            numeros = list(dict.fromkeys(numeros))  # Remover duplicatas mantendo ordem
            
            # Se não temos números suficientes, completar aleatoriamente
            while len(numeros) < n and len(numeros) < 49:
                for num in range(1, 50):
                    if num not in numeros:
                        numeros.append(num)
                    if len(numeros) >= n:
                        break
            
            return numeros[:n]
            
        except Exception:
            # Fallback: números aleatórios
            return list(np.random.choice(range(1, 50), size=n, replace=False))

class GeradorHeuristicasDinamicas:
    """
    Gerencia a criação e evolução de heurísticas dinâmicas
    """
    
    def __init__(self):
        self.gerador_logicas = GeradorLogicasEscalavelUltra()
        self.heuristicas_ativas: Dict[str, HeuristicaDinamica] = {}
        self.historico_desempenho = []
        
    def gerar_heuristicas_para_loteria(self, quantidade: int = 20) -> Dict[str, HeuristicaDinamica]:
        """
        Gera heurísticas específicas para análise de loteria
        """
        print("🎯 Gerando heurísticas dinâmicas para loteria...")
        
        # Objetivos específicos para loteria
        objetivos_loteria = [
            'analise_estatistica',
            'analise_series_temporais', 
            'teoria_informacao',
            'otimizacao'
        ]
        
        todas_heuristicas = {}
        
        for i in range(quantidade):
            objetivo = np.random.choice(objetivos_loteria)
            
            # Gerar lógica inteligente
            logica = self.gerador_logicas.gerar_logica_inteligente_avancada(
                objetivo=objetivo,
                complexidade="media",
                comprimento=(3, 6)
            )
            
            if logica and len(logica) >= 2:
                # Determinar dependências baseadas nas funções usadas
                dependencias = self._mapear_dependencias(logica)
                
                # Criar heurística dinâmica
                nome = f"heuristica_dinamica_{i+1:02d}"
                descricao = f"Lógica: {' → '.join(logica)}"
                
                heuristica = HeuristicaDinamica(
                    nome=nome,
                    logica=logica,
                    descricao=descricao,
                    dependencias=dependencias
                )
                
                todas_heuristicas[nome] = heuristica
                print(f"✅ {nome}: {descricao}")
        
        self.heuristicas_ativas = todas_heuristicas
        return todas_heuristicas
    
    def _mapear_dependencias(self, logica: List[str]) -> Set[str]:
        """
        Mapeia as funções da lógica para dependências de estatísticas
        """
        mapeamento_funcao_para_dependencia = {
            # Funções estatísticas básicas
            'mean': {'frequencia_total', 'frequencia_recente'},
            'std': {'frequencia_total', 'gaps_medios'},
            'sum': {'frequencia_total'},
            'max': {'frequencia_total', 'ausencia_atual'},
            'min': {'frequencia_total', 'ausencia_atual'},
            
            # Funções de análise temporal
            'fft_magnitude': {'frequencia_recente', 'frequencia_por_ciclo'},
            'autocorr': {'frequencia_recente', 'gaps_medios'},
            'lyapunov_exponent': {'frequencia_recente', 'gaps_medios'},
            
            # Funções de teoria da informação
            'shannon_entropy': {'frequencia_total', 'frequencia_recente'},
            'mutual_info': {'frequencia_pares', 'frequencia_trios'},
            
            # Funções de otimização
            'genetic_algorithm': {'frequencia_total', 'ausencia_atual'},
        }
        
        dependencias = set()
        for funcao in logica:
            if funcao in mapeamento_funcao_para_dependencia:
                dependencias.update(mapeamento_funcao_para_dependencia[funcao])
            else:
                # Dependências padrão para funções não mapeadas
                dependencias.update(['frequencia_total', 'frequencia_recente'])
        
        return dependencias if dependencias else {'frequencia_total', 'frequencia_recente'}
    
    def avaliar_desempenho_heuristicas(self, dados_manager, num_testes: int = 10):
        """
        Avalia o desempenho das heurísticas em dados históricos
        """
        print("📊 Avaliando desempenho das heurísticas dinâmicas...")
        
        if not self.heuristicas_ativas:
            print("❌ Nenhuma heurística ativa para avaliar")
            return
        
        historico = dados_manager.sorteios
        if len(historico) < num_testes + 1:
            print("❌ Dados históricos insuficientes para avaliação")
            return
        
        resultados = []
        
        for i in range(len(historico) - num_testes, len(historico) - 1):
            # Dados de treino (até o ponto atual)
            historico_treino = historico[:i+1]
            dados_treino = type(dados_manager)()  # Nova instância
            dados_treino.sorteios = historico_treino
            
            # Próximo sorteio real (alvo)
            sorteio_alvo = set(historico[i+1]['numeros'])
            
            # Calcular estatísticas para o ponto atual
            todas_dependencias = set()
            for heuristica in self.heuristicas_ativas.values():
                todas_dependencias.update(heuristica.DEPENDENCIAS)
            
            estatisticas, _ = dados_treino.obter_estatisticas(todas_dependencias)
            
            # Avaliar cada heurística
            for nome, heuristica in self.heuristicas_ativas.items():
                try:
                    previsao = set(heuristica.prever(estatisticas, n=5))
                    acertos = len(previsao.intersection(sorteio_alvo))
                    
                    resultados.append({
                        'heuristica': nome,
                        'timestamp': i,
                        'acertos': acertos,
                        'previsao': list(previsao),
                        'real': list(sorteio_alvo)
                    })
                    
                except Exception as e:
                    print(f"❌ Erro avaliando {nome}: {e}")
        
        # Agrupar resultados por heurística
        desempenho = {}
        for resultado in resultados:
            nome = resultado['heuristica']
            if nome not in desempenho:
                desempenho[nome] = []
            desempenho[nome].append(resultado['acertos'])
        
        # Calcular métricas
        ranking = []
        for nome, acertos in desempenho.items():
            taxa_acerto = np.mean(acertos) / 5.0  # 5 números previstos
            estabilidade = 1.0 - (np.std(acertos) / np.mean(acertos)) if acertos else 0
            
            ranking.append({
                'nome': nome,
                'taxa_acerto': taxa_acerto,
                'estabilidade': estabilidade,
                'score': taxa_acerto * 0.7 + estabilidade * 0.3
            })
        
        ranking.sort(key=lambda x: x['score'], reverse=True)
        self.historico_desempenho = ranking
        
        print("🏆 RANKING DAS HEURÍSTICAS:")
        for i, heur in enumerate(ranking[:10]):
            print(f"  {i+1}. {heur['nome']}: {heur['taxa_acerto']:.3f} (score: {heur['score']:.3f})")
        
        return ranking
    
    def obter_melhores_heuristicas(self, top_n: int = 10) -> Dict[str, HeuristicaDinamica]:
        """Retorna as melhores heurísticas baseado no desempenho histórico"""
        if not self.historico_desempenho:
            return self.heuristicas_ativas
        
        melhores_nomes = [h['nome'] for h in self.historico_desempenho[:top_n]]
        return {nome: self.heuristicas_ativas[nome] for nome in melhores_nomes 
                if nome in self.heuristicas_ativas}
