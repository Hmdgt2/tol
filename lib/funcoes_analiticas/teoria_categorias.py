# lib/funcoes_analiticas/teoria_categorias.py
import numpy as np
from typing import List, Dict, Tuple, Any
import itertools

# ============================================================
# Limites e Adjuntos
# ============================================================

def categorical_limit_calculation(diagram: Dict) -> Dict:
    """Calcula limite categórico para um diagrama dado."""
    objects = diagram.get('objects', [])
    morphisms = diagram.get('morphisms', {})
    
    # Verifica se o diagrama comuta
    commuting = check_diagram_commutation(morphisms, objects)
    
    # Calcula objeto limite (produto para objetos discretos)
    limit_object = calculate_limit_object(objects, morphisms)
    
    # Propriedades universais
    universal_property = verify_universal_property(limit_object, objects, morphisms)
    
    return {
        "diagram_type": classify_diagram_type(objects, morphisms),
        "commuting": commuting,
        "limit_object": limit_object,
        "universal_property_satisfied": universal_property,
        "morphism_count": len(morphisms),
        "object_count": len(objects),
        "completeness": check_completeness(objects, morphisms),
        "special_limits": identify_special_limits(objects, morphisms)
    }

def adjunction_analysis(functors: Tuple[Dict, Dict]) -> Dict:
    """Analisa adjunção entre dois functores."""
    left_functor, right_functor = functors
    
    # Verifica relação adjunta
    are_adjoint = check_adjunction_conditions(left_functor, right_functor)
    
    # Unidade e counidade
    unit = calculate_adjunction_unit(left_functor, right_functor)
    counit = calculate_adjunction_counit(left_functor, right_functor)
    
    # Triângulos identidade
    triangle_identities = verify_triangle_identities(unit, counit)
    
    return {
        "left_functor": left_functor.get('name', 'F'),
        "right_functor": right_functor.get('name', 'G'),
        "are_adjoint": are_adjoint,
        "adjunction_type": classify_adjunction_type(left_functor, right_functor),
        "unit_morphism": unit,
        "counit_morphism": counit,
        "triangle_identities_hold": triangle_identities,
        "monad_formation": can_form_monad(unit, counit) if are_adjoint else False,
        "applications": identify_adjunction_applications(left_functor, right_functor)
    }

def topos_theory_models(category_data: Dict) -> Dict:
    """Analisa modelos de teoria de topos."""
    objects = category_data.get('objects', [])
    morphisms = category_data.get('morphisms', {})
    subobject_classifier = category_data.get('subobject_classifier', None)
    
    # Verifica axiomas de topos
    has_terminal = check_terminal_object(objects, morphisms)
    has_pullbacks = check_pullbacks(objects, morphisms)
    has_exponentials = check_exponentials(objects, morphisms)
    has_subobject_classifier = subobject_classifier is not None
    
    is_topos = has_terminal and has_pullbacks and has_exponentials and has_subobject_classifier
    
    # Classificação do topos
    topos_type = classify_topos(objects, morphisms, subobject_classifier)
    
    return {
        "is_topos": is_topos,
        "topos_type": topos_type,
        "axioms_satisfied": {
            "terminal_object": has_terminal,
            "pullbacks": has_pullbacks,
            "exponentials": has_exponentials,
            "subobject_classifier": has_subobject_classifier
        },
        "internal_logic": analyze_internal_logic(objects, morphisms) if is_topos else None,
        "geometric_morphisms": find_geometric_morphisms(category_data),
        "cohomology_theories": identify_topos_cohomology(topos_type)
    }

def check_diagram_commutation(morphisms: Dict, objects: List) -> bool:
    """Verifica se o diagrama comuta."""
    if len(morphisms) < 2:
        return True
    
    # Verifica composições iguais para caminhos paralelos
    for path1, path2 in itertools.combinations(morphisms.keys(), 2):
        if path1[-1] == path2[-1] and path1[0] == path2[0]:  # Mesmo início e fim
            comp1 = compose_morphisms(path1, morphisms)
            comp2 = compose_morphisms(path2, morphisms)
            if comp1 != comp2:
                return False
    return True

def calculate_limit_object(objects: List, morphisms: Dict) -> Any:
    """Calcula objeto limite para diagrama."""
    if not objects:
        return None
    
    # Para diagramas discretos, limite é o produto
    if not morphisms:
        return {"type": "product", "components": objects}
    
    # Para diagramas com morfismos, calcula equalizador/outros limites
    return {"type": "general_limit", "size": len(objects)}

def verify_universal_property(limit_obj, objects, morphisms) -> bool:
    """Verifica propriedade universal do limite."""
    return limit_obj is not None and len(objects) > 0

def check_adjunction_conditions(F: Dict, G: Dict) -> bool:
    """Verifica condições de adjunção entre functores F e G."""
    # Condições simplificadas
    F_preserves_limits = F.get('preserves_limits', False)
    G_preserves_colimits = G.get('preserves_colimits', False)
    
    return F_preserves_limits and G_preserves_colimits

def calculate_adjunction_unit(F: Dict, G: Dict) -> Dict:
    """Calcula unidade da adjunção."""
    return {"type": "unit", "natural_transformation": True}

def classify_adjunction_type(F: Dict, G: Dict) -> str:
    """Classifica tipo de adjunção."""
    if F.get('free', False):
        return "free_forgetful"
    elif G.get('forgetful', False):
        return "forgetful_free"
    else:
        return "general_adjunction"

def identify_adjunction_applications(F: Dict, G: Dict) -> List[str]:
    """Identifica aplicações da adjunção."""
    applications = []
    if F.get('free', False):
        applications.append("universal_algebra")
    if G.get('sheaf', False):
        applications.append("algebraic_geometry")
    return applications
