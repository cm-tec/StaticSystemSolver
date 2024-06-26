import matplotlib.pyplot as plt
import numpy as np
from models.design_parameter import DesignParameterElement, DesignParameterNode
from models.element import Element
from models.node import Node
from models.response_variable import (
    ResponseVariableDisplacement,
    ResponseVariableElement,
    ResponseVariableInternalForce,
    ResponseVariableNode,
    ResponseVariableType,
)
from models.settings import Settings
from models.support import Support
from new_utilities import set_lim


"""
pyside6-designer   
pyside6-uic "Ui File/main.ui" -o ui_main.py
"""

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
    3: Node(id=3, x=l, y=-l, support=Support.PINNED),
}


temp_storage = set()
ndofs = 3 * len(nodes)

elements = {
    1: Element(
        node_i=nodes[1],
        node_k=nodes[2],
        f=get_degree_of_freedom,
        q_z=q_z,
        EI=EI,
        EA=EA,
    ),
    2: Element(
        node_i=nodes[2],
        node_k=nodes[3],
        f=get_degree_of_freedom,
        q_z=0,
        EI=EI,
        EA=EA,
    ),
}


# Initialize K
K = np.zeros((ndofs, ndofs))

for element in elements.values():
    dofs_element = element.degrees_of_freedom

    K_element = element.k_global
    B = np.zeros((6, ndofs))
    dof_index = np.array(dofs_element) - 1

    for i in range(6):
        B[i, dof_index[i]] = 1.0

    K += B.T.dot(K_element).dot(B)


restrained_dofs = []


# Construct F_0...
F_0 = np.zeros(ndofs)

# ... by adding all holding forces resulting from forces acting directly on nodes (therefore "-"")...
for node in nodes.values():
    F_0[node.id * 3 - 3 : node.id * 3] -= node.F

    restrained_dofs.extend([dof for dof in node.restrained_degrees_of_freedom])

# ... and by adding all holding forces resulting from surface loads
for element in elements.values():
    F_0[element.node_i.id * 3 - 3 : element.node_i.id * 3] += element.F_0_global[0:3]
    F_0[element.node_k.id * 3 - 3 : element.node_k.id * 3] += element.F_0_global[3:6]


non_restrained_dofs = [dof for dof in range(1, ndofs + 1) if dof not in restrained_dofs]

restrained_ndofs = len(restrained_dofs)
non_restrained_ndofs = len(non_restrained_dofs)


restrained_indices = np.array(restrained_dofs) - 1
non_restrained_indices = np.array(non_restrained_dofs) - 1

# Remove all restrained Rows and Columns (D = 0)
non_restrained_K = np.delete(
    np.delete(K, restrained_indices, axis=0), restrained_indices, axis=1
)

non_restrained_F_0 = np.delete(F_0, restrained_indices)

if np.isclose(np.linalg.det(non_restrained_K), 0.0):
    raise Exception("Matrix is singular. Inversion not possible.")

# Calculate non_restrained_U
non_restrained_U = np.linalg.inv(non_restrained_K).dot(-non_restrained_F_0)


# Construct U, by setting the restrained displacements to zero
U = np.zeros(ndofs)
for i, j in enumerate(non_restrained_dofs):
    U[j - 1] = non_restrained_U[i]

# Update the displacements of the nodes
for node in nodes.values():
    node.set_displacements(*tuple(U[dof - 1] for dof in node.degrees_of_freedom))

S = np.around(F_0 + K.dot(U), 3)
for node in nodes.values():
    node.R_F_x, node.R_F_y, node.R_M_y = tuple(
        S[dof - 1] for dof in node.degrees_of_freedom
    )


for element in elements.values():
    U_element = np.zeros(6)

    for i, d in enumerate(np.array(element.degrees_of_freedom)):
        U_element[i] = U[d - 1]

    U_element_local = np.dot(element.get_tau(), U_element)

    # S = F_0 + F_i
    # S = F_0 + K * U
    S_element_local = element.F_0 + element.k.dot(U_element_local)

    element.set_internal_forces_from_external_forces(*S_element_local)


