from flask import Flask, request
import ast

app = Flask(__name__)

@app.route("/evalcode")
def eval_code():
    '''
    Get the user input from the request, 
    validate it as a safe literal expression, then evaluate it.
    '''
    input_str = request.args.get('input')
    
    if not input_str:
        return "No input provided", 400
    
    try:
        # Parse the input to ensure it's a valid Python literal
        parsed = ast.parse(input_str, mode='eval')
        
        # Check that the parsed AST only contains safe literal nodes
        for node in ast.walk(parsed):
            if not isinstance(node, (
                ast.Expression, ast.Load, ast.Store,
                ast.Constant, ast.Num, ast.Str, ast.Bytes,
                ast.List, ast.Tuple, ast.Set, ast.Dict,
                ast.NameConstant, ast.UnaryOp, ast.UAdd, ast.USub,
                ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div,
                ast.Mod, ast.Pow, ast.FloorDiv
            )):
                return "Invalid input: only literal expressions are allowed", 400
        
        # Use literal_eval for safe evaluation
        result = ast.literal_eval(input_str)
        return f"Result: {result}"
    
    except (ValueError, SyntaxError, TypeError) as e:
        return f"Invalid input: {str(e)}", 400