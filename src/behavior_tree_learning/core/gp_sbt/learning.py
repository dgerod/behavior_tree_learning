from interface import implements
from behavior_tree_learning.core.gp import GeneticEnvironment
from behavior_tree_learning.core.gp import GeneticParameters
from behavior_tree_learning.core.gp import GeneticProgramming
from behavior_tree_learning.core.sbt import behavior_tree as sbt
from behavior_tree_learning.core.gp_sbt.environment import Environment
from behavior_tree_learning.core.gp_sbt.gp_operators import Operators as GeneticOperatorsForStringBehaviorTree


class BehaviorTreeLearner:

    def __init__(self, settings_file):

        self._gp_operators = GeneticOperatorsForStringBehaviorTree()
        sbt.load_settings_from_file(settings_file)

    def execute(self, environment: Environment, parameters: GeneticParameters, 
                hot_start=False, base_line=None):

        class EnvironmentAdapter(implements(GeneticEnvironment)):

            def __init__(self, environment_):
                self._environment = environment_

            def run_and_compute(self, individual):
                raise NotImplementedError

            def plot_individual(self, path, plot_name, individual):
                raise NotImplementedError

        environment_adapter = EnvironmentAdapter(environment)
        gp_algorithm = GeneticProgramming(self._gp_operators)
        gp_algorithm.run(environment_adapter, parameters, hot_start, base_line)
