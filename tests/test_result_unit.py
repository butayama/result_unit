import pytest
from sympy import simplify, sympify
from result_unit import post_order

FORMULAS = ["x + y", "x - y", "x * y", "x / y", "x**2", "(x + y) / y", "(x + y) + y"]


@pytest.mark.parametrize("dimensions, formula, expected", [
    ({"x": "m", "y": "s"}, "x + y", 'Dimension Mismatch'),
    ({"x": "m", "y": "m"}, "x + y", 'm'),
    ({"x": "m", "y": "s"}, "x - y", 'Dimension Mismatch'),
    ({"x": "m", "y": "m"}, "x - y", 'm'),
    ({"x": "m", "y": "s"}, "x * y", 'm*s'),
    ({"x": "m", "y": "m"}, "x * y", 'm*m'),
    ({"x": "m", "y": "s"}, "x / y", 'm/s'),
    ({"x": "m", "y": "m"}, "x / y", ''),
    ({"x": "m", "y": "s"}, "x ** 2", 'm*m'),  # 996
    ({"x": "m", "y": "m"}, "x ** 3", 'm*m*m'),
    ({"x": "m", "y": "s"}, "x * y / (x + y)", 'Dimension Mismatch'),    # 999
    ({"x": "m", "y": "m"}, "x * y / (x + y)", 'm*m/m'),                     # 999
    ({"x": "m", "y": "s"}, "x**2 / y", 'm*m/s'),    # 998
    ({"x": "m", "y": "m"}, "x**2 / y", 'm'),        # 998
    ({"x": "m", "y": "s"}, "5*x**2 / y**2 + 7", 'm*m/s'),    # 997 Wie Einheit für Skalare zuordnen???
    ({"x": "m", "y": "m"}, "5*x**2 / y**2 + 7", 'm'),        # 997
    ({"x": "m", "y": "s"}, "x**2 / y", 'm*m/s'),
    ({"x": "m", "y": "m"}, "x**2 / y", 'm'),
    ({"x": "m", "y": "s"}, "(x + y) / y", 'Dimension Mismatch'),
    ({"x": "m", "y": "m"}, "(x + y) / y", ''),
    ({"x": "m", "y": "s"}, "(x + y) + y", 'Dimension Mismatch'),
    ({"x": "m", "y": "m"}, "(x + y) + y", 'm'),
])
def test_post_order(dimensions, formula, expected):
    r_dim = post_order(dimensions, formula)
    assert r_dim == expected, f"For formula: {formula}, expected: {expected}, but got: {r_dim}"


def test_simplify_equivalent_formulas():
    for formula in FORMULAS:
        r_dim1 = post_order(formula)
        r_dim2 = post_order(str(simplify(sympify(formula))))
        assert r_dim1 == r_dim2, f"{formula} != {str(simplify(sympify(formula)))} but they should be equivalent"


if __name__ == '__main__':
    pytest.main(['-vv', '-s', __file__])

