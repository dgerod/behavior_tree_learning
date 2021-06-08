#!/usr/bin/env python3

import sys
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

from behavior_tree_learning.sbt import bt as behavior_tree
from behavior_tree_learning.gp import gp, GeneticParameters, GeneticSelectionMethods
from behavior_tree_learning.core.gp_sbt import Operators as GeneticOperatorsForStringBehaviorTree
from duplo_state_machine.paths import EXAMPLE_DIRECTORY
from duplo_state_machine.environment import Environment
from duplo_state_machine import state_machine as sm


def run():

    settings_file = os.path.join(EXAMPLE_DIRECTORY, 'BT_SETTINGS_TOWER.yaml')
    behavior_tree.load_settings_from_file(settings_file)

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
    gp_parameters.verbose = False
    gp_parameters.fig_last_gen = False

    start_position = [sm.Pos(-0.05, -0.1, 0),
                      sm.Pos(0.0,  -0.1, 0),
                      sm.Pos(0.05, -0.1, 0)]

    world = sm.StateMachine(start_position)
    target_position = [sm.Pos(0.0, 0.05, 0),
                       sm.Pos(0.0, 0.05, 0.0192),
                       sm.Pos(0.0, 0.05, 2*0.0192)]

    environment = Environment(world, target_position, verbose=False)
    
    n_logs = 10
    for i in range(1, n_logs + 1):
        gp_parameters.log_name = 'tower_no_baseline_' + str(i)
        gp.set_seeds(i)
        gp.set_operators(GeneticOperatorsForStringBehaviorTree())
        gp.run(environment, gp_parameters)

    return

    planner_baseline = ['s(', 
                            'f(', 
                                '0 at pos (0.0, 0.05, 0.0)?', 
                                's(', 
                                    'f(', 'picked 0?', 'pick 0!', ')', 
                                    'place at (0.0, 0.05, 0.0)!', 
                                ')', 
                            ')',
                            'f(', 
                                '1 at pos (0.0, 0.05, 0.0192)?', 
                                's(', 
                                    'f(', '1 on 0?', 
                                        's(', 
                                            'f(', 
                                                'picked 1?', 
                                                'pick 1!', 
                                            ')', 
                                            'place on 0!', 
                                        ')', 
                                    ')', 
                                    'apply force 1!', 
                                ')', 
                            ')', 
                            'f(', 
                                '2 at pos (0.0, 0.05, 0.0384)?', 
                                's(', 
                                    'f(', 
                                        '2 on 1?', 
                                        's(', 
                                            'f(', 
                                                'picked 2?', 
                                                'pick 2!', 
                                            ')', 
                                            'place on 1!', 
                                        ')', 
                                    ')', 
                                    'apply force 2!', 
                                ')', 
                            ')', 
                        ')']

    n_logs = 10
    for i in range(1, n_logs + 1):
        gp_parameters.log_name = 'tower_planner_baseline_' + str(i)
        gp.set_seeds(i)
        gp.set_operators(GeneticOperatorsForStringBehaviorTree())
        gp.run(environment, gp_parameters, base_line=planner_baseline)


if __name__ == "__main__":
    run()
