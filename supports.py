"""
GPL-3.0 License

Copyright (C) 2020-2022 Monirul Shawon

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import matplotlib

# import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import numpy as np

"""
##############################################################
#                                                            #
#             Roller support marker using path               #
#            Pinned Support marker also using path           #
#              Our own custom arrow for rotating             #
#              Reaction arrow using path                     # 
#                                                            # 
#    ----------------- Monirul Shawon ------------------     #
##############################################################
"""


def rollerSupport():
    MAGIC = 0.2652031
    SQRTHALF = np.sqrt(0.5)
    MAGIC45 = SQRTHALF * MAGIC
    verts = np.array(
        [
            [0.0, -1.0],
            [MAGIC, -1.0],
            [SQRTHALF - MAGIC45, -SQRTHALF - MAGIC45],
            [SQRTHALF, -SQRTHALF],
            [SQRTHALF + MAGIC45, -SQRTHALF + MAGIC45],
            [1.0, -MAGIC],
            [1.0, 0.0],
            [1.0, MAGIC],
            [SQRTHALF + MAGIC45, SQRTHALF - MAGIC45],
            [SQRTHALF, SQRTHALF],
            [SQRTHALF - MAGIC45, SQRTHALF + MAGIC45],
            [MAGIC, 1.0],
            [0.0, 1.0],
            [-MAGIC, 1.0],
            [-SQRTHALF + MAGIC45, SQRTHALF + MAGIC45],
            [-SQRTHALF, SQRTHALF],
            [-SQRTHALF - MAGIC45, SQRTHALF - MAGIC45],
            [-1.0, MAGIC],
            [-1.0, 0.0],
            [-1.0, -MAGIC],
            [-SQRTHALF - MAGIC45, -SQRTHALF + MAGIC45],
            [-SQRTHALF, -SQRTHALF],
            [-SQRTHALF + MAGIC45, -SQRTHALF - MAGIC45],
            [-MAGIC, -1.0],
            [0.0, -1.0],
            [0.0, -1.0],
            # line
            [-1.0, -1.0],  # index [26]
            [1.0, -1.0],
            # Wall
            [-1.0, -1.3],
            [-0.8, -1.0],
            [-0.8, -1.3],
            [-0.6, -1.0],
            [-0.6, -1.3],
            [-0.4, -1.0],
            [-0.4, -1.3],
            [-0.2, -1.0],
            [-0.2, -1.3],
            [0.0, -1.0],
            [0.0, -1.3],
            [0.2, -1.0],
            [0.2, -1.3],
            [0.4, -1.0],
            [0.4, -1.3],
            [0.6, -1.0],
            [0.6, -1.3],
            [0.8, -1.0],
        ],
        dtype=float,
    )

    codes = [matplotlib.path.Path.CURVE4] * 46
    codes[0] = matplotlib.path.Path.MOVETO
    codes[-21] = matplotlib.path.Path.CLOSEPOLY
    for i in range(26, 46):
        if i % 2 == 0:
            codes[i] = matplotlib.path.Path.MOVETO
        else:
            codes[i] = matplotlib.path.Path.LINETO

    path = matplotlib.path.Path(verts * 1 + (0, -1.5), codes)
    return path


def pinned_support(angle=0):
    triangle_width = 0.5
    triangle_height = 0.5

    line_distance = 0.1

    verts = np.array(
        [
            [-triangle_width / 2, -triangle_height],
            [0, 0],
            [triangle_width / 2, -triangle_height],
            [-triangle_width / 2, -triangle_height],
            #
            [-triangle_width / 2, -triangle_height - line_distance],
            [triangle_width / 2, -triangle_height - line_distance],
        ],
        dtype=float,
    )

    codes = [
        matplotlib.path.Path.MOVETO,
        matplotlib.path.Path.LINETO,
        matplotlib.path.Path.LINETO,
        matplotlib.path.Path.CLOSEPOLY,
        matplotlib.path.Path.MOVETO,
        matplotlib.path.Path.LINETO,
    ]

    path = matplotlib.path.Path(verts, codes)

    return path.transformed(Affine2D().rotate_deg(angle))


def clampedSupport():
    verts = np.array(
        [
            # Line Add + wall
            [-1.2, -0.0],
            [1.2, -0.0],
            [-1.2, -0.3],
            [-1.0, -0.0],
            # Wall
            [-1.0, -0.3],
            [-0.8, -0.0],
            [-0.8, -0.3],
            [-0.6, -0.0],
            [-0.6, -0.3],
            [-0.4, -0.0],
            [-0.4, -0.3],
            [-0.2, -0.0],
            [-0.2, -0.3],
            [0.0, -0.0],
            [0.0, -0.3],
            [0.2, -0.0],
            [0.2, -0.3],
            [0.4, -0.0],
            [0.4, -0.3],
            [0.6, -0.0],
            [0.6, -0.3],
            [0.8, -0.0],
            [0.8, -0.3],
            [1, -0.0],
        ],
        dtype=float,
    )

    codes = [matplotlib.path.Path.LINETO] * 24
    codes[0] = matplotlib.path.Path.MOVETO

    for i in range(1, 24):
        if i % 2 == 0:
            codes[i] = matplotlib.path.Path.MOVETO
        else:
            codes[i] = matplotlib.path.Path.LINETO

    path = matplotlib.path.Path(verts * 1 + (0, -0), codes)
    return path


def ownArrow(head_starts_at_zero=True, length=1):
    verts = np.array(
        [
            [0, 0],
            [-0.25, 0.1],
            [-0.15, 0],
            [-length, 0],
            [-0.15, 0],
            [-0.25, -0.1],
            [0, 0],
        ],
        dtype=float,
    )

    if not head_starts_at_zero:
        verts[:, 0] += 0.4 + length
    else:
        verts[:, 0] -= 0.4

    codes = [matplotlib.path.Path.LINETO] * 7
    codes[0] = matplotlib.path.Path.MOVETO
    codes[-1] = matplotlib.path.Path.CLOSEPOLY

    path = matplotlib.path.Path(verts, codes)
    return path


def ownArrow_2(length=1):
    verts = np.array(
        [
            [0, 0],
            [-0.25, 0.1],
            [-0.15, 0],
            [-length, 0],
            [-0.15, 0],
            [-0.25, -0.1],
            [0, 0],
        ],
        dtype=float,
    )

    verts[:, 0] -= 0.4
    verts[:, 1] += 0.4

    codes = [matplotlib.path.Path.LINETO] * 7
    codes[0] = matplotlib.path.Path.MOVETO
    codes[-1] = matplotlib.path.Path.CLOSEPOLY

    path = matplotlib.path.Path(verts, codes)
    return path


def circle_arrow(angle_span=270):
    # Define the start and end angles for the arc
    start_angle = 45
    end_angle = start_angle + angle_span

    lw = 0.05

    # Calculate the number of points in the arc
    num_points = 50

    radius = 1

    # Define two radii
    radius_forward = radius + lw / 2
    radius_backward = radius - lw / 2

    # Create angles for forward and backward arcs
    angles_forward = np.linspace(
        np.radians(start_angle), np.radians(end_angle), num_points
    )
    angles_backward = np.linspace(
        np.radians(end_angle), np.radians(start_angle), num_points
    )

    # Calculate the points for the forward and backward arcs
    arc_forward = np.array(
        [
            radius_forward * np.cos(angles_forward),
            radius_forward * np.sin(angles_forward),
        ]
    ).T
    arc_backward = np.array(
        [
            radius_backward * np.cos(angles_backward),
            radius_backward * np.sin(angles_backward),
        ]
    ).T

    # Combine the arcs to form a complete path
    arc = np.concatenate([arc_forward, arc_backward])

    # Define the arrowhead
    arrowhead = np.array(
        [
            [
                1.12 * radius * np.cos(np.deg2rad(end_angle)),
                1.12 * radius * np.sin(np.deg2rad(end_angle)),
            ],
            [
                radius * np.cos(np.deg2rad(end_angle))
                - 4 * lw * np.sin(np.deg2rad(end_angle)),
                radius * np.sin(np.deg2rad(end_angle))
                + 4 * lw * np.cos(np.deg2rad(end_angle)),
            ],
            [
                0.88 * radius * np.cos(np.deg2rad(end_angle)),
                0.88 * radius * np.sin(np.deg2rad(end_angle)),
            ],
        ]
    )

    # Combine the arc and the arrowhead
    verts = np.vstack([arc, arrowhead])

    # Create the codes to define path
    codes = [matplotlib.path.Path.LINETO] * len(verts)
    codes[0] = matplotlib.path.Path.MOVETO

    codes[2 * num_points] = matplotlib.path.Path.MOVETO

    # Create the path
    path = matplotlib.path.Path(verts, codes)
    return path


def reactionArrow():
    verts = np.array(
        [
            [0, 0],
            [0.8, 0],
            [0.7, 0.1],
            [1.0, 0.0],
            [0.7, -0.1],
            [0.8, 0],
            [0, 0],
            [0, 0],
        ],
        dtype=float,
    )

    codes = [matplotlib.path.Path.LINETO] * 8
    codes[0] = matplotlib.path.Path.MOVETO
    codes[-1] = matplotlib.path.Path.CLOSEPOLY

    path = matplotlib.path.Path(verts, codes)
    return path


# roller_support=reactionArrow()
# marker = roller_support.transformed(matplotlib.transforms.Affine2D().rotate_deg(0))

# t = np.arange(0.0,1.5,0.25)
# s = np.sin(2*np.pi*t)

# fig,ax = plt.subplots()
# ax.plot(t,s, marker=marker, color='k',markerfacecolor='#ff3300',markeredgecolor='#ff3300', markersize=50,alpha=0.8)
# ax.margins(.20)

# plt.show()
