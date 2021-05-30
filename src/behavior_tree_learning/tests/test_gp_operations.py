#!/usr/bin/env python

import unittest

import os
import random
from behavior_tree_learning.core.str_bt import behavior_tree
from behavior_tree_learning.core.gp_operations import operations as gp
from behavior_tree_learning.core.tests.fwk.paths import TEST_DIRECTORY


class TestGpOperations(unittest.TestCase):

    BT_SETTINGS = os.path.join(TEST_DIRECTORY, 'BT_TEST_SETTINGS.yaml')

    def test_mutate_gene(self):
        """ Tests mutate_gene function """

        behavior_tree.load_settings_from_file(self.BT_SETTINGS)
        
        genome = ['s(', 'a0', ')']

        with self.assertRaises(Exception):
            gp.mutate_gene(genome, p_add=-1, p_delete=1)
        
        with self.assertRaises(Exception):
            gp.mutate_gene(genome, p_add=1, p_delete=1)

        for _ in range(10):
            #Loop many times to catch random errors
            mutated_genome = gp.mutate_gene(genome, p_add=1, p_delete=0)
            assert len(mutated_genome) >= len(genome)

            mutated_genome = gp.mutate_gene(genome, p_add=0, p_delete=1)
            assert len(mutated_genome) <= len(genome)

            mutated_genome = gp.mutate_gene(genome, p_add=0, p_delete=0)
            bt = behavior_tree.BehaviorTreeStringRepresentation(mutated_genome)
            assert mutated_genome != genome
            assert bt.is_valid()

            mutated_genome = gp.mutate_gene(genome, p_add=0.3, p_delete=0.3)
            bt.set(mutated_genome)
            assert mutated_genome != genome
            assert bt.is_valid()

    def test_crossover_genome(self):
        """ Tests crossover_genome function """

        behavior_tree.load_settings_from_file(self.BT_SETTINGS)

        genome1 = ['s(', 'c0', 'f(', 'c0', 'a0', ')', 'a0', ')']
        genome2 = ['f(', 'c1', 's(', 'c1', 'a1', ')', 'a1', ')']

        offspring1, offspring2 = gp.crossover_genome(genome1, genome2)

        assert offspring1 != []
        assert offspring2 != []
        assert offspring1 != genome1
        assert offspring1 != genome2
        assert offspring2 != genome1
        assert offspring2 != genome2

        bt1 = behavior_tree.BehaviorTreeStringRepresentation(offspring1)
        assert bt1.is_valid()
        bt1 = bt1.set(offspring2)
        assert bt1.is_valid()

        genome1 = ['a0']
        genome2 = ['a1']
        offspring1, offspring2 = gp.crossover_genome(genome1, genome2)
        assert offspring1 == genome2
        assert offspring2 == genome1

        genome1 = []
        offspring1, offspring2 = gp.crossover_genome(genome1, genome2)
        assert offspring1 == []
        assert offspring2 == []

        for i in range(10):
            random.seed(i)
            offspring1, offspring2 = gp.crossover_genome(gp.random_genome(10), 
                                                         gp.random_genome(10))
            bt1 = bt1.set(offspring1)
            assert bt1.is_valid()
            bt1 = bt1.set(offspring2)
            assert bt1.is_valid()

        genome1 = ['s(', 'f(', 'c0', 'a0', ')', 'a0', ')']
        genome2 = ['f(', 's(', 'c1', 'a1', ')', 'a1', ')']
        offspring1, offspring2 = gp.crossover_genome(genome1, genome2, replace=False)
        assert offspring1 != genome1
        assert offspring2 != genome2
        for gene in genome1:
            assert gene in offspring1
        for gene in genome2:
            assert gene in offspring2


if __name__ == '__main__':
    unittest.main()
