import pytest
from sympy import simplify, sympify
from result_unit.result_unit import post_order

FORMULAS = ["x + y", "x - y", "x * y", "x / y", "x**2", "(x + y) / y", "(x + y) + y"]


@pytest.mark.parametrize("dimensions, formula, expected", [
    ({"x": "m", "y": "s"}, "x + y", 'Dimension Mismatch'),
    ({"x": "m", "y": "m"}, "x + y", 'm'),
    ({"x": "m", "y": "m", "z": "m"}, "x + y + z", 'm'),
    ({"x": "m", "y": "s"}, "x - y", 'Dimension Mismatch'),
    ({"x": "m", "y": "m"}, "x - y", 'm'),
    ({"x": "m", "y": "s"}, "x * y", 'm*s'),
    ({"x": "m", "y": "m"}, "x * y", 'm*m'),
    ({"x": "m", "y": "m", "z": "m"}, "x * y * z", 'm*m*m'),
    ({"x": "m", "y": "s"}, "x / y", 'm/s'),
    ({"x": "m", "y": "m"}, "x / y", 'm/m'),
    ({"x": "m", "y": "m", "z": "m"}, "x / y / z", 'm/m/m'),
    ({"x": "m", "y": "m", "z": ""}, "x / y + z", 'm/m'),
    ({"x": "m", "y": "m", "z": ""}, "-z + x / y", 'm/m'),  # 995
    ({"x": "m", "y": "s"}, "x ** 2", 'm**2'),  # 996
    ({"x": "m", "y": "m"}, "x ** 3", 'm**3'),
    ({"x": "m", "y": "s"}, "x * y / (x + y)", 'Dimension Mismatch'),    # 999
    ({"x": "m", "y": "m"}, "x * y / (x + y)", 'm*m/m'),                     # 999
    ({"x": "m", "y": "s"}, "x**2 / y", 'm**2/s'),    # 998
    ({"x": "m", "y": "m"}, "x**2 / y", 'm**2/m'),        # 998
    ({"x": "m", "y": "s"}, "5*x**2 / y**2 + 7", 'm**2/s**2'),    # 997
    ({"x": "m", "y": "m"}, "5*x**2 / y**2 + 7", 'm**2/m**2'),        # 997
    ({"x": "m", "y": "s"}, "5*7*x**2 / y**2 + 7", 'm**2/s**2'),
    ({"x": "m", "y": "s"}, "(x + y) / y", 'Dimension Mismatch'),
    ({"x": "m", "y": "m"}, "(x + y) / y", 'm/m'),
    ({"x": "m", "y": "s"}, "(x + y) + y", 'Dimension Mismatch'),
    ({"x": "m", "y": "m"}, "(x + y) + y", 'm'),
])
def test_post_order(dimensions, formula, expected):
    r_dim = post_order(dimensions, formula)
    assert r_dim == expected, f"For formula: {formula}, expected: {expected}, but got: {r_dim}"


def test_simplify_equivalent_formulas():
    for formula in FORMULAS:
        r_dim1 = post_order({"x": "m", "y": "s"}, formula)
        r_dim2 = post_order({"x": "m", "y": "s"}, str(simplify(sympify(formula))))
        assert r_dim1 == r_dim2, f"{formula} != {str(simplify(sympify(formula)))} but they should be equivalent"


if __name__ == '__main__':
    pytest.main(['-vv', '-s', __file__])

