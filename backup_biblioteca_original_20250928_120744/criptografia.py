# lib/seguranca/criptografia.py
from cryptography.fernet import Fernet
from typing import Union, Optional

# ============================================================
# Armazenamento da chave global
# ============================================================

_fernet_key: Optional[bytes] = None


# ============================================================
# Geração de chave
# ============================================================

def generate_key() -> str:
    """
    Gera uma chave de criptografia Fernet e armazena globalmente.
    
    Returns:
        str: Chave gerada como string.
    """
    global _fernet_key
    _fernet_key = Fernet.generate_key()
    return _fernet_key.decode()


# ============================================================
# Criptografia e Descriptografia
# ============================================================

def encrypt_data(data: Union[str, bytes]) -> bytes:
    """
    Criptografa dados usando a chave Fernet armazenada.
    
    Args:
        data (str | bytes): Dados a criptografar.
    
    Returns:
        bytes: Dados criptografados.
    
    Raises:
        RuntimeError: Se a chave não foi gerada.
    """
    if _fernet_key is None:
        raise RuntimeError("Chave de criptografia não gerada. Chame generate_key() primeiro.")
    
    if isinstance(data, str):
        data = data.encode()
    
    f = Fernet(_fernet_key)
    return f.encrypt(data)


def decrypt_data(token: bytes) -> str:
    """
    Descriptografa dados usando a chave Fernet armazenada.
    
    Args:
        token (bytes): Dados criptografados.
    
    Returns:
        str: Dados descriptografados.
    
    Raises:
        RuntimeError: Se a chave não foi gerada.
    """
    if _fernet_key is None:
        raise RuntimeError("Chave de criptografia não gerada. Chame generate_key() primeiro.")
    
    f = Fernet(_fernet_key)
    return f.decrypt(token).decode()
