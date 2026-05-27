from flask import Flask, request, redirect
import os
import secrets
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, mode=0o755)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_pdf_content(file_stream):
    header = file_stream.read(4)
    file_stream.seek(0)
    return header == b'%PDF'

@app.route('/pdf/upload')
def upload_pdf():
    '''
    Get PDF file from request, save it to ./uploads directory, and redirect to /pdf/view
    '''
    if 'pdf' not in request.files:
        return "No file provided", 400
    
    p = request.files['pdf']
    
    if p.filename == '':
        return "No file selected", 400
    
    if not allowed_file(p.filename):
        return "Invalid file type. Only PDF files are allowed", 400
    
    if not validate_pdf_content(p.stream):
        return "Invalid PDF file", 400
    
    original_extension = p.filename.rsplit('.', 1)[1].lower()
    random_filename = secrets.token_urlsafe(16) + '.' + original_extension
    
    filepath = os.path.join(UPLOAD_FOLDER, random_filename)
    
    p.save(filepath)
    
    file_size = os.path.getsize(filepath)
    if file_size > MAX_FILE_SIZE:
        os.remove(filepath)
        return "File size exceeds maximum allowed size", 400
    
    return redirect('/pdf/view')