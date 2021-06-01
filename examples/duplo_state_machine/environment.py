from interface import implements
from behavior_tree_learning.gp import GeneticEnvironment
from behavior_tree_learning.sbt import World
from behavior_tree_learning.sbt import StringBehaviorTree

from duplo_state_machine import behaviors
from duplo_state_machine import fitness_function


class Environment(implements(GeneticEnvironment)):
    """ Class defining the environment in which the individual operates """

    def __init__(self, world: World, target_positions, static_tree=None,
                 verbose=False, sm_pars=None, mode=0, fitness_coeff=None):

        self.world = world
        self.targets = target_positions
        self.static_tree = static_tree
        self.verbose = verbose
        self.sm_pars = sm_pars
        self.mode = mode
        self.fitness_coeff = fitness_coeff
        self.random_events = False

    def set_random_events(self, random_events):
        """ Sets the random events flag """

        self.random_events = random_events

    def run_and_compute(self, individual):
        """ Run the simulation and return the fitness """

        behavior_tree = StringBehaviorTree(individual[:], behaviors=behaviors, world=self.world, verbose=self.verbose)
        ticks, _ = behavior_tree.run_bt()
        return fitness_function.compute_fitness(self.world, behavior_tree, ticks, self.targets, self.fitness_coeff)

    def plot_individual(self, path, plot_name, individual):
        """ Saves a graphical representation of the individual """

        if self.static_tree is not None:
            pytree = StringBehaviorTree(self._add_to_static_tree(individual), behaviors=behaviors)
        else:
            pytree = StringBehaviorTree(individual[:], behaviors=behaviors)
        pytree.save_fig(path, name=plot_name)

    def _add_to_static_tree(self, individual):
        """ Add invididual to the static part of the tree in the front """

        new_individual = self.static_tree[:]
        new_individual[-2:-2] = individual
        return new_individual


class Environment1(Environment):
    """ Test class for only running first target in list  """

    def __init__(self, targets, static_tree, verbose=False):
        super().__init__(targets, static_tree, verbose)
        self.targets = [self.targets[0]]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))


class Environment12(Environment):
    """ Test class for only running first two targets in list  """

    def __init__(self, targets, static_tree, verbose=False):
        super().__init__(targets, static_tree, verbose)
        self.targets = self.targets[:2]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))


class Environment123(Environment):
    """ Test class for only running first three targets in list  """

    def __init__(self, targets, static_tree, verbose=False):
        super().__init__(targets, static_tree, verbose)
        self.targets = self.targets[:3]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))
