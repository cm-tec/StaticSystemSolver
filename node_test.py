import unittest


from node import Node, SupportMustBeGreaterZero, SupportMustBeLessNine
from vector import vector

from numpy.testing import assert_array_equal


class TestNode(unittest.TestCase):

    def test_create_node(self):
        node = Node(id=1)

        self.assertIsNotNone(node)

    def test_get_id(self):
        node = Node(id=7)

        self.assertEqual(node.id, 7)

    def test_get_coordinate(self):
        node = Node(id=1, x=1, y=2)

        assert_array_equal(node.get_coordinate(), vector(1, 2))

    def test_get_dof(self):

        for id in range(1, 20, 1):
            node = Node(id=id)

            assert_array_equal(node.get_dofs(), vector(id * 3 - 2, id * 3 - 1, id * 3))

    def test_default_support_is_0(self):
        node = Node(id=1)

        self.assertEqual(node.get_support(), 0)

    def test_support_must_be_greater_0(self):
        self.assertRaises(
            SupportMustBeGreaterZero,
            lambda: Node(id=1, support=-1),
        )

    def test_support_must_be_less_9(self):
        self.assertIsNotNone(Node(id=1, support=8))

        self.assertRaises(
            SupportMustBeLessNine,
            lambda: Node(id=1, support=9),
        )

    def test_get_support(self):
        node = Node(id=1, support=3)

        self.assertEqual(node.get_support(), 3)

    def test_get_restrained_dofs(self):
        node = Node(id=1, x=1, y=2, support=0)
        assert_array_equal(node.get_restrained_dofs(), vector())

        node = Node(id=1, x=1, y=2, support=1)
        assert_array_equal(node.get_restrained_dofs(), vector(1))

        node = Node(id=1, x=1, y=2, support=2)
        assert_array_equal(node.get_restrained_dofs(), vector(2))

        node = Node(id=1, x=1, y=2, support=3)
        assert_array_equal(node.get_restrained_dofs(), vector(3))

        node = Node(id=1, x=1, y=2, support=4)
        assert_array_equal(node.get_restrained_dofs(), vector(1, 2))

        node = Node(id=1, x=1, y=2, support=5)
        assert_array_equal(node.get_restrained_dofs(), vector(1, 3))

        node = Node(id=1, x=1, y=2, support=6)
        assert_array_equal(node.get_restrained_dofs(), vector(2, 3))

        node = Node(id=1, x=1, y=2, support=7)
        assert_array_equal(node.get_restrained_dofs(), vector(1, 2, 3))
