# modelos_ml/svm_classifier.py

from sklearn.svm import SVC

def get_model():
    """
    Retorna uma instância do modelo Support Vector Machine (SVM).
    """
    return SVC(probability=True) # probability=True é necessário para o predict_proba
