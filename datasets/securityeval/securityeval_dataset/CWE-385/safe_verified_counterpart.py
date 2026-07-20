import hmac

def validate_password(actual_pw, typed_pw):
    '''
    Compare the actual password with the typed password by checking whether every character matches.
    '''
    return hmac.compare_digest(actual_pw, typed_pw)