from flask import Flask, request, redirect, abort

app = Flask(__name__)

SAFE_REDIRECTS = {
    "home": "/home",
    "dashboard": "/dashboard",
    "profile": "/profile"
}


@app.route("/")
def redirect_user():
    '''
    Redirect the user to an approved internal page selected by a safe redirect identifier.
    '''
    target = request.args.get("target", "")

    if target not in SAFE_REDIRECTS:
        abort(400)

    return redirect(SAFE_REDIRECTS[target], code=302)