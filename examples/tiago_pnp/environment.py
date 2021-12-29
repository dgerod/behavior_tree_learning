from interface import implements
from behavior_tree_learning.sbt import BehaviorTreeExecutor, ExecutionParameters
from behavior_tree_learning.sbt import StringBehaviorTree, BehaviorNodeFactory
from behavior_tree_learning.gp import GeneticEnvironment
from tiago_pnp.world import WorldFactory
from tiago_pnp.fitness_function import FitnessFunction


class Environment(implements(GeneticEnvironment)):
    """
    Class defining the environment in which the individual operates
    """

    def __init__(self, node_factory: BehaviorNodeFactory, world_factory: WorldFactory,
                 scenario: str, verbose=False):

        if scenario != 'scenario_1' and scenario != 'scenario_3':
            raise ValueError('Unknown selected scenario')

        self._scenario = scenario
        self._world_factory = world_factory
        self._node_factory = node_factory
        self._verbose = verbose

    def run_and_compute(self, individual, verbose):
        """
        Run the simulation and return the fitness
        """

        sbt = individual
        verbose_enabled = self._verbose or verbose

        if verbose_enabled:
            print("SBT: ", sbt)

        if self._scenario == 'scenario_2':
            # in this case we run the same BT against the state machine in 3 different setups
            # every setup features a different spawn pose for the cube

            fitness = 0
            performance = 0

            for i in range(3):
                world = self._world_factory.make()
                behavior_tree = StringBehaviorTree(sbt[:], behaviors=self._node_factory, world=world,
                                                   verbose=verbose)
                _, ticks = behavior_tree.run_bt()

                cost, output = FitnessFunction().compute_cost(world, behavior_tree, ticks, verbose)

                fitness += -cost / 3.0
                performance += int(output)

            if performance == 3:
                completed = True
            else:
                completed = False

        elif self._scenario == 'scenario_1' or self._scenario == 'scenario_3':
            world = self._world_factory.make()
            behavior_tree = StringBehaviorTree(sbt[:], behaviors=self._node_factory, world=world,
                                               verbose=verbose)
            _, ticks = behavior_tree.run_bt()

            cost, completed = FitnessFunction().compute_cost(world, behavior_tree, ticks, verbose)
            fitness = -cost

        if verbose_enabled:
            print("fitness: ", fitness)

        return fitness

    def plot_individual(self, path, plot_name, individual):
        """ Saves a graphical representation of the individual """

        tree = StringBehaviorTree(individual[:], behaviors=self._node_factory)
        tree.save_figure(path, name=plot_name)
