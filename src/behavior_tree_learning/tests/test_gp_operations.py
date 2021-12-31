#!/usr/bin/env python

import paths
paths.add_modules_to_path()

import unittest

import random
from behavior_tree_learning.core.sbt import BehaviorTreeStringRepresentation
from behavior_tree_learning.core.sbt import BehaviorNodeFactory
from behavior_tree_learning.core.gp_sbt import Operators
from tests.fwk.behavior_nodes import get_behaviors


class TestGpForSbtOperations(unittest.TestCase):

    def setUp(self) -> None:
        self._node_factory = BehaviorNodeFactory(get_behaviors())

    def test_mutate_gene(self):

        gp_operators = Operators()
        genome = ['s(', 'c0', ')']

        with self.assertRaises(Exception):
            gp_operators.mutate_gene(genome, p_add=-1, p_delete=1)
        
        with self.assertRaises(Exception):
            gp_operators.mutate_gene(genome, p_add=1, p_delete=1)

        for _ in range(10):
            mutated_genome = gp_operators.mutate_gene(genome, p_add=1, p_delete=0)
            self.assertGreaterEqual(len(mutated_genome), len(genome))

            mutated_genome = gp_operators.mutate_gene(genome, p_add=0, p_delete=1)
            self.assertLessEqual(len(mutated_genome), len(genome))

            mutated_genome = gp_operators.mutate_gene(genome, p_add=0, p_delete=0)
            bt = BehaviorTreeStringRepresentation(mutated_genome)
            self.assertNotEqual(mutated_genome, genome)
            self.assertTrue(bt.is_valid())

            mutated_genome = gp_operators.mutate_gene(genome, p_add=0.3, p_delete=0.3)
            bt.set(mutated_genome)
            self.assertNotEqual(mutated_genome, genome)
            self.assertTrue(bt.is_valid())

    def test_crossover_genome(self):

        gp_operators = Operators()
        genome1 = ['s(', 'c0', 'f(', 'c0', 'a0', ')', 'a0', ')']
        genome2 = ['f(', 'c1', 's(', 'c1', 'a1', ')', 'a1', ')']
        offspring1, offspring2 = gp_operators.crossover_genome(genome1, genome2, replace=True)

        assert offspring1 != []
        assert offspring2 != []
        assert offspring1 != genome1
        assert offspring1 != genome2
        assert offspring2 != genome1
        assert offspring2 != genome2

        bt1 = BehaviorTreeStringRepresentation(offspring1)
        assert bt1.is_valid()
        bt1 = bt1.set(offspring2)
        assert bt1.is_valid()

        genome1 = ['a0']
        genome2 = ['a1']
        offspring1, offspring2 = gp_operators.crossover_genome(genome1, genome2, replace=True)
        assert offspring1 == genome2
        assert offspring2 == genome1

        genome1 = []
        offspring1, offspring2 = gp_operators.crossover_genome(genome1, genome2, replace=True)
        assert offspring1 == []
        assert offspring2 == []

        for i in range(10):
            random.seed(i)
            offspring1, offspring2 = gp_operators.crossover_genome(gp_operators.random_genome(10),
                                                                   gp_operators.random_genome(10),
                                                                   replace=True)
            bt1 = bt1.set(offspring1)
            assert bt1.is_valid()
            bt1 = bt1.set(offspring2)
            assert bt1.is_valid()

        genome1 = ['s(', 'f(', 'c0', 'a0', ')', 'a0', ')']
        genome2 = ['f(', 's(', 'c1', 'a1', ')', 'a1', ')']
        offspring1, offspring2 = gp_operators.crossover_genome(genome1, genome2, replace=False)
        assert offspring1 != genome1
        assert offspring2 != genome2
        for gene in genome1:
            assert gene in offspring1
        for gene in genome2:
            assert gene in offspring2


if __name__ == '__main__':
    unittest.main()
