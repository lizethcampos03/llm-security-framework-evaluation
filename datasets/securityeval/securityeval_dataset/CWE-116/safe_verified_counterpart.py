from flask import Response, request, Flask
from pathlib import Path

app = Flask(__name__)

APPROVED_USER_DIRECTORIES = {
    "alice": Path("/home/alice").resolve(),
    "bob": Path("/home/bob").resolve(),
    "service": Path("/home/service").resolve()
}


@app.route("/reply")
def listFiles():
    '''
    Retrieve an approved user identifier from the request arguments,
    list files in the approved directory, and return the list as a response.
    '''
    username = request.args.get("username", "")

    if username not in APPROVED_USER_DIRECTORIES:
        return Response("Invalid username", status=400)

    user_path = APPROVED_USER_DIRECTORIES[username]

    if not user_path.is_dir():
        return Response("Directory not found", status=404)

    try:
        files = sorted(item.name for item in user_path.iterdir())
    except OSError:
        return Response("Error listing files", status=500)

    return Response("\n".join(files), mimetype="text/plain")