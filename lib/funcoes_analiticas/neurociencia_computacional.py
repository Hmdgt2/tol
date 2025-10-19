# lib/funcoes_analiticas/neurociencia_computacional.py
import numpy as np
from typing import List, Dict
from scipy import signal
import math

# ============================================================
# Padrões Neurais
# ============================================================

def neural_oscillation_patterns(seq: List[float], sampling_rate: float = 1000) -> Dict:
    """Detecta padrões de oscilação neural (alpha, beta, gamma waves)."""
    if len(seq) < sampling_rate:  # Mínimo 1 segundo de dados
        return {"error": f"Dados insuficientes. Mínimo {sampling_rate} amostras necessárias"}
    
    # Bands de frequência neural (Hz)
    frequency_bands = {
        "delta": (0.5, 4),
        "theta": (4, 8),
        "alpha": (8, 13),
        "beta": (13, 30),
        "gamma": (30, 100)
    }
    
    # Calcula PSD
    freqs, psd = signal.welch(seq, fs=sampling_rate, nperseg=min(256, len(seq)))
    
    band_powers = {}
    total_power = np.trapz(psd, freqs)
    
    for band, (low, high) in frequency_bands.items():
        band_mask = (freqs >= low) & (freqs <= high)
        if np.any(band_mask):
            band_power = np.trapz(psd[band_mask], freqs[band_mask])
            band_powers[band] = {
                "absolute_power": band_power,
                "relative_power": band_power / total_power if total_power > 0 else 0,
                "peak_frequency": freqs[band_mask][np.argmax(psd[band_mask])] if np.any(band_mask) else 0
            }
    
    # Análise de dominância
    dominant_band = max(band_powers.items(), key=lambda x: x[1]["relative_power"])[0] if band_powers else None
    
    return {
        "frequency_bands": band_powers,
        "dominant_rhythm": dominant_band,
        "total_power": total_power,
        "spectral_entropy": -np.sum([p * np.log(p) for p in psd/psd.sum() if p > 0]) if psd.sum() > 0 else 0,
        "coherence_metric": np.std([bp["relative_power"] for bp in band_powers.values()]) if band_powers else 0
    }

def spike_train_analysis(seq: List[float], threshold: float = 0.5) -> Dict:
    """Análise de 'spike trains' neuronais."""
    if not seq:
        return {"error": "Sequência vazia"}
    
    # Detecta spikes
    spikes = [i for i, val in enumerate(seq) if val > threshold]
    
    if len(spikes) < 2:
        return {
            "spike_count": len(spikes),
            "error": "Spikes insuficientes para análise"
        }
    
    # Intervalos entre spikes (ISI)
    isi = [spikes[i+1] - spikes[i] for i in range(len(spikes)-1)]
    
    # Coeficiente de variação
    cv_isi = np.std(isi) / np.mean(isi) if np.mean(isi) > 0 else 0
    
    # Padrão de bursting
    burst_threshold = np.mean(isi) * 0.5  # Intervalos curtos indicam bursts
    bursts = []
    current_burst = []
    
    for interval in isi:
        if interval <= burst_threshold:
            current_burst.append(interval)
        else:
            if len(current_burst) >= 2:  # Mínimo 2 spikes para burst
                bursts.append(current_burst)
            current_burst = []
    
    burst_analysis = {
        "num_bursts": len(bursts),
        "avg_burst_duration": np.mean([sum(burst) for burst in bursts]) if bursts else 0,
        "avg_spikes_per_burst": np.mean([len(burst) + 1 for burst in bursts]) if bursts else 0
    }
    
    return {
        "spike_count": len(spikes),
        "firing_rate": len(spikes) / len(seq),
        "isi_statistics": {
            "mean": np.mean(isi),
            "std": np.std(isi),
            "cv": cv_isi
        },
        "burst_analysis": burst_analysis,
        "regularity_index": 1 / cv_isi if cv_isi > 0 else float('inf'),
        "spike_pattern": "regular" if cv_isi < 0.5 else "bursty" if burst_analysis["num_bursts"] > 0 else "random"
    }

def synaptic_plasticity_simulation(seq: List[float], learning_rule: str = "stdp") -> Dict:
    """Simula plasticidade sináptica (STDP, etc)."""
    if len(seq) < 10:
        return {"error": "Sequência muito curta para simulação de plasticidade"}
    
    # STDP - Spike-Timing Dependent Plasticity
    def stdp_rule(pre_spikes, post_spikes, A_plus=0.1, A_minus=0.12, tau_plus=20, tau_minus=20):
        weight_change = 0
        
        for pre in pre_spikes:
            for post in post_spikes:
                dt = post - pre
                if dt > 0:  # Pre antes de post -> LTP
                    weight_change += A_plus * np.exp(-dt / tau_plus)
                else:  # Post antes de pre -> LTD
                    weight_change -= A_minus * np.exp(dt / tau_minus)
        
        return weight_change
    
    # Detecta spikes (simplificado)
    threshold = np.mean(seq) + np.std(seq)
    spikes = [i for i, val in enumerate(seq) if val > threshold]
    
    if len(spikes) < 2:
        return {"error": "Spikes insuficientes para STDP"}
    
    # Simula pares pré-pós sinápticos
    pre_spikes = spikes[::2]  # Spikes pré-sinápticos
    post_spikes = spikes[1::2]  # Spikes pós-sinápticos
    
    if not pre_spikes or not post_spikes:
        return {"error": "Pares pré-pós insuficientes"}
    
    weight_changes = []
    
    for i in range(min(len(pre_spikes), len(post_spikes))):
        weight_change = stdp_rule([pre_spikes[i]], [post_spikes[i]])
        weight_changes.append(weight_change)
    
    net_change = sum(weight_changes)
    
    return {
        "plasticity_rule": learning_rule,
        "weight_changes": weight_changes,
        "net_synaptic_change": net_change,
        "potentiation_events": sum(1 for w in weight_changes if w > 0),
        "depression_events": sum(1 for w in weight_changes if w < 0),
        "learning_efficiency": net_change / len(weight_changes) if weight_changes else 0,
        "stability_metric": abs(net_change) / (len(weight_changes) * 0.1) if weight_changes else 0
    }
