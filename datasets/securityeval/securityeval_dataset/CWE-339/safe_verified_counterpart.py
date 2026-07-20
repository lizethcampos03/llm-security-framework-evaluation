import os


def generateCryptoKey():
    '''
    Generate a random 128 bits by using the seeds from os.urandom().
    '''
    key = int.from_bytes(os.urandom(16), byteorder='big')
    return key