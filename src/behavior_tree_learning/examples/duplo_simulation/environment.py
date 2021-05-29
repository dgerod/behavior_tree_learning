"""
A simple simulation environment for duplo handling.
All environments must contain a get_fitness(individual) function
that returns a fitness value and a plot_individual() function that
returns nothing but saves a graphical representation of the individual
"""
import time
from interface import implements
from behavior_tree_learning.core.environment import Environment as GpEnvironment
from behavior_tree_learning.core.str_bt import StringBehaviorTreeForPyTree
import behavior_tree_learning.examples.duplo_simulation.behaviors as behaviors
import behavior_tree_learning.examples.duplo_simulation.fitness_function as fitness_function


class Environment(implements(GpEnvironment)):
    """ General class template defining the environment in which the individual operates """
    def __init__(self, world, targets, static_tree=None, \
                 verbose=False, maximum_runs_per_session=100, fitness_coeff=None):
        # pylint: disable=too-many-arguments
        self.world = world
        self.targets = targets
        self.verbose = verbose
        self.static_tree = static_tree
        self.maximum_runs = maximum_runs_per_session #Number of runs before restarting agx to handle memory leaks
        self.fitness_coeff = fitness_coeff
        self.counter = 0

    def run_and_compute(self, individual, save_video=False):
        """
        Run the simulation and return the fitness
        In case of error, restarts world_interface and tries again.
        """
        pytree = StringBehaviorTreeForPyTree(individual[:], behaviors=behaviors, world=self.world_interface,
                                             verbose=self.verbose)

        status_ok = True
        fitness = None

        while fitness is None:
            if self.counter >= self.maximum_runs or not status_ok:
                self.world_interface.restart()
                self.counter = 0
            else:
                self.world_interface.reset()
            self.counter += 1

            if save_video:
                self.world_interface.start_video()

            ticks, status_ok = pytree.run_bt(max_ticks=200)
            count = 0
            while count < 50 and status_ok: #Wait up to five seconds for everything to come to a resting state
                old_sensor_data = self.world.get_sensor_data()
                status_ok = self.world.get_feedback()
                if status_ok:
                    if self.world.at_standstill(old_sensor_data):
                        break
                    self.world.send_references()
                    count += 1

            if save_video:
                time.sleep(1) #Needed for ros synch
                self.world.stop_video()

            if status_ok:
                fitness = fitness_function.compute_fitness(self.world, pytree, ticks,
                                                           self.targets, self.fitness_coeff, self.verbose)
            else:
                self.world_interface.restart()
                self.counter = 0
                print("Failed:", individual)
                fitness = -9999999

        return fitness

    def plot_individual(self, path, plot_name, individual):
        """ Saves a graphical representation of the individual """
        if self.static_tree is not None:
            bt = StringBehaviorTreeForPyTree(self._add_to_static_tree(individual), behaviors=behaviors)
        else:
            bt = StringBehaviorTreeForPyTree(individual[:], behaviors=behaviors)
        bt.save_fig(path, name=plot_name)

    def _add_to_static_tree(self, individual):
        """ Add invididual to the static part of the tree in the front """
        new_individual = self.static_tree[:]
        new_individual[-2:-2] = individual
        return new_individual


class Environment1(Environment):
    """ Test class for only running first target in list  """

    def __init__(self, world, targets, static_tree, verbose=False):
        super().__init__(world, targets, static_tree, verbose)
        self.targets = [self.targets[0]] #Only first target

    def get_fitness(self, individual, save_video=False):
        return super().get_fitness(self._add_to_static_tree(individual), save_video)


class Environment12(Environment):
    """ Test class for only running first two targets in list  """

    def __init__(self, world, targets, static_tree, verbose=False):
        super().__init__(world, targets, static_tree, verbose)
        self.targets = self.targets[:2] #Only first two targets

    def get_fitness(self, individual, save_video=False):
        return super().get_fitness(self._add_to_static_tree(individual), save_video)


class Environment123(Environment):
    """ Test class for only running first three targets in list  """

    def __init__(self, world, targets, static_tree, verbose=False):
        super().__init__(world, targets, static_tree, verbose)
        self.targets = self.targets[:3] #Only first three targets

    def get_fitness(self, individual, save_video=False):
        return super().get_fitness(self._add_to_static_tree(individual), save_video)
