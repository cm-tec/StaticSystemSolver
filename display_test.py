import unittest

from display import Display
from example_static_systems import (
    create_beam_on_two_supports_with_cantilever_arm,
    create_bernoulli_beam_with_area_load,
    create_cantilever_arm_with_support,
)

from numpy.testing import assert_array_equal


class TestDisplay(unittest.TestCase):

    def test_prepare_static_system_for_display_returns_dict(self):
        static_system = create_cantilever_arm_with_support(q_z=2)

        self.assertIsInstance(
            Display.prepare_static_system_for_display(static_system), dict
        )

    def test_dict_of_length_equal_number_of_nodes(self):
        static_system = create_cantilever_arm_with_support(q_z=2)

        self.assertEqual(
            len(Display.prepare_static_system_for_display(static_system)), 3
        )

        static_system = create_bernoulli_beam_with_area_load(q_z=1)
        self.assertEqual(
            len(Display.prepare_static_system_for_display(static_system)), 2
        )

    def test_dict_key_equal_coords_of_node(self):
        static_system = create_cantilever_arm_with_support(q_z=2)
        assert_array_equal(
            list(Display.prepare_static_system_for_display(static_system).keys()),
            ["x=0 z=0", "x=1 z=0", "x=1 z=-1"],
        )

        static_system = create_bernoulli_beam_with_area_load(q_z=1)

        assert_array_equal(
            list(Display.prepare_static_system_for_display(static_system).keys()),
            ["x=0 z=0", "x=1 z=0"],
        )

    def test_dict(self):
        static_system = create_cantilever_arm_with_support(q_z=2)
        self.assertEqual(
            Display.prepare_static_system_for_display(static_system),
            {
                "x=0 z=0": {
                    "dof_x": {1: {"dependencies": False, "restrained": True}},
                    "dof_z": {2: {"dependencies": False, "restrained": True}},
                    "dof_phi": {3: {"dependencies": False, "restrained": True}},
                },
                "x=1 z=0": {
                    "dof_x": {4: {"dependencies": True, "restrained": False}},
                    "dof_z": {5: {"dependencies": True, "restrained": False}},
                    "dof_phi": {
                        6: {"dependencies": False, "restrained": False},
                        9: {"dependencies": False, "restrained": False},
                    },
                },
                "x=1 z=-1": {
                    "dof_x": {10: {"dependencies": False, "restrained": True}},
                    "dof_z": {11: {"dependencies": False, "restrained": True}},
                    "dof_phi": {12: {"dependencies": False, "restrained": False}},
                },
            },
        )

    def test_is_phi_of_node_restrained(self):
        # If only one dof, phi_of_node_restrained = (restrained of dof)

        data = {3: {"dependencies": False, "restrained": True}}
        self.assertEqual(Display.is_phi_of_node_restrained(data), True)

        data = {3: {"dependencies": False, "restrained": False}}
        self.assertEqual(Display.is_phi_of_node_restrained(data), False)

        data = {3: {"dependencies": True, "restrained": True}}
        self.assertEqual(Display.is_phi_of_node_restrained(data), True)

        data = {3: {"dependencies": True, "restrained": False}}
        self.assertEqual(Display.is_phi_of_node_restrained(data), False)

        # If multiple dofs the dof with dependencies is placed in the middle

        data = {
            6: {"dependencies": False, "restrained": False},
            9: {"dependencies": True, "restrained": False},
        }
        self.assertEqual(Display.is_phi_of_node_restrained(data), False)

        data = {
            6: {"dependencies": False, "restrained": False},
            9: {"dependencies": True, "restrained": True},
        }
        self.assertEqual(Display.is_phi_of_node_restrained(data), True)

        data = {
            6: {"dependencies": True, "restrained": False},
            9: {"dependencies": False, "restrained": True},
        }
        self.assertEqual(Display.is_phi_of_node_restrained(data), False)

        # If no object has dependencies return always False
        data = {
            6: {"dependencies": False, "restrained": False},
            9: {"dependencies": False, "restrained": False},
        }
        self.assertEqual(Display.is_phi_of_node_restrained(data), False)

        data = {
            6: {"dependencies": False, "restrained": False},
            9: {"dependencies": False, "restrained": True},
        }
        self.assertEqual(Display.is_phi_of_node_restrained(data), False)

        data = {
            6: {"dependencies": False, "restrained": False},
            9: {"dependencies": False, "restrained": True},
        }
        self.assertEqual(Display.is_phi_of_node_restrained(data), False)

    def test_get_dof_of_node(self):
        # If only one dof, phi_of_node_restrained = (restrained of dof)
        data = {3: {"dependencies": False, "restrained": True}}
        self.assertEqual(Display.get_dof_of_node(data), 3)

        data = {5: {"dependencies": False, "restrained": False}}
        self.assertEqual(Display.get_dof_of_node(data), 5)

        data = {6: {"dependencies": True, "restrained": True}}
        self.assertEqual(Display.get_dof_of_node(data), 6)

        data = {1: {"dependencies": True, "restrained": False}}
        self.assertEqual(Display.get_dof_of_node(data), 1)

        # If multiple dofs the dof with dependencies is returned

        data = {
            6: {"dependencies": False, "restrained": False},
            9: {"dependencies": True, "restrained": False},
        }
        self.assertEqual(Display.get_dof_of_node(data), 9)

        data = {
            6: {"dependencies": False, "restrained": False},
            9: {"dependencies": True, "restrained": True},
        }
        self.assertEqual(Display.get_dof_of_node(data), 9)

        data = {
            6: {"dependencies": True, "restrained": False},
            9: {"dependencies": False, "restrained": True},
        }
        self.assertEqual(Display.get_dof_of_node(data), 6)

        # If no object has dependencies return first
        data = {
            6: {"dependencies": False, "restrained": False},
            9: {"dependencies": False, "restrained": False},
        }
        self.assertEqual(Display.get_dof_of_node(data), 6)

        data = {
            6: {"dependencies": False, "restrained": False},
            9: {"dependencies": False, "restrained": True},
        }
        self.assertEqual(Display.get_dof_of_node(data), 6)

        data = {
            6: {"dependencies": False, "restrained": False},
            9: {"dependencies": False, "restrained": True},
        }
        self.assertEqual(Display.get_dof_of_node(data), 6)

    def test_should_place_moment_joint(self):

        static_system = create_cantilever_arm_with_support(q_z=2)

        self.assertEqual(Display.should_place_moment_joint(static_system, 3), False)

        self.assertEqual(Display.should_place_moment_joint(static_system, 6), False)

        self.assertEqual(Display.should_place_moment_joint(static_system, 9), True)

        self.assertEqual(Display.should_place_moment_joint(static_system, 12), False)

        static_system = create_beam_on_two_supports_with_cantilever_arm()

        self.assertEqual(Display.should_place_moment_joint(static_system, 3), False)

        self.assertEqual(Display.should_place_moment_joint(static_system, 6), False)

        # Return always false if dof dependends on other dof
        self.assertEqual(Display.should_place_moment_joint(static_system, 9), False)

        self.assertEqual(Display.should_place_moment_joint(static_system, 12), False)
