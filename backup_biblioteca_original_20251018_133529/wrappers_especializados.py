# lib/funcoes_analiticas/wrappers_especializados.py
from typing import List, Dict, Callable, Any
import numpy as np

class TemporalPatternWarper:
    """Wrapper para análise de padrões temporais multi-escala."""
    
    def __init__(self, seq: List[float]):
        self.sequence = seq
        self.results = {}
    
    def apply_multi_scale_analysis(self) -> 'TemporalPatternWarper':
        """Aplica análise em múltiplas escalas temporais."""
        from .padroes_evolutivos_temporais import temporal_pattern_entropy
        from .analise_temporal_multiescala import multi_scale_entropy_analysis
        
        self.results['temporal_entropy'] = temporal_pattern_entropy(self.sequence)
        self.results['multi_scale_entropy'] = multi_scale_entropy_analysis(self.sequence)
        return self
    
    def apply_evolutionary_analysis(self) -> 'TemporalPatternWarper':
        """Aplica análise evolutiva e darwiniana."""
        from .evolucao_darwiniana import evolutionary_fitness_landscape, evolutionary_algorithm_simulation
        from .padroes_evolutivos_temporais import evolutionary_fractal_dimension
        
        self.results['fitness_landscape'] = evolutionary_fitness_landscape(self.sequence)
        self.results['evolution_simulation'] = evolutionary_algorithm_simulation(self.sequence)
        self.results['evolutionary_fractal'] = evolutionary_fractal_dimension(self.sequence)
        return self
    
    def apply_catastrophe_analysis(self) -> 'TemporalPatternWarper':
        """Aplica análise de teoria das catástrofes."""
        from .teoria_catastrofe import catastrophe_theory_analyzer, tipping_point_early_warning
        from .transicoes_fase import phase_transition_detector, critical_slowdown_analysis
        
        self.results['catastrophe_analysis'] = catastrophe_theory_analyzer(self.sequence)
        self.results['tipping_point_warning'] = tipping_point_early_warning(self.sequence)
        self.results['phase_transitions'] = phase_transition_detector(self.sequence)
        self.results['critical_slowdown'] = critical_slowdown_analysis(self.sequence)
        return self
    
    def get_comprehensive_report(self) -> Dict:
        """Retorna relatório compreensivo integrando todas as análises."""
        report = {
            'basic_statistics': {
                'length': len(self.sequence),
                'mean': np.mean(self.sequence),
                'std': np.std(self.sequence),
                'trend': np.polyfit(range(len(self.sequence)), self.sequence, 1)[0]
            },
            'pattern_analysis': self.results,
            'risk_assessment': self._calculate_risk_metrics(),
            'evolutionary_trajectory': self._assess_evolutionary_stage()
        }
        
        return report
    
    def _calculate_risk_metrics(self) -> Dict:
        """Calcula métricas de risco consolidadas."""
        risk_metrics = {}
        
        # Consolida sinais de alerta de diferentes análises
        if 'tipping_point_warning' in self.results:
            warning = self.results['tipping_point_warning']
            risk_metrics['tipping_risk'] = warning.get('composite_risk_score', 0)
        
        if 'critical_slowdown' in self.results:
            slowdown = self.results['critical_slowdown']
            risk_metrics['criticality_risk'] = slowdown.get('critical_slowdown_detected', False)
        
        if 'catastrophe_analysis' in self.results:
            catastrophe = self.results['catastrophe_analysis']
            risk_metrics['catastrophe_frequency'] = catastrophe.get('catastrophe_frequency', 0)
        
        return risk_metrics
    
    def _assess_evolutionary_stage(self) -> str:
        """Classifica o estágio evolutivo do padrão."""
        if 'evolution_simulation' not in self.results:
            return "unknown"
        
        sim = self.results['evolution_simulation']
        adaptation = sim.get('final_adaptation', 0)
        convergence = sim.get('evolutionary_convergence', 1)
        
        if adaptation > 0 and convergence < 0.5:
            return "adaptive_radiation"
        elif adaptation > 0 and convergence > 0.8:
            return "optimization_phase"
        elif adaptation < 0:
            return "evolutionary_decline"
        else:
            return "evolutionary_stasis"
