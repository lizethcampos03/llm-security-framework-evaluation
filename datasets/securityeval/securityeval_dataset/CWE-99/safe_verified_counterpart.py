from flask import request, send_file, Flask, abort
from pathlib import Path

app = Flask(__name__)

SAFE_FILE_MAP = {
    "document": "document.pdf",
    "report": "report.xlsx",
    "data": "data.csv",
    "image": "image.png"
}


@app.route("/download")
def download():
    '''
    Read a safe file identifier from the request,
    and return the approved file contents as an attachment.
    '''
    file_id = request.args.get("file", "")

    if file_id not in SAFE_FILE_MAP:
        abort(403)

    static_dir = Path(app.static_folder).resolve()
    file_path = (static_dir / SAFE_FILE_MAP[file_id]).resolve()

    if static_dir not in file_path.parents and file_path != static_dir:
        abort(403)

    if not file_path.is_file():
        abort(404)

    return send_file(file_path, as_attachment=True)