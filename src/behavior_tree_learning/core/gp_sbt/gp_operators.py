import random
from interface import implements
from behavior_tree_learning.core.gp import GeneticOperators
from behavior_tree_learning.core.sbt import BehaviorTreeStringRepresentation


class Operators(implements(GeneticOperators)):

    def random_genome(self, length):
        """
        Returns a random genome
        """

        bt = BehaviorTreeStringRepresentation([])
        return bt.random(length)

    def mutate_gene(self, genome, p_add, p_delete):
        """
        Mutate only a single gene.
        """

        if p_add < 0 or p_delete < 0:
            raise Exception("Mutation parameters must not be negative.")

        if p_add + p_delete > 1:
            raise Exception("Sum of the mutation probabilities must be less than 1.")

        mutated_individual = BehaviorTreeStringRepresentation([])
        max_attempts = 100
        attempts = 0
        while (not mutated_individual.is_valid() or mutated_individual.bt == genome) and attempts < max_attempts:
            mutated_individual.set(genome)
            try:
                index = random.randint(0, len(genome) - 1)
            except:
                import pdb;
                pdb.set_trace()

            mutation = random.random()

            if mutation < p_delete:
                mutated_individual.delete_node(index)
            elif mutation < p_delete + p_add:
                mutated_individual.add_node(index)
            else:
                mutated_individual.change_node(index)

            mutated_individual.close()
            mutated_individual.trim()
            attempts += 1

        if attempts >= max_attempts and (not mutated_individual.is_valid() or mutated_individual.bt == genome):
            mutated_individual = BehaviorTreeStringRepresentation([])

        return mutated_individual.bt

    def crossover_genome(self, genome1, genome2, replace):
        """
        Do crossover between genomes at random points
        """

        bt1 = BehaviorTreeStringRepresentation(genome1)
        bt2 = BehaviorTreeStringRepresentation(genome2)
        offspring1 = BehaviorTreeStringRepresentation([])
        offspring2 = BehaviorTreeStringRepresentation([])

        if bt1.is_valid() and bt2.is_valid():
            max_attempts = 100
            attempts = 0
            found = False
            while not found and attempts < max_attempts:
                offspring1.set(bt1.bt)
                offspring2.set(bt2.bt)
                cop1 = -1
                cop2 = -1
                if len(genome1) == 1:
                    cop1 = 0  # Change whole tree
                else:
                    while not offspring1.is_subtree(cop1):
                        cop1 = random.randint(1, len(genome1) - 1)
                if len(genome2) == 1:
                    cop2 = 0  # Change whole tree
                else:
                    while not offspring2.is_subtree(cop2):
                        cop2 = random.randint(1, len(genome2) - 1)

                if replace:
                    offspring1.swap_subtrees(offspring2, cop1, cop2)
                else:
                    subtree1 = offspring1.get_subtree(cop1)
                    subtree2 = offspring2.get_subtree(cop2)
                    if len(genome1) == 1:
                        index1 = random.randint(0, 1)
                    else:
                        index1 = random.randint(1, len(genome1) - 1)
                    if len(genome2) == 1:
                        index2 = random.randint(0, 1)
                    else:
                        index2 = random.randint(1, len(genome2) - 1)
                    offspring1.insert_subtree(subtree2, index1)
                    offspring2.insert_subtree(subtree1, index2)

                attempts += 1
                if offspring1.is_valid() and offspring2.is_valid():
                    found = True
            if not found:
                offspring1.set([])
                offspring2.set([])

        return offspring1.bt, offspring2.bt
