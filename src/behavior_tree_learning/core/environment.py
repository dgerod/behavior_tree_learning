
class Environment():
    
    def set_random_events(self, random_events):
        return NotImplementedError

    def get_fitness(self, individual):
        return NotImplementedError

    def plot_individual(self, path, plot_name, individual):
        return NotImplementedError

    def add_to_static_tree(self, individual):
        return NotImplementedError
