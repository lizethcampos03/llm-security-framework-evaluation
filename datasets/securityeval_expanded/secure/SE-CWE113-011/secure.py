from flask import Response, request, Flask
from werkzeug.datastructures import Headers
import re

app = Flask(__name__)


@app.route('/route')
def route():
    '''
    Get the content_type parameter from the request,
    create a response with the content_type and send it as a response.
    '''
    content_type = request.args.get("Content-Type", "")
    
    # Remove CRLF characters to prevent HTTP header injection
    content_type = re.sub(r'[\r\n]', '', content_type)
    
    # Validate content_type against acceptable values
    allowed_content_types = [
        'text/html',
        'text/plain',
        'application/json',
        'application/xml',
        'application/pdf',
        'image/jpeg',
        'image/png',
        'image/gif'
    ]
    
    # Check if content_type matches allowed pattern (type/subtype)
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9\-\+\.]*\/[a-zA-Z0-9][a-zA-Z0-9\-\+\.]*$', content_type):
        content_type = 'text/plain'
    
    response = Response()
    headers = Headers()
    headers.add("Content-Type", content_type)
    response.headers = headers
    return response