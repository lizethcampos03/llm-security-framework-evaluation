from flask import request, send_file, Flask, abort
import os
from pathlib import Path

app = Flask(__name__)

ALLOWED_FILES = {
    'document.pdf',
    'report.xlsx',
    'data.csv',
    'image.png'
}

@app.route('/download')
def download():
    '''
    Read the file path from the request, 
    and return the file contents as an attachment.
    '''
    file = request.args.get('file', '')
    
    if not file:
        abort(400)
    
    filename = os.path.basename(file)
    
    if filename not in ALLOWED_FILES:
        abort(403)
    
    static_dir = Path(app.static_folder).resolve()
    file_path = (static_dir / filename).resolve()
    
    if not str(file_path).startswith(str(static_dir)):
        abort(403)
    
    if not file_path.is_file():
        abort(404)
    
    return send_file(file_path, as_attachment=True)