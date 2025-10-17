from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

def get_model(input_dim=100, encoding_dim=32):
    """
    Retorna um autoencoder simples para compressão de dados.
    """
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(encoding_dim, activation='relu')(input_layer)
    decoded = Dense(input_dim, activation='sigmoid')(encoded)
    autoencoder = Model(inputs=input_layer, outputs=decoded)
    autoencoder.compile(optimizer='adam', loss='mse')
    return autoencoder
