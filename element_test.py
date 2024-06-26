import math
import unittest

import numpy as np

from element import (
    EAMustBeGreaterZero,
    EIMustBeGreaterZero,
    Element,
    LengthMustBeGreaterZero,
)
from node import Node

from numpy.testing import assert_array_equal, assert_allclose

from vector import vector


def create_element(
    p_i=vector(0, 0),
    p_k=vector(1, 0),
    EA=1,
    EI=1,
    f_x_i=0,
    f_z_i=0,
    m_y_i=0,
    f_x_k=0,
    f_z_k=0,
    m_y_k=0,
    q_x=0,
    q_z=0,
):
    e = Element(p_i=p_i, p_k=p_k, EA=EA, EI=EI)

    e.f_x_i = f_x_i
    e.f_z_i = f_z_i
    e.m_y_i = m_y_i
    e.f_x_k = f_x_k
    e.f_z_k = f_z_k
    e.m_y_k = m_y_k
    e.q_x = q_x
    e.q_z = q_z

    return e


class TestElement(unittest.TestCase):

    def assert_length(self, p_i, p_k, length):
        element = create_element(p_i, p_k)

        self.assertEqual(element.get_length(), length)

    def assert_element_vector(self, p_i, p_k, element_vector):
        element = create_element(p_i, p_k)

        assert_array_equal(element.get_element_vector(), element_vector)

    def test_get_length(self):
        self.assert_length(vector(0, 0), vector(1, 0), 1)

        self.assert_length(vector(0, 0), vector(0, 1), 1)

        self.assert_length(vector(0, 0), vector(1, 1), math.sqrt(2))

    def test_length_must_be_greater_0(self):
        self.assertRaises(
            LengthMustBeGreaterZero,
            lambda: create_element(vector(0, 0), vector(0, 0)),
        )

    def test_ea_must_be_greater_0(self):

        self.assertRaises(
            EAMustBeGreaterZero,
            lambda: create_element(EA=0),
        )

        self.assertRaises(
            EAMustBeGreaterZero,
            lambda: create_element(EA=-1),
        )

    def test_ei_must_be_greater_0(self):
        self.assertRaises(
            EIMustBeGreaterZero,
            lambda: create_element(EI=0),
        )

        self.assertRaises(
            EIMustBeGreaterZero,
            lambda: create_element(EI=-1),
        )

    def test_get_element_vector(self):
        self.assert_element_vector(vector(0, 0), vector(1, 0), vector(1, 0))

        self.assert_element_vector(vector(0, 0), vector(2, 3), vector(2, 3))

        self.assert_element_vector(vector(-3, 4), vector(1, 8), vector(4, 4))

    def test_get_dofs(self):
        element = create_element()

        assert_array_equal(element.get_dofs(), vector(1, 2, 3, 4, 5, 6))

    def test_get_k(self):
        element = create_element()

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

        assert_array_equal(element.get_k(), expected_k)

    def test_get_k_with_angle(self):
        element = create_element(p_k=vector(0, 1))

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

        assert_array_equal(element.get_k(), expected_k)

    def test_default_area_load_z_equals_0(self):
        e = create_element()
        self.assertEqual(e.q_z, 0)

    def test_default_area_load_x_equals_0(self):
        e = create_element()
        self.assertEqual(e.q_x, 0)

    def test_default_force_i_z_equals_0(self):
        e = create_element()
        self.assertEqual(e.f_z_i, 0)

    def test_default_force_k_z_equals_0(self):
        e = create_element()
        self.assertEqual(e.f_z_k, 0)

    def test_default_force_i_x_equals_0(self):
        e = create_element()
        self.assertEqual(e.f_x_i, 0)

    def test_default_force_k_x_equals_0(self):
        e = create_element()
        self.assertEqual(e.f_x_k, 0)

    def test_default_moment_y_i_equals_0(self):
        e = create_element()
        self.assertEqual(e.m_y_i, 0)

    def test_default_moment_y_k_equals_0(self):
        e = create_element()
        self.assertEqual(e.m_y_k, 0)

    def test_empty_force_vector(self):
        e = create_element()

        assert_array_equal(e.get_force_vector(), np.zeros(6))

    def test_get_force_vector_with_forces_set(self):
        e = create_element()
        e.f_x_i = 1
        e.f_z_i = 2
        e.m_y_i = 3

        e.f_x_k = 4
        e.f_z_k = 5
        e.m_y_k = 6

        assert_array_equal(e.get_force_vector(), vector(1, 2, 3, 4, 5, 6))

    def test_get_force_vector_with_area_load_z_set(self):
        e = create_element()
        e.q_z = 4
        assert_allclose(
            e.get_force_vector(),
            vector(0, 2, -1 / 3, 0, 2, 1 / 3),
            rtol=1e-7,
            atol=0,
        )

        e = create_element()
        e.q_z = 6
        assert_allclose(
            e.get_force_vector(),
            vector(0, 3, -0.5, 0, 3, 0.5),
            rtol=1e-7,
            atol=0,
        )

        e = create_element()
        e.q_z = 7
        assert_allclose(
            e.get_force_vector(),
            vector(0, 3.5, -7 / 12, 0, 3.5, 7 / 12),
            rtol=1e-7,
            atol=0,
        )

    def test_get_force_vector_with_area_load_x_set(self):
        e = create_element()
        e.q_x = 7
        assert_allclose(
            e.get_force_vector(),
            vector(3.5, 0, 0, 3.5, 0, 0),
            rtol=1e-7,
            atol=0,
        )

        e = create_element()
        e.q_x = -4
        assert_allclose(
            e.get_force_vector(),
            vector(-2, 0, 0, -2, 0, 0),
            rtol=1e-7,
            atol=0,
        )

    def test_get_force_vector_with_all_loads_set(self):
        e = create_element()
        e.f_x_i = 1
        e.f_z_i = 2
        e.m_y_i = 3

        e.f_x_k = 4
        e.f_z_k = 5
        e.m_y_k = 6

        e.q_z = 4
        e.q_x = 2

        assert_allclose(
            e.get_force_vector(),
            vector(2, 4, 3 - 1 / 3, 5, 7, 6 + 1 / 3),
            rtol=1e-7,
            atol=0,
        )

    def test_get_local_area_loads(self):
        e = create_element(p_k=vector(0, 1), q_x=7, q_z=13)

        self.assertEqual(e.q_x, 7)
        self.assertEqual(e.q_z, 13)

        assert_array_equal(e.get_local_area_loads(), [-13, 7])
