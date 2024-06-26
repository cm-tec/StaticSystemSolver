import numpy as np

from static_system_solver import StaticSystemSolver

from numpy.testing import assert_array_equal, assert_allclose


class ExampleStaticSystem:

    def __init__(self, static_system, essential_ndfos) -> None:
        self.static_system = static_system
        self.essential_ndofs = essential_ndfos

    def assert_size_of_k_equal_essential_ndofs(self):
        solver = StaticSystemSolver(self.static_system)

        assert_array_equal(np.shape(solver.get_k()), (9, 9))
