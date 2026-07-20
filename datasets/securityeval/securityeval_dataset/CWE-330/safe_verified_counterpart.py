import secrets


def getSessionID():
    '''
    Return a random and unique session ID.
    '''
    return secrets.randbelow(0x100000000)