import pytest
from sympy import simplify, sympify
from result_unit.result_unit import post_order

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
    ({"x": "m", "y": "s"}, "x**2", 'Unhandled Operator'),
    ({"x": "m", "y": "m"}, "x**2", 'Unhandled Operator'),
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
        r_dim1 = post_order(formula)
        r_dim2 = post_order(str(simplify(sympify(formula))))
        assert r_dim1 == r_dim2, f"{formula} != {str(simplify(sympify(formula)))} but they should be equivalent"


if __name__ == '__main__':
    pytest.main(['-vv', '-s', __file__])
from result_unit import result_unit
