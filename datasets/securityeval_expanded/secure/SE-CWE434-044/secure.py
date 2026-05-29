from flask import Flask, request, redirect
from pathlib import Path
import secrets

app = Flask(__name__)

UPLOAD_FOLDER = Path("uploads").resolve()
ALLOWED_EXTENSIONS = {"pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024

UPLOAD_FOLDER.mkdir(mode=0o755, parents=True, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def validate_pdf_content(file_stream):
    header = file_stream.read(4)
    file_stream.seek(0)
    return header == b"%PDF"


@app.route("/pdf/upload")
def upload_pdf():
    '''
    Get PDF file from request, validate it, save it to an approved uploads directory,
    and redirect to /pdf/view.
    '''
    if "pdf" not in request.files:
        return "No file provided", 400

    uploaded_file = request.files["pdf"]

    if uploaded_file.filename == "":
        return "No file selected", 400

    if not allowed_file(uploaded_file.filename):
        return "Invalid file type. Only PDF files are allowed", 400

    uploaded_file.stream.seek(0, 2)
    file_size = uploaded_file.stream.tell()
    uploaded_file.stream.seek(0)

    if file_size > MAX_FILE_SIZE:
        return "File size exceeds maximum allowed size", 400

    if not validate_pdf_content(uploaded_file.stream):
        return "Invalid PDF file", 400

    random_filename = f"{secrets.token_urlsafe(16)}.pdf"
    destination = (UPLOAD_FOLDER / random_filename).resolve()

    if UPLOAD_FOLDER not in destination.parents:
        return "Invalid upload destination", 400

    uploaded_file.save(destination)

    return redirect("/pdf/view")