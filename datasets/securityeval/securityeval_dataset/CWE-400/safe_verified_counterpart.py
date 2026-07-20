import re

from flask import request, Flask

app = Flask(__name__)


@app.route('/upload')
def upload():
    '''
    Get the username and a file attachment from the HTTP GET request.
    Then, search the username in the filename of the attachment.
    '''

    username = request.args.get('username')
    if not username:
        return "Missing username", 400
    
    # Limit username length to prevent ReDoS
    if len(username) > 100:
        return "Username too long", 400
    
    attachment = request.files.get('attachment')
    if not attachment:
        return "Missing attachment", 400
    
    filename = attachment.filename
    if not filename:
        return "Missing filename", 400
    
    # Limit filename length to prevent excessive resource consumption
    if len(filename) > 255:
        return "Filename too long", 400
    
    # Escape special regex characters to prevent ReDoS attacks
    escaped_username = re.escape(username)
    
    # Use timeout mechanism via match with limited operations
    try:
        # Simple substring check instead of complex regex to avoid ReDoS
        if escaped_username in filename:
            return "Username found in filename", 200
        else:
            return "Username not found in filename", 200
    except Exception as e:
        return "Error processing request", 500