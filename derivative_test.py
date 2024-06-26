import unittest

from derivative import central_difference_derivative


class TestDerivative(unittest.TestCase):

    def test_central_difference_derivative_of_constant(self):
        f = lambda x: 10
        x = 0
        self.assertAlmostEqual(central_difference_derivative(f, dx="x", x=x), 0)

    def test_central_difference_derivation_of_linear(self):
        f = lambda x: 2 * x
        x = 0
        self.assertAlmostEqual(central_difference_derivative(f, dx="x", x=x), 2)

        f = lambda x: 7 * x
        x = 3
        self.assertAlmostEqual(central_difference_derivative(f, dx="x", x=x), 7)

    def test_central_difference_derivation_of_quadratic(self):
        f = lambda x: 2 * x**2
        x = 0
        self.assertAlmostEqual(central_difference_derivative(f, dx="x", x=x), 0)

        f = lambda x: 2 * x**2
        x = 1
        self.assertAlmostEqual(central_difference_derivative(f, dx="x", x=x), 4)

    def test_multi_parameter_central_difference_of_constant(self):
        f = lambda x, y: 10
        x = 0
        y = 0
        self.assertAlmostEqual(central_difference_derivative(f, dx="x", x=x, y=y), 0)

    def test_multi_parameter_central_difference_of_linear(self):
        f = lambda x, y: 10 * y
        x = 0
        y = 0
        self.assertAlmostEqual(central_difference_derivative(f, dx="x", x=x, y=y), 0)

        x = 0
        y = 0
        self.assertAlmostEqual(central_difference_derivative(f, dx="y", x=x, y=y), 10)

    def test_non_existing_parameter_returns_zero(self):
        f = lambda x: 10 * x
        x = 0
        y = 0
        self.assertAlmostEqual(central_difference_derivative(f, dx="y", x=x, y=y), 0)

        f = lambda x: 10 * x
        x = 0
        self.assertAlmostEqual(central_difference_derivative(f, dx="y", x=x), 0)
