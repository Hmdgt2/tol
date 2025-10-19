# lib/funcoes_analiticas/teoria_musical.py
import numpy as np
from typing import List, Dict, Tuple
import math

# ============================================================
# Análise Harmônica e Contraponto
# ============================================================

def harmonic_analysis_musical(notes: List[str], key: str = "C") -> Dict:
    """Realiza análise harmônica de sequência de notas musicais."""
    if not notes:
        return {"error": "Lista de notas vazia"}
    
    # Mapeamento de notas para números
    note_to_number = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
                     'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    
    # Converte notas para números
    note_numbers = [note_to_number.get(note.upper(), 0) for note in notes]
    
    # Análise de tons
    tonal_center = estimate_tonal_center(note_numbers)
    key_signature = identify_key_signature(tonal_center)
    
    # Progressões harmônicas
    chord_progressions = identify_chord_progressions(note_numbers, key_signature)
    
    # Tensão e resolução
    tension_analysis = analyze_musical_tension(note_numbers, chord_progressions)
    
    return {
        "input_notes": notes,
        "numerical_representation": note_numbers,
        "tonal_analysis": {
            "estimated_tonal_center": number_to_note(tonal_center),
            "key_signature": key_signature,
            "modal_character": identify_mode(note_numbers, tonal_center)
        },
        "harmonic_analysis": {
            "chord_progressions": chord_progressions,
            "cadence_points": find_cadence_points(chord_progressions),
            "harmonic_rhythm": calculate_harmonic_rhythm(chord_progressions)
        },
        "melodic_analysis": {
            "contour": analyze_melodic_contour(note_numbers),
            "intervallic_content": analyze_intervals(note_numbers),
            "phrase_structure": identify_phrases(note_numbers)
        },
        "tension_analysis": tension_analysis
    }

def voice_leading_optimization(chord_progression: List[List[str]]) -> Dict:
    """Otimiza condução de vozes para progressão de acordes."""
    if len(chord_progression) < 2:
        return {"error": "Progressão de acordes muito curta"}
    
    # Regras de condução de vozes
    voice_leading_rules = {
        "parallel_fifths": False,
        "parallel_octaves": False,
        "voice_crossing": False,
        "large_leaps": False
    }
    
    # Gera vozes (SATB - Soprano, Alto, Tenor, Baixo)
    voices = generate_voice_leading(chord_progression)
    
    # Avalia qualidade
    voice_leading_quality = evaluate_voice_leading(voices, voice_leading_rules)
    
    # Contraponto
    counterpoint_analysis = analyze_counterpoint(voices)
    
    return {
        "chord_progression": chord_progression,
        "voice_leading": voices,
        "voice_leading_quality": voice_leading_quality,
        "counterpoint_rules": {
            "first_species": analyze_first_species(voices),
            "second_species": analyze_second_species(voices),
            "fuxian_rules": check_fuxian_rules(voices)
        },
        "optimization_suggestions": suggest_voice_leading_improvements(voices, voice_leading_quality),
        "historical_style": identify_historical_style(voices)
    }

def counterpoint_rules_analysis(melodies: List[List[str]]) -> Dict:
    """Analisa regras de contraponto entre melodias."""
    if len(melodies) < 2:
        return {"error": "Pelo menos duas melodias necessárias para contraponto"}
    
    # Converte melodias para números
    melody_numbers = []
    for melody in melodies:
        note_to_number = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        numbers = [note_to_number.get(note.upper(), 0) for note in melody]
        melody_numbers.append(numbers)
    
    # Análise de espécies
    species_analysis = analyze_counterpoint_species(melody_numbers)
    
    # Regras de Fux
    fux_rules = check_fux_counterpoint_rules(melody_numbers)
    
    # Consonância e dissonância
    consonance_analysis = analyze_consonance_dissonance(melody_numbers)
    
    return {
        "input_melodies": melodies,
        "species_analysis": species_analysis,
        "fux_rules_compliance": fux_rules,
        "consonance_analysis": consonance_analysis,
        "interval_analysis": {
            "perfect_consonances": count_perfect_consonances(melody_numbers),
            "imperfect_consonances": count_imperfect_consonances(melody_numbers),
            "dissonances": count_dissonances(melody_numbers)
        },
        "style_classification": classify_counterpoint_style(melody_numbers),
        "composition_suggestions": generate_counterpoint_suggestions(melody_numbers, fux_rules)
    }

def number_to_note(number: int) -> str:
    """Converte número para nota musical."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[number % 12]

def estimate_tonal_center(note_numbers: List[int]) -> int:
    """Estima centro tonal da sequência."""
    if not note_numbers:
        return 0
    
    # Histograma de notas
    histogram = np.zeros(12)
    for note in note_numbers:
        histogram[note % 12] += 1
    
    return int(np.argmax(histogram))
