import math

import numpy as np
from models.settings import Settings
from new_utilities import plot_center_of_origin, plot_graph
from models.design_parameter import DesignParameterElement

xAxis = np.array([1, 0])
yAxis = np.array([0, 1])


class Element:
    def __init__(
        self,
        node_i,
        node_k,
        f,
        q_z=0,
        q_x=0,
        EI=1,
        EA=1,
    ):
        self.node_i = node_i
        self.node_k = node_k
        self.EI = EI
        self.EA = EA

        self.q_z = q_z
        self.q_x = q_x

        self.N_i = 0
        self.V_i = 0
        self.M_i = 0

        self.N_k = 0
        self.V_k = 0
        self.M_k = 0

        self.N_i_derivation = 0
        self.V_i_derivation = 0
        self.M_i_derivation = 0

        self.N_k_derivation = 0
        self.V_k_derivation = 0
        self.M_k_derivation = 0

        self.dof_x_i, self.dof_y_i, self.dof_phi_i = f(node_i)
        self.dof_x_k, self.dof_y_k, self.dof_phi_k = f(node_k)

    @property
    def length(self):
        x1, y1 = self.node_i.x, self.node_i.y
        x2, y2 = self.node_k.x, self.node_k.y
        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return length

    @property
    def element_vector(self):
        return (
            self.node_k.x - self.node_i.x,
            self.node_k.y - self.node_i.y,
        )

    @property
    def k(self):
        l = self.length

        return self.EA / l * np.array(
            [
                [1, 0, 0, -1, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [-1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ]
        ) + 2 * self.EI / l**3 * np.array(
            [
                [0, 0, 0, 0, 0, 0],
                [0, 6, -3 * l, 0, -6, -3 * l],
                [0, -3 * l, 2 * l**2, 0, 3 * l, l**2],
                [0, 0, 0, 0, 0, 0],
                [0, -6, 3 * l, 0, 6, 3 * l],
                [0, -3 * l, l**2, 0, 3 * l, 2 * l**2],
            ]
        )

    def delta_k(
        self,
        delta_EA=0,
        delta_EI=0,
        delta_l=0,
    ):
        EA = self.EA + delta_EA
        EI = self.EI + delta_EI
        l = self.length + delta_l

        return EA / l * np.array(
            [
                [1, 0, 0, -1, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [-1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ]
        ) + 2 * EI / l**3 * np.array(
            [
                [0, 0, 0, 0, 0, 0],
                [0, 6, -3 * l, 0, -6, -3 * l],
                [0, -3 * l, 2 * l**2, 0, 3 * l, l**2],
                [0, 0, 0, 0, 0, 0],
                [0, -6, 3 * l, 0, 6, 3 * l],
                [0, -3 * l, l**2, 0, 3 * l, 2 * l**2],
            ]
        )

    def delta_k_global(
        self,
        delta_EA=0,
        delta_EI=0,
        delta_l=0,
    ):
        tau = self.get_tau()
        return tau.T.dot(
            self.delta_k(
                delta_EA=delta_EA,
                delta_EI=delta_EI,
                delta_l=delta_l,
            )
        ).dot(tau)

    @property
    def F_0(self):
        q_x, q_z = self.local_surface_load
        return (
            -q_x * self.length / 2,
            -q_z * self.length / 2,
            q_z * self.length**2 / 12,
            -q_x * self.length / 2,
            -q_z * self.length / 2,
            -q_z * self.length**2 / 12,
        )

    def F_0_delta(
        self,
        delta_l=0,
        delta_q_x=0,
        delta_q_z=0,
    ):
        q_x_local, q_z_local = np.dot(
            self.get_tau_of_element(),
            (self.q_x + delta_q_x, self.q_z + delta_q_z),
        )
        l = self.length + delta_l

        return np.array(
            (
                -q_x_local * l / 2,
                -q_z_local * l / 2,
                q_z_local * l**2 / 12,
                -q_x_local * l / 2,
                -q_z_local * l / 2,
                -q_z_local * l**2 / 12,
            )
        )

    def F_0_delta_global(
        self,
        delta_l=0,
        delta_q_x=0,
        delta_q_z=0,
    ):
        return self.get_tau().T.dot(
            self.F_0_delta(
                delta_l=delta_l,
                delta_q_x=delta_q_x,
                delta_q_z=delta_q_z,
            )
        )

    def F_0_derived(self, p_value):
        # Settings / Constants
        delta_p = Settings.delta_p

        # Delta Input for derivation calculation
        forward_delta_input = tuple(
            delta_p / 2 if p.value == p_value else 0 for p in DesignParameterElement
        )
        backward_delta_input = tuple(-x for x in forward_delta_input)

        F_0_d1 = self.F_0_delta(*backward_delta_input[2:6])[0:6]
        F_0_d2 = self.F_0_delta(*forward_delta_input[2:6])[0:6]

        F_0_derivation = (F_0_d2 - F_0_d1) / delta_p

        return F_0_derivation

    def F_0_derived_global(self, p_value):
        return self.get_tau().T.dot(self.F_0_derived(p_value=p_value))

    def k_derived(self, p_value):
        # Settings / Constants
        delta_p = Settings.delta_p

        # Delta Input for derivation calculation
        d2 = tuple(
            delta_p / 2 if p.value == p_value else 0 for p in DesignParameterElement
        )
        d1 = tuple(-x for x in d2)

        K_d1 = self.delta_k(*d1[0:3])
        K_d2 = self.delta_k(*d2[0:3])

        K_derived = (K_d2 - K_d1) / delta_p

        return K_derived

    def k_derived_global(self, p_value):
        tau = self.get_tau()
        return tau.T.dot(self.k_derived(p_value=p_value)).dot(tau)

    @property
    def F_0_global(self):
        return self.get_tau().T.dot(self.F_0)

    def get_tau(self):
        elementVector = self.element_vector

        cosine = np.dot(elementVector, xAxis) / self.length
        sine = np.dot(elementVector, yAxis) / self.length

        return np.array(
            [
                [cosine, -sine, 0, 0, 0, 0],
                [sine, cosine, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0],
                [0, 0, 0, cosine, -sine, 0],
                [0, 0, 0, sine, cosine, 0],
                [0, 0, 0, 0, 0, 1],
            ],
            dtype=float,
        )

    def get_tau_of_element(self):
        elementVector = self.element_vector

        cosine = np.dot(elementVector, xAxis) / self.length
        sine = np.dot(elementVector, yAxis) / self.length

        return np.array(
            [
                [cosine, -sine],
                [sine, cosine],
            ],
            dtype=float,
        )

    @property
    def k_global(self):
        tau = self.get_tau()
        return tau.T.dot(self.k).dot(tau)

    @property
    def degrees_of_freedom(self):
        return [
            self.dof_x_i,
            self.dof_y_i,
            self.dof_phi_i,
            self.dof_x_k,
            self.dof_y_k,
            self.dof_phi_k,
        ]

    @property
    def displacements(self):
        return (
            self.node_i.displacement_x,
            self.node_i.displacement_y,
            self.node_i.displacement_phi,
            self.node_k.displacement_x,
            self.node_k.displacement_y,
            self.node_k.displacement_phi,
        )

    @property
    def local_displacements(self):
        return np.dot(self.get_tau(), self.displacements)

    @property
    def internal_forces(self):
        return (
            self.N_i,
            self.V_i,
            self.M_i,
            self.N_k,
            self.V_k,
            self.M_k,
        )

    @property
    def local_surface_load(self):
        return np.dot(
            self.get_tau_of_element(),
            (self.q_x, self.q_z),
        )

    def set_internal_forces_from_external_forces(self, N_i, V_i, M_i, N_k, V_k, M_k):
        self.N_i = -N_i
        self.V_i = -V_i
        self.M_i = -M_i
        self.N_k = N_k
        self.V_k = V_k
        self.M_k = M_k

    def set_direct_sensitivity_from_external_direct_sensitivity(
        self,
        N_i_derivation,
        V_i_derivation,
        M_i_derivation,
        N_k_derivation,
        V_k_derivation,
        M_k_derivation,
    ):
        self.N_i_derivation = -N_i_derivation
        self.V_i_derivation = -V_i_derivation
        self.M_i_derivation = -M_i_derivation
        self.N_k_derivation = N_k_derivation
        self.V_k_derivation = V_k_derivation
        self.M_k_derivation = M_k_derivation

    def plot(self, ax, show_displacements=True, bar_color="green"):
        l = self.length
        scalingFactor = Settings.scalingFactor

        if not show_displacements:
            ax.plot(
                [self.node_i.x, self.node_k.x],
                [self.node_i.y, self.node_k.y],
                color=bar_color,
                linewidth=2,
            )
            return

        tau = self.get_tau_of_element()

        n = 51
        x = np.linspace(0, 1, n)

        u_i_local, w_i_local, _, u_k_local, w_k_local, _ = self.local_displacements

        _, q_z = self.local_surface_load

        w = -scalingFactor * (
            w_i_local * (1 - x)
            + w_k_local * x
            + ((1 - x) - (1 - x) ** 3) * l**2 / 6 * self.M_i / self.EI
            + (x - x**3) * l**2 / 6 * self.M_k / self.EI
            + (x - 2 * x**3 + x**4) * l**2 / 3 * q_z * l**2 / 8 / self.EI
        )
        x = np.linspace(0, l + scalingFactor * (u_k_local - u_i_local), n)

        for i in range(0, n):
            coords = np.array([x[i], w[i]])

            x[i], w[i] = np.dot(tau, coords)

        x += -x[0] + self.node_i.x + self.node_i.displacement_x * scalingFactor
        y = w - w[0] + self.node_i.y - self.node_i.displacement_y * scalingFactor

        self.plot_surface_load(ax=ax, x_i=x[0], x_k=x[-1], y_i=y[0], y_k=y[-1])

        ax.plot(x, y, color=bar_color, linewidth=2)

    def plot_surface_load(self, ax, x_i, x_k, y_i, y_k, color="red"):
        number_of_arrows = 10

        if self.q_x != 0 or self.q_z != 0:
            x = np.linspace(x_i, x_k, number_of_arrows)
            y = np.linspace(y_i, y_k, number_of_arrows)

            x = np.delete(x, [-1, 0])
            y = np.delete(y, [-1, 0])

            v_q_x = np.full_like(x, self.q_x / max(abs(self.q_x), abs(self.q_z)))
            v_q_z = -np.full_like(x, self.q_z / max(abs(self.q_x), abs(self.q_z)))
            scale = 12

            # Erstelle Pfeile, die die Last darstellen
            ax.quiver(
                x,
                y,
                v_q_x,
                v_q_z,
                scale=scale,
                scale_units="xy",
                units="dots",
                width=6.0,
                pivot="tip",
                color=color,
            )

            # Zeichne eine Linie, die die Enden der Pfeile verbindet
            ax.plot(
                x - v_q_x / scale,
                y - v_q_z / scale,
                color=color,
                linewidth=2,
            )

    def plot_normal_force(self, ax):
        y = lambda x: self.N_i * (1 - x) + self.N_k * x

        plot_graph(ax=ax, y_x=y)

    def plot_shear_force(self, ax):
        y = lambda x: self.V_i * (1 - x) + self.V_k * x

        plot_graph(ax=ax, y_x=y)

    def plot_bending_moment(self, ax):
        _, q_z = self.local_surface_load

        y = lambda x: (
            self.M_i * (1 - x) + self.M_k * x + q_z * self.length**2 * (x - x**2) / 2
        )

        plot_graph(ax=ax, y_x=y)
        ax.invert_yaxis()

    def plot_normal_force_derived(self, ax):
        y = lambda x: self.N_i_derivation * (1 - x) + self.N_k_derivation * x

        plot_graph(ax=ax, y_x=y)

    def plot_shear_force_derived(self, ax):
        y = lambda x: self.V_i_derivation * (1 - x) + self.V_k_derivation * x

        plot_graph(ax=ax, y_x=y)

    def plot_bending_moment_derived(self, ax, design_parameter):
        _, q_z = self.local_surface_load

        if design_parameter == DesignParameterElement.LENGTH:
            y = lambda x: (
                self.M_i_derivation * (1 - x)
                + self.M_k_derivation * x
                + 2 * q_z * self.length * (x - x**2) / 2
            )
        elif design_parameter == DesignParameterElement.QZ:
            y = lambda x: (
                self.M_i_derivation * (1 - x)
                + self.M_k_derivation * x
                + self.length**2 * (x - x**2) / 2
            )
        else:
            y = lambda x: self.M_i_derivation * (1 - x) + self.M_k_derivation * x

        plot_graph(ax=ax, y_x=y)

        ax.invert_yaxis()
