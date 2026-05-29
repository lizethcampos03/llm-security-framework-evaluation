from flask import Response, request, Flask
from pathlib import Path

app = Flask(__name__)

BASE_HOME_DIR = Path("/home").resolve()


@app.route("/reply")
def listFiles():
    '''
    Retrieve the username from the request arguments,
    validate it, list files in the approved user directory,
    and return the list as a response.
    '''
    username = request.args.get("username", "")

    if not username or not all(c.isalnum() or c in ("_", "-") for c in username):
        return Response("Invalid username", status=400)

    user_path = (BASE_HOME_DIR / username).resolve()

    if BASE_HOME_DIR not in user_path.parents:
        return Response("Invalid path", status=400)

    if not user_path.is_dir():
        return Response("Directory not found", status=404)

    try:
        files = sorted(
            item.name
            for item in user_path.iterdir()
        )
    except OSError:
        return Response("Error listing files", status=500)

    return Response("\n".join(files), mimetype="text/plain")