from sklearn.linear_model import LogisticRegression

def get_model():
    return LogisticRegression(solver='liblinear')
