# modelos_ml/lightgbm_classifier.py

from lightgbm import LGBMClassifier

def get_model():
    """
    Retorna uma instância do modelo LightGBM Classifier.
    """
    return LGBMClassifier(n_estimators=100)
