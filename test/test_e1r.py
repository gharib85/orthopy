import numpy
import pytest
import sympy
from sympy import oo

import orthopy


def _integrate(f, alpha, x):
    return sympy.integrate(f * x ** alpha * sympy.exp(-x), (x, 0, +oo))


@pytest.mark.parametrize("alpha", [0, 1])
def test_integral0(alpha, n=4):
    x = sympy.Symbol("x")
    vals = orthopy.e1r.tree(n, x, alpha=alpha, scaling="normal", symbolic=True)

    assert _integrate(vals[0], alpha, x) == 1
    for val in vals[1:]:
        assert _integrate(val, alpha, x) == 0


@pytest.mark.parametrize("alpha", [0, 1])
@pytest.mark.parametrize("scaling", ["monic", "classical", "normal"])
def test_orthogonality(alpha, scaling, n=4):
    x = sympy.Symbol("x")
    tree = orthopy.e1r.tree(n, x, scaling, alpha=alpha, symbolic=True)
    vals = tree * numpy.roll(tree, 1, axis=0)

    for val in vals:
        assert _integrate(val, alpha, x) == 0


@pytest.mark.parametrize("alpha", [0, 1])
def test_normality(alpha, n=4):
    x = sympy.Symbol("x")
    tree = orthopy.e1r.tree(n, x, "normal", alpha=alpha, symbolic=True)
    for val in tree:
        assert _integrate(val ** 2, alpha, x) == 1


def test_show():
    orthopy.e1r.show(L=4)


if __name__ == "__main__":
    test_show()
    # import matplotlib.pyplot as plt
    # plt.show()
    # plt.savefig("e1r.png", transparent=True)
