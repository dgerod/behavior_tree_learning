#!/usr/bin/env python

import paths
paths.add_modules_to_path()

import unittest

from behavior_tree_learning.core.sbt import StringBehaviorTree
from behavior_tree_learning.core.sbt import BehaviorNodeFactory
from behavior_tree_learning.core.plotter import print_ascii_tree
from tests.fwk.behavior_nodes import get_behaviors


class TestStringBehaviorTree(unittest.TestCase):

    def setUp(self) -> None:

        self._node_factory = BehaviorNodeFactory(get_behaviors())

    def test_bt_from_str(self):

        sbt = ['f(', 'c0', 'c0', ')']
        bt = StringBehaviorTree(sbt, behaviors=self._node_factory)
        self.assertEqual(sbt, [])
        self.assertEqual(len(bt.root.children), 2)
        print_ascii_tree(bt)

        sbt = ['f(', 'f(', 'c0', 'c0', ')', ')']
        bt = StringBehaviorTree(sbt, behaviors=self._node_factory)
        self.assertEqual(sbt, [])
        self.assertEqual(len(bt.root.children), 1)
        print_ascii_tree(bt)

        sbt = ['f(', 'f(', 'c0', 'c0', ')', 's(', 'c0', 'c0', ')', ')']
        bt = StringBehaviorTree(sbt, behaviors=self._node_factory)
        self.assertEqual(sbt, [])
        self.assertEqual(len(bt.root.children), 2)
        print_ascii_tree(bt)

        sbt = ['f(', 'f(', 'c0', 'c0', ')', 'f(', 's(', 'c0', ')', ')', ')']
        bt = StringBehaviorTree(sbt, behaviors=self._node_factory)
        self.assertEqual(sbt, [])
        self.assertEqual(len(bt.root.children), 2)
        print_ascii_tree(bt)
        
        sbt = ['f(', 'f(', 'c0', 'c0', ')']
        bt = StringBehaviorTree(sbt, behaviors=self._node_factory)
        self.assertEqual(sbt, [])
        self.assertEqual(len(bt.root.children), 1)
        print_ascii_tree(bt)

        sbt = ['f(', 'f(', 'c0', ')', ')', 'c0', ')']
        bt = StringBehaviorTree(sbt, behaviors=self._node_factory)
        self.assertEqual(sbt, ['c0', ')'])
        self.assertEqual(len(bt.root.children), 1)
        print_ascii_tree(bt)
       
        with self.assertRaises(Exception):
            StringBehaviorTree(['nonbehavior'], behaviors=self._node_factory)
        
        with self.assertRaises(Exception):
            StringBehaviorTree(['f(', 'nonpytreesbehavior', ')'], behaviors=self._node_factory)
        
    def test_str_from_bt(self):

        sbt = ['f(', 'f(', 'c0', 'c0', ')', 'f(', 's(', 'c0', ')', ')', ')']
        bt = StringBehaviorTree(sbt[:], behaviors=self._node_factory)
        self.assertEqual(bt.to_string(), sbt)

        sbt = ['f(', 'f(', 'c0', ')', 'c0', ')']
        bt = StringBehaviorTree(sbt[:], behaviors=self._node_factory)
        self.assertEqual(bt.to_string(), sbt)


if __name__ == '__main__':
    unittest.main()
