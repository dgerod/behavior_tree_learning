#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

from behavior_tree_learning.sbt import BehaviorNodeFactory, BehaviorRegister
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
    environment = Environment(node_factory, world, target_position, verbose=True)

    gp_parameters = GeneticParameters()
    gp_parameters.n_population = 16
    gp_parameters.n_generations = 200
    gp_parameters.ind_start_length = 8
    gp_parameters.f_crossover = 0.5
    gp_parameters.n_offspring_crossover = 2
    gp_parameters.replace_crossover = False
    gp_parameters.f_mutation = 0.5
    gp_parameters.n_offspring_mutation = 2
    gp_parameters.parent_selection = GeneticSelectionMethods.RANK
    gp_parameters.survivor_selection = GeneticSelectionMethods.RANK
    gp_parameters.f_elites = 0.1
    gp_parameters.f_parents = gp_parameters.f_elites
    gp_parameters.mutate_co_offspring = False
    gp_parameters.mutate_co_parents = True
    gp_parameters.mutation_p_add = 0.4
    gp_parameters.mutation_p_delete = 0.3
    gp_parameters.allow_identical = False
    gp_parameters.plot = True
    #gp_parameters.verbose = False
    gp_parameters.fig_last_gen = False

    bt_learner = BehaviorTreeLearner(environment)
    success = bt_learner.run(gp_parameters, verbose=True)
    print("Succeed: ", success)


if __name__ == "__main__":
    run()
