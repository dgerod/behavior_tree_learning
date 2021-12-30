#!/usr/bin/env python

import paths
paths.add_modules_to_path()

import unittest

import os
import random
from behavior_tree_learning.core.sbt import behavior_tree
from behavior_tree_learning.core.sbt import BehaviorTreeStringRepresentation, StringBehaviorTree
from behavior_tree_learning.core.sbt import BehaviorNodeFactory


behavior_tree.load_settings_from_file(os.path.join(paths.get_test_directory(), 'BT_TEST_SETTINGS.yaml'))


class TestBehaviorTree(unittest.TestCase):

    def test_init(self):
        """ Tests init function """

        _ = BehaviorTreeStringRepresentation([])

    def test_random(self):
        """ Tests random function """
    
        bt = BehaviorTreeStringRepresentation([])

        random.seed(1337)

        for length in range(1, 11):
            bt.random(length)
            assert bt.length() == length
            assert bt.is_valid()

    def test_is_valid(self):
        """ Tests is_valid function """
    
        bt = BehaviorTreeStringRepresentation([])
        assert not bt.is_valid()

        #Valid tree
        bt.set(['s(', 'c0', 'f(', 'c0', 'a0', ')', 'a0', ')'])
        assert bt.is_valid()

        #Minimal valid tree - just an action node
        bt.set(['a0'])
        assert bt.is_valid()

        #Two control nodes at root level - not valid
        bt.set(['s(', 'c0', 'f(', 'c0', 'a0', ')', 'a0', ')', 's(', 'a0', ')'])
        assert not bt.is_valid()

        #Action node at root level - not valid
        bt.set(['s(', 'c0', 'f(', 'c0', 'a0', ')', ')', 'a0', ')'])
        assert not bt.is_valid()

        #Too few up nodes - not valid
        bt.set(['s(', 'c0', 'f(', 'c0', 'a0', ')', 'a0'])
        assert not bt.is_valid()

        #Too few up nodes - not valid
        bt.set(['s(', 'c0', 'f(', 'c0', 'a0', ')'])
        assert not bt.is_valid()

        #No control nodes, but more than one action - not valid
        bt.set(['a0', 'a0'])
        assert not bt.is_valid()

        #Starts with an up node - not valid
        bt.set([')', 'f(', 'c0', 'a0', ')'])
        assert not bt.is_valid()

        #Just a control node - not valid
        bt.set(['s(', ')'])
        assert not bt.is_valid()

        #Just a control node - not valid
        bt.set(['s(', 's('])
        assert not bt.is_valid()

        #Up just after control node
        bt.set(['s(', 'f(', ')', 'a0', ')'])
        assert not bt.is_valid()

        #Unknown characters
        bt.set(['s(', 'c0', 'x', 'y', 'z', ')'])
        assert not bt.is_valid()

    def test_subtree_is_valid(self):
        """ Tests subtree_is_valid function """
        
        bt = BehaviorTreeStringRepresentation([])

        assert bt.is_subtree_valid(['s(', 'f(', 'a0', ')', ')', ')'], True, True)

        assert not bt.is_subtree_valid(['s(', 'f(', 'a0', ')', ')', ')'], True, False)

        assert not bt.is_subtree_valid(['f(', 's(', 'a0', ')', ')', ')'], False, True)

        assert not bt.is_subtree_valid(['f(', 'f(', 'a0', ')', ')', ')'], True, True)

        assert not bt.is_subtree_valid(['s(', 's(', 'a0', ')', ')', ')'], True, True)

        assert not bt.is_subtree_valid(['s(', 'f(', 'a0', ')', ')'], True, True)

        assert bt.is_subtree_valid(['s(', 'f(', 'c0', ')', ')', ')'], True, True)

    def test_close(self):
        """ Tests close function """

        bt = BehaviorTreeStringRepresentation([])

        bt.close()
        assert bt.bt == []

        #Correct tree with just one action
        bt.set(['a0']).close()
        assert bt.bt == ['a0']

        #Correct tree
        bt.set(['s(', 's(', 'a0', ')', ')']).close()
        assert bt.bt == ['s(', 's(', 'a0', ')', ')']

        #Missing up at end
        bt.set(['s(', 's(', 'a0', ')', 's(', 'a0', 's(', 'a0']).close()
        assert bt.bt == ['s(', 's(', 'a0', ')', 's(', 'a0', 's(', 'a0', ')', ')', ')']

        #Too many up at end
        bt.set(['s(', 'a0', ')', ')', ')']).close()
        assert bt.bt == ['s(', 'a0', ')']

        #Too many up but not at the end
        bt.set(['s(', 's(', 'a0', ')', ')', ')', 'a1', ')']).close()
        assert bt.bt == ['s(', 's(', 'a0', ')', 'a1', ')']

    def test_trim(self):
        """ Tests trim function """
        
        bt = BehaviorTreeStringRepresentation([])

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', 's(', 'a0', ')', ')'])
        bt.trim()
        assert bt.bt == ['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', 'a0', ')']

        bt.set(['s(', 'a0', 'f(', ')', 'a0', 's(', 'a0', ')', ')'])
        bt.trim()
        assert bt.bt == ['s(', 'a0', 'a0', 'a0', ')']

        bt.set(['s(', 'a0', 'f(', 'a1', 's(', 'a2', ')', 'a3', ')', 'a4', ')'])
        bt.trim()
        assert bt.bt == ['s(', 'a0', 'f(', 'a1', 'a2', 'a3', ')', 'a4', ')']

        bt.set(['s(', 'a0', 'f(', 's(', 'a2', 'a3', ')', ')', 'a4', ')'])
        bt.trim()
        assert bt.bt == ['s(', 'a0', 'a2', 'a3', 'a4', ')']

        bt.set(['s(', 'a0', ')'])
        bt.trim()
        assert bt.bt == ['s(', 'a0', ')']

    def test_depth(self):
        """ Tests bt_depth function """
        
        bt = BehaviorTreeStringRepresentation([])

        #Normal correct tree
        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        assert bt.depth() == 2

        #Goes to 0 before last node - invalid
        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')', 's(', 'a0', ')'])
        assert bt.depth() == -1

        #Goes to 0 before last node  - invalid
        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', ')', 'a0', ')'])
        assert bt.depth() == -1

        #Goes to 0 before last node - invalid
        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0'])
        assert bt.depth() == -1

        #Just an action node - no depth
        bt.set(['a0'])
        assert bt.depth() == 0

    def test_length(self):
        """ Tests bt_length function """
        
        bt = BehaviorTreeStringRepresentation([])

        bt.set(['s(', 'a0', 'a1', ')'])
        assert bt.length() == 3

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        assert bt.length() == 6

        bt.set(['s(', ')'])
        assert bt.length() == 1

        bt.set(['a0'])
        assert bt.length() == 1

    def test_change_node(self):
        """ Tests change_node function """
        
        bt = BehaviorTreeStringRepresentation([])

        random.seed(1337)

        #No new node given, change to random node
        bt.set(['s(', 'a0', 'a0', ')']).change_node(2)
        assert bt.bt[2] != 'a0'

        #Change control node to action node
        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).change_node(2, 'a0')
        assert bt.bt == ['s(', 'a0', 'a0', 'a0', ')']

        #Change control node to action node - correct up must be removed too
        bt.set(['s(', 'a0', 'f(', 's(', 'a0', ')', 'a0', ')', 'a0', ')']).change_node(2, 'a0')
        assert bt.bt == ['s(', 'a0', 'a0', 'a0', ')']

        bt.set(['s(', 'a0', 'f(', 's(', 'a0', ')', 'a1', ')', 'a0', ')']).change_node(3, 'a0')
        assert bt.bt == ['s(', 'a0', 'f(', 'a0', 'a1', ')', 'a0', ')']

        #Change action node to control node
        bt.set(['s(', 'a0', 'a0', ')']).change_node(1, 'f(')
        assert bt.bt == ['s(', 'f(', 'a0', 'a0', ')', 'a0', ')']

        #Change action node to action node
        bt.set(['s(', 'a0', 'a0', ')']).change_node(1, 'a1')
        assert bt.bt == ['s(', 'a1', 'a0', ')']

        #Change control node to control node
        bt.set(['s(', 'a0', 'a0', ')']).change_node(0, 'f(')
        assert bt.bt == ['f(', 'a0', 'a0', ')']

        #Change up node, not possible
        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).change_node(5, 'a0')
        assert bt.bt == ['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']

    def test_add_node(self):
        """ Tests add_node function """
        
        bt = BehaviorTreeStringRepresentation([])

        random.seed(1337)

        bt.set(['a0']).add_node(0, 's(')
        assert bt.bt == ['s(', 'a0', ')']

        bt.set(['s(', 'a0', 'a0', ')']).add_node(2)
        assert bt.bt == ['s(', 'a0', 'a3', 'a0', ')']

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(2, 'a0')
        assert bt.bt == ['s(', 'a0', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(3, 'a0')
        assert bt.bt == ['s(', 'a0', 'f(', 'a0', 'a0', 'a0', ')', 'a0', ')']

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(0, 'f(')
        assert bt.bt == ['f(', 's(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')', ')']

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(4, 's(')
        assert bt.is_valid()

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(2, 'f(')
        assert bt.is_valid()

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).add_node(1, 'f(')
        assert bt.is_valid()

        bt.set(['s(', 'a0', 'f(', 'c1', 'a0', ')', ')']).add_node(2, 'f(')
        assert bt.is_valid()

    def plot_individual(self, individual, plot_name):
        """ Saves a graphical representation of the individual """
                
        behavior_factory = BehaviorNodeFactory(make_execution_node)
        pytree = StringBehaviorTree(individual[:], behaviors=behavior_factory)
        pytree.save_fig('logs/', name=plot_name)

    def test_delete_node(self):
        """ Tests delete_node function """
        
        bt = BehaviorTreeStringRepresentation([])

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).delete_node(0)
        assert bt.bt == []

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', ')', ')']).delete_node(0)
        assert bt.bt == []

        bt.set(['s(', 'a0', 'f(', 'a0', 's(', 'a0', ')', ')', 's(', 'a0', ')', ')']).delete_node(0)
        assert bt.bt == []

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']).delete_node(1)
        assert bt.bt == ['s(', 'f(', 'a0', 'a0', ')', 'a0', ')']

        bt.set(['s(', 'a0', 'f(', 'a1', 'a2', ')', 'a3', ')']).delete_node(2)
        assert bt.bt == ['s(', 'a0', 'a3', ')']

        bt.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')']).delete_node(3)
        assert bt.bt == ['s(', 'a0', 'f(', ')', 'a0', ')']

        bt.set(['s(', 'a0', ')']).delete_node(2)
        assert bt.bt == ['s(', 'a0', ')']

    def test_find_parent(self):
        """ Tests find_parent function """
        
        bt = BehaviorTreeStringRepresentation([])

        bt.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')'])
        assert bt.find_parent(0) is None
        assert bt.find_parent(1) == 0
        assert bt.find_parent(2) == 0
        assert bt.find_parent(3) == 2
        assert bt.find_parent(4) == 2
        assert bt.find_parent(5) == 0

    def test_find_children(self):
        """ Tests find_children function """
        
        bt = BehaviorTreeStringRepresentation([])

        bt.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')'])
        assert bt.find_children(0) == [1, 2, 5]
        assert bt.find_children(1) == []
        assert bt.find_children(2) == [3]
        assert bt.find_children(3) == []
        assert bt.find_children(4) == []
        assert bt.find_children(5) == []

    def test_find_up_node(self):
        """ Tests find_up_node function """
        
        bt = BehaviorTreeStringRepresentation([])

        bt.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')'])
        assert bt.find_up_node(0) == 6

        bt.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')'])
        assert bt.find_up_node(2) == 4

        bt.set(['s(', 'a0', 'f(', 's(', 'a0', ')', 'a0', ')'])
        assert bt.find_up_node(2) == 7

        bt.set(['s(', 'a0', 'f(', 'a0', ')', 'a0', ')'])
        with self.assertRaises(Exception):
            _ = bt.find_up_node(1)

        bt.set(['s(', 'a0', 'f(', 'a0', ')', 'a0'])
        with self.assertRaises(Exception):
            _ = bt.find_up_node(0)

        bt.set(['s(', 's(', 'a0', 'f(', 'a0', ')', 'a0'])
        with self.assertRaises(Exception):
            _ = bt.find_up_node(1)

    def test_get_subtree(self):
        """ Tests get_subtree function """

        bt = BehaviorTreeStringRepresentation(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        subtree = bt.get_subtree(1)
        assert subtree == ['a0']

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', 'a0', ')', ')'])
        subtree = bt.get_subtree(6)
        assert subtree == ['s(', 'a0', 'a0', ')']

        bt.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', ')'])
        subtree = bt.get_subtree(2)
        assert subtree == ['f(', 'a0', 'a0', ')']

        subtree = bt.get_subtree(5)
        assert subtree == []

    def test_insert_subtree(self):
        """ Tests insert_subtree function """
        
        bt1 = BehaviorTreeStringRepresentation(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        
        bt1.insert_subtree(['f(', 'a1', ')'], 1)
        assert bt1.bt == ['s(', 'f(', 'a1', ')', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']

        bt1.insert_subtree(['f(', 'a1', ')'], 6)
        assert bt1.bt == ['s(', 'f(', 'a1', ')', 'a0', 'f(', 'f(', 'a1', ')', 'a0', 'a0', ')', 'a0', ')']

    def test_swap_subtrees(self):
        """ Tests swap_subtrees function """

        bt1 = BehaviorTreeStringRepresentation(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        bt2 = BehaviorTreeStringRepresentation(['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', 'a0', ')', ')'])
        bt1.swap_subtrees(bt2, 6, 6)

        assert bt1.bt == ['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', 'a0', ')', ')']
        assert bt2.bt == ['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']

        # Invalid subtree because it's an up node, no swap
        bt1.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])
        bt2.set(['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', 'a0', ')', ')'])
        bt1.swap_subtrees(bt2, 5, 6)
        
        assert bt1.bt == ['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')']
        assert bt2.bt == ['s(', 'a0', 'f(', 'a0', 'a0', ')', 's(', 'a0', 'a0', ')', ')']

    def test_is_subtree(self):
        """ Tests is_subtree function """

        bt = BehaviorTreeStringRepresentation(['s(', 'a0', 'f(', 'a0', 'a0', ')', 'a0', ')'])

        assert bt.is_subtree(0)
        assert bt.is_subtree(1)
        assert not bt.is_subtree(5)


if __name__ == '__main__':
    unittest.main()
