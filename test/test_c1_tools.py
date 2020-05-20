import itertools
import math

import numpy
from scipy.special import legendre

import orthopy


def test_clenshaw(tol=1.0e-14):
    n = 5
    iterator = orthopy.c1.legendre.IteratorRCMonic("monic")
    _, alpha, beta = numpy.array(list(itertools.islice(iterator, 5))).T

    t = 1.0

    a = numpy.ones(n + 1)
    value = orthopy.c1.clenshaw(a, alpha, beta, t)

    ref = math.fsum([numpy.polyval(legendre(i, monic=True), t) for i in range(n + 1)])
    assert abs(value - ref) < tol


if __name__ == "__main__":
    test_clenshaw()
