# modelos_ml/xgboost_classifier.py

from xgboost import XGBClassifier

def get_model():
    """
    Retorna uma instância do modelo XGBoost Classifier.
    """
    return XGBClassifier(n_estimators=100)
