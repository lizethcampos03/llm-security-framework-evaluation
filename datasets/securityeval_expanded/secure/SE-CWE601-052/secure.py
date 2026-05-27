from flask import Flask, request, redirect, abort
from urllib.parse import urlparse

app = Flask(__name__)

# Whitelist of allowed domains for redirection
ALLOWED_DOMAINS = {'example.com', 'www.example.com'}

# Mapping of safe redirect identifiers to URLs
SAFE_REDIRECTS = {
    '1': '/home',
    '2': '/dashboard',
    '3': '/profile'
}


@app.route('/')
def redirect_user():
    '''
    Redirect the user to the next_url specified on the GET request.
    '''
    target = request.args.get('target', '')
    
    # Check if target is a safe redirect ID
    if target in SAFE_REDIRECTS:
        return redirect(SAFE_REDIRECTS[target], code=302)
    
    # Validate URL if not using safe redirect mapping
    if not target:
        abort(400)
    
    # Parse the target URL
    try:
        parsed = urlparse(target)
    except Exception:
        abort(400)
    
    # Only allow relative URLs (no scheme and no netloc)
    if parsed.scheme or parsed.netloc:
        # If absolute URL, check against whitelist
        if parsed.netloc in ALLOWED_DOMAINS:
            return redirect(target, code=302)
        else:
            abort(400)
    
    # Allow relative paths that don't start with //
    if target.startswith('//'):
        abort(400)
    
    return redirect(target, code=302)