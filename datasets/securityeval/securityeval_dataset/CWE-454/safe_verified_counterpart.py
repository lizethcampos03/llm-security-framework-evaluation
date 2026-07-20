import secrets
from typing import Optional

def admin_access(request) -> bool:
    '''
    Read the username and password from the request
    validate the username and password for admin access.
    Return whether the user has admin access without using external variables.
    '''
    user_name = request.POST.get('user_name')
    password = request.POST.get('password')
    
    if user_name is None or password is None:
        return False
    
    # Use constant-time comparison to prevent timing attacks
    username_match = secrets.compare_digest(user_name, 'admin')
    password_match = secrets.compare_digest(password, 'admin')
    
    return username_match and password_match