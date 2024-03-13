import ast


def to_puml(node, indent=''):
    node_name = node.id if isinstance(node, ast.Name) else type(node).__name__
    result = indent + '* ' + node_name + '\n'
    for child in ast.iter_child_nodes(node):
        result += to_puml(child, indent + '*')
    return result


def tree_to_puml(tree_):
    return '@startmindmap\n' + to_puml(tree_) + '@endmindmap'


if __name__ == '__main__':
    formula = 'x/(y**2*cos(PI/2))'
    # Parse the formula to an AST
    tree = ast.parse(formula)
    # Print the tree
    # print(ast.dump(tree))
    print(tree_to_puml(tree))