for node in nodes.values():
    node.plot(ax=ax, show_displacements=True)

for element in elements.values():
    element.plot(ax=ax)


# set_lim(ax=ax)
# plt.show()


# adjungierte sensitivity analaysis


"""

Global vs Local (G vs L)
Total vs Element (T vs E)

D... Derived
NR... non restrained
R ... restrained
"""


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


# Select Displacements or internal Force as Response Variable

responseVariableType = ResponseVariableType.INTERNAL_FORCE


# Select the element from which the response variable should be selected
response_element_id = 1
response_element = elements[response_element_id]

if responseVariableType is ResponseVariableType.DISPLACEMENT:
    # Select the response variable
    response_variable = ResponseVariableDisplacement("W_k")

    # Get the degree of freedom number of the selected displacement

    response_variable_dof = response_element.degrees_of_freedom[
        list(ResponseVariableDisplacement).index(response_variable)
    ]

    # Calculate the sensitivity
    if response_variable_dof in restrained_dofs:
        # TODO: Handle this case
        print("Alle Ableitungen gleich null")
    else:
        non_restrained_K_inv = np.linalg.inv(non_restrained_K)

        print(
            f"Die Sensitivät von {response_variable.value} des Elements {response_element_id} gegenüber..."
        )

        for p_element_id, p_element in elements.items():
            for parameter in DesignParameterElement:
                p_value = parameter.value

                # Construct Matrix to convert element to non_restrained_total
                M_element_to_non_restrained_total = (
                    get_M_element_to_non_restrained_total(
                        non_restrained_dofs=non_restrained_dofs,
                        element_dofs=p_element.degrees_of_freedom,
                    )
                )

                F_0_element_ableitung = p_element.F_0_derived_global(p_value=p_value)

                K_ableitung_element = p_element.k_derived_global(p_value=p_value)
                U_element = p_element.displacements

                non_restrained_F_star = M_element_to_non_restrained_total.dot(
                    -F_0_element_ableitung - K_ableitung_element.dot(U_element)
                )

                U_i_ableitung = non_restrained_K_inv.dot(non_restrained_F_star)[
                    non_restrained_dofs.index(response_variable_dof)
                ]

                print(
                    f"      ... {parameter.value} des Elements {p_element_id} beträgt: {U_i_ableitung}"
                )


elif responseVariableType is ResponseVariableType.INTERNAL_FORCE:
    # Select the response variable
    response_variable = ResponseVariableInternalForce.M_Y_I

    # Get the internal Force index
    internal_force_index = list(ResponseVariableInternalForce).index(response_variable)

    # Calculate the sensitivity
    non_restrained_K_inv = np.linalg.inv(non_restrained_K)

    K_element_local = response_element.k
    K_element_local_i = K_element_local[internal_force_index, :]

    # Construct Matrix to convert non_restrained_global to global
    M_non_restrained_total_to_total = get_M_non_restrained_total_to_total(
        ndofs=ndofs,
        non_restrained_dofs=non_restrained_dofs,
        element_dofs=response_element.degrees_of_freedom,
    )

    # Construct Matrix to convert Global to element
    M_total_to_element = get_M_total_to_element(
        ndofs=ndofs,
        element_dofs=response_element.degrees_of_freedom,
    )

    # Construct Matrix to convert element_global to element_local
    M_element_global_to_element_local = response_element.get_tau()

    zeta_base = (
        K_element_local_i.dot(M_element_global_to_element_local)
        .dot(M_total_to_element)
        .dot(M_non_restrained_total_to_total)
        .dot(non_restrained_K_inv)
    )

    print(
        f"Die Sensitivät von {response_variable.value} des Elements {response_element_id} gegenüber..."
    )

    for p_element_id, p_element in elements.items():
        # Construct U_element
        U_element_local = p_element.local_displacements

        # Construct Matrix to convert element_local to element_global
        M_element_local_to_element_global = p_element.get_tau().T

        # Construct Matrix to convert element to non_restrained_global
        M_element_to_non_restrained_total = get_M_element_to_non_restrained_total(
            non_restrained_dofs=non_restrained_dofs,
            element_dofs=p_element.degrees_of_freedom,
        )

        zeta_0 = np.zeros(6)
        if response_element_id == p_element_id:
            zeta_0[internal_force_index] = -1

        zeta = zeta_base.dot(M_element_to_non_restrained_total).dot(
            M_element_local_to_element_global
        )

        for parameter in DesignParameterElement:
            p_value = parameter.value

            K_element_local_ableitung = p_element.k_derived(p_value=p_value)
            F_0_element_local_ableitung = p_element.F_0_derived(p_value=p_value)

            F_star_element_local = (
                -F_0_element_local_ableitung
                - K_element_local_ableitung.dot(U_element_local)
            )

            S_element_local_i_ableitung = calculate_response_variable(
                zeta_0=zeta_0,
                zeta=zeta,
                F_star=F_star_element_local,
            )  # np.dot((zeta_0 + zeta), F_star_element_local)

            print(
                f"      ... {parameter.value} des Elements {p_element_id} beträgt: {S_element_local_i_ableitung}"
            )
