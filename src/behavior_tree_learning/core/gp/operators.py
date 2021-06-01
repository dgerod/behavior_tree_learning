from interface import Interface


class GeneticOperators(Interface):

    def random_genome(self, length):
        pass

    def mutate_gene(self, genome, p_add, p_delete):
        pass

    def crossover_genome(self, genome1, genome2, replace):
        pass
