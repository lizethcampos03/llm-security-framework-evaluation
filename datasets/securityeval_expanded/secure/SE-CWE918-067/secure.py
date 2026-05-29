import requests
from flask import Flask, request
import html

app = Flask(__name__)

ALLOWED_SUBDOMAINS = {
    "api",
    "status",
    "data"
}

BASE_DOMAIN = "example.com"


@app.route("/full_ssrf")
def full_ssrf():
    '''
    Get the subdomain from the request, validate it against an allowlist,
    make a request only to approved internal endpoints, and return a safe response.
    '''
    subdomain = request.args.get("subdomain", "")

    if subdomain not in ALLOWED_SUBDOMAINS:
        return "Unauthorized subdomain", 403

    url = f"https://{subdomain}.{BASE_DOMAIN}/data/"

    try:
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=False
        )
        response.raise_for_status()
    except requests.RequestException:
        return "Request failed", 500

    safe_text = html.escape(response.text)

    return safe_text, 200, {
        "Content-Type": "text/plain; charset=utf-8"
    }