else:
    raise Exception("Unkown ResponseVaribleType selected")


"""
# External Inputs
element_id = 1
# 2... M_i
IFs_index = 2


element = elements[element_id]

non_restrained_K_inv = np.linalg.inv(non_restrained_K)

K_element_local = element.k
K_element_local_i = K_element_local[IFs_index, :]


# Construct Matrix to convert non_restrained_global to global
M_non_restrained_global_to_global = np.zeros((ndofs, non_restrained_ndofs))
for i, d in enumerate(np.array(element.degrees_of_freedom)):
    if d in non_restrained_dofs:
        M_non_restrained_global_to_global[i][non_restrained_dofs.index(d)] = 1


# Construct Matrix to convert Global to element
M_global_to_element = np.zeros((6, ndofs))
for i, d in enumerate(element.degrees_of_freedom):
    M_global_to_element[i][d - 1] = 1

# Construct Matrix to convert element_global to element_local
M_element_global_to_element_local = element.get_tau()


zeta_base = (
    K_element_local_i.dot(M_element_global_to_element_local)
    .dot(M_global_to_element)
    .dot(M_non_restrained_global_to_global)
    .dot(non_restrained_K_inv)
)

for p_element_id, p_element in elements.items():
    # Construct U_element
    U_element_local = p_element.local_displacements

    # Construct Matrix to convert element_local to element_global
    M_element_local_to_element_global = p_element.get_tau().T

    # Construct Matrix to convert element to non_restrained_global
    M_element_to_non_restrained_global = np.zeros((non_restrained_ndofs, 6))
    for i, d in enumerate(p_element.degrees_of_freedom):
        if d in non_restrained_dofs:
            M_element_to_non_restrained_global[non_restrained_dofs.index(d)][i] = 1

    zeta_0 = np.zeros(6)
    if element_id == p_element_id:
        zeta_0[IFs_index] = -1

    zeta = zeta_base.dot(M_element_to_non_restrained_global).dot(
        M_element_local_to_element_global
    )
    print(f"Die Sensitivät von {IFs_index} des Elements {element_id} gegenüber...")

    for parameter in DesignParameterElement:
        p_value = parameter.value

        K_element_local_ableitung = p_element.k_derived(p_value=p_value)
        F_0_element_local_ableitung = p_element.F_0_derived(p_value=p_value)

        F_star_element_local = (
            -F_0_element_local_ableitung
            - K_element_local_ableitung.dot(U_element_local)
        )

        S_element_local_i_ableitung = np.dot((zeta_0 + zeta), F_star_element_local)

        print(
            f"      ... {parameter.value} des Elements {p_element_id} beträgt: {S_element_local_i_ableitung}"
        )
"""

