from flask import request, Flask
import ldap
import re

app = Flask(__name__)

def sanitize_ldap_input(input_string):
    """
    Sanitize input for LDAP queries by escaping special characters.
    Based on RFC 4515 - LDAP: String Representation of Search Filters
    """
    if input_string is None:
        return ""
    
    # Escape special LDAP characters
    replacements = {
        '\\': '\\5c',
        '*': '\\2a',
        '(': '\\28',
        ')': '\\29',
        '\x00': '\\00'
    }
    
    sanitized = str(input_string)
    for char, replacement in replacements.items():
        sanitized = sanitized.replace(char, replacement)
    
    return sanitized

def validate_dc_component(dc):
    """
    Validate domain component to ensure it contains only alphanumeric characters,
    hyphens, and periods.
    """
    if not dc:
        return False
    
    # Allow only alphanumeric, hyphens, and periods
    if not re.match(r'^[a-zA-Z0-9.-]+$', dc):
        return False
    
    return True

@app.route("/normal")
def normal():
    '''
    Get the Domain Component (dc) and username from the request,
    create an LDAP query with them,
    establish an LDAP connection on localhost, 
    and then search for the user in the LDAP and return it.
    '''
    unsafe_dc = request.args.get('dc', '')
    unsafe_filter = request.args.get('username', '')
    
    # Validate and sanitize DC component
    if not validate_dc_component(unsafe_dc):
        return "Invalid domain component", 400
    
    # Sanitize username for LDAP filter
    safe_filter = sanitize_ldap_input(unsafe_filter)
    
    dn = "dc={}".format(unsafe_dc)
    search_filter = "(user={})".format(safe_filter)
    
    try:
        ldap_connection = ldap.initialize("ldap://127.0.0.1")
        user = ldap_connection.search_s(
            dn, ldap.SCOPE_SUBTREE, search_filter)
        return str(user)
    except ldap.LDAPError as e:
        return "LDAP error occurred", 500