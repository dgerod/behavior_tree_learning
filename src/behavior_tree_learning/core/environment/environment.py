from interface import Interface


class Environment(Interface):
    
    def set_random_events(self, random_events):
        pass

    def run_and_compute_fitness(self, individual):
        """ Run the simulation and return the fitness """
        pass

    def plot_individual(self, path, plot_name, individual):
        """ Saves a graphical representation of the individual """
        pass

    def add_to_static_tree(self, individual):
        """ Add invididual to the static part of the tree in the front """
        pass
