#!/usr/bin/env python

import unittest

import os
from statistics import mean
from behavior_tree_learning.core.str_bt import behavior_tree as bt
from behavior_tree_learning.core.gp import genetic_programming as gp
from behavior_tree_learning.core.gp.parameters import GeneticParameters

from behavior_tree_learning.core.tests.fwk.paths import TEST_DIRECTORY as CORE_TEST_DIRECTORY
from behavior_tree_learning.examples.duplo_state_machine.paths import EXAMPLE_DIRECTORY
from behavior_tree_learning.examples.duplo_state_machine import state_machine as sm
from behavior_tree_learning.examples.duplo_state_machine import environment as sm_environment
from behavior_tree_learning.examples.duplo_state_machine.state_machine import Pos
from behavior_tree_learning.examples.duplo_simulation.fitness_function import Coefficients


class TestStateMachine(unittest.TestCase):

      def test_tower(self):
            """ Test stacking tower scenario """

            gp_par = GeneticParameters()
            gp_par.ind_start_length = 8
            gp_par.n_population = 16
            gp_par.f_crossover = 0.5
            gp_par.n_offspring_crossover = 2
            gp_par.replace_crossover = False
            gp_par.f_mutation = 0.5
            gp_par.n_offspring_mutation = 2
            gp_par.parent_selection = gp.SelectionMethods.RANK
            gp_par.survivor_selection = gp.SelectionMethods.RANK
            gp_par.f_elites = 0.1
            gp_par.f_parents = gp_par.f_elites
            gp_par.mutate_co_offspring = False
            gp_par.mutate_co_parents = True
            gp_par.mutation_p_add = 0.4
            gp_par.mutation_p_delete = 0.3
            gp_par.allow_identical = False
            gp_par.plot = True
            gp_par.n_generations = 200
            gp_par.verbose = False
            gp_par.fig_last_gen = False

            bt.load_settings_from_file(os.path.join(EXAMPLE_DIRECTORY, 'BT_SETTINGS_TOWER.yaml'))

            planner_baseline = ['s(', 'f(', '0 at pos (0.0, 0.05, 0.0)?', \
                                                's(', 'f(', 'picked 0?', 'pick 0!', ')', 'place at (0.0, 0.05, 0.0)!', ')', ')', \
                                    'f(', '1 at pos (0.0, 0.05, 0.0192)?', \
                                          's(', 'f(', '1 on 0?', 's(', 'f(', 'picked 1?', 'pick 1!', ')', 'place on 0!', ')', ')', \
                                                'apply force 1!', ')', ')',  \
                                    'f(', '2 at pos (0.0, 0.05, 0.0384)?', \
                                          's(', 'f(', '2 on 1?', 's(', 'f(', 'picked 2?', 'pick 2!', ')', 'place on 1!', ')', ')', \
                                                'apply force 2!', ')', ')', ')']

            solved = ['s(', 'f(', '0 at pos (0.0, 0.05, 0.0)?', 's(', 'pick 0!', 'place at (0.0, 0.05, 0.0)!', ')', ')', \
                        'f(', '1 at pos (0.0, 0.05, 0.0192)?', \
                              's(', 'f(', '1 on 0?', 's(', 'pick 1!', 'place on 0!', ')', ')', 'apply force 1!', ')', ')',  \
                        'f(', '2 at pos (0.0, 0.05, 0.0384)?', \
                              's(', 'f(', '2 on 1?', 's(', 'pick 2!', 'place on 1!', ')', ')', 'apply force 2!', ')', ')', ')']

            start_positions = []
            start_positions.append(sm.Pos(-0.05, -0.1, 0))
            start_positions.append(sm.Pos(0, -0.1, 0))
            start_positions.append(sm.Pos(0.05, -0.1, 0))
            targets = []
            targets.append(Pos(0.0, 0.05, 0))
            targets.append(Pos(0.0, 0.05, 0.0192))
            targets.append(Pos(0.0, 0.05, 2*0.0192))
            environment = sm_environment.Environment(start_positions, targets, verbose=False)

            fitness = environment.get_fitness(planner_baseline)
            assert fitness > -4

            fitness = environment.get_fitness(solved)
            assert fitness > -3

            gp_par.log_name = 'test_tower'
            _, _, best_fitness, _ = gp.run(environment, gp_par, base_line=planner_baseline)
            assert best_fitness[-1] > -3

            bt.load_settings_from_file(os.path.join(CORE_TEST_DIRECTORY, 'BT_TEST_SETTINGS.yaml'))

      def test_croissant(self):
            """ Test croissant scenario """

            gp_par = GeneticParameters()
            gp_par.ind_start_length = 8
            gp_par.n_population = 16
            gp_par.f_crossover = 0.5
            gp_par.n_offspring_crossover = 2
            gp_par.replace_crossover = False
            gp_par.f_mutation = 0.5
            gp_par.n_offspring_mutation = 2
            gp_par.parent_selection = gp.SelectionMethods.RANK
            gp_par.survivor_selection = gp.SelectionMethods.RANK
            gp_par.f_elites = 0.1
            gp_par.f_parents = gp_par.f_elites
            gp_par.mutate_co_offspring = False
            gp_par.mutate_co_parents = True
            gp_par.mutation_p_add = 0.4
            gp_par.mutation_p_delete = 0.3
            gp_par.allow_identical = False
            gp_par.plot = True
            gp_par.n_generations = 1000
            gp_par.verbose = False
            gp_par.fig_last_gen = False

            bt.load_settings_from_file(os.path.join(EXAMPLE_DIRECTORY, 'BT_SETTINGS_CROISSANT.yaml'))

            planner_baseline = ['s(', 'f(', '0 at pos (0.0, 0.0, 0.0)?', \
                                                's(', 'f(', 'picked 0?', 'pick 0!', ')', 'place at (0.0, 0.0, 0.0)!', ')', ')', \
                                    'f(', '1 at pos (0.0, 0.0, 0.0192)?', \
                                          's(', 'f(', '1 on 0?', 's(', 'f(', 'picked 1?', 'pick 1!', ')', 'place on 0!', ')', ')', \
                                                'apply force 1!', ')', ')', \
                                    'f(', '2 at pos (0.016, -0.032, 0.0)?', \
                                          's(', 'f(', 'picked 2?', 'pick 2!', ')', 'place at (0.016, -0.032, 0.0)!', ')', ')', \
                                    'f(', '3 at pos (0.016, 0.032, 0.0)?', \
                                          's(', 'f(', 'picked 3?', 'pick 3!', ')', 'place at (0.016, 0.032, 0.0)!', ')', ')', ')']

            solved = ['s(', 'f(', '0 at pos (0.0, 0.0, 0.0)?', 's(', 'pick 0!', 'place at (0.0, 0.0, 0.0)!', ')', ')', \
                                    'f(', '2 at pos (0.016, -0.032, 0.0)?', \
                                          's(', 'pick 2!', 'place at (0.016, -0.032, 0.0)!', ')', ')', \
                                    'f(', '3 at pos (0.016, 0.032, 0.0)?', \
                                          's(', 'pick 3!', 'place at (0.016, 0.032, 0.0)!', ')', ')', \
                                    'f(', '1 at pos (0.0, 0.0, 0.0192)?', \
                                          's(', 'f(', '1 on 0?', 's(', 'pick 1!', 'place on 0!', ')', ')', \
                                                'apply force 1!', ')', ')', ')']

            start_positions = []
            start_positions.append(Pos(-0.05, -0.1, 0))
            start_positions.append(Pos(0, -0.1, 0))
            start_positions.append(Pos(0.05, -0.1, 0))
            start_positions.append(Pos(0.1, -0.1, 0))
            targets = []
            targets.append(Pos(0.0, 0.0, 0.0))
            targets.append(Pos(0.0, 0.0, 0.0192))
            targets.append(Pos(0.016, -0.032, 0.0))
            targets.append(Pos(0.016, 0.032, 0.0))
            environment = sm_environment.Environment(start_positions, targets, verbose=False, mode=sm.SMMode.CROISSANT)

            fitness = environment.get_fitness(planner_baseline)
            assert fitness < -100

            fitness = environment.get_fitness(solved)
            assert fitness > -3

            gp_par.log_name = 'test_croissant'
            _, _, best_fitness, _ = gp.run(environment, gp_par, base_line=planner_baseline)
            assert best_fitness[-1] > -4

            bt.load_settings_from_file(os.path.join(CORE_TEST_DIRECTORY, 'BT_TEST_SETTINGS.yaml'))

      def test_balance(self):
            """ Test balance scenario """

            gp_par = GeneticParameters()
            gp_par.ind_start_length = 8
            gp_par.n_population = 16
            gp_par.f_crossover = 0.5
            gp_par.n_offspring_crossover = 2
            gp_par.replace_crossover = False
            gp_par.f_mutation = 0.5
            gp_par.n_offspring_mutation = 2
            gp_par.parent_selection = gp.SelectionMethods.RANK
            gp_par.survivor_selection = gp.SelectionMethods.RANK
            gp_par.f_elites = 0.1
            gp_par.f_parents = gp_par.f_elites
            gp_par.mutate_co_offspring = False
            gp_par.mutate_co_parents = True
            gp_par.mutation_p_add = 0.4
            gp_par.mutation_p_delete = 0.3
            gp_par.allow_identical = False
            gp_par.plot = True
            gp_par.n_generations = 300
            gp_par.verbose = False
            gp_par.fig_last_gen = False

            bt.load_settings_from_file(os.path.join(EXAMPLE_DIRECTORY, 'BT_SETTINGS_BALANCE.yaml'))
            planner_baseline = ['s(', 'f(', '0 at pos (0.0, 0.0, 0.0192)?', \
                                                's(', 'f(', '1 at pos (0.0, 0.0, 0.0)?', 'put 1 at (0.0, 0.0, 0.0)!', ')', \
                                                      'f(', '0 on 1?', 'put 0 on 1!', ')', 'apply force 0!', ')', ')', ')']

            solved = ['f(', '0 at pos (0.0, 0.0, 0.0192)?', \
                              's(', 'put 2 at (0.0, 0.0, 0.0)!', 'put 0 on 2!', 'apply force 0!', ')', ')']

            start_positions = []
            start_positions.append(Pos(-0.05, -0.1, 0.0))
            start_positions.append(Pos(0.0, -0.1, 0.0))
            start_positions.append(Pos(0.05, -0.1, 0.0))
            targets = []
            targets.append(Pos(0.0, 0.0, 0.0192))
            fitness_coeff = Coefficients()
            fitness_coeff.hand_not_empty = 100.0

            environment = sm_environment.Environment(start_positions, targets, verbose=False, \
                                                      mode=sm.SMMode.BALANCE, fitness_coeff=fitness_coeff)

            fitness = environment.get_fitness(planner_baseline)
            assert fitness < -10

            fitness = environment.get_fitness(solved)
            assert fitness > -1

            gp_par.log_name = 'test_balance'
            _, _, best_fitness, _ = gp.run(environment, gp_par, base_line=planner_baseline)
            assert best_fitness[-1] > -1


            bt.load_settings_from_file(os.path.join(CORE_TEST_DIRECTORY, 'BT_TEST_SETTINGS.yaml'))

      def test_blocking(self):
            """ Test scenario of shuffling bricks to avoid blocking """

            gp_par = GeneticParameters()
            gp_par.ind_start_length = 8
            gp_par.n_population = 16
            gp_par.f_crossover = 0.5
            gp_par.n_offspring_crossover = 2
            gp_par.replace_crossover = False
            gp_par.f_mutation = 0.5
            gp_par.n_offspring_mutation = 2
            gp_par.parent_selection = gp.SelectionMethods.RANK
            gp_par.survivor_selection = gp.SelectionMethods.RANK
            gp_par.f_elites = 0.1
            gp_par.f_parents = gp_par.f_elites
            gp_par.mutate_co_offspring = False
            gp_par.mutate_co_parents = True
            gp_par.mutation_p_add = 0.4
            gp_par.mutation_p_delete = 0.3
            gp_par.allow_identical = False
            gp_par.plot = True
            gp_par.n_generations = 1000
            gp_par.verbose = False
            gp_par.fig_last_gen = False

            bt.load_settings_from_file(os.path.join(EXAMPLE_DIRECTORY, 'BT_SETTINGS_BLOCKING.yaml'))
            planner_baseline = ['s(', 'f(', '0 at pos (-0.1, 0.0, 0.0)?', 'put 0 at (-0.1, 0.0, 0.0)!', ')', \
                              'f(', '1 at pos (-0.1, 0.0, 0.0192)?', \
                                    's(', 'f(', '1 on 0?', 'put 1 on 0!', ')', 'apply force 1!', ')', ')', \
                              'f(', '2 at pos (0.0, 0.0, 0.0)?', 'put 2 at (0.0, 0.0, 0.0)!', ')', ')']

            solved = ['s(', 'put 1 on 0!', 'f(', '0 at pos (-0.1, 0.0, 0.0)?', 'put 2 at (0.0, 0.05, 0.0)!', ')', \
                                    'put 0 at (-0.1, 0.0, 0.0)!', \
                                    'f(', '1 at pos (-0.1, 0.0, 0.0192)?', 'apply force 1!', ')', \
                                    'put 2 at (0.0, 0.0, 0.0)!', ')']

            start_positions = []
            start_positions.append(sm.Pos(0.0, -0.05, 0.0))
            start_positions.append(sm.Pos(0.0, 0.05, 0.0))
            start_positions.append(sm.Pos(-0.1, 0.0, 0.0))

            targets = []
            targets.append(Pos(-0.1, 0.0, 0.0))
            targets.append(Pos(-0.1, 0.0, 0.0192))
            targets.append(Pos(0.0, 0.0, 0.0))

            environment = sm_environment.Environment(start_positions, targets, verbose=False, mode=sm.SMMode.BLOCKING)
            fitness = environment.get_fitness(planner_baseline)
            assert fitness < -50

            fitness = environment.get_fitness(solved)
            assert fitness > -2

            gp_par.log_name = 'test_blocking'
            _, _, best_fitness, _ = gp.run(environment, gp_par, base_line=planner_baseline)
            assert best_fitness[-1] > -2

            bt.load_settings_from_file(os.path.join(CORE_TEST_DIRECTORY, 'BT_TEST_SETTINGS.yaml'))

      def test_baselining(self):
            # pylint: disable=too-many-statements
            """ Tests various baseline setups in the blocking task """

            gp_par = GeneticParameters()
            gp_par.ind_start_length = 8
            gp_par.n_population = 16
            gp_par.f_crossover = 0.5
            gp_par.n_offspring_crossover = 2
            gp_par.replace_crossover = False
            gp_par.f_mutation = 0.5
            gp_par.n_offspring_mutation = 2
            gp_par.parent_selection = gp.SelectionMethods.RANK
            gp_par.survivor_selection = gp.SelectionMethods.RANK
            gp_par.f_elites = 0.1
            gp_par.f_parents = gp_par.f_elites
            gp_par.mutate_co_offspring = False
            gp_par.mutate_co_parents = True
            gp_par.mutation_p_add = 0.4
            gp_par.mutation_p_delete = 0.3
            gp_par.allow_identical = False
            gp_par.plot = True
            gp_par.verbose = False
            gp_par.fig_last_gen = False

            bt.load_settings_from_file(os.path.join(EXAMPLE_DIRECTORY, 'BT_SETTINGS_BLOCKING.yaml'))
            planner_baseline = ['s(', 'f(', '0 at pos (-0.1, 0.0, 0.0)?', 'put 0 at (-0.1, 0.0, 0.0)!', ')', \
                              'f(', '1 at pos (-0.1, 0.0, 0.0192)?', \
                                    's(', 'f(', '1 on 0?', 'put 1 on 0!', ')', 'apply force 1!', ')', ')', \
                              'f(', '2 at pos (0.0, 0.0, 0.0)?', 'put 2 at (0.0, 0.0, 0.0)!', ')', ')']

            start_positions = []
            start_positions.append(sm.Pos(0.0, -0.05, 0.0))
            start_positions.append(sm.Pos(0.0, 0.05, 0.0))
            start_positions.append(sm.Pos(-0.1, 0.0, 0.0))

            targets = []
            targets.append(Pos(-0.1, 0.0, 0.0))
            targets.append(Pos(-0.1, 0.0, 0.0192))
            targets.append(Pos(0.0, 0.0, 0.0))

            environment = sm_environment.Environment(start_positions, targets, verbose=False, mode=sm.SMMode.BLOCKING)

            n_logs = 10
            gp_par.n_generations = 10
            best_list_baseline_no_keep = []
            gp_par.keep_baseline = False
            for i in range(1, n_logs + 1):
                  gp_par.log_name = 'test_baseline_no_keep' + str(i)
                  gp.set_seeds(i)
                  _, _, best_fitness, _ = gp.run(environment, gp_par, base_line=planner_baseline)
                  best_list_baseline_no_keep.append(best_fitness[-1])

            gp_par.n_generations = 200
            best_list_baseline = []
            for i in range(1, n_logs + 1):
                  gp_par.log_name = 'test_baseline' + str(i)
                  gp.set_seeds(i)
                  _, _, best_fitness, _ = gp.run(environment, gp_par, base_line=planner_baseline)
                  best_list_baseline.append(best_fitness[-1])

            best_list_baseline_boost = []
            gp_par.keep_baseline = True
            gp_par.boost_baseline = True
            gp_par.boost_baseline_only_co = False
            for i in range(1, n_logs + 1):
                  gp_par.log_name = 'test_baseline_boost' + str(i)
                  gp.set_seeds(i)
                  _, _, best_fitness, _ = gp.run(environment, gp_par, base_line=planner_baseline)
                  best_list_baseline_boost.append(best_fitness[-1])

            best_list_baseline_boost_only_co = []
            gp_par.keep_baseline = True
            gp_par.boost_baseline = True
            gp_par.boost_baseline_only_co = True
            for i in range(1, n_logs + 1):
                  gp_par.log_name = 'test_baseline_boost_only_co' + str(i)
                  gp.set_seeds(i)
                  _, _, best_fitness, _ = gp.run(environment, gp_par, base_line=planner_baseline)
                  best_list_baseline_boost_only_co.append(best_fitness[-1])

            print(best_list_baseline_no_keep)
            print(best_list_baseline)
            print(best_list_baseline_boost)
            print(best_list_baseline_boost_only_co)

            print(mean(best_list_baseline_no_keep))
            print(mean(best_list_baseline))
            print(mean(best_list_baseline_boost))
            print(mean(best_list_baseline_boost_only_co))

            assert mean(best_list_baseline_boost) > mean(best_list_baseline)
            assert mean(best_list_baseline_boost_only_co) > mean(best_list_baseline_boost)

            #Results after 500 gens run
            #[-51.6, -89.6, -12.2, -2.3, -1.0, -50.2, -51.6, -1.0, -1.0, -1.0]
            #[-12.2, -50.2, -10.8, -1.0, -1.0, -1.0, -2.2999999999999985, -0.9, -50.2, -89.6]
            #[-1.0, -1.0, -1.3, -1.0, -1.0, -1.0, -50.2, -1.0, -1.0, -50.199999999999996]
            #[-1.0, -1.0, -1.1, -1.0, -1.0, -1.2, -1.0, -10.8, -40.3, -1.0]
            #-26.15
            #-21.9
            #-10.87
            #-5.9

            bt.load_settings_from_file(os.path.join(CORE_TEST_DIRECTORY, 'BT_TEST_SETTINGS.yaml'))

if __name__ == '__main__':
    unittest.main()
