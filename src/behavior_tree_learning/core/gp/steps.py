import interface
from interface import Interface, implements


class AlgorithmSteps(Interface):

    @interface.default
    def notify_start(self):
        pass

    @interface.default
    def current_population(self, last_generation, population):
        pass

    def calculate_fitness(self, individual, verbose):
        pass

    def plot_individual(self, path, plot_name, individual):
        pass

    @interface.default
    def more_generations(self, generation, last_generation, error):
        pass
