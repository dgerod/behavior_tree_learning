from interface import Interface, implements
from behavior_tree_learning.core.gp.steps import AlgorithmSteps


class GeneticEnvironment(Interface):

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


def make_steps(environment: GeneticEnvironment):

    class StepsForEnvironment(implements(AlgorithmSteps)):
        def __init__(self, environment_):
            self._environment = environment_

        def calculate_fitness(self, individual, verbose):
            return self._environment.run_and_compute(individual, verbose)

        def plot_individual(self, path, plot_name, individual):
            self._environment.plot_individual(path, plot_name, individual)

    return StepsForEnvironment(environment)
