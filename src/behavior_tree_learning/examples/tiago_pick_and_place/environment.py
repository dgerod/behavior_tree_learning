"""
A simple simulation environment for testing duplo handling.
All environments must contain a get_fitness(individual) function
that returns a fitness value and a plot_individual() function that
returns nothing but saves a graphical representation of the individual
"""
import os
from interface import implements
from behavior_tree_learning.core.str_bt import behavior_tree as bt
from behavior_tree_learning.core.str_bt import StringBehaviorTreeForPyTree
from behavior_tree_learning.core.environment import Environment as GpEnvironment

from behavior_tree_learning.examples.tiago_pick_and_place.paths import EXAMPLE_DIRECTORY
from behavior_tree_learning.examples.tiago_pick_and_place import behaviors
from behavior_tree_learning.examples.tiago_pick_and_place import fitness_function
from behavior_tree_learning.examples.tiago_pick_and_place import state_machine as sm


class Environment(implements(GpEnvironment)):
    """ Class defining the environment in which the individual operates """

    def __init__(self, scenario, deterministic=False, verbose=False):

        self.scenario = scenario
        self.deterministic = deterministic
        self.verbose = verbose

        settings_file = os.path.join(EXAMPLE_DIRECTORY, 'BT_SCENARIO_' + str(self.scenario) + '.yaml')
        bt.load_settings_from_file(settings_file)

    def run_and_compute(self, individual):
        """ Run the simulation and return the fitness """

        if self.scenario == 2:
            # in this case we run the same BT against the state machine in 3 different setups
            # every setup features a different spawn pose for the cube
            fitness = 0
            performance = 0
            completed = False
            for i in range(3):
                state_machine = sm.StateMachine(self.scenario, self.deterministic, self.verbose, pose_id=i)
                behavior_tree = StringBehaviorTreeForPyTree(individual[:], behaviors, world_interface=state_machine)

                ticks, _ = behavior_tree.run_bt()

                cost, output = fitness_function.compute_cost(state_machine, behavior_tree, ticks)

                fitness += -cost/3.0
                performance += int(output)

            if performance == 3:
                completed = True

        else:
            state_machine = sm.StateMachine(self.scenario, self.deterministic, self.verbose)
            behavior_tree = StringBehaviorTreeForPyTree(individual[:], behaviors, world_interface=state_machine)

            ticks, _ = behavior_tree.run_bt()

            cost, completed = fitness_function.compute_cost(state_machine, behavior_tree, ticks)
            fitness = -cost

        return fitness #, completed

    def plot_individual(self, path, plot_name, individual):
        """ Saves a graphical representation of the individual """

        pytree = StringBehaviorTreeForPyTree(individual[:], behaviors)
        pytree.save_fig(path, name=plot_name)

