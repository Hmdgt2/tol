# heuristicas/meta_avaliacao.py
import importlib
from typing import Dict, Any, List
from collections import Counter

class MetaAvaliacao:
    # --- Metadados da Heurística ---
    NOME = "meta_avaliacao"
    DESCRICAO = "Escolhe a heurística mais precisa dos últimos sorteios, com base nos resultados de treino."
    # IMPORTANTE: As dependências precisam ser listadas explicitamente pelo 'despachante.py'.
    # A dependência 'precisao_posicional_historica' deve ser calculada por uma nova estatística no dados.py
    # As outras dependências são as que a heurística vencedora necessitar.
    DEPENDENCIAS = ["precisao_posicional_historica", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na heurística mais precisa, conforme o histórico de treino.
        """
        performance_historica = estatisticas.get('precisao_posicional_historica', {})

        if not performance_historica:
            # Fallback para os mais frequentes se não houver dados de performance
            frequencia = estatisticas.get('frequencia_total', {})
            return sorted([num for num in frequencia.keys()][:n])

        # Encontra a heurística com a melhor pontuação global
        melhor_heuristica = None
        melhor_pontuacao = -1
        
        for nome_heuristica, dados_heuristica in performance_historica.items():
            pontuacao_total = sum(dados_heuristica.values())
            if pontuacao_total > melhor_pontuacao:
                melhor_pontuacao = pontuacao_total
                melhor_heuristica = nome_heuristica
                
        # Chama a heurística vencedora com os dados necessários
        if melhor_heuristica:
            try:
                # Importa dinamicamente o módulo da heurística vencedora
                modulo = importlib.import_module(f'heuristicas.{melhor_heuristica}')
                
                # Obtém a classe da heurística, instanciando-a, e chama o seu método prever
                # O nome da classe é o nome do módulo capitalizado e sem sublinhados
                nome_classe = melhor_heuristica.replace('_', ' ').title().replace(' ', '')
                
                heuristic_instance = getattr(modulo, nome_classe)()
                
                # O despachante já forneceu todas as dependências necessárias da heurística vencedora.
                previsao_final = heuristic_instance.prever(estatisticas, n=n)
                return sorted(list(set(previsao_final)))
            except (ImportError, AttributeError) as e:
                # Caso a importação ou a chamada falhe, um aviso será impresso pelo despachante.
                print(f"Aviso: Falha ao executar a heurística vencedora '{melhor_heuristica}': {e}")
                pass

        # Fallback final se algo der errado
        frequencia = estatisticas.get('frequencia_total', {})
        return sorted([num for num in frequencia.keys()][:n])
