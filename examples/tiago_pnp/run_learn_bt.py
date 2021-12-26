#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

from behavior_tree_learning.sbt import BehaviorNodeFactory
from behavior_tree_learning.learning import BehaviorTreeLearner, GeneticParameters, GeneticSelectionMethods

from tiago_pnp.execution_nodes import get_behaviors
from tiago_pnp.world import WorldSimulator, WorldFactory
from tiago_pnp.environment import Environment


def run():

    # if scenario == 2:
    #    world = sm.StateMachine(self.scenario, self.deterministic, self.verbose, pose_id=i)
    # else:
    #    world = sm.StateMachine(self.scenario, self.deterministic, self.verbose)

    scenario = 'scenario_1'
    deterministic = False

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

    num_trials = 10
    for tdx in range(1, num_trials+1):

        # add specific class for plot_parametes
        parameters.plot = True
        parameters.fig_last_gen = False
        parameters.log_name = scenario + '_' + str(tdx)

        node_factory = BehaviorNodeFactory(get_behaviors(scenario))
        world_factory = WorldFactory(scenario, deterministic)
        environment = Environment(node_factory, world_factory, scenario)

        seed = tdx*100
        bt_learner = BehaviorTreeLearner(environment)
        success = bt_learner.run(parameters, seed, verbose=False)

        print("Trial: %d, Succeed: %s" % (tdx, success))


if __name__ == "__main__":
    run()
