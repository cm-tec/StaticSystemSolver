import unittest

import numpy as np
from numpy.testing import assert_array_equal, assert_allclose

from element_test import create_element
from utilities import (
    get_derived_F_global_of_element,
    get_derived_k_global_of_element,
    get_k,
    get_k_global,
    get_k_global_of_element,
    get_rotation_matrix,
    get_rotation_matrix_of_element,
)
from vector import vector


class TestUtilities(unittest.TestCase):

    def test_get_k(self):
        expected_k = np.array(
            [
                [1, 0, 0, -1, 0, 0],
                [0, 12, -6, 0, -12, -6],
                [0, -6, 4, 0, 6, 2],
                [-1, 0, 0, 1, 0, 0],
                [0, -12, 6, 0, 12, 6],
                [0, -6, 2, 0, 6, 4],
            ]
        )

        assert_array_equal(get_k(EA=1, EI=1, l=1), expected_k)

        expected_k = np.array(
            [
                [1 / 2, 0, 0, -1 / 2, 0, 0],
                [0, 12 / 8, -6 / 4, 0, -12 / 8, -6 / 4],
                [0, -6 / 4, 4 / 2, 0, 6 / 4, 2 / 2],
                [-1 / 2, 0, 0, 1 / 2, 0, 0],
                [0, -12 / 8, 6 / 4, 0, 12 / 8, 6 / 4],
                [0, -6 / 4, 2 / 2, 0, 6 / 4, 4 / 2],
            ]
        )

        assert_array_equal(get_k(EA=1, EI=1, l=2), expected_k)

        expected_k = np.array(
            [
                [2, 0, 0, -2, 0, 0],
                [0, 12, -6, 0, -12, -6],
                [0, -6, 4, 0, 6, 2],
                [-2, 0, 0, 2, 0, 0],
                [0, -12, 6, 0, 12, 6],
                [0, -6, 2, 0, 6, 4],
            ]
        )

        assert_array_equal(get_k(EA=2, EI=1, l=1), expected_k)

        expected_k = np.array(
            [
                [1, 0, 0, -1, 0, 0],
                [0, 24, -12, 0, -24, -12],
                [0, -12, 8, 0, 12, 4],
                [-1, 0, 0, 1, 0, 0],
                [0, -24, 12, 0, 24, 12],
                [0, -12, 4, 0, 12, 8],
            ]
        )

        assert_array_equal(get_k(EA=1, EI=2, l=1), expected_k)

    def test_get_0_angle_rotation_matrix(self):
        tau = np.array([[1, 0], [0, 1]])
        v = vector(2, 0)

        assert_array_equal(get_rotation_matrix(v), tau)

    def test_get_90_angle_rotation_matrix(self):
        tau = np.array([[0, -1], [1, 0]])
        v = vector(0, 4)

        assert_array_equal(get_rotation_matrix(v), tau)

    def test_get_45_angle_rotation_matrix(self):
        tau = np.array([[0.7071, -0.7071], [0.7071, 0.7071]])
        v = vector(7, 7)

        assert_allclose(get_rotation_matrix(v), tau, rtol=1e-3, atol=1e-3)

    def test_size_of_rotation_matrix_of_element_equal_6(self):

        assert_array_equal(
            np.shape(get_rotation_matrix_of_element(vector(0, 0))), (6, 6)
        )

    def test_get_rotation_matrix_of_element(self):
        expected_t = np.array(
            [
                [0.7071, -0.7071, 0, 0, 0, 0],
                [0.7071, 0.7071, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0.7071, -0.7071, 0],
                [0, 0, 0, 0.7071, 0.7071, 0],
                [0, 0, 0, 0, 0, 1],
            ]
        )

        assert_allclose(
            get_rotation_matrix_of_element(vector(1, 1)),
            expected_t,
            rtol=1e-3,
            atol=1e-3,
        )

    def test_get_k_global(self):
        expected_k = np.array(
            [
                [1, 0, 0, -1, 0, 0],
                [0, 12, -6, 0, -12, -6],
                [0, -6, 4, 0, 6, 2],
                [-1, 0, 0, 1, 0, 0],
                [0, -12, 6, 0, 12, 6],
                [0, -6, 2, 0, 6, 4],
            ]
        )

        assert_array_equal(get_k_global(EA=1, EI=1, l=1, v=vector(1, 0)), expected_k)

        expected_k = np.array(
            [
                [12, 0, -6, -12, 0, -6],
                [0, 1, 0, 0, -1, 0],
                [-6, 0, 4, 6, 0, 2],
                [-12, 0, 6, 12, 0, 6],
                [0, -1, 0, 0, 1, 0],
                [-6, 0, 2, 6, 0, 4],
            ]
        )
        assert_array_equal(get_k_global(EA=1, EI=1, l=1, v=vector(0, 1)), expected_k)

    def test_get_k_global_of_element(self):
        e = create_element()

        expected_k = np.array(
            [
                [1, 0, 0, -1, 0, 0],
                [0, 12, -6, 0, -12, -6],
                [0, -6, 4, 0, 6, 2],
                [-1, 0, 0, 1, 0, 0],
                [0, -12, 6, 0, 12, 6],
                [0, -6, 2, 0, 6, 4],
            ]
        )

        assert_array_equal(get_k_global_of_element(e), expected_k)

    def test_get_k_global_of_element_with_angle(self):
        e = create_element(p_k=vector(0, 1))

        expected_k = np.array(
            [
                [12, 0, -6, -12, 0, -6],
                [0, 1, 0, 0, -1, 0],
                [-6, 0, 4, 6, 0, 2],
                [-12, 0, 6, 12, 0, 6],
                [0, -1, 0, 0, 1, 0],
                [-6, 0, 2, 6, 0, 4],
            ]
        )

        assert_array_equal(get_k_global_of_element(e), expected_k)

    def test_get_derived_k_global_of_element(self):
        e = create_element(p_k=vector(1, 0))

        expected_k = np.array(
            [
                [1, 0, 0, -1, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [-1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ]
        )

        assert_allclose(
            get_derived_k_global_of_element(e, dx="EA"),
            expected_k,
            rtol=1e-8,
            atol=1e-8,
        )

        expected_k = np.array(
            [
                [0, 0, 0, 0, 0, 0],
                [0, 12, -6, 0, -12, -6],
                [0, -6, 4, 0, 6, 2],
                [0, 0, 0, 0, 0, 0],
                [0, -12, 6, 0, 12, 6],
                [0, -6, 2, 0, 6, 4],
            ]
        )

        assert_allclose(
            get_derived_k_global_of_element(e, dx="EI"),
            expected_k,
            rtol=1e-8,
            atol=1e-8,
        )

    def test_get_derived_F_global_of_element(self):
        expected_F = np.zeros(6)
        dx = "EA"
        e = create_element()

        assert_array_equal(get_derived_F_global_of_element(e, dx=dx), expected_F)

        expected_F = vector(0.5, 0, 0, 0.5, 0, 0)
        dx = "q_x"
        e = create_element()

        assert_array_equal(get_derived_F_global_of_element(e, dx=dx), expected_F)
