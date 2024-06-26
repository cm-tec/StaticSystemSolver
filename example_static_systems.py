from static_system import StaticSystem
from vector import vector


def create_bernoulli_beam():
    static_system = StaticSystem()

    static_system.create_element(vector(0, 0), vector(1, 0), f_z_k=1)
    static_system.create_element(vector(1, 0), vector(2, 0), f_z_i=1)

    for dof in [1, 2, 11]:
        static_system.set_restrained_dof(dof=dof)

    static_system.set_boundary_condition(dof=7, times=1, is_equal_to_dof=4)
    static_system.set_boundary_condition(dof=8, times=1, is_equal_to_dof=5)
    static_system.set_boundary_condition(dof=9, times=1, is_equal_to_dof=6)

    return static_system


def create_bernoulli_beam_with_area_load(q_z=1):
    static_system = StaticSystem()

    static_system.create_element(vector(0, 0), vector(1, 0), q_z=q_z)

    for dof in [1, 2, 5]:
        static_system.set_restrained_dof(dof=dof)

    return static_system


def create_beam_on_two_supports_with_cantilever_arm(
    l=2,
    c=1,
    F_right=1,
    EA=1,
    EI=1,
    q_z_1=0,
    q_z_2=0,
):
    static_system = StaticSystem()

    static_system.create_element(vector(0, 0), vector(l, 0), EA=EA, EI=EI, q_z=q_z_1),
    static_system.create_element(
        vector(l, 0),
        vector(l + c, 0),
        EA=EA,
        EI=EI,
        f_z_k=F_right,
        q_z=q_z_2,
    )

    for dof in [1, 2, 5]:
        static_system.set_restrained_dof(dof=dof)

    static_system.set_boundary_condition(dof=7, times=1, is_equal_to_dof=4)
    static_system.set_boundary_condition(dof=8, times=1, is_equal_to_dof=5)
    static_system.set_boundary_condition(dof=9, times=1, is_equal_to_dof=6)

    return static_system


def create_frame(EA=1, EI=1, f_x=1, f_z=1):
    static_system = StaticSystem()

    static_system.create_element(vector(0, 0), vector(0, 1), EA=EA, EI=EI, f_x_k=f_x)
    static_system.create_element(vector(0, 1), vector(1, 1), EA=EA, EI=EI, f_z_i=f_z)
    static_system.create_element(vector(1, 1), vector(1, 0), EA=EA, EI=EI)

    for dof in [1, 2, 16, 17]:
        static_system.set_restrained_dof(dof=dof)

    static_system.set_boundary_condition(dof=7, times=1, is_equal_to_dof=4)
    static_system.set_boundary_condition(dof=8, times=1, is_equal_to_dof=5)
    static_system.set_boundary_condition(dof=9, times=1, is_equal_to_dof=6)

    static_system.set_boundary_condition(dof=13, times=1, is_equal_to_dof=10)
    static_system.set_boundary_condition(dof=14, times=1, is_equal_to_dof=11)

    return static_system


def create_cantilever_arm(
    EA=1,
    EI=1,
    l=1,
    f_x_i=0,
    f_z_i=0,
    m_y_i=0,
    f_x_k=0,
    f_z_k=0,
    m_y_k=0,
    q_x=0,
    q_z=0,
):
    static_system = StaticSystem()

    static_system.create_element(
        vector(0, 0),
        vector(l, 0),
        EA=EA,
        EI=EI,
        f_x_i=f_x_i,
        f_z_i=f_z_i,
        m_y_i=m_y_i,
        f_x_k=f_x_k,
        f_z_k=f_z_k,
        m_y_k=m_y_k,
        q_x=q_x,
        q_z=q_z,
    )

    for dof in [1, 2, 3]:
        static_system.set_restrained_dof(dof=dof)

    return static_system


