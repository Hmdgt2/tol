# lib/funcoes_analiticas/nlp_avancado.py
import numpy as np
from typing import List, Dict
import re
from collections import Counter, defaultdict

def word_embeddings_cosine(text1: str, text2: str, 
                          word_vectors: Dict[str, List[float]]) -> float:
    """Similaridade de cosseno entre embeddings de palavras."""
    def text_to_vector(text):
        words = re.findall(r'\w+', text.lower())
        vectors = [word_vectors[word] for word in words if word in word_vectors]
        if not vectors:
            return [0.0] * 100  # Dimensão padrão
        return np.mean(vectors, axis=0)
    
    vec1, vec2 = text_to_vector(text1), text_to_vector(text2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2) + 1e-8)

def tfidf_vectorizer(documents: List[str]) -> List[List[float]]:
    """Vectorização TF-IDF simplificada."""
    # Calcular frequência de termos
    doc_terms = [re.findall(r'\w+', doc.lower()) for doc in documents]
    term_doc_freq = defaultdict(int)
    
    for terms in doc_terms:
        unique_terms = set(terms)
        for term in unique_terms:
            term_doc_freq[term] += 1
    
    # TF-IDF
    tfidf_vectors = []
    for terms in doc_terms:
        term_freq = Counter(terms)
        vector = []
        for term in term_doc_freq:
            tf = term_freq[term] / len(terms) if len(terms) > 0 else 0
            idf = np.log(len(documents) / (term_doc_freq[term] + 1))
            vector.append(tf * idf)
        tfidf_vectors.append(vector)
    
    return tfidf_vectors

def perplexity_language_model(text: str, 
                             ngram_probs: Dict[str, float], 
                             n: int = 2) -> float:
    """Perplexidade de modelo de linguagem n-gram."""
    words = re.findall(r'\w+', text.lower())
    if len(words) < n:
        return float('inf')
    
    log_prob_sum = 0.0
    for i in range(len(words) - n + 1):
        ngram = ' '.join(words[i:i+n])
        prob = ngram_probs.get(ngram, 1e-8)  # Suavização
        log_prob_sum += np.log(prob)
    
    avg_log_prob = log_prob_sum / (len(words) - n + 1)
    return np.exp(-avg_log_prob)

def named_entity_recognition_confidence(text: str, 
                                      entities: List[str]) -> List[float]:
    """Confiança de reconhecimento de entidades nomeadas."""
    words = re.findall(r'\w+', text.lower())
    entity_confidence = []
    
    for entity in entities:
        entity_words = re.findall(r'\w+', entity.lower())
        # Verificar ocorrências
        occurrences = 0
        for i in range(len(words) - len(entity_words) + 1):
            if words[i:i+len(entity_words)] == entity_words:
                occurrences += 1
        
        # Confiança baseada em frequência e comprimento
        confidence = occurrences * len(entity_words) / len(words) if words else 0
        entity_confidence.append(confidence)
    
    return entity_confidence