"""
# External Inputs
r_node_id = 2
r_node = nodes[r_node_id]
r_value = "displacement_y"
response = ResponseVariableNode(r_value)

r_dof = r_node.degrees_of_freedom[1]


if r_dof in restrained_dofs:
    print("Alle Ableitungen gleich null")
else:
    non_restrained_K_inv = np.linalg.inv(non_restrained_K)

    print(f"Die Sensitivät von {response.value} des Knoten {r_node_id} gegenüber...")

    for p_element_id, p_element in elements.items():
        for parameter in DesignParameterElement:
            p_value = parameter.value

            # Construct Matrix to convert element to non_restrained_total
            M_element_to_non_restrained_total = np.zeros((non_restrained_ndofs, 6))
            for i, d in enumerate(p_element.degrees_of_freedom):
                if d in non_restrained_dofs:
                    M_element_to_non_restrained_total[non_restrained_dofs.index(d)][
                        i
                    ] = 1

            F_0_element_ableitung = p_element.F_0_derived_global(p_value=p_value)

            K_ableitung_element = p_element.k_derived_global(p_value=p_value)
            U_element = p_element.displacements

            non_restrained_F_star = M_element_to_non_restrained_total.dot(
                -F_0_element_ableitung - K_ableitung_element.dot(U_element)
            )

            U_i_ableitung = non_restrained_K_inv.dot(non_restrained_F_star)[
                non_restrained_dofs.index(r_dof)
            ]

            print(
                f"      ... {parameter.value} des Elements {p_element_id} beträgt: {U_i_ableitung}"
            )
"""

