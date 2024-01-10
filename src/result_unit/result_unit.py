"""
result_unit.py
Abstract Syntax Tree code with stack based post order traversal method.
Rules to be followed:
    formula1 = "x + y"  # unit: m + m = m
        formula1.1 = "x + y"  # unit: m + s = ERROR
    formula2 = "x - y"  # unit: m - m = m
        formula1.1 = "x - y"  # unit: m + s = ERROR
    formula3 = "x * y"  # unit: m * s = ms
    formula4 = "x / y"  # unit: m / s = m/s
    formula5 = "x**2"   # unit: m^2
    formula6 = "(x + y) / y"  # unit: (m + s) / s = dimensionless

These rules must be interpreted along with the correct mathematical order of operations (BIDMAS/BODMAS/PEDMAS).
"""

import ast

from pint import UndefinedUnitError, UnitRegistry
import sympy

symbol_dict = {}
DIMENSIONS = {'x': 'm', 'y': 'm'}
ureg = UnitRegistry()
UnitQuantity = ureg.Quantity


class UnitError(Exception):
    """Exception raised for errors in the input unit."""

    def __init__(self, message="Invalid unit"):
        self.message = message
        super().__init__(self.message)


def create_symbol(symbol_dict, symbol_name):
    if symbol_name not in symbol_dict:
        try:
            test_quantity = UnitQuantity(1, symbol_name)  # Creates a Quantity with magnitude 1 and the specified unit
        except UndefinedUnitError as e:
            raise UnitError(f"Dimension {symbol_name} is not defined in the pint module") from e
        print(f"{symbol_name} = {test_quantity} is validated as defined in the `pint` module")
        symbol_dict[symbol_name] = sympy.symbols(symbol_name)


def visit_node(node, indent=''):
    """Utility function to visit and print details of an ast node"""

    # print type and attributes of current node
    print(f'{indent}{type(node).__name__} : {node.__dict__}')

    # iterate over children of current node
    for child_node in ast.iter_child_nodes(node):
        visit_node(child_node, indent + '  ')


def post_order(formula):
    print(f"Post order traversing starts here")
    ast_tree = ast.parse(formula)
    visit_node(ast_tree)
    stack = [(False, ast_tree.body[0].value)]
    out = []

    while stack:
        visit, node = stack.pop()
        if isinstance(node, ast.Name):
            dim = DIMENSIONS.get(node.id, None)
            out.append(dim)
        elif isinstance(node, ast.BinOp):
            if visit:
                right_dim = out.pop()
                create_symbol(symbol_dict, right_dim)
                left_dim = out.pop()
                create_symbol(symbol_dict, left_dim)
                if isinstance(node.op, ast.Mult):
                    result_dim = left_dim + '*' + right_dim
                elif isinstance(node.op, ast.Add) or isinstance(node.op, ast.Sub):
                    result_dim = left_dim if left_dim == right_dim else 'Dimension Mismatch'
                elif isinstance(node.op, ast.Div):
                    result_dim = left_dim + '/' + right_dim if left_dim != right_dim else ''
                else:
                    result_dim = 'Unhandled Operator'
                out.append(result_dim)
            else:
                stack.extend([(True, node), (False, node.right), (False, node.left)])
        else:
            print(f"Skipping node type {type(node)} during post_order() traversal.")

    return out[0]


def main(formula):
    r_dim = post_order(formula)
    print(f"r_dim = {r_dim if r_dim else 'None'}")

    # Convert the string to a symbolic expression using the mapping
    base_dim = sympy.sympify(r_dim, locals=symbol_dict)
    print(f" base_dim = {base_dim}")


if __name__ == '__main__':
    main("x * y / (x + y)")
