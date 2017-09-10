# -*- coding: utf-8 -*-
#
from mpmath import mp
from mpmath.matrices.eigen_symmetric import tridiag_eigen
import numpy
import scipy
from scipy.linalg import eig_banded
import sympy

from . import recurrence_coefficients


def custom(alpha, beta, mode='mpmath', decimal_places=32):
    '''Compute the Gauss nodes and weights from the recurrence coefficients
    associated with a set of orthogonal polynomials. See [2] and
    <http://www.scientificpython.net/pyblog/radau-quadrature>.
    '''

    if mode == 'sympy':
        x, w = _gauss_from_coefficients_sympy(alpha, beta)
    elif mode == 'mpmath':
        x, w = _gauss_from_coefficients_mpmath(alpha, beta, decimal_places)
    else:
        assert mode == 'numpy'
        x, w = _gauss_from_coefficients_numpy(alpha, beta)
    return x, w


def _sympy_tridiag(a, b):
    '''Creates the tridiagonal sympy matrix tridiag(b, a, b).
    '''
    n = len(a)
    assert n == len(b)
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = a[i]
    for i in range(n-1):
        A[i][i+1] = b[i+1]
        A[i+1][i] = b[i+1]
    return sympy.Matrix(A)


def _gauss_from_coefficients_sympy(alpha, beta):
    assert isinstance(alpha[0], sympy.Rational)
    # Construct the triadiagonal matrix [sqrt(beta), alpha, sqrt(beta)]
    A = _sympy_tridiag(alpha, [sympy.sqrt(bta) for bta in beta])

    # Extract points and weights from eigenproblem
    x = []
    w = []
    for item in A.eigenvects():
        val, multiplicity, vec = item
        assert multiplicity == 1
        assert len(vec) == 1
        vec = vec[0]
        x.append(val)
        norm2 = sum([v**2 for v in vec])
        w.append(sympy.simplify(beta[0] * vec[0]**2 / norm2))
    # sort by x
    order = sorted(range(len(x)), key=lambda i: x[i])
    x = [x[i] for i in order]
    w = [w[i] for i in order]
    return x, w


def _gauss_from_coefficients_mpmath(alpha, beta, decimal_places):
    mp.dps = decimal_places

    # Create vector cut of the first value of beta
    n = len(alpha)
    b = mp.zeros(n, 1)
    for i in range(n-1):
        b[i] = mp.sqrt(beta[i+1])

    z = mp.zeros(1, n)
    z[0, 0] = 1
    d = mp.matrix(alpha)
    tridiag_eigen(mp, d, b, z)

    # nx1 matrix -> list of sympy floats
    x = numpy.array([sympy.Float(xx) for xx in d])
    w = numpy.array([beta[0] * mp.power(ww, 2) for ww in z])
    return x, w


def _gauss_from_coefficients_numpy(alpha, beta):
    assert isinstance(alpha, numpy.ndarray)
    assert isinstance(beta, numpy.ndarray)
    A = numpy.vstack((numpy.sqrt(beta), alpha))
    # TODO keep an eye on https://github.com/scipy/scipy/pull/7810
    x, V = eig_banded(A, lower=False)
    w = beta[0]*scipy.real(scipy.power(V[0, :], 2))
    return x, w


def legendre(n, decimal_places):
    alpha, beta = recurrence_coefficients.legendre(n, mode='sympy')
    return custom(alpha, beta, mode='mpmath', decimal_places=decimal_places)


def jacobi(a, b, n, decimal_places):
    alpha, beta = recurrence_coefficients.jacobi(n, a, b, mode='sympy')
    return custom(alpha, beta, mode='mpmath', decimal_places=decimal_places)


def chebyshev1(n, decimal_places):
    # There are explicit representations, too, but for the sake of consistency
    # go for the recurrence coefficients approach here.
    alpha, beta = recurrence_coefficients.chebyshev1(n)
    beta[0] = sympy.N(beta[0], decimal_places)
    return custom(alpha, beta, mode='mpmath', decimal_places=decimal_places)


def chebyshev2(n, decimal_places):
    # There are explicit representations, too, but for the sake of consistency
    # go for the recurrence coefficients approach here.
    alpha, beta = recurrence_coefficients.chebyshev2(n)
    beta[0] = sympy.N(beta[0], decimal_places)
    return custom(alpha, beta, mode='mpmath', decimal_places=decimal_places)


def laguerre(n, decimal_places):
    alpha, beta = recurrence_coefficients.laguerre(n)
    return custom(alpha, beta, mode='mpmath', decimal_places=decimal_places)


def laguerre_generalized(n, a, decimal_places):
    alpha, beta = recurrence_coefficients.laguerre_generalized(n, a)
    return custom(alpha, beta, mode='mpmath', decimal_places=decimal_places)


def hermite(n, decimal_places):
    alpha, beta = recurrence_coefficients.hermite(n)
    beta[0] = sympy.N(beta[0], decimal_places)
    return custom(alpha, beta, mode='mpmath', decimal_places=decimal_places)