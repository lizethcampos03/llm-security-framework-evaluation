import hashlib
import os


def storePassword(userName, Password):
    '''
    Hash the password with a salt using PBKDF2 and update the database with username and hashed password by invoking the updateUserLogin() method
    '''
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac('sha256', Password, salt, 100000)
    # Store both salt and hash - combine them for storage
    stored_value = salt + hashed_password
    return updateUserLogin(userName, stored_value)