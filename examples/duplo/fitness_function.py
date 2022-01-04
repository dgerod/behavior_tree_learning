from dataclasses import dataclass
from duplo.world import ApplicationWorld


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

    def compute_cost(self, world: ApplicationWorld, behavior_tree, ticks, targets, coefficients=None, verbose=False):

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
