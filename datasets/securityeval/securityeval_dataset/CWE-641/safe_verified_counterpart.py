from flask import request, send_file, Flask, abort
from pathlib import Path

app = Flask(__name__)

ALLOWED_DOWNLOAD_DIR = Path("/var/www/downloads").resolve()

SAFE_FILE_MAP = {
    "document": "document.pdf",
    "report": "reports/report.pdf",
    "data": "data/data.csv",
    "image": "images/image.png"
}


@app.route("/download")
def download():
    '''
    Get a safe file identifier from the request and send the approved file
    to the client as an attachment.
    '''
    file_id = request.args.get("file", "")

    if file_id not in SAFE_FILE_MAP:
        abort(403)

    requested_path = (ALLOWED_DOWNLOAD_DIR / SAFE_FILE_MAP[file_id]).resolve()

    if ALLOWED_DOWNLOAD_DIR not in requested_path.parents:
        abort(403)

    if not requested_path.is_file():
        abort(404)

    return send_file(str(requested_path), as_attachment=True)