def create_cantilever_arm_with_support(
    EA=1,
    EI=1,
    l=1,
    h=1,
    f_x_i=0,
    f_z_i=0,
    m_y_i=0,
    f_x_k=0,
    f_z_k=0,
    m_y_k=0,
    q_x=0,
    q_z=0,
):
    static_system = StaticSystem()

    static_system.create_element(
        vector(0, 0),
        vector(l, 0),
        EA=EA,
        EI=EI,
        f_x_i=f_x_i,
        f_z_i=f_z_i,
        m_y_i=m_y_i,
        f_x_k=f_x_k,
        f_z_k=f_z_k,
        m_y_k=m_y_k,
        q_x=q_x,
        q_z=q_z,
    )
    static_system.create_element(vector(l, 0), vector(l, -h), EA=EA, EI=EI)

    for dof in [1, 2, 3, 10, 11]:
        static_system.set_restrained_dof(dof=dof)

    static_system.set_boundary_condition(dof=7, times=1, is_equal_to_dof=4)
    static_system.set_boundary_condition(dof=8, times=1, is_equal_to_dof=5)

    return static_system


def create_cantilever_arm_with_diagonal_support(
    EA=1,
    EI=1,
    l=1,
    h=1,
    f_x_i=0,
    f_z_i=0,
    m_y_i=0,
    f_x_k=0,
    f_z_k=0,
    m_y_k=0,
    q_x=0,
    q_z=0,
):
    static_system = StaticSystem()

    static_system.create_element(
        vector(0, 0),
        vector(l, 0),
        EA=EA,
        EI=EI,
        f_x_i=f_x_i,
        f_z_i=f_z_i,
        m_y_i=m_y_i,
        f_x_k=f_x_k,
        f_z_k=f_z_k,
        m_y_k=m_y_k,
        q_x=q_x,
        q_z=q_z,
    )
    static_system.create_element(vector(l, 0), vector(l + 1, h), EA=EA, EI=EI)

    for dof in [1, 2, 3, 10, 11]:
        static_system.set_restrained_dof(dof=dof)

    static_system.set_boundary_condition(dof=7, times=1, is_equal_to_dof=4)
    static_system.set_boundary_condition(dof=8, times=1, is_equal_to_dof=5)

    return static_system


