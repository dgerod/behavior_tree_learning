"""
A simple simulation environment for test purposes only.
All environments must contain a get_fitness(individual) function
that returns a fitness value and a plot_individual() function that
returns nothing but saves a graphical representation of the individual
"""

from behavior_tree_learning.core.sbt import StringBehaviorTree
from behavior_tree_learning.tests.fwk import fitness_function
from behavior_tree_learning.tests.fwk import behaviors_states as behaviors
from behavior_tree_learning.tests.fwk import state_machine as sm


def get_fitness(string):
    """ Run the simulation and return the fitness """
    state_machine = sm.StateMachine()
    behavior_tree = StringBehaviorTree(string[:], behaviors=behaviors, world=state_machine)

    # run the Behavior Tree
    behavior_tree.run_bt()

    return fitness_function.compute_fitness(state_machine, behavior_tree)


def plot_individual(path, plot_name, individual):
    """ Saves a graphical representation of the individual """
    pytree = StringBehaviorTree(individual[:], behaviors=behaviors)
    pytree.save_fig(path, name=plot_name)
