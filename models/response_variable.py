from enum import Enum


class ResponseVariableElement(Enum):
    NI = "N_i"
    VI = "V_i"
    MYI = "M_y_i"
    NK = "N_k"
    VK = "V_k"
    MYK = "M_y_k"
    U_I = "U_i"
    W_I = "W_i"
    PHI_I = "PHI_i"
    U_K = "U_i"
    W_K = "W_i"
    PHI_K = "PHI_i"


class ResponseVariableDisplacement(Enum):
    U_I = "u_i"
    W_I = "w_i"
    PHI_I = "phi_i"
    U_K = "u_k"
    W_K = "w_k"
    PHI_K = "phi_k"


class ResponseVariableInternalForce(Enum):
    N_I = "n_i"
    V_I = "v_i"
    M_Y_I = "m_y_i"
    N_K = "n_k"
    V_K = "v_k"
    M_Y_K = "m_y_k"


class ResponseVariableType(Enum):
    DISPLACEMENT = "DISPLACEMENT"
    INTERNAL_FORCE = "INTERNAL_FORCE"


class ResponseVariableNode(Enum):
    DISPLACEMENT_X = "displacement_x"
    DISPLACEMENT_Y = "displacement_y"
    DISPLACEMENT_PHI = "displacement_phi"
