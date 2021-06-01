from interface import Interface


class Environment(Interface):

    def run_and_compute(self, individual):
        pass

    def plot_individual(self, path, plot_name, individual):
        pass
