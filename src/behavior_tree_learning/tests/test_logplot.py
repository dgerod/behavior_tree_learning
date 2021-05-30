#!/usr/bin/env python

import unittest

import os
import shutil
from behavior_tree_learning.core.logger import logplot
from behavior_tree_learning.core.tests.fwk.paths import TEST_DIRECTORY


class TestStringBehaviorTreeForPyTree(unittest.TestCase):

    OUTPUT_DIR = os.path.join(TEST_DIRECTORY, 'tmp')
    
    def test_trim_logs(self):
        """ Tests trim_logs function """

        logs = []
        logs.append([1, 2, 3])
        logs.append([1, 2, 3, 4])
        logs.append([1, 2, 3, 4, 5])

        logplot.trim_logs(logs)

        assert logs == [[1, 2, 3], [1, 2, 3], [1, 2, 3]]

    def test_plot_fitness(self):
        """ Tests plot_fitness function """

        TEST_DIR = os.path.join(self.OUTPUT_DIR, 'test')
        
        logplot.clear_logs('test')
        logplot.plot_fitness('test', [0, 1, 2])
        assert os.path.isfile(logplot.get_log_folder('test') +  '/Fitness.png')
        try:
            shutil.rmtree(logplot.get_log_folder('test'))
        except FileNotFoundError:
            pass

    def test_extend_gens(self):
        """ Tests plot of learning curves with extended gens """
        
        TEST_1_DIR = os.path.join(self.OUTPUT_DIR, 'test1')
        TEST_2_DIR = os.path.join(self.OUTPUT_DIR, 'test2')
        PDF_FILE_PATH = os.path.join(self.OUTPUT_DIR, 'test.pdf')
    
        logplot.clear_logs(TEST_1_DIR)
        logplot.log_best_fitness(TEST_1_DIR, [1, 2, 3, 4, 5])
        logplot.log_n_episodes(TEST_1_DIR, [5, 10, 15, 20, 25])
        logplot.clear_logs(TEST_2_DIR)
        logplot.log_best_fitness(TEST_2_DIR, [1, 2, 5])
        logplot.log_n_episodes(TEST_2_DIR, [5, 10, 15])

        parameters = logplot.PlotParameters()
        parameters.path = PDF_FILE_PATH
        parameters.extend_gens = 5
        parameters.save_fig = True
        parameters.x_max = 30
        
        logplot.plot_learning_curves([TEST_1_DIR, TEST_2_DIR], parameters)

    def test_plot_learning_curves(self):
        """ Tests plot_learning_curves function """
        
        TEST_DIR = os.path.join(self.OUTPUT_DIR, 'test')
        PDF_FILE_PATH = os.path.join(TEST_DIR, 'test.pdf')
        
        try:
            os.remove(PDF_FILE_PATH)
        except FileNotFoundError:
            pass

        logplot.clear_logs('test')
        logplot.log_best_fitness('test', [1, 2, 3, 4, 5])
        logplot.log_n_episodes('test', [5, 10, 15, 20, 25])

        parameters = logplot.PlotParameters()
        parameters.path = PDF_FILE_PATH
        parameters.extrapolate_y = False
        parameters.plot_mean = False
        parameters.plot_std = False
        parameters.plot_ind = False
        parameters.save_fig = False
        parameters.x_max = 0
        parameters.plot_horizontal = True
        logplot.plot_learning_curves([TEST_DIR], parameters)
        assert not os.path.isfile(PDF_FILE_PATH)

        parameters.extrapolate_y = True
        parameters.plot_mean = True
        parameters.plot_std = True
        parameters.plot_ind = True
        parameters.save_fig = True
        parameters.x_max = 100
        parameters.plot_horizontal = True
        parameters.save_fig = True
        logplot.plot_learning_curves([TEST_DIR], parameters)
        assert os.path.isfile(PDF_FILE_PATH)
        os.remove(PDF_FILE_PATH)

        parameters.x_max = 10
        parameters.plot_horizontal = False
        logplot.plot_learning_curves([TEST_DIR], parameters)
        assert os.path.isfile(PDF_FILE_PATH)

        os.remove(PDF_FILE_PATH)
        try:
            shutil.rmtree(logplot.get_log_folder(TEST_DIR))
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
