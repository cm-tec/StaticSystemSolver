import matplotlib.pyplot as plt

from example_static_systems import (
    create_beam_on_two_supports_with_cantilever_arm,
    create_bernoulli_beam,
    create_bernoulli_beam_with_area_load,
    create_cantilever_arm,
    create_cantilever_arm_with_support,
    create_frame,
    create_rhein_bruecke,
)
from new_utilities import set_lim
from plotter import plot_static_system
from static_system_solution import StaticSystemSolution
from static_system_solver import StaticSystemSolver


def test_plot_system(
    static_system,
    show_reaction_forces=True,
    show_loads=True,
    show_element_id=True,
):
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.grid(True)

    solver = StaticSystemSolver(static_system)

    solution = StaticSystemSolution(
        displacements=solver.get_displacements(),
        external_forces=solver.get_external_forces(),
        internal_forces=[
            solver.get_internal_forces_of_element(i + 1)
            for i in range(len(static_system.get_elements()))
        ],
    )

    plot_static_system(
        ax=ax,
        static_system=static_system,
        static_system_solution=solution,
        show_reaction_forces=show_reaction_forces,
        show_loads=show_loads,
        show_element_id=show_element_id,
    )

    set_lim(ax=ax)

    # ax.set_xlim(-50, 700)
    # ax.set_ylim(-50, 100)

    plt.show()


# test_plot_system(create_cantilever_arm_with_support(f_z_k=2, EI=1))

# test_plot_system(create_beam_on_two_supports_with_cantilever_arm())

test_plot_system(create_frame(f_x=0.5, f_z=0))

# test_plot_system(create_bernoulli_beam_with_area_load(q_z=1))

# test_plot_system(create_bernoulli_beam())

# test_plot_system(create_cantilever_arm(f_z_k=2))

"""
test_plot_system(
    create_rhein_bruecke(
        EA_fahrbahn=1,
        EI_fahrbahn=10e9,
        EA_stuetze=168 * 10e6,
        EI_stuetze=10000,
        EA_seil=12 * 10e6,
        EI_seil=1,
        q_z_fahrbahn=1000,
    ),
    show_element_id=False,
    show_reaction_forces=False,
    show_loads=False,
)
"""
