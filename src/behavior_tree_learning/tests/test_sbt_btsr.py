#!/usr/bin/env python

import paths
paths.add_modules_to_path()

import unittest

import os
import random
from behavior_tree_learning.core.sbt import behavior_tree
from behavior_tree_learning.core.sbt import BehaviorTreeStringRepresentation, StringBehaviorTree


class TestBehaviorTreeStringRepresentation(unittest.TestCase):

    def setUp(self):

        behavior_tree.load_settings_from_file(
            os.path.join(paths.get_test_directory(), 'fwk', 'BT_TEST_SETTINGS.yaml'))

    def test_init(self):

        _ = BehaviorTreeStringRepresentation([])

    def test_random(self):

        btsr = BehaviorTreeStringRepresentation([])
        random.seed(1337)

        for length in range(1, 11):
            btsr.random(length)
            assert btsr.length() == length
            assert btsr.is_valid()

    def test_is_valid(self):

        btsr = BehaviorTreeStringRepresentation([])
        self.assertFalse(btsr.is_valid())

        # Valid tree
        btsr.set(['s(', 'c0', 'f(', 'c0', 'a0', ')', 'a0', ')'])
        self.assertTrue(btsr.is_valid())

        # Minimal valid tree - just an action node
        btsr.set(['a0'])
        self.assertTrue(btsr.is_valid())

        # Two control nodes at root level - not valid
        btsr.set(['s(', 'c0', 'f(', 'c0', 'a0', ')', 'a0', ')', 's(', 'a0', ')'])
        self.assertFalse(btsr.is_valid())

        # Action node at root level - not valid
        btsr.set(['s(', 'c0', 'f(', 'c0', 'a0', ')', ')', 'a0', ')'])
        self.assertFalse(btsr.is_valid())

        # Too few up nodes - not valid
        btsr.set(['s(', 'c0', 'f(', 'c0', 'a0', ')', 'a0'])
        self.assertFalse(btsr.is_valid())

        # Too few up nodes - not valid
        btsr.set(['s(', 'c0', 'f(', 'c0', 'a0', ')'])
        self.assertFalse(btsr.is_valid())

        # No control nodes, but more than one action - not valid
        btsr.set(['a0', 'a0'])
        self.assertFalse(btsr.is_valid())

        # Starts with an up node - not valid
        btsr.set([')', 'f(', 'c0', 'a0', ')'])
        self.assertFalse(btsr.is_valid())

        # Just a control node - not valid
        btsr.set(['s(', ')'])
        self.assertFalse(btsr.is_valid())

        # Just a control node - not valid
        btsr.set(['s(', 's('])
        self.assertFalse(btsr.is_valid())

        # Up just after control node
        btsr.set(['s(', 'f(', ')', 'a0', ')'])
        self.assertFalse(btsr.is_valid())

        # Unknown characters
        btsr.set(['s(', 'c0', 'x', 'y', 'z', ')'])
        self.assertFalse(btsr.is_valid())

    def test_subtree_is_valid(self):

        btsr = BehaviorTreeStringRepresentation([])

        self.assertTrue(btsr.is_subtree_valid(['s(', 'f(', 'a0', ')', ')', ')'], True, True))

        self.assertFalse(btsr.is_subtree_valid(['s(', 'f(', 'a0', ')', ')', ')'], True, False))

        self.assertFalse(btsr.is_subtree_valid(['f(', 's(', 'a0', ')', ')', ')'], False, True))

        self.assertFalse(btsr.is_subtree_valid(['f(', 'f(', 'a0', ')', ')', ')'], True, True))

        self.assertFalse(btsr.is_subtree_valid(['s(', 's(', 'a0', ')', ')', ')'], True, True))

        self.assertFalse(btsr.is_subtree_valid(['s(', 'f(', 'a0', ')', ')'], True, True))

        self.assertTrue(btsr.is_subtree_valid(['s(', 'f(', 'c0', ')', ')', ')'], True, True))

    def test_close(self):
        """ Tests close function """

        btsr = BehaviorTreeStringRepresentation([])

        btsr.close()
        self.assertEqual(btsr.bt, [])

        # Correct tree with just one action
        btsr.set(['a0']).close()
        self.assertEqual(btsr.bt, ['a0'])

        # Correct tree
        btsr.set(['s(', 's(', 'a0', ')', ')']).close()
        self.assertEqual(btsr.bt, ['s(', 's(', 'a0', ')', ')'])

        # Missing up at end
        btsr.set(['s(', 's(', 'a0', ')', 's(', 'a0', 's(', 'a0']).close()
        self.assertEqual(btsr.bt, ['s(', 's(', 'a0', ')', 's(', 'a0', 's(', 'a0', ')', ')', ')'])

        # Too many up at end
        btsr.set(['s(', 'a0', ')', ')', ')']).close()
        self.assertEqual(btsr.bt, ['s(', 'a0', ')'])

        # Too many up but not at the end
        btsr.set(['s(', 's(', 'a0', ')', ')', ')', 'a1', ')']).close()
        self.assertEqual(btsr.bt, ['s(', 's(', 'a0', ')', 'a1', ')'])

    def test_trim(self):
        """ Tests trim function """
        
        btsr = BehaviorTreeStringRepresentation([])

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', 's(', 'a0', ')', ')'])
        btsr.trim()
        self.assertEqual(btsr.bt, ['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', 'a0', ')'])

        btsr.set(['s(', 'a0', 'f(', ')', 'a0', 's(', 'a0', ')', ')'])
        btsr.trim()
        self.assertEqual(btsr.bt, ['s(', 'a0', 'a0', 'a0', ')'])

        btsr.set(['s(', 'a0', 'f(', 'a1', 's(', 'a2', ')', 'a3', ')', 'a4', ')'])
        btsr.trim()
        self.assertEqual(btsr.bt, ['s(', 'a0', 'f(', 'a1', 'a2', 'a3', ')', 'a4', ')'])

        btsr.set(['s(', 'a0', 'f(', 's(', 'a2', 'a3', ')', ')', 'a4', ')'])
        btsr.trim()
        self.assertEqual(btsr.bt, ['s(', 'a0', 'a2', 'a3', 'a4', ')'])

        btsr.set(['s(', 'a0', ')'])
        btsr.trim()
        self.assertEqual(btsr.bt, ['s(', 'a0', ')'])

    def test_depth(self):
        """ Tests bt_depth function """
        
        btsr = BehaviorTreeStringRepresentation([])

        # Normal correct tree
        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        self.assertEqual(btsr.depth(), 2)

        # Goes to 0 before last node - invalid
        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')', 's(', 'a0', ')'])
        self.assertEqual(btsr.depth(),  -1)

        # Goes to 0 before last node  - invalid
        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', ')', 'a0', ')'])
        self.assertEqual(btsr.depth(), -1)

        # Goes to 0 before last node - invalid
        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0'])
        self.assertEqual(btsr.depth(),  -1)

        # Just an action node - no depth
        btsr.set(['a0'])
        self.assertEqual(btsr.depth(),  0)

    def test_length(self):
        """ Tests bt_length function """
        
        btsr = BehaviorTreeStringRepresentation([])

        btsr.set(['s(', 'a0', 'a1', ')'])
        self.assertEqual(btsr.length(),  3)

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        self.assertEqual(btsr.length(), 6)

        btsr.set(['s(', ')'])
        self.assertEqual(btsr.length(), 1)

        btsr.set(['a0'])
        self.assertEqual(btsr.length(), 1)

    def test_change_node(self):
        """ Tests change_node function """
        
        btsr = BehaviorTreeStringRepresentation([])
        random.seed(1337)

        # No new node given, change to random node
        btsr.set(['s(', 'a0', 'a0', ')']).change_node(2)
        self.assertNotEqual(btsr.bt[2], 'a0')

        # Change control node to action node
        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).change_node(2, 'a0')
        self.assertEqual(btsr.bt, ['s(', 'a0', 'a0', 'a0', ')'])

        # Change control node to action node - correct up must be removed too
        btsr.set(['s(', 'a0', 'f(', 's(', 'a0', ')', 'a0', ')', 'a0', ')']).change_node(2, 'a0')
        self.assertEqual(btsr.bt, ['s(', 'a0', 'a0', 'a0', ')'])

        btsr.set(['s(', 'a0', 'f(', 's(', 'a0', ')', 'a1', ')', 'a0', ')']).change_node(3, 'a0')
        self.assertEqual(btsr.bt, ['s(', 'a0', 'f(', 'a0', 'a1', ')', 'a0', ')'])

        # Change action node to control node
        btsr.set(['s(', 'a0', 'a0', ')']).change_node(1, 'f(')
        self.assertEqual(btsr.bt, ['s(', 'f(', 'a0', 'a0', ')', 'a0', ')'])

        # Change action node to action node
        btsr.set(['s(', 'a0', 'a0', ')']).change_node(1, 'a1')
        self.assertEqual(btsr.bt, ['s(', 'a1', 'a0', ')'])

        # Change control node to control node
        btsr.set(['s(', 'a0', 'a0', ')']).change_node(0, 'f(')
        self.assertEqual(btsr.bt, ['f(', 'a0', 'a0', ')'])

        # Change up node, not possible
        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).change_node(5, 'a0')
        self.assertEqual(btsr.bt, ['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])

    def test_add_node(self):
        """ Tests add_node function """
        
        btsr = BehaviorTreeStringRepresentation([])
        random.seed(1337)

        btsr.set(['a0']).add_node(0, 's(')
        self.assertEqual(btsr.bt, ['s(', 'a0', ')'])

        btsr.set(['s(', 'a0', 'a0', ')']).add_node(2)
        self.assertEqual(btsr.bt, ['s(', 'a0', 'a3', 'a0', ')'])

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(2, 'a0')
        self.assertEqual(btsr.bt, ['s(', 'a0', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(3, 'a0')
        self.assertEqual(btsr.bt, ['s(', 'a0', 'f(', 'a0', 'a0', 'a0', ')', 'a0', ')'])

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(0, 'f(')
        self.assertEqual(btsr.bt, ['f(', 's(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')', ')'])

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(4, 's(')
        self.assertTrue(btsr.is_valid())

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(2, 'f(')
        self.assertTrue(btsr.is_valid())

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(1, 'f(')
        self.assertTrue(btsr.is_valid())

        btsr.set(['s(', 'a0', 'f(', 'c1', 'a0', ')', ')']).add_node(2, 'f(')
        self.assertTrue(btsr.is_valid())

    def test_delete_node(self):
        """ Tests delete_node function """
        
        btsr = BehaviorTreeStringRepresentation([])

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).delete_node(0)
        self.assertEqual(btsr.bt, [])

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', ')', ')']).delete_node(0)
        self.assertEqual(btsr.bt, [])

        btsr.set(['s(', 'a0', 'f(', 'a0', 's(', 'a0', ')', ')', 's(', 'a0', ')', ')']).delete_node(0)
        self.assertEqual(btsr.bt, [])

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).delete_node(1)
        self.assertEqual(btsr.bt, ['s(', 'f(', 'a0', 'a0', ')', 'a0', ')'])

        btsr.set(['s(', 'a0', 'f(', 'a1', 'a2', ')', 'a3', ')']).delete_node(2)
        self.assertEqual(btsr.bt, ['s(', 'a0', 'a3', ')'])

        btsr.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')']).delete_node(3)
        self.assertEqual(btsr.bt, ['s(', 'a0', 'f(', ')', 'a0', ')'])

        btsr.set(['s(', 'a0', ')']).delete_node(2)
        self.assertEqual(btsr.bt, ['s(', 'a0', ')'])

    def test_find_parent(self):
        """ Tests find_parent function """
        
        btsr = BehaviorTreeStringRepresentation([])
        btsr.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')'])

        self.assertEqual(btsr.find_parent(0), None)
        self.assertEqual(btsr.find_parent(1), 0)
        self.assertEqual(btsr.find_parent(2), 0)
        self.assertEqual(btsr.find_parent(3), 2)
        self.assertEqual(btsr.find_parent(4), 2)
        self.assertEqual(btsr.find_parent(5), 0)

    def test_find_children(self):
        """ Tests find_children function """
        
        btsr = BehaviorTreeStringRepresentation([])
        btsr.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')'])

        self.assertEqual(btsr.find_children(0), [1, 2, 5])
        self.assertEqual(btsr.find_children(1), [])
        self.assertEqual(btsr.find_children(2), [3])
        self.assertEqual(btsr.find_children(3), [])
        self.assertEqual(btsr.find_children(4), [])
        self.assertEqual(btsr.find_children(5), [])

    def test_find_up_node(self):
        """ Tests find_up_node function """
        
        btsr = BehaviorTreeStringRepresentation([])

        btsr.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')'])
        self.assertEqual(btsr.find_up_node(0), 6)

        btsr.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')'])
        self.assertEqual(btsr.find_up_node(2), 4)

        btsr.set(['s(', 'a0', 'f(', 's(', 'a0', ')', 'a0', ')'])
        self.assertEqual(btsr.find_up_node(2), 7)

        btsr.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')'])
        with self.assertRaises(Exception):
            _ = btsr.find_up_node(1)

        btsr.set(['s(', 'a0', 'f(', 'a0', ')', 'a0'])
        with self.assertRaises(Exception):
            _ = btsr.find_up_node(0)

        btsr.set(['s(', 's(', 'a0', 'f(', 'a0', ')', 'a0'])
        with self.assertRaises(Exception):
            _ = btsr.find_up_node(1)

    def test_get_subtree(self):
        """ Tests get_subtree function """

        btsr = BehaviorTreeStringRepresentation(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])

        subtree = btsr.get_subtree(1)
        self.assertEqual(subtree, ['a0'])

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', 'a0', ')', ')'])
        subtree = btsr.get_subtree(6)
        self.assertEqual(subtree, ['s(', 'a0', 'a0', ')'])

        btsr.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', ')'])
        subtree = btsr.get_subtree(2)
        self.assertEqual(subtree, ['f(', 'a0', 'a0', ')'])

        subtree = btsr.get_subtree(5)
        self.assertEqual(subtree, [])

    def test_insert_subtree(self):

        btsr = BehaviorTreeStringRepresentation(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        
        btsr.insert_subtree(['f(', 'a1', ')'], 1)
        self.assertEqual(btsr.bt, ['s(', 'f(', 'a1', ')', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])

        btsr.insert_subtree(['f(', 'a1', ')'], 6)
        self.assertEqual(btsr.bt, ['s(', 'f(', 'a1', ')', 'a0', 'f(', 'f(', 'a1', ')', 'a0', 'a0', ')', 'a0', ')'])

    def test_swap_subtrees(self):

        btsr_1 = BehaviorTreeStringRepresentation(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        btsr_2 = BehaviorTreeStringRepresentation(['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', 'a0', ')', ')'])
        btsr_1.swap_subtrees(btsr_2, 6, 6)

        self.assertEqual(btsr_1.bt, ['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', 'a0', ')', ')'])
        self.assertEqual(btsr_2.bt, ['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])

        # Invalid subtree because it's an up node, no swap
        btsr_1.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        btsr_2.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', 'a0', ')', ')'])
        btsr_1.swap_subtrees(btsr_2, 5, 6)
        
        self.assertEqual(btsr_1.bt, ['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        self.assertEqual(btsr_2.bt, ['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', 'a0', ')', ')'])

    def test_is_subtree(self):

        btsr = BehaviorTreeStringRepresentation(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])

        self.assertTrue(btsr.is_subtree(0))
        self.assertTrue(btsr.is_subtree(1))
        self.assertFalse(btsr.is_subtree(5))


if __name__ == '__main__':
    unittest.main()
