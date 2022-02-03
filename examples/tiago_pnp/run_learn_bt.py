#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

import os
import logging

from behavior_tree_learning.sbt import BehaviorNodeFactory
from behavior_tree_learning.learning import BehaviorTreeLearner, GeneticParameters, GeneticSelectionMethods

from tiago_pnp.execution_nodes import get_behaviors
from tiago_pnp.world import ApplicationWorld, ApplicationWorldFactory
from tiago_pnp.environment import ApplicationEnvironment


def _configure_logger(level, log_name):

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    file_path = os.path.join('logs', log_name + '.log')
    logging.basicConfig(filename=file_path,
                        format='%(filename)s: %(message)s')
    logging.getLogger("gp").setLevel(level)


def run():

    scenario = 'scenario_1'

    parameters = GeneticParameters()
    parameters.ind_start_length = 4
    parameters.n_population = 30
    parameters.f_crossover = 0.4
    parameters.f_mutation = 0.6
    parameters.n_offspring_crossover = 2
    parameters.n_offspring_mutation = 4
    parameters.parent_selection = GeneticSelectionMethods.TOURNAMENT
    parameters.survivor_selection = GeneticSelectionMethods.TOURNAMENT
    parameters.f_elites = 0.1
    parameters.f_parents = 1
    parameters.mutation_p_add = 0.5
    parameters.mutation_p_delete = 0.2
    parameters.rerun_fitness = 0
    parameters.allow_identical = False
    parameters.n_generations = 8000

    # add specific class for plot_parameters
    parameters.plot_fitness = True
    parameters.plot_best_individual = True
    parameters.plot_last_generation = True

    num_trials = 10
    for tdx in range(1, num_trials+1):

        log_name = scenario + '_' + str(tdx)
        _configure_logger(logging.DEBUG, log_name)

        parameters.log_name = log_name
        seed = tdx*100

        node_factory = BehaviorNodeFactory(get_behaviors(scenario))
        world_factory = ApplicationWorldFactory(scenario, deterministic=True)
        environment = ApplicationEnvironment(node_factory, world_factory, scenario, verbose=False)

        bt_learner = BehaviorTreeLearner.from_environment(environment)
        success = bt_learner.run(parameters, seed, verbose=False)

        print("Trial: %d, Succeed: %s" % (tdx, success))


if __name__ == "__main__":
    run()
