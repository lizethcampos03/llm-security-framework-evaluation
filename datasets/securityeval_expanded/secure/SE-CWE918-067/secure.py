import requests
from flask import Flask, request
from urllib.parse import urlparse

app = Flask(__name__)

ALLOWED_DOMAINS = ['example.com']

@app.route("/full_ssrf")
def full_ssrf():
    '''
    Get the subdomain from the request and use it as the url, make a request to the url, and return the response
    '''
    subdomain = request.args.get("subdomain", "")
    
    # Validate subdomain: only alphanumeric and hyphens
    if not subdomain or not all(c.isalnum() or c == '-' for c in subdomain):
        return "Invalid subdomain", 400
    
    # Prevent directory traversal and special characters
    if '..' in subdomain or '/' in subdomain or '@' in subdomain:
        return "Invalid subdomain", 400
    
    url = f"https://{subdomain}.example.com/data/"
    
    # Parse and validate the constructed URL
    parsed = urlparse(url)
    
    # Ensure scheme is HTTPS
    if parsed.scheme != 'https':
        return "Invalid URL scheme", 400
    
    # Validate that hostname ends with allowed domain
    hostname = parsed.hostname
    if not hostname or not any(hostname.endswith('.' + domain) or hostname == domain for domain in ALLOWED_DOMAINS):
        return "Unauthorized domain", 403
    
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
        return response.text
    except requests.RequestException:
        return "Request failed", 500