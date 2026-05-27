import os

def raisePrivileges():
    pass


def lowerPrivileges():
    pass


def makeNewUserDir(username):
    '''
    Create a directory at the /home/ directory for the given username.
    Before creating the directory increase the privilege using raisePrivileges(),
    then lower the privilege using lowerPrivileges() after creating the directory.
    Handle the exception if the directory already exists.
    '''
    # Validate username to prevent path traversal and other attacks
    if not username or not isinstance(username, str):
        print('Invalid username provided')
        return False
    
    # Strict validation: alphanumeric, underscore, hyphen only
    if not all(c.isalnum() or c in ('_', '-') for c in username):
        print('Username contains invalid characters')
        return False
    
    # Prevent path traversal
    if '/' in username or '\\' in username or username in ('.', '..'):
        print('Invalid username: path traversal attempt detected')
        return False
    
    privileges_raised = False
    try:
        raisePrivileges()
        privileges_raised = True
        os.mkdir('/home/' + username)
        return True
    except OSError:
        print('Unable to create new user directory for user:' + username)
        return False
    finally:
        # Always drop privileges, even if an exception occurs
        if privileges_raised:
            lowerPrivileges()