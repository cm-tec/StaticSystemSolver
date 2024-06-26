import math
from matplotlib import markers, patches, pyplot, transforms
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
from numpy.linalg import norm

from derivative import central_difference_derivative
from new_utilities import plot_graph
from supports import clampedSupport, ownArrow, ownArrow_2, pinned_support, rollerSupport
import numpy as np
from numpy import cos, linspace, sin, radians, dot

from vector import vector

import matplotlib.path as mpath
from matplotlib.transforms import Affine2D


xAxis = np.array([1, 0])
yAxis = np.array([0, 1])


def offset_circle_marker(offset):
    circle_path = mpath.Path.unit_circle()
    circle_transform = Affine2D().translate(*offset)

    return circle_path.transformed(circle_transform)


def get_tau(elementVector):
    cosine = dot(elementVector, xAxis) / norm(elementVector)
    sine = dot(elementVector, yAxis) / norm(elementVector)

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


def get_rotation_matrix(v):
    cosine = dot(v, xAxis) / norm(v)
    sine = dot(v, yAxis) / norm(v)

    return np.array([[cosine, -sine], [sine, cosine]])


def get_rotation_matrix_of_element(element_vector):
    t = get_rotation_matrix(element_vector)

    rotation_matrix = np.eye(6)

    rotation_matrix[:2, :2] = t
    rotation_matrix[3:5, 3:5] = t

    return rotation_matrix


def get_tau_2d(radiant):
    return np.array(
        [
            [cos(radiant), -sin(radiant)],
            [sin(radiant), cos(radiant)],
        ],
        dtype=float,
    )


def get_tau_of_element(element_vector):
    cosine = dot(element_vector, xAxis) / norm(element_vector)
    sine = dot(element_vector, yAxis) / norm(element_vector)

    return np.array(
        [
            [cosine, -sine],
            [sine, cosine],
        ],
        dtype=float,
    )


def get_k(EA=1, EI=1, l=1):
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


def get_k_global(EA, EI, l, v):
    tau = get_rotation_matrix_of_element(v)

    return tau.T.dot(get_k(EA=EA, EI=EI, l=l)).dot(tau)


def get_k_global_of_element(e):
    return get_k_global(
        EA=e.EA,
        EI=e.EI,
        l=e.get_length(),
        v=e.get_element_vector(),
    )


def get_force_vector(
    l,
    f_x_i=0,
    f_z_i=0,
    m_y_i=0,
    f_x_k=0,
    f_z_k=0,
    m_y_k=0,
    q_x=0,
    q_z=0,
):
    return vector(
        f_x_i + q_x * l / 2,
        f_z_i + q_z * l / 2,
        m_y_i - q_z * l**2 / 12,
        f_x_k + q_x * l / 2,
        f_z_k + q_z * l / 2,
        m_y_k + q_z * l**2 / 12,
    )


def get_derived_k_global_of_element(e, dx):
    return central_difference_derivative(
        get_k_global,
        dx=dx,
        EA=e.EA,
        EI=e.EI,
        l=e.get_length(),
        v=e.get_element_vector(),
    )


def get_dofs_of_element(id):
    return vector(1, 2, 3, 4, 5, 6) + (id - 1) * 6


def get_derived_F_global_of_element(e, dx):
    return central_difference_derivative(
        get_force_vector,
        dx=dx,
        l=e.get_length(),
        f_x_i=e.f_x_i,
        f_z_i=e.f_z_i,
        m_y_i=e.m_y_i,
        f_x_k=e.f_x_k,
        f_z_k=e.f_z_k,
        m_y_k=e.m_y_k,
        q_x=e.q_x,
        q_z=e.q_z,
    )


def get_D_local(D_big, node):
    return [v for v in D_big[node * 3 - 3 : node * 3]]


def get_internal_forces(F):
    return (
        -F[0],
        -F[1],
        -F[2],
        F[3],
        F[4],
        F[5],
    )


