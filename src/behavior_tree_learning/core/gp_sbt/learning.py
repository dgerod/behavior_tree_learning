from interface import implements
from behavior_tree_learning.core.gp import GeneticEnvironment, make_steps
from behavior_tree_learning.core.gp import GeneticParameters, TraceConfiguration
from behavior_tree_learning.core.gp import AlgorithmSteps
from behavior_tree_learning.core.gp import GeneticProgramming
from behavior_tree_learning.core.gp_sbt.environment \
    import Environment, EnvironmentWithFitnessFunction
from behavior_tree_learning.core.gp_sbt.gp_operators \
    import Operators as GeneticOperatorsForSBT


class BehaviorTreeLearner:

    @staticmethod
    def from_environment(environment: Environment):

        bt = BehaviorTreeLearner()
        bt._gp_operators = GeneticOperatorsForSBT()
        bt._steps = make_steps(_EnvironmentAdapter(environment))
        return bt

    @staticmethod
    def from_steps(steps: AlgorithmSteps):

        bt = BehaviorTreeLearner()
        bt._gp_operators = GeneticOperatorsForSBT()
        bt._steps = steps
        return bt

    def __init__(self):
        self._gp_operators = None
        self._steps = None

    def run(self, parameters: GeneticParameters, seed=None, hot_start=False, base_line=None, verbose=False,
            outputs_dir_path="", trace_conf=TraceConfiguration()):

        if not self._gp_operators or not self._steps:
            raise RuntimeError("Object not created correctly, a factory method should be used")

        gp = GeneticProgramming(self._gp_operators, outputs_dir_path)
        gp.run(self._steps, parameters, seed, hot_start, base_line, trace_conf=trace_conf, verbose=verbose)

        return True


class _EnvironmentAdapter(implements(GeneticEnvironment)):

    def __init__(self, environment_):
        self._environment = environment_

    def run_and_compute(self, individual, verbose):
        return self._environment.run_and_compute(individual, verbose)

    def plot_individual(self, path, plot_name, individual):
        self._environment.plot_individual(path, plot_name, individual)
