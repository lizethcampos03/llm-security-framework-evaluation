import jwt
import os


def verifyJsonWebToken(token):
    '''
    Decode the JSON web token passed and return it.
    '''
    secret_key = os.environ.get('JWT_SECRET_KEY')
    if not secret_key:
        raise ValueError("JWT_SECRET_KEY environment variable not set")
    
    return jwt.decode(token, secret_key, algorithms=['HS256'])