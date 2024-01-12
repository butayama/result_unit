""" Test rename Master to Main
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
Variables as Exponent: raising a unit to the power of another unit is not commonly used or meaningful.
A VariableExponentError will be raised.
These rules must be interpreted along with the correct mathematical order of operations (BIDMAS/BODMAS/PEDMAS).
"""

import ast

from pint import UndefinedUnitError, UnitRegistry
import sympy

symbol_dict = {}
ureg = UnitRegistry()
UnitQuantity = ureg.Quantity


class UnitError(Exception):
    """Exception raised for errors in the input unit."""

    def __init__(self, message="Invalid unit"):
        self.message = message
        super().__init__(self.message)


class SecondOperandError(Exception):
    """Exception raised if a BinOp Pow Module has a Variable as right child"""

    def __init__(self, message="BinOp Pow Module has a Variable as right child: raising a unit to the power of another "
                               "unit is not commonly used or meaningful."):
        self.message = message
        super().__init__(self.message)


class VariableExponentError(Exception):
    """Exception raised if a BinOp Module has no left and right child: The second operand is missing"""

    def __init__(self, message="BinOp Module has no left and right child: The second operand is missing"):
        self.message = message
        super().__init__(self.message)


def create_symbol(symbol_dict_, symbol_name):
    if isinstance(symbol_name, int):
        # convert integer constant to string and store it in symbol_dict
        symbol_name = str(symbol_name)
        symbol_dict_[symbol_name] = symbol_name
    elif symbol_name != '':  # check if the symbol name is not an empty string
        if symbol_name and symbol_name not in symbol_dict:
            try:
                # Creates a Quantity with magnitude 1 and the specified unit
                test_quantity = UnitQuantity(1, symbol_name)
            except UndefinedUnitError as e:
                raise UnitError(f"Dimension {symbol_name} is not defined in the pint module") from e
            print(f"{symbol_name} = {test_quantity} is validated as defined in the `pint` module")
            symbol_dict_[symbol_name] = sympy.symbols(symbol_name)
    return symbol_name

def visit_node(node, indent=''):
    """Utility function to visit and print details of an ast node"""

    # print type and attributes of current node
    # print(f'{indent}{type(node).__name__} : {node.__dict__}')

    # iterate over children of current node
    for child_node in ast.iter_child_nodes(node):
        visit_node(child_node, indent + '  ')


def post_order(dimensions, formula):
    # print(f"Post order traversing starts here")
    # ToDo Variablen als Exponent
    ast_tree = ast.parse(formula)
    visit_node(ast_tree)
    stack = [(False, ast_tree.body[0].value)]
    out = []

    while stack:
        visit, node = stack.pop()
        if isinstance(node, ast.Constant):
            value = node.value
            out.append(value)
        if isinstance(node, ast.Name):
            dim = dimensions.get(node.id, None)
            out.append(dim)



        elif isinstance(node, ast.BinOp) or isinstance(node, ast.UnaryOp):
            if visit:
                if len(out) >= 2:
                    right_dim = out.pop()
                    if isinstance(right_dim, int) and not isinstance(node.op, ast.Pow):
                        right_dim = ''
                    else:
                        try:
                            right_dim = create_symbol(symbol_dict, right_dim)
                        except UnitError:
                            return 'Dimension Mismatch'
                    if not isinstance(node, ast.UnaryOp):
                        left_dim = out.pop()
                    elif isinstance(left_dim, int):
                        left_dim = '1'
                    else:
                        try:
                            left_dim = create_symbol(symbol_dict, left_dim)
                        except UnitError:
                            return 'Dimension Mismatch'
                    if isinstance(node.op, ast.Mult):
                        if right_dim == '':
                            result_dim = left_dim
                        else:
                            result_dim = left_dim + '*' + right_dim
                    elif isinstance(node.op, ast.Add) or isinstance(node.op, ast.Sub):
                        if right_dim == '':
                            result_dim = left_dim
                        else:
                            result_dim = left_dim if left_dim == right_dim else 'Dimension Mismatch'
                    elif isinstance(node.op, ast.Div):
                        if right_dim == '':
                            result_dim = left_dim
                        else:
                            result_dim = left_dim + '/' + right_dim
                    elif isinstance(node.op, ast.Pow):
                        result_dim = left_dim + '**' + right_dim
                    elif isinstance(node.op, ast.USub):
                        result_dim = right_dim
                    else:
                        result_dim = 'Unhandled Operator'
                    out.append(result_dim)
            else:
                if isinstance(node, ast.UnaryOp):
                    stack.extend([(True, node)])
                else:
                    stack.extend([(True, node), (False, node.right), (False, node.left)])
        else:
            print(f"Skipping node type {type(node)} during post_order() traversal.")

    return out[0]


def main(dimensions, formula):
    r_dim = post_order(dimensions, formula)
    print(f"r_dim = {r_dim if r_dim else 'None'}")

    # Convert the string to a symbolic expression using the mapping
    base_dim = sympy.sympify(r_dim, locals=symbol_dict)
    print(f" base_dim = {base_dim}")


if __name__ == '__main__':
    # DIMENSIONS = {'x': 'm', 'y': 'm'}
    DIMENSIONS = {'x': 'm', 'y': 's'}
    # DIMENSIONS = {"x": "m", "y": "m", "z": "m/m"}
    main(DIMENSIONS, "5*x**2 / y**2 + 7")
