#!/usr/bin/env python

import paths
paths.add_modules_to_path()

import unittest
from interface import implements
from behavior_tree_learning.core.gp.hash_table import HashTable
from behavior_tree_learning.core.gp.parameters import GeneticParameters
from behavior_tree_learning.core.gp.operators import GeneticOperators
from behavior_tree_learning.core.gp.environment import GeneticEnvironment
from behavior_tree_learning.core.gp.algorithm import GeneticProgramming


class FakeOperators(implements(GeneticOperators)):

    def random_genome(self, length):
        pass

    def mutate_gene(self, genome, p_add, p_delete):
        pass

    def crossover_genome(self, genome1, genome2, replace):
        pass


class FakEnvironment(implements(GeneticEnvironment)):

        def run_and_compute(self, individual, verbose):
            pass

        def plot_individual(self, path, plot_name, individual):
            pass


class TestGpAlgorithm(unittest.TestCase):

    def test_create_population(self):

        operators = FakeOperators()
        parameters = GeneticParameters()
        environment = FakEnvironment()

        gp_algorithm = GeneticProgramming(operators)
        gp_algorithm.run(environment, parameters)


if __name__ == '__main__':
    unittest.main()
