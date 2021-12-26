from enum import Enum, auto
import random
import numpy as np


def _elite_selection(population, fitness, n_elites, verbose):
    """
    Elite selection from population
    """

    sorted_population = sorted(zip(fitness, population), reverse=True)
    selected = [x for _, x in sorted_population[:n_elites]]

    if verbose:
        print('Elite selection - population: %d, num selected: %d' % (len(population), n_elites))
        print('Sorted: population:')
        for fitness, genome in sorted_population:
            print('fitness: %f, genome: %s' % (fitness, genome))

    return selected


def _tournament_selection(population, fitness, n_winners, verbose):
    """
    Tournament selection.
    """

    tournament_size = n_winners
    while tournament_size < len(population):
        tournament_size *= 2

    tournament_population = list(zip(fitness, population))
    random.shuffle(tournament_population)

    for i in range(tournament_size - len(population)):
        # Add dummies to make sure we have a full tournament
        tournament_population.insert(i * 2, (-float("inf"), []))

    winner_fitness, winners = [list(x) for x in zip(*tournament_population)]
    while len(winners) > n_winners:
        for i in range(0, int(len(winners) / 2)):
            if winner_fitness[i] < winner_fitness[i+1]:
                winner_fitness.pop(i)
                winners.pop(i)
            else:
                winner_fitness.pop(i + 1)
                winners.pop(i + 1)

    return winners


def _rank_selection(population, fitness, n_selected, verbose):
    """
    Rank proportional selection
    Probabilities for each individual are scaled linearly according to rank
    such that the highest ranked individual get n_ranks as weight
    and the lowest ranked individual gets 1. The weights are then scaled so
    that they sum to 1.
    """

    sorted_population = sorted(zip(fitness, population), reverse=True)
    _, sorted_indices = [list(x) for x in zip(*sorted_population)]
    n_ranks = len(sorted_indices)
    p = np.linspace(2 / (n_ranks + 1), 2 / (n_ranks * (n_ranks + 1)), n_ranks)
    return list(np.random.choice(sorted_indices, size=n_selected, replace=False, p=p))


def _random_selection(population, n_selected, verbose):
    return random.sample(population, n_selected)


class SelectionMethods(Enum):
    """
    Enum class for selection methods
    """

    ELITISM = auto()
    TOURNAMENT = auto()
    RANK = auto()
    RANDOM = auto()
    ALL = auto()


def selection(selection_method, population, fitness, n_selected, verbose=False):
    """
    Select individuals from population
    """

    if selection_method == SelectionMethods.ELITISM:
        selected = _elite_selection(population, fitness, n_selected, verbose)
    elif selection_method == SelectionMethods.TOURNAMENT:
        selected = _tournament_selection(population, fitness, n_selected, verbose)
    elif selection_method == SelectionMethods.RANK:
        selected = _rank_selection(population, fitness, n_selected, verbose)
    elif selection_method == SelectionMethods.RANDOM:
        selected = _random_selection(population, n_selected, verbose)
    elif selection_method == SelectionMethods.ALL:
        selected = population
    else:
        raise Exception('Invalid selection method')

    return selected
