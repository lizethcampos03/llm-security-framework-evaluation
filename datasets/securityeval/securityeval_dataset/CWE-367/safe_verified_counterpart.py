import os


def readFile(fileName):
    '''
    Read the file and return its content.
    Handle file existence through exception handling to avoid TOCTOU.
    '''

    try:
        with open(fileName, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except IOError:
        return None