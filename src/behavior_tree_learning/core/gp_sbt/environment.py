from interface import Interface, implements
from behavior_tree_learning.core.sbt import BehaviorNodeFactory, StringBehaviorTree, ExecutionParameters
from behavior_tree_learning.core.gp_sbt.world_factory import WorldFactory
from behavior_tree_learning.core.gp_sbt.fitness_function import FitnessFunction


class Environment(Interface):

    def run_and_compute(self, individual, verbose):
        """
        Run the simulation and return the fitness

        Parameters:
            individual
            verbose (bool)
        Returns:
            fitness (float)
        """
        pass

    def plot_individual(self, path, plot_name, individual):
        """
        Saves a graphical representation of the individual

        Parameters:
            path (str) : where to store the figure
            plot_name (str) : name of the figure
            individual
        Returns:
            None
        """
        pass


class EnvironmentWithFitnessFunction(implements(Environment)):

    def __init__(self,
                 node_factory: BehaviorNodeFactory,
                 world_factory: WorldFactory,
                 fitness_function: FitnessFunction,
                 verbose=False):

        self._node_factory = node_factory
        self._world_factory = world_factory
        self._fitness_function = fitness_function
        self._verbose = verbose

    def run_and_compute(self, individual, verbose):

        verbose_enabled = self._verbose or verbose

        sbt = list(individual)
        if verbose_enabled:
            print("SBT: ", sbt)

        world = self._world_factory.make()

        tree = StringBehaviorTree(sbt, behaviors=self._node_factory, world=world, verbose=verbose)
        success, ticks = tree.run_bt(parameters=ExecutionParameters(successes_required=1))

        fitness = FitnessFunction().compute_cost(world, tree, ticks, self._targets,
                                                 self._fitness_coefficients, verbose=verbose)

        if verbose_enabled:
            print("fitness: ", fitness)

        return fitness

    def plot_individual(self, path, plot_name, individual):

        sbt = list(individual)
        tree = StringBehaviorTree(sbt[:], behaviors=self._node_factory)
        tree.save_figure(path, name=plot_name)
