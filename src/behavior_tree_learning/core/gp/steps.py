import interface
from interface import Interface, implements


class AlgorithmSteps(Interface):

    @interface.default
    def execution_started(self):
        pass

    @interface.default
    def execute_generation(self, generation):
        pass

    @interface.default
    def current_population(self, population):
        pass

    @interface.default
    def crossover_population(self, population):
        pass

    @interface.default
    def mutated_population(self, population):
        pass

    @interface.default
    def survided_population(self, population):
        pass

    def calculate_fitness(self, individual, verbose):
        pass

    @interface.default
    def more_generations(self, generation, last_generation, fitness_achieved):
        pass

    @interface.default
    def plot_individual(self, path, plot_name, individual):
        pass

    @interface.default
    def execution_completed(self):
        pass
