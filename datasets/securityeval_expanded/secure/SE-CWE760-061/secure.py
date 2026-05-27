from hashlib import pbkdf2_hmac
import os


def getHash(password):
    '''
    create a hash of the password with a salt.
    '''
    salt = os.urandom(32)
    hash = pbkdf2_hmac('sha256', password, salt, 100000)
    return salt + hash