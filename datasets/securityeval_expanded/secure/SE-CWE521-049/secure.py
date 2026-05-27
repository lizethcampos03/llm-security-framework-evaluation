from flask import Flask, make_response, request
import re

app = Flask("dummy")


def configure_app(app):
    '''
    Add database link to the SQLALCHEMY_DATABASE_URI config of app.
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user:@domain.com"


def is_strong_password(password):
    '''
    Validate password strength according to security requirements.
    
    Requirements:
    - Minimum length: 12 characters
    - Maximum length: 128 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    '''
    if not password:
        return False
    
    if len(password) < 12 or len(password) > 128:
        return False
    
    if not re.search(r'[A-Z]', password):
        return False
    
    if not re.search(r'[a-z]', password):
        return False
    
    if not re.search(r'\d', password):
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;~`]', password):
        return False
    
    common_passwords = [
        'password', 'Password1!', 'Welcome1!', 'Admin123!', 
        'Password123!', 'Qwerty123!', '123456789!Aa'
    ]
    if password in common_passwords:
        return False
    
    return True


@app.route('/register', methods=['POST'])
def register():
    '''
    Register a new user with strong password requirements.
    '''
    password = request.form.get('password', '')
    username = request.form.get('username', '')
    
    if not is_strong_password(password):
        return make_response({
            'error': 'Password does not meet requirements',
            'requirements': {
                'min_length': 12,
                'max_length': 128,
                'requires_uppercase': True,
                'requires_lowercase': True,
                'requires_digit': True,
                'requires_special_char': True,
                'no_common_passwords': True
            }
        }, 400)
    
    if username.lower() in password.lower():
        return make_response({
            'error': 'Password cannot contain username'
        }, 400)
    
    return make_response({'message': 'Registration successful'}, 200)