#!/usr/bin/env python

import paths

paths.add_modules_to_path()

import unittest

from behavior_tree_learning.core.sbt import BehaviorTreeStringRepresentation
from behavior_tree_learning.core.sbt import BehaviorNodeFactory
from tests.fwk.behavior_nodes import get_behaviors


class TestBehaviorNodeFactory(unittest.TestCase):

    def setUp(self) -> None:

        from behavior_tree_learning.core.sbt.behavior_tree import _clean_settings
        _clean_settings()

    def test_btsr_does_not_work_without_factory(self):

        btsr = BehaviorTreeStringRepresentation(['s(', 'c0', 'f(', 'c0', 'a0', ')', 'a0', ')'])
        self.assertFalse(btsr.is_valid())

    def test_btsr_work_after_initialize_factory(self):

        node_factory = BehaviorNodeFactory(get_behaviors())
        btsr = BehaviorTreeStringRepresentation(['s(', 'c0', 'f(', 'c0', 'a0', ')', 'a0', ')'])
        self.assertTrue(btsr.is_valid())


if __name__ == '__main__':
    unittest.main()
