import requests
from flask import Flask, request
import html

app = Flask(__name__)

APPROVED_ENDPOINTS = {
    "api": "https://api.example.com/data/",
    "status": "https://status.example.com/data/",
    "data": "https://data.example.com/data/"
}


@app.route("/full_ssrf")
def full_ssrf():
    '''
    Get an approved endpoint identifier from the request,
    make a request only to a fixed approved URL, and return a safe response.
    '''
    endpoint_id = request.args.get("subdomain", "")

    if endpoint_id not in APPROVED_ENDPOINTS:
        return "Unauthorized endpoint", 403

    url = APPROVED_ENDPOINTS[endpoint_id]

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