from interface import Interface


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
