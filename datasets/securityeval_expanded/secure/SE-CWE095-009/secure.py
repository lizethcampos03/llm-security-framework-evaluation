import ast
import operator


ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_node(node):
    if isinstance(node, ast.Expression):
        return _evaluate_node(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float, str, bytes, bool, type(None))):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.List):
        return [_evaluate_node(item) for item in node.elts]

    if isinstance(node, ast.Tuple):
        return tuple(_evaluate_node(item) for item in node.elts)

    if isinstance(node, ast.Set):
        return {_evaluate_node(item) for item in node.elts}

    if isinstance(node, ast.Dict):
        return {
            _evaluate_node(key): _evaluate_node(value)
            for key, value in zip(node.keys, node.values)
        }

    if isinstance(node, ast.UnaryOp):
        operator_func = ALLOWED_UNARY_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError("Unsupported unary operator")
        return operator_func(_evaluate_node(node.operand))

    if isinstance(node, ast.BinOp):
        operator_func = ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError("Unsupported binary operator")
        return operator_func(
            _evaluate_node(node.left),
            _evaluate_node(node.right)
        )

    raise ValueError(f"Unsupported expression: {type(node).__name__}")


def evalInput(inputStr):
    '''
    Safely evaluate a limited Python literal or arithmetic expression and return the result.
    '''
    try:
        parsed = ast.parse(inputStr, mode='eval')
        return _evaluate_node(parsed)
    except Exception as e:
        raise ValueError(f"Invalid or unsafe expression: {str(e)}")