from interface import Interface
from typing import Tuple
from behavior_tree_learning.core.str_bt import StringBehaviorTree


class GeneticOperations(Interface):

    def random_genome(self, length) -> StringBehaviorTree:
        pass

    def mutate_gene(self, genome, p_add, p_delete) -> StringBehaviorTree:
        pass

    def crossover_genome(self, genome1, genome2, replace) -> Tuple[StringBehaviorTree, StringBehaviorTree]:
        pass
