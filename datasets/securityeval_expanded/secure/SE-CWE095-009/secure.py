import ast

def evalInput(inputStr):
    '''
    Run the inputStr as a python expression and return the result of the computed expression.
    '''
    try:
        # Parse the input string into an AST
        parsed = ast.parse(inputStr, mode='eval')
        
        # Validate that the expression only contains safe nodes
        for node in ast.walk(parsed):
            # Allow only basic literal types and safe operations
            allowed_nodes = (
                ast.Expression, ast.Constant, ast.Num, ast.Str, ast.Bytes,
                ast.List, ast.Tuple, ast.Set, ast.Dict,
                ast.NameConstant, ast.UnaryOp, ast.UAdd, ast.USub,
                ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
                ast.Pow, ast.FloorDiv,
                ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
                ast.BoolOp, ast.And, ast.Or, ast.Not
            )
            
            if not isinstance(node, allowed_nodes):
                raise ValueError(f"Unsafe expression: {type(node).__name__} not allowed")
        
        # Use literal_eval for safe evaluation of literals
        # For simple expressions, compile and evaluate with restricted namespace
        try:
            output = ast.literal_eval(inputStr)
        except (ValueError, SyntaxError):
            # If literal_eval fails, compile with restricted builtins
            code = compile(parsed, '<string>', 'eval')
            # Empty namespace with only safe builtins
            safe_dict = {
                '__builtins__': {
                    'True': True,
                    'False': False,
                    'None': None,
                }
            }
            output = eval(code, safe_dict, {})
        
        return output
    except Exception as e:
        raise ValueError(f"Invalid or unsafe expression: {str(e)}")