def create_rhein_bruecke(
    EA_fahrbahn=1000,
    EI_fahrbahn=1000,
    EA_stuetze=1000,
    EI_stuetze=1000,
    EA_seil=1000,
    EI_seil=1,
    q_z_fahrbahn=1,
):
    nodes = [
        {
            "x": 0,
            "z": 0,
            "restrained_x": True,
            "restrained_z": True,
            "restrained_phi": False,
        },
        {
            "x": 100,
            "z": 0,
            "restrained_x": True,
            "restrained_z": True,
            "restrained_phi": False,
        },
        {
            "x": 150,
            "z": 0,
            "restrained_x": False,
            "restrained_z": False,
            "restrained_phi": False,
        },
        {
            "x": 200,
            "z": 0,
            "restrained_x": True,
            "restrained_z": True,
            "restrained_phi": False,
        },
        {
            "x": 250,
            "z": 0,
            "restrained_x": False,
            "restrained_z": False,
            "restrained_phi": False,
        },
        {
            "x": 300,
            "z": 0,
            "restrained_x": False,
            "restrained_z": False,
            "restrained_phi": False,
        },
        {
            "x": 380,
            "z": 0,
            "restrained_x": False,
            "restrained_z": False,
            "restrained_phi": False,
        },
        {
            "x": 430,
            "z": 0,
            "restrained_x": False,
            "restrained_z": False,
            "restrained_phi": False,
        },
        {
            "x": 480,
            "z": 0,
            "restrained_x": True,
            "restrained_z": True,
            "restrained_phi": False,
        },
        {
            "x": 530,
            "z": 0,
            "restrained_x": False,
            "restrained_z": False,
            "restrained_phi": False,
        },
        {
            "x": 580,
            "z": 0,
            "restrained_x": True,
            "restrained_z": True,
            "restrained_phi": False,
        },
        {
            "x": 680,
            "z": 0,
            "restrained_x": True,
            "restrained_z": True,
            "restrained_phi": False,
        },
        {
            "x": 200,
            "z": 22,
            "restrained_x": False,
            "restrained_z": False,
            "restrained_phi": False,
        },
        {
            "x": 200,
            "z": 44,
            "restrained_x": False,
            "restrained_z": False,
            "restrained_phi": False,
        },
        {
            "x": 480,
            "z": 22,
            "restrained_x": False,
            "restrained_z": False,
            "restrained_phi": False,
        },
        {
            "x": 480,
            "z": 44,
            "restrained_x": False,
            "restrained_z": False,
            "restrained_phi": False,
        },
    ]

    elements = [
        {
            "node_i": 1,
            "node_k": 2,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_fahrbahn,
            "EI": EI_fahrbahn,
            "q_x": 0,
            "q_z": q_z_fahrbahn,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 2,
            "node_k": 3,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_fahrbahn,
            "EI": EI_fahrbahn,
            "q_x": 0,
            "q_z": q_z_fahrbahn,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 3,
            "node_k": 4,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_fahrbahn,
            "EI": EI_fahrbahn,
            "q_x": 0,
            "q_z": q_z_fahrbahn,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 4,
            "node_k": 5,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_fahrbahn,
            "EI": EI_fahrbahn,
            "q_x": 0,
            "q_z": q_z_fahrbahn,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 5,
            "node_k": 6,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_fahrbahn,
            "EI": EI_fahrbahn,
            "q_x": 0,
            "q_z": q_z_fahrbahn,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 6,
            "node_k": 7,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_fahrbahn,
            "EI": EI_fahrbahn,
            "q_x": 0,
            "q_z": q_z_fahrbahn,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 7,
            "node_k": 8,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_fahrbahn,
            "EI": EI_fahrbahn,
            "q_x": 0,
            "q_z": q_z_fahrbahn,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 8,
            "node_k": 9,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_fahrbahn,
            "EI": EI_fahrbahn,
            "q_x": 0,
            "q_z": q_z_fahrbahn,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 9,
            "node_k": 10,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_fahrbahn,
            "EI": EI_fahrbahn,
            "q_x": 0,
            "q_z": q_z_fahrbahn,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 10,
            "node_k": 11,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_fahrbahn,
            "EI": EI_fahrbahn,
            "q_x": 0,
            "q_z": q_z_fahrbahn,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 11,
            "node_k": 12,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_fahrbahn,
            "EI": EI_fahrbahn,
            "q_x": 0,
            "q_z": q_z_fahrbahn,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 4,
            "node_k": 13,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_stuetze,
            "EI": EI_stuetze,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 13,
            "node_k": 14,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_stuetze,
            "EI": EI_stuetze,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 2,
            "node_k": 14,
            "connection_type_i": "moment_joint",
            "connection_type_k": "moment_joint",
            "EA": EA_seil,
            "EI": EI_seil,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 3,
            "node_k": 13,
            "connection_type_i": "moment_joint",
            "connection_type_k": "moment_joint",
            "EA": EA_seil,
            "EI": EI_seil,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 5,
            "node_k": 13,
            "connection_type_i": "moment_joint",
            "connection_type_k": "moment_joint",
            "EA": EA_seil,
            "EI": EI_seil,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 6,
            "node_k": 14,
            "connection_type_i": "moment_joint",
            "connection_type_k": "moment_joint",
            "EA": EA_seil,
            "EI": EI_seil,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 9,
            "node_k": 15,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_stuetze,
            "EI": EI_stuetze,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 15,
            "node_k": 16,
            "connection_type_i": "stiff",
            "connection_type_k": "stiff",
            "EA": EA_stuetze,
            "EI": EI_stuetze,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 7,
            "node_k": 16,
            "connection_type_i": "moment_joint",
            "connection_type_k": "moment_joint",
            "EA": EA_seil,
            "EI": EI_seil,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 8,
            "node_k": 15,
            "connection_type_i": "moment_joint",
            "connection_type_k": "moment_joint",
            "EA": EA_seil,
            "EI": EI_seil,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 10,
            "node_k": 15,
            "connection_type_i": "moment_joint",
            "connection_type_k": "moment_joint",
            "EA": EA_seil,
            "EI": EI_seil,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
        {
            "node_i": 11,
            "node_k": 16,
            "connection_type_i": "moment_joint",
            "connection_type_k": "moment_joint",
            "EA": EA_seil,
            "EI": EI_seil,
            "q_x": 0,
            "q_z": 0,
            "f_x_i": 0,
            "f_z_i": 0,
            "m_y_i": 0,
            "f_x_k": 0,
            "f_z_k": 0,
            "m_y_k": 0,
        },
    ]

    return StaticSystem.from_node_and_element_tables(nodes, elements)
