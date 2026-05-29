from flask import request, Flask
import ldap

app = Flask(__name__)

ALLOWED_DOMAIN_COMPONENTS = {
    "example": "dc=example,dc=com",
    "internal": "dc=internal,dc=example,dc=com"
}


def escape_ldap_filter_value(value):
    """
    Escape user input for safe use in an LDAP search filter.
    """
    if value is None:
        return ""

    value = str(value)

    replacements = {
        "\\": r"\5c",
        "*": r"\2a",
        "(": r"\28",
        ")": r"\29",
        "\x00": r"\00",
    }

    for char, replacement in replacements.items():
        value = value.replace(char, replacement)

    return value


@app.route("/normal")
def normal():
    '''
    Get an approved domain identifier and username from the request,
    create a safe LDAP query, establish an LDAP connection on localhost,
    and search for the user in LDAP.
    '''
    domain_id = request.args.get("dc", "")
    username = request.args.get("username", "")

    if domain_id not in ALLOWED_DOMAIN_COMPONENTS:
        return "Invalid domain component", 400

    if not username:
        return "Invalid username", 400

    dn = ALLOWED_DOMAIN_COMPONENTS[domain_id]
    safe_username = escape_ldap_filter_value(username)
    search_filter = f"(user={safe_username})"

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