def plot_displacement(
    ax,
    P_i,
    P_k,
    w_i,
    w_k,
    M_i,
    M_k,
    EI,
    u_i=0,
    q_z=0,
    scalingFactor=1,
):
    elementVector = np.array(P_k) - np.array(P_i)
    length = norm(elementVector)

    tau = get_tau_of_element(elementVector)

    n = 51
    x = linspace(0, 1, n)

    w = -scalingFactor * (
        w_i * (1 - x)
        + w_k * x
        + ((1 - x) - (1 - x) ** 3) * length**2 / 6 * M_i / EI
        + (x - x**3) * length**2 / 6 * M_k / EI
        + (x - 2 * x**3 + x**4) * length**2 / 3 * q_z * length**2 / 8 / EI
    )
    x = linspace(0, length, n)
    for i in range(0, n):
        coords = np.array([x[i], w[i]])

        x[i], w[i] = np.dot(tau, coords)

    x += P_i[0] + u_i * scalingFactor
    w += P_i[1]

    ax.plot(x, w, color="green", linewidth=2)


def set_lim(ax):
    # ax.set_aspect("equal")

    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()

    xMean = (x0 + x1) / 2
    yMean = (y0 + y1) / 2

    deltaX = abs(x1 - x0)
    deltaY = abs(y1 - y0)

    dx = 1.5 * max(deltaX, deltaY / 4) / 2
    dy = 1.5 * max(deltaX / 4, deltaY) / 2

    ax.set_xlim(xMean - dx, xMean + dx)
    ax.set_ylim(yMean - dy, yMean + dy)


def plot_internal_force(ax, F_i, F_k, angle=0):
    plot_center_of_origin(ax, angle=angle)

    tau = np.array(
        [
            [cos(radians(angle)), -sin(radians(angle))],
            [sin(radians(angle)), cos(radians(angle))],
        ],
        dtype=float,
    )

    Point_F_i = tuple(np.dot(tau, (0, F_i)))
    Point_F_k = tuple(np.dot(tau, (1, F_k)))

    P_0 = tuple(np.dot(tau, (0, 0)))
    P_1 = tuple(np.dot(tau, (1, 0)))

    ax.plot(*zip(*[P_0, P_1]), color="black", linewidth=2)

    ax.plot(*zip(*[P_0, Point_F_i]), color="blue", linewidth=2)

    ax.plot(*zip(*[Point_F_i, Point_F_k]), color="blue", linewidth=2)

    ax.plot(*zip(*[Point_F_k, P_1]), color="blue", linewidth=2)

    xScale = 0.1 * np.cos(np.radians(angle)) + 1 * np.sin(np.radians(angle))
    yScale = 1 * np.cos(np.radians(angle)) + 0.1 * np.sin(np.radians(angle))

    current_xlim = ax.get_xlim()
    deltaX = max([abs(v) for v in current_xlim]) * xScale
    ax.set_xlim(current_xlim[0] - deltaX, current_xlim[1] + deltaX)

    current_ylim = ax.get_ylim()
    deltaY = max([abs(v) for v in current_ylim]) * yScale
    ax.set_ylim(current_ylim[0] - deltaY, current_ylim[1] + deltaY)


def plot_force(
    ax, coords, length=1, value=None, angle=0, head_starts_at_zero=True, color="red"
):
    rounded_value = round(value, 3)

    if rounded_value == 0:
        return

    arrow = ownArrow(head_starts_at_zero=head_starts_at_zero, length=length)

    scale = 40
    angleDiff = 18 + 180
    if not head_starts_at_zero:
        angleDiff += 180

    arrow = arrow.transformed(matplotlib.transforms.Affine2D().rotate_deg(angle))
    ax.plot(
        coords[0],
        coords[1],
        marker=arrow,
        color=color,
        markersize=length * 60,
        markeredgewidth=1,
        zorder=6,
    )

    ax.annotate(
        rounded_value,
        xy=coords,
        xycoords="data",
        xytext=(
            scale * np.cos(np.radians(angle + angleDiff)),
            scale * np.sin(np.radians(angle + angleDiff)),
        ),
        textcoords="offset points",
        va="center",
        zorder=20,
        color=color,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none"),
    )


