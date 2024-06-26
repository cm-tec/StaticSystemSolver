import re
import matplotlib as mpl
from matplotlib import cm, pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from display import Display
from models.settings import Settings
from new_utilities import plot_moment
from static_system_solver import StaticSystemSolver
from supports import pinned_support, rollerSupport
from utilities import (
    get_bending_moment_curve,
    get_color_map,
    get_derived_normal_force_curve,
    get_dofs_of_element,
    get_normal_force_curve,
    get_rotation_matrix,
    get_rotation_matrix_of_element,
    get_shear_force_curve,
    get_w_displacement_curve,
    offset_circle_marker,
    plot_force,
    plot_horizontal_surface_load,
    plot_surface_load,
)
from vector import vector


def plot_element(
    ax,
    element_id,
    p_i,
    p_k,
    EI,
    f_x_i=0,
    f_z_i=0,
    m_y_i=0,
    f_x_k=0,
    f_z_k=0,
    m_y_k=0,
    s_m_y_i=0,
    s_m_y_k=0,
    q_z=0,
    q_x=0,
    local_q_z=0,
    d1=0,
    d2=0,
    d3=0,
    d4=0,
    d5=0,
    d6=0,
    moment_joint_i=False,
    moment_joint_k=False,
    show_loads=True,
    show_element_id=True,
):
    element_vector = p_k - p_i
    l = np.linalg.norm(element_vector)

    scaling_factor = Settings.scalingFactor
    tau = get_rotation_matrix(element_vector)

    n = 51
    x = np.linspace(0, 1, n)

    u_i_local, w_i_local, _, u_k_local, w_k_local, _ = np.dot(
        get_rotation_matrix_of_element(element_vector), [d1, d2, d3, d4, d5, d6]
    )

    w = -scaling_factor * get_w_displacement_curve(
        w_i=w_i_local,
        w_k=w_k_local,
        m_y_i=s_m_y_i,
        m_y_k=s_m_y_k,
        q_z=local_q_z,
        l=l,
        EI=EI,
    )(x)

    x = np.linspace(0, l + scaling_factor * (u_k_local - u_i_local), n)

    for i in range(0, n):
        coords = np.array([x[i], w[i]])

        x[i], w[i] = np.dot(tau, coords)

    x += -x[0] + p_i[0] + d1 * scaling_factor
    y = w - w[0] + p_i[1] - d2 * scaling_factor

    if show_element_id:
        ax.annotate(
            element_id,
            (x[n // 2], y[n // 2]),
            zorder=10,
            ha="center",
            va="center",
            size="10",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black"),
        )

    v = p_k + vector(d4, -d5) * scaling_factor - p_i - vector(d1, -d2) * scaling_factor
    normalized_v = v / np.linalg.norm(v)

    if moment_joint_i:
        ax.plot(
            x[0],
            y[0],
            marker=offset_circle_marker(offset=2 * normalized_v),
            markersize=30,
            markerfacecolor="w",
            markeredgecolor="k",
            zorder=5,
        )

    if moment_joint_k:
        ax.plot(
            x[-1],
            y[-1],
            marker=offset_circle_marker(offset=-2 * normalized_v),
            markersize=30,
            markerfacecolor="w",
            markeredgecolor="k",
            zorder=5,
        )
    d = 1
    if show_loads:
        if q_z != 0:
            plot_surface_load(ax=ax, p_i=p_i, p_k=p_k)

        if q_x != 0:
            plot_horizontal_surface_load(ax=ax, p_i=p_i, p_k=p_k)

        plot_force(ax=ax, coords=(x[d], y[d]), value=f_x_i)
        plot_force(ax=ax, coords=(x[d], y[d]), value=f_z_i, angle=-90)
        plot_moment(ax=ax, coords=(x[d], y[d]), value=m_y_i)

        plot_force(ax=ax, coords=(x[-d - 1], y[-d - 1]), value=f_x_k)
        plot_force(ax=ax, coords=(x[-d - 1], y[-d - 1]), value=f_z_k, angle=-90)
        plot_moment(ax=ax, coords=(x[-d - 1], y[-d - 1]), value=m_y_k)

    points = np.array([x, y]).transpose().reshape(-1, 1, 2)
    return np.concatenate([points[:-1], points[1:]], axis=1)


def plot_static_system(
    ax,
    static_system,
    static_system_solution,
    show_reaction_forces=True,
    show_loads=True,
    show_element_id=True,
    show_joints_and_supports=True,
    element_line_width=1,
    color_quantity=None,
    color_functions=None,
):
    display_data = Display.prepare_static_system_for_display(static_system)

    segments = []
    color_values = []

    for i, e in enumerate(static_system.get_elements()):

        indices = static_system.get_essential_dof_indices(get_dofs_of_element(i + 1))

        d1, d2, d3, d4, d5, d6 = static_system_solution.displacements[indices]

        n_i, v_i, s_m_y_i, n_k, v_k, s_m_y_k = static_system_solution.internal_forces[i]

        f_x_i, f_z_i, m_y_i, f_x_k, f_z_k, m_y_k = e.get_boundary_force_vector()

        _, local_q_z = e.get_local_area_loads()

        moment_joint_i = (
            Display.should_place_moment_joint(
                static_system, get_dofs_of_element(i + 1)[2]
            )
            if show_joints_and_supports
            else False
        )
        moment_joint_k = (
            Display.should_place_moment_joint(
                static_system, get_dofs_of_element(i + 1)[5]
            )
            if show_joints_and_supports
            else False
        )

        n = 50
        x = np.linspace(0, 1, n)

        if color_functions:
            color_values.extend(color_functions[i](x))

        segs = plot_element(
            ax=ax,
            element_id=i + 1,
            p_i=e.p_i,
            p_k=e.p_k,
            q_z=e.q_z,
            q_x=e.q_x,
            local_q_z=local_q_z,
            f_x_i=f_x_i,
            f_z_i=f_z_i,
            m_y_i=m_y_i,
            f_x_k=f_x_k,
            f_z_k=f_z_k,
            m_y_k=m_y_k,
            s_m_y_i=s_m_y_i,
            s_m_y_k=s_m_y_k,
            EI=e.EI,
            d1=d1,
            d2=d2,
            d3=d3,
            d4=d4,
            d5=d5,
            d6=d6,
            moment_joint_i=moment_joint_i,
            moment_joint_k=moment_joint_k,
            show_loads=show_loads,
            show_element_id=show_element_id,
        )

        segments.extend(segs)

    lc = LineCollection(
        segments,
        linewidths=element_line_width,
        zorder=4,
        capstyle="round",
        norm=mpl.colors.CenteredNorm(),
    )

    if color_functions:
        lc.set_cmap(get_color_map())
        lc.set_array(color_values)
        cbar = plt.colorbar(lc, ax=ax)

    else:
        lc.set_color("k")

    ax.add_collection(lc)

    for k, v in display_data.items():
        # Extracting the values of x and z using regular expressions
        x = float(re.search(r"x=(-?\d+)", k).group(1))
        z = float(re.search(r"z=(-?\d+)", k).group(1))

        dof = Display.get_dof_of_node(v["dof_phi"])

        element_id = (dof - 1) // 6 + 1
        element_dof = (dof - 1) % 6 + 1

        if element_dof > 3:
            dof_x, dof_z, dof_phi = get_dofs_of_element(element_id)[3:6]
        else:
            dof_x, dof_z, dof_phi = get_dofs_of_element(element_id)[0:3]

        indices = static_system.get_essential_dof_indices([dof_x, dof_z, dof_phi])

        dx, dz, _ = (
            static_system_solution.displacements[indices] * Settings.scalingFactor
        )

        if show_joints_and_supports:

            if dof_x in static_system.get_restrained_dofs():
                ax.plot(
                    x + dx,
                    z + dz,
                    marker=pinned_support(angle=270),
                    color="k",
                    markerfacecolor="w",
                    markersize=35,
                    zorder=3,
                )
            if dof_z in static_system.get_restrained_dofs():

                ax.plot(
                    x + dx,
                    z + dz,
                    marker=pinned_support(angle=0),
                    color="k",
                    markerfacecolor="w",
                    markersize=35,
                    zorder=3,
                )

            if dof_phi in static_system.get_restrained_dofs():
                ax.scatter(
                    x + dx,
                    z + dz,
                    c="whitesmoke",
                    s=100,
                    edgecolors="k",
                    zorder=9,
                    marker="s",
                )

        r_f_x, r_f_z, r_m_y = static_system_solution.external_forces[indices]

        if show_reaction_forces:
            plot_force(ax=ax, coords=(x + dx, z + dz), value=r_f_x, color="g")

            plot_force(
                ax=ax, coords=(x + dx, z + dz), value=r_f_z, angle=-90, color="g"
            )

            plot_moment(ax=ax, coords=(x + dx, z + dz), value=r_m_y, color="g")


def plot_plain_static_system(
    ax,
    static_system,
    show_loads=True,
    show_element_id=True,
    show_joints_and_supports=True,
    element_line_width=1,
):
    display_data = Display.prepare_static_system_for_display(static_system)

    segments = []

    for i, e in enumerate(static_system.get_elements()):
        moment_joint_i = (
            Display.should_place_moment_joint(
                static_system, get_dofs_of_element(i + 1)[2]
            )
            if show_joints_and_supports
            else False
        )
        moment_joint_k = (
            Display.should_place_moment_joint(
                static_system, get_dofs_of_element(i + 1)[5]
            )
            if show_joints_and_supports
            else False
        )

        n = 50
        x = np.linspace(0, 1, n)

        segs = plot_element(
            ax=ax,
            element_id=i + 1,
            p_i=e.p_i,
            p_k=e.p_k,
            q_z=0,
            f_x_i=0,
            f_z_i=0,
            m_y_i=0,
            f_x_k=0,
            f_z_k=0,
            m_y_k=0,
            s_m_y_i=0,
            s_m_y_k=0,
            EI=e.EI,
            d1=0,
            d2=0,
            d3=0,
            d4=0,
            d5=0,
            d6=0,
            moment_joint_i=moment_joint_i,
            moment_joint_k=moment_joint_k,
            show_loads=show_loads,
            show_element_id=show_element_id,
        )

        segments.extend(segs)

    lc = LineCollection(
        segments,
        linewidths=element_line_width,
        zorder=4,
        capstyle="round",
        norm=mpl.colors.CenteredNorm(),
    )

    lc.set_color("k")

    ax.add_collection(lc)

    for k, v in display_data.items():
        # Extracting the values of x and z using regular expressions
        x = float(re.search(r"x=(-?\d+)", k).group(1))
        z = float(re.search(r"z=(-?\d+)", k).group(1))

        dof = Display.get_dof_of_node(v["dof_phi"])

        element_id = (dof - 1) // 6 + 1
        element_dof = (dof - 1) % 6 + 1

        if element_dof > 3:
            dof_x, dof_z, dof_phi = get_dofs_of_element(element_id)[3:6]
        else:
            dof_x, dof_z, dof_phi = get_dofs_of_element(element_id)[0:3]

        if show_joints_and_supports:

            if dof_x in static_system.get_restrained_dofs():
                ax.plot(
                    x,
                    z,
                    marker=pinned_support(angle=270),
                    color="k",
                    markerfacecolor="w",
                    markersize=35,
                    zorder=3,
                )
            if dof_z in static_system.get_restrained_dofs():

                ax.plot(
                    x,
                    z,
                    marker=pinned_support(angle=0),
                    color="k",
                    markerfacecolor="w",
                    markersize=35,
                    zorder=3,
                )

            if dof_phi in static_system.get_restrained_dofs():
                ax.scatter(
                    x,
                    z,
                    c="whitesmoke",
                    s=100,
                    edgecolors="k",
                    zorder=9,
                    marker="s",
                )
