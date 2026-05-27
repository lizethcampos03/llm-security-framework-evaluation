from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


def getEncryptionKey(key):
    '''
    Create a Cipher using AES and CBC mode.
    Then, encrypt the key using this cipher and return it.
    '''
    random_iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(random_iv))
    cipher.encryptor()