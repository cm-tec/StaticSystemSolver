import math
import numpy as np

from utilities import get_k_global, get_rotation_matrix, get_rotation_matrix_of_element
from vector import vector


class Element:

    def __init__(self, p_i, p_k, EA=1, EI=1):

        if np.array_equal(p_i, p_k):
            raise LengthMustBeGreaterZero()

        if not EA > 0:
            raise EAMustBeGreaterZero()

        if not EI > 0:
            raise EIMustBeGreaterZero()

        self.id = id

        self.p_i = p_i
        self.p_k = p_k

        self.EA = EA
        self.EI = EI

        self.q_x = 0
        self.q_z = 0

        self.f_x_i = 0
        self.f_z_i = 0
        self.m_y_i = 0

        self.f_x_k = 0
        self.f_z_k = 0
        self.m_y_k = 0

    def get_length(self):
        return np.linalg.norm(self.get_element_vector())

    def get_element_vector(self):
        return self.p_k - self.p_i

    def get_local_area_loads(self):
        return get_rotation_matrix(self.get_element_vector()) @ vector(
            self.q_x, self.q_z
        )

    def get_force_vector(self):
        l = self.get_length()
        return self.get_boundary_force_vector() + self.get_element_force_vector()

    def get_boundary_force_vector(self):
        return vector(
            self.f_x_i,
            self.f_z_i,
            self.m_y_i,
            self.f_x_k,
            self.f_z_k,
            self.m_y_k,
        )

    def get_element_force_vector(self):
        l = self.get_length()
        return vector(
            self.q_x * l / 2,
            self.q_z * l / 2,
            -self.q_z * l**2 / 12,
            self.q_x * l / 2,
            self.q_z * l / 2,
            self.q_z * l**2 / 12,
        )

    def get_dofs(self):
        return vector(1, 2, 3, 4, 5, 6)

    def get_tau(self):
        return get_rotation_matrix_of_element(element_vector=self.get_element_vector())

    def get_local_area_loads(self):
        return get_rotation_matrix(self.get_element_vector()) @ [self.q_x, self.q_z]

    def get_k(self):
        return get_k_global(
            EA=self.EA,
            EI=self.EI,
            l=self.get_length(),
            v=self.get_element_vector(),
        )

    def __eq__(self, other):
        if not isinstance(other, Element):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (
            np.array_equal(self.p_i, other.p_i)
            and np.array_equal(self.p_k, other.p_k)
            and self.EA == other.EA
            and self.EI == other.EI
            and self.f_x_i == other.f_x_i
            and self.f_z_i == other.f_z_i
            and self.m_y_i == other.m_y_i
            and self.f_x_k == other.f_x_k
            and self.f_z_k == other.f_z_k
            and self.m_y_k == other.m_y_k
        )


class LengthMustBeGreaterZero(Exception):
    pass


class EAMustBeGreaterZero(Exception):
    pass


class EIMustBeGreaterZero(Exception):
    pass
