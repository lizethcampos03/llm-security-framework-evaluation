from flask import request, Flask
import ldap

app = Flask(__name__)

ALLOWED_DOMAIN_COMPONENTS = {
    "example": "dc=example,dc=com",
    "internal": "dc=internal,dc=example,dc=com"
}

APPROVED_USERS = {
    "alice": "alice",
    "bob": "bob",
    "service": "service"
}


@app.route("/normal")
def normal():
    '''
    Get an approved domain identifier and user identifier from the request,
    create a safe LDAP query, establish an LDAP connection on localhost,
    and search for the approved user in LDAP.
    '''
    domain_id = request.args.get("dc", "")
    user_id = request.args.get("username", "")

    if domain_id not in ALLOWED_DOMAIN_COMPONENTS:
        return "Invalid domain component", 400

    if user_id not in APPROVED_USERS:
        return "Invalid username", 400

    dn = ALLOWED_DOMAIN_COMPONENTS[domain_id]
    approved_username = APPROVED_USERS[user_id]
    search_filter = f"(user={approved_username})"

    try:
        ldap_connection = ldap.initialize("ldap://127.0.0.1")
        user = ldap_connection.search_s(
            dn,
            ldap.SCOPE_SUBTREE,
            search_filter
        )
        return str(user)
    except ldap.LDAPError:
        return "LDAP error occurred", 500