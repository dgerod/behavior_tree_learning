from dataclasses import dataclass

@dataclass
class Coefficients:
    """
    Coefficients for tuning the cost function
    """
    depth: int = 0
    length: int = 1
    task_completion: int = 10


def compute_fitness(world, sbt):
    """ Retrieve values and compute cost """

    coeff = Coefficients()

    depth = sbt.depth
    length = sbt.length

    cost = coeff.length * length + \
           coeff.depth * depth

    for state in world.state:
        if state:
            cost += coeff.task_completion * -1

    fitness = -cost
    return fitness