"""


dof     Degree of freedom
dofs    Degrees of freedom

S       External Forces Vector consisting of retention forces S_i
U       Displacement vector consisting of displacements D_i
F_0     F resulting from Load condition
F_i     F resulting from displacements
K       System stiffness matrix
M_n     Matrix to convert vector x from non_restrained to total: M_n * non_restrained_x = x


S = F_0 + F_i
S = F_0 + K * U

For restrained dofs is by definition    D_i = 0     => restrained_U     = 0
For non restrained dof is               S_i = 0     => non_restrained_S = 0

If only considering non restrained dofs the equation can be simplified to:
0 = non_restrained_F_0 + non_restrained_F_i
0 = non_restrained_F_0 + non_restrained_K * non_restrained_U

non_restrained_U = inv(non_restrained_K) *  (-non_restrained_F_0)
U = M_n * non_restrained_U = M_n * inv(non_restrained_K) *  (-non_restrained_F_0)






U_ableitung = M_n * ( non_restrained_K_inv * (-non_restrained_F_0_ableitung) + non_restrained_K_inv_ableitung * (-non_restrained_F_0) )

ableitung( A_inv * A = E )
A_inv_ableitung *  A + A_inv * A_ableitung = 0
A_inv_ableitung *  A = - A_inv * A_ableitung

non_restrained_F_0 = - non_restrained_K * non_restrained_U

U_ableitung = M_n * ( non_restrained_K_inv * (-non_restrained_F_0_ableitung) + non_restrained_K_inv_ableitung * (-non_restrained_F_0) )
            = M_n * ( non_restrained_K_inv * (-non_restrained_F_0_ableitung) + non_restrained_K_inv_ableitung * non_restrained_K * non_restrained_U )
            = M_n * ( non_restrained_K_inv * (-non_restrained_F_0_ableitung) - non_restrained_K_inv * non_restrained_K_ableitung * non_restrained_U )
            = M_n * non_restrained_K_inv * (-non_restrained_F_0_ableitung - non_restrained_K_ableitung * non_restrained_U )

SENSITIVTY

S_ableitung = F_0_ableitung + F_i_ableitung
F_i_ableitung = K_ableitung * U + K * U_ableitung

S_ableitung = F_0_ableitung + K_ableitung * U + K * U_ableitung
            = F_0_ableitung + K_ableitung * U + K * M_n * non_restrained_K_inv * (-non_restrained_F_0_ableitung - non_restrained_K_ableitung * non_restrained_U )

S_i_ableitung   = F_0_i_ableitung + K_i_ableitung * U + K_i * M_n * non_restrained_K_inv * (-non_restrained_F_0_ableitung - non_restrained_K_ableitung * non_restrained_U )
                    
F_star                  = - F_0_ableitung - K_ableitung * U
non_restrained_F_star   = - non_restrained_F_0_ableitung - non_restrained_K_ableitung * non_restrained_U 

F_star = M_n * non_restrained_F_star                    #### TO CHECK / VALIDATE
non_restrained_F_star = M_n_trans * F_star

zeta_0 = [0 .. -1 .. 0]        -1 at the i-th column
F_0_i_ableitung + K_i_ableitung * U =  zeta_0 * (- F_0_ableitung - K_ableitung * U) = zeta_0 * F_star

zeta = K_i * M_n * non_restrained_K_inv * M_n_trans

S_i_ableitung   = zeta_0 * F_star + K_i * M_n * non_restrained_K_inv * M_n_trans * F_star
                = (zeta_0 + zeta) * F_star 

                












S_element_local = F_0_element_local + F_i_element_local
S_element_local = F_0_element_local + K_element_local * U_element_local


E * x = x_element
T * x = x_local

U_element_local = T * E * U = T * E * M_n * non_restrained_U = T * E * M_n * inv(non_restrained_K) *  (-non_restrained_F_0)






U_element_local_ableitung = T * E * M_n * non_restrained_K_inv * (-non_restrained_F_0_ableitung - non_restrained_K_ableitung * non_restrained_U )
            

SENSITIVTY

S_element_local__ableitung = F_0_element_local_ableitung + F_i_element_local__ableitung
F_i_element_local_ableitung = K_element_local_ableitung * U_element_local + K_element_local * U_element_local_ableitung

S_element_local_ableitung = F_0_element_local_ableitung + K_element_local_ableitung * U_element_local + K_element_local * U_element_local_ableitung
            = F_0_element_local_ableitung + K_element_local_ableitung * U_element_local + K_element_local * T * E * M_n * non_restrained_K_inv * (-non_restrained_F_0_ableitung - non_restrained_K_ableitung * non_restrained_U )

S_element_local_i_ableitung = F_0_element_local_i_ableitung + K_element_local_i_ableitung * U + K_element_local_i * T * E * M_n * non_restrained_K_inv * (-non_restrained_F_0_ableitung - non_restrained_K_ableitung * non_restrained_U )
                    
F_star_element_local        = - F_0_element_local_ableitung - K_element_local_ableitung * U_element_local

zeta_0 = [0 .. -1 .. 0]        -1 at the i-th column
F_0_element_local_i_ableitung + K_element_local_i_ableitung * U =  zeta_0 * (- F_0_element_local_ableitung - K_element_local_ableitung * U) = zeta_0 * F_star_element_local


S_element_local_i_ableitung = zeta_0 * F_star_element_local + K_element_local_i * T * E * M_n * non_restrained_K_inv * non_restrained_F_star



non_restrained_X = C_e * x_element

X = T_e * X_local

non_restrained_F_star = C_e * F_star_element = C_e * T_e * F_star_element_local


S_element_local_i_ableitung = zeta_0 * F_star_element_local + K_element_local_i * T * E * M_n * non_restrained_K_inv * C_e * T_e * F_star_element_local

zeta = K_element_local_i * T * E * M_n * non_restrained_K_inv * C_e * T_e


S_element_local_i_ableitung = zeta_0 * F_star_element_local + zeta * F_star_element_local
                            = (zeta_0 + zeta) * F_star_element_local


                            



For displacements:


U_element_local_ableitung   = T * E * M_n * non_restrained_K_inv * (-non_restrained_F_0_ableitung - non_restrained_K_ableitung * non_restrained_U )
                            = T * E * M_n * non_restrained_K_inv * non_restrained_F_star
                            = T * E * M_n * non_restrained_K_inv * C_e * T_e * F_star_element_local
"""
