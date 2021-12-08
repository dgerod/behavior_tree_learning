from dataclasses import dataclass
from interface import implements
from behavior_tree_learning.sbt import BehaviorTreeExecutor, ExecutionParameters
from behavior_tree_learning.sbt import StringBehaviorTree, BehaviorNodeFactory
from behavior_tree_learning.gp import GeneticEnvironment
from duplo_bt_run_example.world import WorldSimulator


@dataclass
class Coefficients:
    """
    Coefficients for tuning the cost function
    """
    task_completion: float = 1000.0
    pos_acc: float = 0.0004
    depth: float = 0.0
    length: float = 0.1
    ticks: float = 0.0
    failed: float = 50.0
    timeout: float = 10.0
    hand_not_empty: float = 0.0


class FitnessFunction:

    def compute_fitness(self, world: WorldSimulator, behavior_tree, ticks, targets, coefficients=None, verbose=False):

        if coefficients is None:
            coefficients = Coefficients()

        depth = behavior_tree.depth
        length = behavior_tree.length

        cost = (coefficients.length * length + coefficients.depth * depth +
                coefficients.ticks * ticks)

        if verbose:
            print("Cost from length:", cost)

        for i in range(len(targets)):
            cost += coefficients.task_completion * max(0, world.distance(i, targets[i]) - coefficients.pos_acc)
            if verbose:
                print("Cost:", cost)

        if behavior_tree.failed:
            cost += coefficients.failed
            if verbose:
                print("Failed: ", cost)
        if behavior_tree.timeout:
            cost += coefficients.timeout
            if verbose:
                print("Timed out: ", cost)
        if world.get_picked() is not None:
            cost += coefficients.hand_not_empty
            if verbose:
                print("Hand not empty: ", cost)

        fitness = -cost
        return fitness


class Environment(implements(GeneticEnvironment)):

    def __init__(self, node_factory: BehaviorNodeFactory, world: WorldSimulator,
                 target_positions,
                 static_tree=None, verbose=False, sm_pars=None, mode=0, fitness_coefficients=None):

        self._node_factory = node_factory
        self._world = world

        self._targets = target_positions
        self._static_tree = static_tree
        self._verbose = verbose
        self._sm_pars = sm_pars
        self._mode = mode
        self._fitness_coefficients = fitness_coefficients
        self._random_events = False

    def run_and_compute(self, individual):

        print('[Environment::run_and_compute] -- {')

        sbt = individual
        print("SBT: ", sbt)

        tree = StringBehaviorTree(sbt, behaviors=self._node_factory, world=self._world)
        success, ticks = tree.run_bt(parameters=ExecutionParameters(successes_required=1))

        fitness_value = FitnessFunction().compute_fitness(self._world, tree, ticks, self._targets,
                                                          self._fitness_coefficients, verbose=self._verbose)
        print("fitness: ", fitness_value)

        print('} --')
        return fitness_value

    def plot_individual(self, path, plot_name, individual):
        """ Saves a graphical representation of the individual """

        if self._static_tree is not None:
            tree = StringBehaviorTree(self._add_to_static_tree(individual), behaviors=self._node_factory)
        else:
            tree = StringBehaviorTree(individual[:], behaviors=self._node_factory)

        tree.save_figure(path, name=plot_name)

    def set_random_events(self, random_events):
        """ Sets the random events flag """
        import pdb; pdb.set_trace()
        self._random_events = random_events

    def _add_to_static_tree(self, individual):
        """ Add invididual to the static part of the tree in the front """

        new_individual = self._static_tree[:]
        new_individual[-2:-2] = individual
        return new_individual


class Environment1(Environment):
    """ Test class for only running first target in list  """

    def __init__(self, targets, static_tree, verbose=False):
        super().__init__(targets, static_tree, verbose)
        self._targets = [self._targets[0]]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))


class Environment12(Environment):
    """ Test class for only running first two targets in list  """

    def __init__(self, targets, static_tree, verbose=False):
        super().__init__(targets, static_tree, verbose)
        self._targets = self._targets[:2]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))


class Environment123(Environment):
    """ Test class for only running first three targets in list  """

    def __init__(self, targets, static_tree, verbose=False):
        super().__init__(targets, static_tree, verbose)
        self._targets = self._targets[:3]

    def get_fitness(self, individual):
        return super().get_fitness(self._add_to_static_tree(individual))
