from interface import implements
from behavior_tree_learning.core.gp import GeneticEnvironment
from behavior_tree_learning.core.gp import GeneticParameters
from behavior_tree_learning.core.gp import GeneticProgramming
from behavior_tree_learning.core.gp_sbt.environment import Environment
from behavior_tree_learning.core.gp_sbt.gp_operators \
    import Operators as GeneticOperatorsForSBT


class BehaviorTreeLearner:

    # __init__(BNF, environment)
    #   GPO_for_SBT(BNF) internally it creates ABN
    # Environment(cost_function, world)
    def __init__(self, environment: Environment):

        class EnvironmentAdapter(implements(GeneticEnvironment)):

            def __init__(self, environment_):
                self._environment = environment_

            def run_and_compute(self, individual, verbose):
                return self._environment.run_and_compute(individual, verbose)

            def plot_individual(self, path, plot_name, individual):
                self._environment.plot_individual(path, plot_name, individual)

        # GeneticOperatorsForStringBehaviorTree(ABN)
        self._gp_operators = GeneticOperatorsForSBT()
        self._environment_adapter = EnvironmentAdapter(environment)

    def run(self, parameters: GeneticParameters, seed=None, hot_start=False, base_line=None, verbose=False):

        gp = GeneticProgramming(self._gp_operators)
        gp.run(self._environment_adapter, parameters, seed, hot_start, base_line, verbose)

        return True
