# lib/seguranca/criptografia.py
from cryptography.fernet import Fernet
from typing import Union

_fernet_key = None

def generate_key() -> str:
    """Gera uma chave de criptografia Fernet e a retorna como uma string."""
    global _fernet_key
    _fernet_key = Fernet.generate_key()
    return _fernet_key.decode()

def encrypt_data(data: Union[str, bytes]) -> bytes:
    """Criptografa dados usando a chave Fernet gerada."""
    if _fernet_key is None:
        raise RuntimeError("Chave de criptografia não gerada. Chame generate_key() primeiro.")
    if isinstance(data, str):
        data = data.encode()
    f = Fernet(_fernet_key)
    return f.encrypt(data)

def decrypt_data(token: bytes) -> str:
    """Descriptografa dados usando a chave Fernet gerada."""
    if _fernet_key is None:
        raise RuntimeError("Chave de criptografia não gerada. Chame generate_key() primeiro.")
    f = Fernet(_fernet_key)
    return f.decrypt(token).decode()
