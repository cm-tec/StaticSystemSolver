import matplotlib.pyplot as plt
import numpy as np
from models.element import Element
from models.node import Node
from models.settings import Settings
from models.support import Support
from new_utilities import set_lim


temp_storage = []


def create_new_dof(dof):
    global temp_storage
    global ndofs
    if dof not in temp_storage:
        temp_storage.add(dof)
        return dof
    ndofs += 1
    return ndofs


fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.grid(True)


def get_degree_of_freedom(node):
    if node.support == Support.PINNED:
        return node.dof_x, node.dof_y, create_new_dof(node.dof_phi)
    elif node.support == Support.ROLLER:
        return node.dof_x, node.dof_y, create_new_dof(node.dof_phi)
    elif node.support == Support.CLAMPED:
        return node.dof_x, node.dof_y, node.dof_phi
    elif node.support == Support.MOMENT_JOINT:
        return node.dof_x, node.dof_y, create_new_dof(node.dof_phi)
    else:
        return node.dof_x, node.dof_y, node.dof_phi


l = 1
EI = 1
EA = 1
q_z = 1

nodes = {
    1: Node(id=1, x=0, y=0, support=Support.CLAMPED),
    2: Node(id=2, x=l, y=0, support=Support.MOMENT_JOINT),
}


temp_storage = set()
ndofs = 3 * len(nodes)

elements = {
    1: Element(
        node_i=nodes[1],
        node_k=nodes[2],
        f=get_degree_of_freedom,
        q_z=q_z,
        q_x=1,
        EI=EI,
        EA=EA,
    ),
}


for i, node in nodes.items():
    node.plot(ax=ax, show_displacements=True)
    node.plot(
        ax=ax,
        show_displacements=False,
        show_forces=False,
        show_reaction_forces=False,
    )

# Plot displacement Graph
for i, element in elements.items():
    """element.plot(
        ax=ax,
        show_displacements=False,
        bar_color="lightsteelblue",
    )"""
    element.plot(ax=ax, show_displacements=True)

set_lim(ax=ax)
plt.show()
