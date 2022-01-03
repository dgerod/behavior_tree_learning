#!/usr/bin/env python

import paths
paths.add_modules_to_path()

import unittest

import random
from behavior_tree_learning.core.sbt import BehaviorNodeFactory
from behavior_tree_learning.core.gp import selection as gps
from tests.fwk.behavior_nodes import get_behaviors


class TestSelection(unittest.TestCase):

    def setUp(self) -> None:

        self._node_factory = BehaviorNodeFactory(get_behaviors())

    def test_elite_selection(self):

        population = list(range(6))
        fitness = [0, 1, 2, 1, 3, 1]

        selected = gps.selection(gps.SelectionMethods.ELITISM, population, fitness, 2)
        self.assertEqual(selected, [4, 2])

        population = list(range(8))
        fitness = [0, 6, 2, 8, 3, 2, 1, 1]

        selected = gps.selection(gps.SelectionMethods.ELITISM, population, fitness, 2)
        self.assertEqual(selected, [3, 1])

    def test_tournament_selection(self):

        population = list(range(6))
        fitness = [0, 1, 2, 1, 3, 1]

        selected = gps.selection(gps.SelectionMethods.TOURNAMENT, population, fitness, 2)
        self.assertEqual(selected, [4, 2])

        population = list(range(10))
        fitness = [2, 1, 2, 1, 3, 1, 4, 5, 0, 0]

        selected = gps.selection(gps.SelectionMethods.TOURNAMENT, population, fitness, 5)
        self.assertEqual(selected, [6, 3, 7, 4, 2])

        population = list(range(10))
        fitness = [2, 1, 2, 1, 3, 1, 4, 5, 0, 0]

        selected = gps.selection(gps.SelectionMethods.TOURNAMENT, population, fitness, 3)
        self.assertEqual(selected, [7, 2, 6])

    def test_rank_selection(self):

        population = list(range(6))
        fitness = [0, 1, 2, 1, 3, 1]

        selected = []
        for _ in range(10):
            selected += gps.selection(gps.SelectionMethods.RANK, population, fitness, 2)
        assert 4 in selected

        population = list(range(10))
        fitness = [2, 1, 1, 1, 3, 1, 4, 5, 3, 0]

        num_times_selected = 0
        num_runs = 100
        for seed in range(0, num_runs):
            selected = gps.selection(gps.SelectionMethods.RANK, population, fitness, 2)
            if 0 in selected:
                num_times_selected += 1

        # 0 is the 5th in rank so the probability of getting selected
        # should be (10 - 4) / sum(1 to 10) = 6 / 55
        # Probability of getting selected when picking 2 out of 10 is then
        # 6 / 55 + (55 - 6) / 55 * 6 / 55 = 6 / 55 * (2 - 6 / 55)
        # Check is with some margin
        assert 6/55 * (2 - 6 / 55) - 0.05 < num_times_selected / num_runs < 6/55 * (2 - 6 / 55) + 0.05

    def test_random_selection(self):

        population = list(range(6))
        fitness = [0, 1, 2, 1, 3, 1]

        random.seed(0)
        selected_1 = gps.selection(gps.SelectionMethods.RANDOM, population, fitness, 3)
        selected2 = gps.selection(gps.SelectionMethods.RANDOM, population, fitness, 3)
        self.assertNotEqual(selected_1, selected2)

    def test_all_selection(self):

        population = list(range(6))
        fitness = [0, 1, 2, 1, 3, 1]

        selected = gps.selection(gps.SelectionMethods.ALL, population, fitness, 2)
        self.assertEqual(selected, population)


if __name__ == '__main__':
    unittest.main()
