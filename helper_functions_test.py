import unittest

import numpy as np
from numpy.testing import assert_array_equal

from helper_functions import (
    delete_columns_from_matrix,
    delete_rows_and_columns_from_matrix,
    delete_rows_from_matrix,
)


class TestHelperFunctions(unittest.TestCase):

    def assert_matrix_was_not_modified(self, m):
        assert_array_equal(m, np.arange(12).reshape(3, 4))

    def test_delete_rows_from_matrix(self):
        m = np.arange(12).reshape(3, 4)

        assert_array_equal(
            delete_rows_from_matrix(m, indices_to_delete=[0, 1]),
            np.array([[8, 9, 10, 11]]),
        )
        self.assert_matrix_was_not_modified(m)

    def test_delete_columns_from_matrix(self):
        m = np.arange(12).reshape(3, 4)

        assert_array_equal(
            delete_columns_from_matrix(m, indices_to_delete=[0, 1]),
            np.array([[2, 3], [6, 7], [10, 11]]),
        )
        self.assert_matrix_was_not_modified(m)

    def test_delete_rows_and_columns_from_matrix(self):
        m = np.arange(12).reshape(3, 4)

        assert_array_equal(
            delete_rows_and_columns_from_matrix(m, indices_to_delete=[1]),
            np.array(
                [
                    [0, 2, 3],
                    [8, 10, 11],
                ]
            ),
        )
        self.assert_matrix_was_not_modified(m)

    def test_duplication_in_indices_doesnt_affect_outcome(self):
        m = np.arange(12).reshape(3, 4)

        assert_array_equal(
            delete_rows_and_columns_from_matrix(m, indices_to_delete=[1, 1, 1]),
            np.array(
                [
                    [0, 2, 3],
                    [8, 10, 11],
                ]
            ),
        )
        self.assert_matrix_was_not_modified(m)
