import sys
import time

import behavior_tree_learning.core.str_bt.behavior_tree as behavior_tree
import behavior_tree_learning.core.gp.genetic_programming as gp
import behavior_tree_learning.core.logger.logplot as logplot

import behavior_tree_learning.examples.duplo_state_machine.environment as Environment

def run():

    behavior_tree.load_settings_from_file('BT_SETTINGS_TOWER.yaml')

    gp_parameters = gp.GpParameters()
    gp_parameters.ind_start_length = 8
    gp_parameters.n_population = 16
    gp_parameters.f_crossover = 0.5
    gp_parameters.n_offspring_crossover = 2
    gp_parameters.replace_crossover = False
    gp_parameters.f_mutation = 0.5
    gp_parameters.n_offspring_mutation = 2
    gp_parameters.parent_selection = gp.SelectionMethods.RANK
    gp_parameters.survivor_selection = gp.SelectionMethods.RANK
    gp_parameters.f_elites = 0.1
    gp_parameters.f_parents = gp_parameters.f_elites
    gp_parameters.mutate_co_offspring = False
    gp_parameters.mutate_co_parents = True
    gp_parameters.mutation_p_add = 0.4
    gp_parameters.mutation_p_delete = 0.3
    gp_parameters.allow_identical = False
    gp_parameters.plot = True
    gp_parameters.n_generations = 200
    gp_parameters.verbose = False
    gp_parameters.fig_last_gen = False
    
    targets = []
    targets.append(agx_interface.Pos(0.0, 0.05, 0))
    targets.append(agx_interface.Pos(0.0, 0.05, 0.0192))
    targets.append(agx_interface.Pos(0.0, 0.05, 2*0.0192))

    rosid = "1"
    world_interface = agx_interface.AgxInterface(rosid)
    environment = Environment(world_interface, targets, verbose=False)
    
    n_logs = 10
    for i in range(1, n_logs + 1):
        gp_parameters.log_name = 'tower_no_baseline_' + str(i)
        gp.set_seeds(i)
        gp.run(environment, gp_parameters)

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
        gp.run(environment, gp_parameters, baseline=planner_baseline)
