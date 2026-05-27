from flask import request, send_file, Flask, abort
import os
from pathlib import Path

app = Flask(__name__)

# Define allowed base directory for downloads
ALLOWED_DOWNLOAD_DIR = '/var/www/downloads'

@app.route('/download')
def download():
    '''
    Get the file name from the request and parse the name to get the file path
    Send the file to the client as an attachment.
    '''
    file = request.args.get('file', '')
    
    # Validate input is not empty
    if not file:
        abort(400)
    
    # Allowlist: Only allow alphanumeric characters, underscores, hyphens, and dots
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.')
    if not all(c in allowed_chars for c in file):
        abort(400)
    
    # Construct filepath
    filepath = '/'.join(file.split('_'))
    
    # Resolve to absolute path within allowed directory
    try:
        base_path = Path(ALLOWED_DOWNLOAD_DIR).resolve()
        requested_path = (base_path / filepath).resolve()
        
        # Ensure the resolved path is within the allowed directory
        if not str(requested_path).startswith(str(base_path)):
            abort(403)
        
        # Check if file exists and is a file (not a directory)
        if not requested_path.is_file():
            abort(404)
        
        return send_file(str(requested_path), as_attachment=True)
    except (ValueError, OSError):
        abort(400)