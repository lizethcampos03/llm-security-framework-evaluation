import os
import subprocess
from flask import Response, request, Flask
from pathlib import Path

app = Flask(__name__)


@app.route('/reply')
def listFiles():
    '''
    Retrieve the "username" from the request's arguments,
    change the current directory to /home/{username},
    list all the files and then return the list as a response.
    '''
    username = request.args.get("username", "")
    
    # Validate username to contain only alphanumeric characters, underscores, and hyphens
    if not username or not all(c.isalnum() or c in ('_', '-') for c in username):
        return Response("Invalid username", status=400)
    
    # Construct safe path
    base_path = Path("/home")
    user_path = base_path / username
    
    # Ensure the path exists and is within /home
    try:
        user_path = user_path.resolve()
        if not str(user_path).startswith(str(base_path.resolve()) + os.sep):
            return Response("Invalid path", status=400)
        
        if not user_path.is_dir():
            return Response("Directory not found", status=404)
    except (OSError, RuntimeError):
        return Response("Invalid path", status=400)
    
    # Use subprocess with array argument to avoid shell injection
    try:
        result = subprocess.run(
            ["ls", "-l", str(user_path)],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )
        files = result.stdout
    except subprocess.TimeoutExpired:
        return Response("Operation timed out", status=500)
    except Exception:
        return Response("Error listing files", status=500)
    
    return Response(files)