import os
import hashlib
import secrets

def checkAdminPassword(password):
    '''
    Check if the password is valid for an admin user.
    '''
    stored_hash = os.environ.get('ADMIN_PASSWORD_HASH')
    stored_salt = os.environ.get('ADMIN_PASSWORD_SALT')
    
    if not stored_hash or not stored_salt:
        raise ValueError("Admin password hash and salt must be configured in environment variables")
    
    salt = bytes.fromhex(stored_salt)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    return secrets.compare_digest(password_hash.hex(), stored_hash)