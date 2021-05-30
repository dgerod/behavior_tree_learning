from interface import Interface


class GeneticEnvironment(Interface):

    def run_and_compute(self, individual):
        """ Run the simulation and return the fitness """
        pass

    def plot_individual(self, path, plot_name, individual):
        """ Saves a graphical representation of the individual """
        pass
