#!/usr/bin/env python

import unittest

import os
from behavior_tree_learning.core.sbt import behavior_tree
from behavior_tree_learning.core.sbt import StringBehaviorTree
from behavior_tree_learning.core.logger import print_ascii_tree
from behavior_tree_learning.tests.fwk.paths import TEST_DIRECTORY
from behavior_tree_learning.tests.fwk import behaviors_states as behaviors


class TestStringBehaviorTreeForPyTree(unittest.TestCase):

    BT_SETTINGS = os.path.join(TEST_DIRECTORY, 'BT_TEST_SETTINGS.yaml')

    def test_pytree(self):
        """ Tests the StringBehaviorTree class initialization """

        behavior_tree.load_settings_from_file(self.BT_SETTINGS)

        bt = ['f(', 'a', 'a', ')']
        py_tree = StringBehaviorTree(bt, behaviors=behaviors)
        assert bt == []
        assert len(py_tree.root.children) == 2
        print_ascii_tree(py_tree)

        bt = ['f(', 'f(', 'a', 'a', ')', ')']
        py_tree = StringBehaviorTree(bt, behaviors=behaviors)
        assert bt == []
        assert len(py_tree.root.children) == 1
        print_ascii_tree(py_tree)

        bt = ['f(', 'f(', 'a', 'a', ')', 's(', 'a', 'a', ')', ')']
        py_tree = StringBehaviorTree(bt, behaviors=behaviors)
        assert bt == []
        assert len(py_tree.root.children) == 2
        print_ascii_tree(py_tree)

        bt = ['f(', 'f(', 'a', 'a', ')', 'f(', 's(', 'a', ')', ')', ')']
        py_tree = StringBehaviorTree(bt, behaviors=behaviors)
        assert bt == []
        assert len(py_tree.root.children) == 2
        print_ascii_tree(py_tree)
        
        bt = ['f(', 'f(', 'a', 'a', ')']
        py_tree = StringBehaviorTree(bt, behaviors=behaviors)
        assert bt == []
        assert len(py_tree.root.children) == 1
        print_ascii_tree(py_tree)

        bt = ['f(', 'f(', 'a', ')', ')', 'a', ')']
        py_tree = StringBehaviorTree(bt, behaviors=behaviors)
        assert bt != []
        print_ascii_tree(py_tree)
       
        with self.assertRaises(Exception):
            StringBehaviorTree(['nonbehavior'], behaviors=behaviors)
        
        with self.assertRaises(Exception):
            StringBehaviorTree(['f(', 'nonpytreesbehavior', ')'], behaviors=behaviors)
        
    def test_get_bt_from_root(self):
        """ Specific test for get_string_from_root function """

        behavior_tree.load_settings_from_file(self.BT_SETTINGS)
        
        bt = ['f(', 'f(', 'a', 'a', ')', 'f(', 's(', 'a', ')', ')', ')']
        py_tree = StringBehaviorTree(bt[:], behaviors=behaviors)
        assert py_tree.get_bt_from_root() == bt

        bt = ['f(', 'f(', 'a', ')', 'a', ')']
        py_tree = StringBehaviorTree(bt[:], behaviors=behaviors)
        assert py_tree.get_bt_from_root() == bt


if __name__ == '__main__':
    unittest.main()