def plot_surface_load(ax, p_i, p_k, n=10, color="r", length=1):

    arrow = ownArrow(head_starts_at_zero=True, length=length)
    arrow = arrow.transformed(matplotlib.transforms.Affine2D().rotate_deg(-90))
    x = np.linspace(p_i[0], p_k[0], n)
    y = np.linspace(p_i[1], p_k[1], n)

    for i in range(n):
        ax.plot(
            x[i],
            y[i],
            marker=arrow,
            color=color,
            markersize=length * 60,
            markeredgewidth=1,
        )


def plot_horizontal_surface_load(ax, p_i, p_k, n=10, color="r", length=1):

    arrow = ownArrow_2(length=length)
    x = np.linspace(p_i[0], p_k[0], n)
    y = np.linspace(p_i[1], p_k[1], n)

    for i in range(n):
        ax.plot(
            x[i],
            y[i],
            marker=arrow,
            color=color,
            markersize=length * 60,
            markeredgewidth=1,
        )


def plot_center_of_origin(plt, P_0=(0, 0), angle=0):
    center_of_origin = (
        P_0[0] - 0.2 * np.cos(np.radians(angle)),
        P_0[1] - 0.2 * np.sin(np.radians(angle)),
    )

    xAxis = ownArrow(head_starts_at_zero=False).transformed(
        transforms.Affine2D().rotate_deg(angle)
    )
    zAxis = ownArrow(head_starts_at_zero=False).transformed(
        transforms.Affine2D().rotate_deg(angle - 90)
    )

    plt.plot(
        center_of_origin[0],
        center_of_origin[1],
        marker=xAxis,
        color="r",
        markersize=60,
        markeredgewidth=1,
    )
    plt.plot(
        center_of_origin[0],
        center_of_origin[1],
        marker=zAxis,
        color="r",
        markersize=60,
        markeredgewidth=1,
    )

    scale = 20
    angleDiff = 30

    plt.annotate(
        "x",
        xy=center_of_origin,
        xycoords="data",
        xytext=(
            scale * np.cos(np.radians(angle + angleDiff)),
            scale * np.sin(np.radians(angle + angleDiff)),
        ),
        textcoords="offset points",
        va="center",
        zorder=20,
        color="r",
    )
    plt.annotate(
        "z",
        xy=center_of_origin,
        xycoords="data",
        xytext=(
            scale * np.cos(np.radians(angle + angleDiff - 90)),
            scale * np.sin(np.radians(angle + angleDiff - 90)),
        ),
        textcoords="offset points",
        va="center",
        zorder=20,
        color="r",
    )


def get_normal_force_curve(n_i, n_k):
    return lambda x: n_i * (1 - x) + n_k * x


def get_shear_force_curve(v_i, v_k):
    return lambda x: v_i * (1 - x) + v_k * x


def get_bending_moment_curve(m_y_i, m_y_k, q_z, l):
    return lambda x: (m_y_i * (1 - x) + m_y_k * x + q_z * l**2 * (x - x**2) / 2)


def get_derived_normal_force_curve(derived_n_i, derived_n_k):
    return lambda x: derived_n_i * (1 - x) + derived_n_k * x


def get_derived_shear_force_curve(derived_v_i, derived_v_k):
    return lambda x: derived_v_i * (1 - x) + derived_v_k * x


def get_derived_bending_moment_curve(d_m_y_i, d_m_y_k, q_z, l, dx):
    if dx == "l":
        return lambda x: (
            d_m_y_i * (1 - x) + d_m_y_k * x + 2 * q_z * l * (x - x**2) / 2
        )
    elif dx == "q_z":
        return lambda x: (d_m_y_i * (1 - x) + d_m_y_k * x + l**2 * (x - x**2) / 2)
    else:
        return lambda x: d_m_y_i * (1 - x) + d_m_y_k * x


