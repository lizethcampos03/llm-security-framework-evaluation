from flask import Flask, request
import ast

app = Flask(__name__)


@app.route("/evalcode")
def eval_code():
    '''
    Get user input from the request,
    validate it as a safe literal expression, then evaluate it.
    '''
    input_str = request.args.get("input")

    if not input_str:
        return "No input provided", 400

    try:
        ast.literal_eval(input_str)
    except (ValueError, SyntaxError, TypeError):
        return "Invalid input", 400

    result = ast.literal_eval(input_str)
    return f"Result: {result}", 200