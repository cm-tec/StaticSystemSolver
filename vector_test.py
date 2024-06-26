import unittest

import numpy as np
from vector import vector

from numpy.testing import assert_array_equal


class TestVector(unittest.TestCase):

    def test_vector_creation(self):
        v = vector()
        assert_array_equal(v, np.array([]))

        v = vector(12, 3)
        assert_array_equal(v, np.array([12, 3]))

        v = vector(1, 2, 3)
        assert_array_equal(v, np.array([1, 2, 3]))

        v = vector(4, -2, 3)
        assert_array_equal(v, np.array([4, -2, 3]))
