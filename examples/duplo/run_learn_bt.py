#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

import os
import logging

from behavior_tree_learning.sbt import BehaviorNodeFactory
from behavior_tree_learning.learning import BehaviorTreeLearner, GeneticParameters, GeneticSelectionMethods

from duplo.execution_nodes import get_behaviors
from duplo.world import Pos as WorldPos
from duplo.world import WorldSimulator, WorldFactory
from duplo.environment import Environment


def _configure_logger(level, log_name):

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    file_path = os.path.join('logs', log_name + '.log')
    logging.basicConfig(filename=file_path,
                        format='%(filename)s: %(message)s')
    logging.getLogger("gp").setLevel(level)


def run():

    scenario = 'tower'

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

    # add specific class for plot_parametes
    parameters.plot_fitness = True
    parameters.plot_best_individual = True
    parameters.plot_last_generation = True

    num_trials = 10
    for tdx in range(1, num_trials+1):

        log_name = scenario + '_' + str(tdx)
        _configure_logger(logging.DEBUG, log_name)

        parameters.log_name = log_name
        seed = tdx

        node_factory = BehaviorNodeFactory(get_behaviors(scenario))
        start_position = [WorldPos(-0.05, -0.1, 0), WorldPos(0.0, -0.1, 0), WorldPos(0.05, -0.1, 0)]
        target_position = [WorldPos(0.0, 0.05, 0), WorldPos(0.0, 0.05, 0.0192), WorldPos(0.0, 0.05, 2 * 0.0192)]

        world_factory = WorldFactory(start_position)
        environment = Environment(node_factory, world_factory, target_position, verbose=False)

        bt_learner = BehaviorTreeLearner(environment)
        success = bt_learner.run(parameters, seed, verbose=False)

        print("Trial: %d, Succeed: %s" % (tdx, success))


if __name__ == "__main__":
    run()
