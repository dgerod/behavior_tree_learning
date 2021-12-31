#!/usr/bin/env python

import paths
paths.add_modules_to_path()

import unittest
import os
import shutil
from behavior_tree_learning.core.logger import logplot


class TestStringBehaviorTreeForPyTree(unittest.TestCase):

    OUTPUT_DIR = 'logs'
    
    def test_trim_logs(self):

        logs = []
        logs.append([1, 2, 3])
        logs.append([1, 2, 3, 4])
        logs.append([1, 2, 3, 4, 5])

        logplot.trim_logs(logs)

        assert logs == [[1, 2, 3], [1, 2, 3], [1, 2, 3]]

    def test_plot_fitness(self):

        LOG_NAME = 'test'
        
        logplot.clear_logs(LOG_NAME)
        logplot.plot_fitness(LOG_NAME, [0, 1, 2])
        assert os.path.isfile(logplot.get_log_folder(LOG_NAME) + '/Fitness.png')
        try:
            shutil.rmtree(logplot.get_log_folder('test'))
        except FileNotFoundError:
            pass

    def test_plot_learning_curves_with_extend_gens(self):

        LOG_NAME_1 = 'test1'
        LOG_NAME_2 = 'test2'
        PDF_FILE_NAME = 'test.pdf'
    
        logplot.clear_logs(LOG_NAME_1)
        logplot.log_best_fitness(LOG_NAME_1, [1, 2, 3, 4, 5])
        logplot.log_n_episodes(LOG_NAME_1, [5, 10, 15, 20, 25])
        logplot.clear_logs(LOG_NAME_2)
        logplot.log_best_fitness(LOG_NAME_2, [1, 2, 5])
        logplot.log_n_episodes(LOG_NAME_2, [5, 10, 15])

        parameters = logplot.PlotParameters()
        parameters.path = PDF_FILE_NAME
        parameters.extend_gens = 5
        parameters.save_fig = True
        parameters.x_max = 30
        
        logplot.plot_learning_curves([LOG_NAME_1, LOG_NAME_2], parameters)

    def test_plot_learning_curves(self):

        LOG_NAME = 'test'
        PDF_FILE_NAME = 'test.pdf'
        
        try:
            os.remove(PDF_FILE_NAME)
        except FileNotFoundError:
            pass

        logplot.clear_logs(LOG_NAME)
        logplot.log_best_fitness(LOG_NAME, [1, 2, 3, 4, 5])
        logplot.log_n_episodes(LOG_NAME, [5, 10, 15, 20, 25])

        parameters = logplot.PlotParameters()
        parameters.path = PDF_FILE_NAME
        parameters.extrapolate_y = False
        parameters.plot_mean = False
        parameters.plot_std = False
        parameters.plot_ind = False
        parameters.save_fig = False
        parameters.x_max = 0
        parameters.plot_horizontal = True
        logplot.plot_learning_curves([LOG_NAME], parameters)
        self.assertFalse(os.path.isfile(PDF_FILE_NAME))

        parameters.extrapolate_y = True
        parameters.plot_mean = True
        parameters.plot_std = True
        parameters.plot_ind = True
        parameters.save_fig = True
        parameters.x_max = 100
        parameters.plot_horizontal = True
        parameters.save_fig = True
        logplot.plot_learning_curves([LOG_NAME], parameters)
        self.assertTrue(os.path.isfile(PDF_FILE_NAME))
        os.remove(PDF_FILE_NAME)

        parameters.x_max = 10
        parameters.plot_horizontal = False
        logplot.plot_learning_curves([LOG_NAME], parameters)
        assert os.path.isfile(PDF_FILE_NAME)

        os.remove(PDF_FILE_NAME)
        try:
            shutil.rmtree(logplot.get_log_folder(LOG_NAME))
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
