from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

def get_model(input_shape=(10, 1), num_classes=2):
    """
    Retorna uma instância de um modelo LSTM simples.
    """
    model = Sequential()
    model.add(LSTM(64, input_shape=input_shape, return_sequences=False))
    model.add(Dropout(0.3))
    model.add(Dense(num_classes, activation='softmax' if num_classes > 1 else 'sigmoid'))
    model.compile(optimizer=Adam(), loss='categorical_crossentropy' if num_classes > 1 else 'binary_crossentropy', metrics=['accuracy'])
    return model
