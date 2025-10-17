from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

def get_model(input_shape=(100, 1), num_classes=2):
    """
    Retorna uma instância de um modelo CNN 1D simples.
    """
    model = Sequential()
    model.add(Conv1D(64, kernel_size=3, activation='relu', input_shape=input_shape))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dropout(0.3))
    model.add(Dense(num_classes, activation='softmax' if num_classes > 1 else 'sigmoid'))
    model.compile(optimizer=Adam(), loss='categorical_crossentropy' if num_classes > 1 else 'binary_crossentropy', metrics=['accuracy'])
    return model
