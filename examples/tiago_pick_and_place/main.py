#!/usr/bin/env python3

import sys
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

from behavior_tree_learning.core.logger import logplot
from behavior_tree_learning.core.gp import algorithm as gp
from behavior_tree_learning.core.gp.parameters import GeneticParameters
from tiago_pick_and_place.environment import Environment


def _run_simulation():

    # Define run details
    #   Scenario 1: one cube to pick from a fixed position
    #   Scenario 2: one cube to pick from a random position out of three possibilities
    #   Scenario 3: three cubes to pick from three different fixed positions

    deterministic = True
    verbose = False

    gp_par = GeneticParameters()
    gp_par.ind_start_length = 4
    gp_par.n_population = 30
    gp_par.f_crossover = 0.4
    gp_par.f_mutation = 0.6
    gp_par.n_offspring_crossover = 2
    gp_par.n_offspring_mutation = 4
    gp_par.parent_selection = gp.SelectionMethods.TOURNAMENT
    gp_par.survivor_selection = gp.SelectionMethods.TOURNAMENT
    gp_par.f_elites = 0.1
    gp_par.f_parents = 1
    gp_par.mutation_p_add = 0.5
    gp_par.mutation_p_delete = 0.2
    gp_par.rerun_fitness = 0
    gp_par.allow_identical = False
    gp_par.plot = True
    gp_par.n_generations = 8000
    gp_par.verbose = False
    gp_par.fig_last_gen = False

    for i in range(1, 11):
        gp_par.log_name = 'scenario1_' + str(i)
        gp.set_seeds(i * 100)
        scenario = 1
        environment = Environment(scenario, deterministic, verbose)
        gp.run(environment, gp_par)

    for i in range(1, 11):
        gp_par.log_name = 'scenario2_' + str(i)
        gp.set_seeds(i * 100)
        scenario = 2
        environment = Environment(scenario, deterministic, verbose)
        gp.run(environment, gp_par)

    for i in range(1, 11):
        gp_par.log_name = 'scenario3_' + str(i)
        gp.set_seeds(i * 100)
        scenario = 3
        environment = Environment(scenario, deterministic, verbose)
        gp.run(environment, gp_par)


def _plot_results():

    # which plot?
    failure_prob = True
    noise = True
    safety = True
    scenarios = True

    # Load paths base
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

    plotpars = logplot.PlotParameters()

    plotpars.ylabel = 'Fitness'
    plotpars.xlabel = 'Episodes'
    plotpars.x_max = 400000
    plotpars.plot_optimal = True
    plotpars.plot_std = False
    plotpars.optimum = -15.0
    plotpars.legend_fsize = 16.0
    plotpars.title_fsize = 18.0
    plotpars.label_fsize = 16.0

    n_logs = 10

    # PLOT 1: impact of the failure probabilities on the learning
    if failure_prob:
        plotpars.save_fig = False
        plotpars.title = 'Impact of the failure probabilities'
        plotpars.path = os.path.join(parent_dir, 'plots/runs_probability.svg')

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario1_deterministic_' + str(i))
        plotpars.mean_color = 'b'
        plotpars.legend_name = 'Deterministic'
        logplot.plot_learning_curves(logs, plotpars)

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario1_stoch1_' + str(i))
        plotpars.mean_color = 'r'
        plotpars.legend_name = 'Stochastic 1'
        logplot.plot_learning_curves(logs, plotpars)

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario1_stoch2_' + str(i))
        plotpars.mean_color = 'g'
        plotpars.legend_name = 'Stochastic 2'
        logplot.plot_learning_curves(logs, plotpars)

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario1_stoch3_' + str(i))
        plotpars.mean_color = 'c'
        plotpars.legend_name = 'Stochastic 3'
        logplot.plot_learning_curves(logs, plotpars)

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario1_stoch4_' + str(i))
        plotpars.mean_color = 'k'
        plotpars.legend_name = 'Stochastic 4'
        plotpars.save_fig = True

        logplot.plot_learning_curves(logs, plotpars)

    # PLOT 2: impact of the noise on the learning
    if noise:
        plotpars.save_fig = False
        plotpars.title = 'Effects of adding non-essential behaviors'
        plotpars.path = os.path.join(parent_dir, 'plots/runs_noise.svg')

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario1_base_' + str(i))
        plotpars.mean_color = 'b'
        plotpars.legend_name = 'Necessary behaviors'
        logplot.plot_learning_curves(logs, plotpars)

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario1_lowNoise_' + str(i))
        plotpars.mean_color = 'r'
        plotpars.legend_name = '7 non-essential behaviors'
        logplot.plot_learning_curves(logs, plotpars)

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario1_highNoise_' + str(i))
        plotpars.mean_color = 'g'
        plotpars.legend_name = '14 non-essential behaviors'
        plotpars.save_fig = True

        logplot.plot_learning_curves(logs, plotpars)

    # PLOT 3: impact of the failure probability cost on the fitness function
    if safety:
        plotpars.save_fig = False
        plotpars.title = 'Impact of the failure cost on the fitness'
        plotpars.path = os.path.join(parent_dir, 'plots/runs_safety.svg')

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario1_safe_' + str(i))
        plotpars.mean_color = 'r'
        plotpars.legend_name = 'Safe Path'
        logplot.plot_learning_curves(logs, plotpars)

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario1_risky_' + str(i))
        plotpars.mean_color = 'b'
        plotpars.legend_name = 'Risky Path'
        plotpars.save_fig = True

        logplot.plot_learning_curves(logs, plotpars)

    # PLOT 4: comparative study on the difficulty of learning a task
    if scenarios:
        plotpars.x_max = 4 * 400000
        plotpars.legend_fsize = 14.0
        plotpars.title_fsize = 16.0
        plotpars.label_fsize = 14.0
        plotpars.save_fig = False
        plotpars.title = 'Learning of tasks with increasing difficulty'
        plotpars.path = os.path.join(parent_dir, 'plots/runs_scenarios.svg')

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario1_' + str(i))
        plotpars.mean_color = 'b'
        plotpars.std_color = 'b'
        plotpars.legend_name = '1st Scenario'
        logplot.plot_learning_curves(logs, plotpars)

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario2_' + str(i))
        plotpars.mean_color = 'r'
        plotpars.std_color = 'r'
        plotpars.legend_name = '2nd Scenario'
        logplot.plot_learning_curves(logs, plotpars)

        logs = []
        for i in range(1, n_logs + 1):
            logs.append('scenario3_' + str(i))
        plotpars.mean_color = 'g'
        plotpars.std_color = 'g'
        plotpars.legend_name = '3rd Scenario'
        plotpars.save_fig = True

        logplot.plot_learning_curves(logs, plotpars)

    """
    # example: plotting 10 different lines in the same figure wit colormap
    colormap = plt.cm.gist_ncar #nipy_spectral, Set1,Paired  
    colorst = [colormap(i) for i in np.linspace(0, 0.9, 10)]

    for i in range(1, 10):
        logs = []
        logs.append('scenario1_' + str(i))
        plotpars.plot_std = False
        plotpars.mean_color = colorst[i-1]
        plotpars.legend_name = 'run_' + str(i)
        logplot.plot_learning_curves(logs, plotpars)

    logs = []
    logs.append('3cubes_5f_10')
    plotpars.plot_std = False
    plotpars.mean_color = colorst[9]
    plotpars.legend_name = 'run_10'
    plotpars.save_fig = True
    logplot.plot_learning_curves(logs, plotpars)
    """


def run():
    _run_simulation()
    _plot_results()


if __name__ == "__main__":
    run()
