#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

import os
import logging

from behavior_tree_learning.sbt import BehaviorNodeFactory
from behavior_tree_learning.learning import BehaviorTreeLearner, GeneticParameters, GeneticSelectionMethods

from duplo.execution_nodes import get_behaviors
from duplo.world import Pos as WorldPos
from duplo.world import ApplicationWorldFactory
from duplo.environment import ApplicationEnvironment


def _configure_logger(level, directory_path, name):

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    try:
        file_path = os.path.join(directory_path, name + '.log')
        os.mkdir(directory_path)
    except:
        pass

    logging.basicConfig(filename=file_path,
                        format='%(filename)s: %(message)s')
    logging.getLogger("gp").setLevel(level)


def _plot_summary(outputs_dir_path, scenario_name, trials):

    from behavior_tree_learning.core.logger import logplot

    parameters = logplot.PlotParameters()
    parameters.plot_std = True
    parameters.xlabel = 'Episodes'
    parameters.ylabel = 'Fitness'
    parameters.mean_color = 'r'
    parameters.std_color = 'r'
    parameters.horizontal = -3.0
    parameters.save_fig = True
    parameters.save_fig = True
    parameters.path = os.path.join(outputs_dir_path, scenario_name + '.pdf')

    logplot.plot_learning_curves(trials, parameters)


def _prepare_scenarios():

    scenarios = []

    scenario_name = 'tower'
    start_position = [WorldPos(-0.05, -0.1, 0), WorldPos(0.0, -0.1, 0), WorldPos(0.05, -0.1, 0)]
    target_position = [WorldPos(0.0, 0.05, 0), WorldPos(0.0, 0.05, 0.0192), WorldPos(0.0, 0.05, 2 * 0.0192)]
    scenarios.append((scenario_name, start_position, target_position))

    scenario_name = 'croissant'
    start_position = [WorldPos(-0.05, -0.1, 0), WorldPos(0.05, -0.1, 0), WorldPos(0.05, 0.1, 0),
                      WorldPos(-0.05, 0.1, 0)]
    target_position = [WorldPos(0.0, 0.0, 0.0), WorldPos(0.0, 0.0, 0.0192), WorldPos(0.016, -0.032, 0.0),
                       WorldPos(0.016, 0.032, 0.0)]
    scenarios.append((scenario_name, start_position, target_position))

    return scenarios


def run():

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

    # add specific class for plot_parameters
    parameters.plot_fitness = True
    parameters.plot_best_individual = True
    parameters.plot_last_generation = True

    scenarios = _prepare_scenarios()
    for scenario_name, start_position, target_position in scenarios:

        num_trials = 10
        trials = []
        for tdx in range(1, num_trials+1):

            trial_name = scenario_name + '_' + str(tdx)
            trials.append(trial_name)
            print("Trial: %s" % trial_name)

            log_name = trial_name
            _configure_logger(logging.DEBUG, paths.get_log_directory(), log_name)

            parameters.log_name = log_name
            seed = tdx

            node_factory = BehaviorNodeFactory(get_behaviors(scenario_name))
            world_factory = ApplicationWorldFactory(start_position, scenario=scenario_name)
            environment = ApplicationEnvironment(node_factory, world_factory, target_position, verbose=False)

            bt_learner = BehaviorTreeLearner.from_environment(environment)
            success = bt_learner.run(parameters, seed,
                                     outputs_dir_path=paths.get_outputs_directory(),
                                     verbose=False)

            print("Trial: %d, Succeed: %s" % (tdx, success))

        _plot_summary(paths.get_outputs_directory(), scenario_name, trials)


if __name__ == "__main__":
    run()

