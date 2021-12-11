#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

from behavior_tree_learning.sbt import BehaviorNodeFactory
from behavior_tree_learning.learning import BehaviorTreeLearner, GeneticParameters, GeneticSelectionMethods

from duplo.execution_nodes import get_behaviors
from duplo.world import Pos as WorldPos
from duplo.world import WorldSimulator
from duplo.environment import Environment


def run():

    node_factory = BehaviorNodeFactory(get_behaviors('tower'))
    start_position = [WorldPos(-0.05, -0.1, 0), WorldPos(0.0, -0.1, 0), WorldPos(0.05, -0.1, 0)]
    target_position = [WorldPos(0.0, 0.05, 0), WorldPos(0.0, 0.05, 0.0192), WorldPos(0.0, 0.05, 2*0.0192)]

    world = WorldSimulator(start_position)
    environment = Environment(node_factory, world, target_position)

    parameters = GeneticParameters()
    parameters.n_population = 16
    parameters.n_generations = 200
    parameters.ind_start_length = 8
    parameters.f_crossover = 0.5
    parameters.n_offspring_crossover = 2
    parameters.replace_crossover = False
    parameters.f_mutation = 0.5
    parameters.n_offspring_mutation = 2
    parameters.parent_selection = GeneticSelectionMethods.RANK
    parameters.survivor_selection = GeneticSelectionMethods.RANK
    parameters.f_elites = 0.1
    parameters.f_parents = parameters.f_elites
    parameters.mutate_co_offspring = False
    parameters.mutate_co_parents = True
    parameters.mutation_p_add = 0.4
    parameters.mutation_p_delete = 0.3
    parameters.allow_identical = False
    parameters.plot = True
    parameters.fig_last_gen = False

    bt_learner = BehaviorTreeLearner(environment)
    success = bt_learner.run(parameters, verbose=True)
    print("Succeed: ", success)


if __name__ == "__main__":
    run()
