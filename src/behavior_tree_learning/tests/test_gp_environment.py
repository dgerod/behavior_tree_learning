#!/usr/bin/env python

import unittest

import os
from behavior_tree_learning.core.sbt import behavior_tree
from behavior_tree_learning.tests.fwk.paths import TEST_DIRECTORY
from behavior_tree_learning.tests.fwk import environment_states


behavior_tree.load_settings_from_file(os.path.join(TEST_DIRECTORY, 'BT_TEST_SETTINGS.yaml'))


class TestStateEnvironment(unittest.TestCase):
    
    def test_states(self):
        """
        Tests a state machine environment
        """

        assert environment_states.get_fitness(['t1']) == 9
        assert environment_states.get_fitness(['s(', 't1', 't2', 't3', 't4', ')']) == 35
        assert environment_states.get_fitness(['s(', 't1', 't2', 't3', 'r1', 'r2', 'r3', 'r4', ')']) == 22


if __name__ == '__main__':
    unittest.main()
