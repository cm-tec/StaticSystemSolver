import math
from matplotlib import markers, patches, pyplot, transforms
import matplotlib
from numpy.linalg import norm
import matplotlib.pyplot as plt

from supports import (
    circle_arrow,
    clampedSupport,
    ownArrow,
    pinned_support,
    rollerSupport,
)
import numpy as np
from numpy import cos, linspace, sin, radians, dot
from models.support import Support

xAxis = np.array([1, 0])
yAxis = np.array([0, 1])


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


def get_tau_2d(radiant):
    return np.array(
        [
            [cos(radiant), -sin(radiant)],
            [sin(radiant), cos(radiant)],
        ],
        dtype=float,
    )


def get_tau_of_element(elementVector):
    cosine = dot(elementVector, xAxis) / norm(elementVector)
    sine = dot(elementVector, yAxis) / norm(elementVector)

    return np.array(
        [
            [cosine, -sine],
            [sine, cosine],
        ],
        dtype=float,
    )


def get_k(EA, EI, l):
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


def add_elements(list, add_values):
    """
    Adds elements from add_values to elements in list.

    :param list: List to be modified.
    :param add_values: List of values to be added.
    :return: Modified list.
    """

    # Check if the two lists have the same length
    if len(list) != len(add_values):
        raise ValueError("The two lists must be of equal length.")

    return [x + add for x, add in zip(list, add_values)]


def subtract_elements(list, subtract_values):
    """
    Adds elements from add_values to elements in list.

    :param list: List to be modified.
    :param add_values: List of values to be added.
    :return: Modified list.
    """

    # Check if the two lists have the same length
    if len(list) != len(subtract_values):
        raise ValueError("The two lists must be of equal length.")

    return [x - add for x, add in zip(list, subtract_values)]


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


def plot_internal_force(ax, F_i, F_k, q=0, angle=0):
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

    if q == 0:
        ax.plot(*zip(*[Point_F_i, Point_F_k]), color="blue", linewidth=2)
    else:
        x = np.linspace(0, 1, n)
        ax.plot(x, w, color="blue", linewidth=2)

    ax.plot(*zip(*[Point_F_k, P_1]), color="blue", linewidth=2)

    xScale = 0.1 * np.cos(np.radians(angle)) + 1 * np.sin(np.radians(angle))
    yScale = 1 * np.cos(np.radians(angle)) + 0.1 * np.sin(np.radians(angle))

    current_xlim = ax.get_xlim()
    deltaX = max([abs(v) for v in current_xlim]) * xScale
    ax.set_xlim(current_xlim[0] - deltaX, current_xlim[1] + deltaX)

    current_ylim = ax.get_ylim()
    deltaY = max([abs(v) for v in current_ylim]) * yScale
    ax.set_ylim(current_ylim[0] - deltaY, current_ylim[1] + deltaY)


def plot_force(ax, coords, length=1, text=None, angle=0, head_starts_at_zero=True):
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
        color="r",
        markersize=length * 60,
        markeredgewidth=1,
    )

    if text:
        ax.annotate(
            text,
            xy=coords,
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


def plot_moment(ax, coords, value=None, angle_span=90, color="red"):
    rounded_value = round(value, 3)

    if rounded_value == 0:
        return

    arrow = circle_arrow(angle_span=angle_span)

    scale = 30

    ax.plot(
        coords[0],
        coords[1],
        marker=arrow,
        color=color,
        markersize=40,
        markeredgewidth=1,
        zorder=6,
    )

    if value:
        ax.annotate(
            rounded_value,
            xy=coords,
            xycoords="data",
            xytext=(
                scale * np.cos(np.radians(3 * angle_span / 4)),
                scale * np.sin(np.radians(3 * angle_span / 4)),
            ),
            textcoords="offset points",
            va="center",
            zorder=20,
            color=color,
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


def plot_graph(ax, y_x):
    plot_center_of_origin(ax)

    P_start = (0, 0)
    P_mid = (0.5, 0)
    P_end = (1, 0)

    ax.plot(*zip(*[P_start, P_end]), color="black", linewidth=2)

    n = 51

    x = np.linspace(0, 1, n)
    y = np.around(y_x(x), 6)

    V_start = (0, y[0])
    V_mid = (0.5, y[n // 2])
    V_end = (1, y[-1])

    ax.plot(*zip(*[P_start, V_start]), color="gray", linewidth=2)
    ax.plot(*zip(*[P_mid, V_mid]), color="gray", linewidth=2)
    ax.plot(*zip(*[P_end, V_end]), color="gray", linewidth=2)

    ax.plot(x, y, color="blue", linewidth=2)

    y_max = max(abs(y))

    for p in [V_start, V_mid, V_end]:
        y_a = (
            math.copysign(y_max * 0.3, p[1]) + p[1]
            if p[1] != 0
            else 0.4 * y_max if y_max != 0 else 0.2
        )

        ax.annotate(
            f"{round(p[1], 3)}",
            p,
            xytext=(p[0], y_a),
            ha="center",
        )

    xScale = 0.1
    yScale = 1

    current_xlim = ax.get_xlim()
    current_ylim = ax.get_ylim()

    deltaX = max([abs(v) for v in current_xlim]) * xScale
    deltaY = max([abs(v) for v in current_ylim]) * yScale

    ax.set_xlim(current_xlim[0] - deltaX, current_xlim[1] + deltaX)
    ax.set_ylim(current_ylim[0] - deltaY, current_ylim[1] + deltaY)


def calculate_response_variable(zeta_0, zeta, F_star):
    R = np.dot((zeta_0 + zeta), F_star)

    return R


def get_M_element_to_non_restrained_total(non_restrained_dofs, element_dofs):
    # Construct Matrix to convert element to non_restrained_total
    M_element_to_non_restrained_total = np.zeros((len(non_restrained_dofs), 6))

    for i, d in enumerate(element_dofs):
        if d in non_restrained_dofs:
            M_element_to_non_restrained_total[non_restrained_dofs.index(d)][i] = 1

    return M_element_to_non_restrained_total


def get_M_non_restrained_total_to_total(ndofs, non_restrained_dofs, element_dofs):
    # Construct Matrix to convert non_restrained_global to global
    M_non_restrained_total_to_total = np.zeros((ndofs, len(non_restrained_dofs)))
    for i, d in enumerate(element_dofs):
        if d in non_restrained_dofs:
            M_non_restrained_total_to_total[i][non_restrained_dofs.index(d)] = 1

    return M_non_restrained_total_to_total


def get_M_total_to_element(ndofs, element_dofs):
    # Construct Matrix to convert Total to element
    M_total_to_element = np.zeros((6, ndofs))
    for i, d in enumerate(element_dofs):
        M_total_to_element[i][d - 1] = 1

    return M_total_to_element
