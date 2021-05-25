from interface import Interface


class Environment(Interface):
    
    def set_random_events(self, random_events):
        pass

    def get_fitness(self, individual):
        pass

    def plot_individual(self, path, plot_name, individual):
        pass

    def add_to_static_tree(self, individual):
        pass