def plot_normal_force(ax, n_i, n_k):
    y = get_normal_force_curve(n_i=n_i, n_k=n_k)

    plot_graph(ax=ax, y_x=y)


def plot_shear_force(ax, v_i, v_k):
    y = get_shear_force_curve(v_i, v_k)

    plot_graph(ax=ax, y_x=y)


def plot_bending_moment(ax, m_y_i, m_y_k, q_z, l):
    y = get_bending_moment_curve(m_y_i, m_y_k, q_z, l)

    plot_graph(ax=ax, y_x=y)
    ax.invert_yaxis()


def plot_derived_normal_force(ax, derived_n_i, derived_n_k):
    y = get_derived_normal_force_curve(derived_n_i=derived_n_i, derived_n_k=derived_n_k)

    plot_graph(ax=ax, y_x=y)


def plot_derived_shear_force(ax, derived_v_i, derived_v_k):
    y = get_derived_shear_force_curve(derived_v_i=derived_v_i, derived_v_k=derived_v_k)

    plot_graph(ax=ax, y_x=y)


def plot_derived_bending_moment(ax, d_m_y_i, d_m_y_k, q_z, l, dx):
    y = get_derived_bending_moment_curve(d_m_y_i, d_m_y_k, q_z, l, dx)

    plot_graph(ax=ax, y_x=y)
    ax.invert_yaxis()


def get_color_map():
    colors = [
        (0, 0, 1),
        (0, 1, 1),
        (0, 0, 0),
        (1, 1, 0),
        (1, 0, 0),
    ]  # Red, Yellow, Green, Cyan, Blue
    positions = np.linspace(0, 1, len(colors))

    # Create the colormap
    return LinearSegmentedColormap.from_list(
        "custom_colormap", list(zip(positions, colors))
    )


def get_u_displacement_curve(n_i, n_k, u_i, EA):
    return lambda x: (n_i * (x - x**2 / 2) + 1 / 2 * n_k * x**2) / EA + u_i


def get_w_displacement_curve(w_i, w_k, m_y_i, m_y_k, q_z, l, EI):
    return lambda x: (
        w_i * (1 - x)
        + w_k * x
        + ((1 - x) - (1 - x) ** 3) * l**2 / 6 * m_y_i / EI
        + (x - x**3) * l**2 / 6 * m_y_k / EI
        + (x - 2 * x**3 + x**4) * l**2 / 3 * q_z * l**2 / 8 / EI
    )


def get_phi_displacement_curve(w_i, w_k, m_y_i, m_y_k, q_z, l, EI):
    return lambda x: (
        -w_i
        + w_k
        + (-1 + 3 * (x - 1) ** 2) * l**2 / 6 * m_y_i / EI
        + (1 - 3 * x**2) * l**2 / 6 * m_y_k / EI
        + (1 - 6 * x**2 + 4 * x**3) * l**2 / 3 * q_z * l**2 / 8 / EI
    )


def plot_u_displacement(ax, n_i, n_k, u_i, EA):
    y = get_u_displacement_curve(n_i=n_i, n_k=n_k, u_i=u_i, EA=EA)

    plot_graph(ax=ax, y_x=y)


def plot_w_displacement(ax, w_i, w_k, m_y_i, m_y_k, q_z, l, EI):
    y = get_w_displacement_curve(
        w_i=w_i,
        w_k=w_k,
        m_y_i=m_y_i,
        m_y_k=m_y_k,
        q_z=q_z,
        l=l,
        EI=EI,
    )

    plot_graph(ax=ax, y_x=y)
    ax.invert_yaxis()


def plot_phi_displacement(ax, w_i, w_k, m_y_i, m_y_k, q_z, l, EI):
    y = get_phi_displacement_curve(
        w_i=w_i,
        w_k=w_k,
        m_y_i=m_y_i,
        m_y_k=m_y_k,
        q_z=q_z,
        l=l,
        EI=EI,
    )

    plot_graph(ax=ax, y_x=y)
