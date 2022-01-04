from interface import Interface


class GeneticOperators(Interface):

    def random_genome(self, length):
        """
        Generate one genome

        Parameters:
            length (int) : length of the genome
        Returns:
            genome
        """
        pass

    def mutate_gene(self, genome, p_add, p_delete):
        """
        Mutate only a single gene.

        Parameters:
            genome
            p_add (int) : mutate parameter
            p_delete (int) : mutate parameter
        Returns:
            genome
        """
        pass

    def crossover_genome(self, genome1, genome2, replace):
        """
        Do crossover between genomes at random points

        Parameters:
            genome1
            genome2
            replace (bool)
        Returns:
            genome1
            genome2
        """
        pass
