# pylint: disable=global-at-module-level, too-many-instance-attributes
"""
A genetic programming algorithm with many possible settings
"""
import random
from statistics import mean
import numpy as np

from behavior_tree_learning.core.environment import GeneticEnvironment
from behavior_tree_learning.core.gp_sbt import gp_operators

from behavior_tree_learning.core.hash_table import HashTable
from behavior_tree_learning.core.logger import logplot
from behavior_tree_learning.core.gp.selection import SelectionMethods, selection

_operators = {'random_genome': gp_operators.random_genome,
              'crossover_genome': gp_operators.crossover_genome,
              'mutate_gene': gp_operators.mutate_gene }


def set_seeds(seed):
    """
    Sets random seeds for random number generators
    """

    random.seed(seed)
    np.random.seed(seed)


def set_operators(random_genome, crossover_genome, mutate_gene):

    global _operators
    _operators['random_genome'] = random_genome
    _operators['crossover_genome'] = crossover_genome
    _operators['mutate_gene'] = mutate_gene


def run(environment: GeneticEnvironment, gp_par, hotstart=False, baseline=None):
    """
    Runs the genetic programming algorithm
    """

    hash_table = HashTable(gp_par.hash_table_size, gp_par.log_name)

    if hotstart:
        best_fitness, n_episodes, last_generation, population = _load_state(gp_par.log_name, hash_table)
    else:
        population = _create_population(gp_par.n_population, gp_par.ind_start_length)
        logplot.clear_logs(gp_par.log_name)
        best_fitness = []
        n_episodes = []
        n_episodes.append(hash_table.n_values)
        last_generation = 0

        if baseline is not None:
            population[0] = baseline
            baseline_index = 0

    fitness = []
    for individual in population:
        fitness.append(_calculate_fitness(individual, hash_table, environment, rerun=0))

    if not hotstart:
        best_fitness.append(max(fitness))

        if gp_par.verbose:
            _print_population(population, fitness, last_generation)
            print("Generation: ", last_generation, " Best fitness: ", best_fitness[-1])

        logplot.log_fitness(gp_par.log_name, fitness)
        logplot.log_population(gp_par.log_name, population)

    generation = gp_par.n_generations - 1 #In case loop is skipped due to hotstart
    for generation in range(last_generation + 1, gp_par.n_generations):
        if gp_par.keep_baseline:
            if baseline is not None and not baseline in population:
                population.append(baseline) #Make sure we are always able to source from baseline

        if generation > 1:
            fitness = []
            for index, individual in enumerate(population):
                fitness.append(_calculate_fitness(individual, hash_table, environment, gp_par.rerun_fitness))
                if baseline is not None and individual == baseline:
                    baseline_index = index
        if gp_par.keep_baseline and gp_par.boost_baseline and baseline is not None:
            baseline_fitness = fitness[baseline_index]
            fitness[baseline_index] = max(fitness)

        co_parents = _crossover_parent_selection(population, fitness, gp_par)
        co_offspring = _crossover(population, co_parents, gp_par)
        for offspring in co_offspring:
            fitness.append(_calculate_fitness(offspring, hash_table, environment, gp_par.rerun_fitness))

        if gp_par.boost_baseline and gp_par.boost_baseline_only_co and baseline is not None:
            fitness[baseline_index] = baseline_fitness #Restore original fitness for survivor selection

        mutation_parents = _mutation_parent_selection(population, fitness, co_parents, co_offspring, gp_par)
        mutated_offspring = _mutation(population + co_offspring, mutation_parents, gp_par)
        for offspring in mutated_offspring:
            fitness.append(_calculate_fitness(offspring, hash_table, environment, gp_par.rerun_fitness))

        if gp_par.boost_baseline and baseline is not None:
            fitness[baseline_index] = baseline_fitness #Restore original fitness for survivor selection

        population, fitness = _survivor_selection(population, fitness, co_offspring, mutated_offspring, gp_par)

        best_fitness.append(max(fitness))
        n_episodes.append(hash_table.n_values)

        logplot.log_fitness(gp_par.log_name, fitness)
        logplot.log_population(gp_par.log_name, population)

        if gp_par.verbose:
            print("Generation: ", generation, "Fitness: ", fitness, "Best fitness: ", best_fitness[generation])

        if (generation + 1) % 25 == 0 and generation < gp_par.n_generations - 1: #Last generation will be saved later
            _save_state(gp_par, population, None, best_fitness, n_episodes, baseline, generation, hash_table)

    print("\nFINAL POPULATION: ")
    _print_population(population, fitness, generation)

    best_individual = selection(SelectionMethods.ELITISM, population, fitness, 1)[0]

    _save_state(gp_par, population, best_individual, best_fitness, n_episodes, baseline, generation, hash_table)

    if gp_par.plot:
        logplot.plot_fitness(gp_par.log_name, best_fitness, n_episodes)
    if gp_par.fig_best:
        environment.plot_individual(logplot.get_log_folder(gp_par.log_name), 'best individual', best_individual)
    if gp_par.fig_last_gen:
        for i in range(gp_par.n_population):
            environment.plot_individual(logplot.get_log_folder(gp_par.log_name), 'individual_' + str(i), population[i])

    return population, fitness, best_fitness, best_individual


def _create_population(population_size, genome_length):
    """
    Creates an initial random population
    """
    new_population = []
    max_attempts = 100

    for _ in range(population_size):
        individual = []
        attempts = 0

        while attempts < max_attempts:

            individual = _operators['random_genome'](genome_length)
            if individual != [] and individual not in new_population:
                new_population.append(individual)
                break
            attempts += 1

    return new_population


def _mutation(population, parents, gp_par):
    """
    Generate offspring by mutating a gene
    """
    mutated_population = []
    max_attempts = 100

    for parent in parents:
        for _ in range(gp_par.n_offspring_mutation):

            mutated_individual = []
            attempts = 0

            while attempts < max_attempts:

                mutated_individual = \
                    _operators['mutate_gene'](population[parent], gp_par.mutation_p_add, gp_par.mutation_p_delete)
                if len(mutated_individual) >= gp_par.min_length and \
                    (gp_par.allow_identical or (mutated_individual not in population + mutated_population)):
                    mutated_population.append(mutated_individual)
                    break
                attempts += 1

    return mutated_population


def _crossover(population, parents, gp_par):
    """
    Generates offspring by crossovers
    """

    if len(parents) % 2 != 0:
        raise ValueError("Number of parents for crossover must be even number")

    crossover_offspring = []
    max_attempts = 100

    for _ in range(gp_par.n_offspring_crossover):
        unused_parents = list(parents)
        attempts = 0

        while len(unused_parents) >= 2 and attempts < max_attempts:

            crossover_parents = random.sample(range(len(unused_parents)), 2)
            parent1 = unused_parents[int(crossover_parents[0])] 
            parent2 = unused_parents[int(crossover_parents[1])]

            offspring1, offspring2 = \
                _operators['crossover_genome'](population[parent1], population[parent2], gp_par.replace_crossover)
            if len(offspring1) >= gp_par.min_length and len(offspring2) >= gp_par.min_length and \
                (gp_par.allow_identical or
                 (offspring1 not in population + crossover_offspring and
                  offspring2 not in population + crossover_offspring)):
                crossover_offspring.append(offspring1)
                crossover_offspring.append(offspring2)
                unused_parents.pop(crossover_parents[0])
                if crossover_parents[0] < crossover_parents[1]:
                    crossover_parents[1] -= 1
                unused_parents.pop(crossover_parents[1])
                attempts = 0
            else:
                attempts += 1

        if attempts == max_attempts and len(unused_parents) > 0 and \
            gp_par.n_offspring_mutation <= 1 and gp_par.n_offspring_crossover <= 1:
            #Fill up with mutation in case we can't find enough good crossovers
            crossover_offspring += _mutation(population + crossover_offspring, unused_parents, gp_par)

    return crossover_offspring


def _rerun_probability(n_runs):
    """
    Calculates a probability for running another episode with the same
    genome.
    """
    if n_runs <= 0:
        return 1
    return 1 / n_runs**2


def _calculate_fitness(individual, hash_table, environment: GeneticEnvironment, rerun=0):
    """
    Gets fitness from hash table if possible, otherwise gets it from simulation
    rerun = 0 means never rerun
    rerun = 1 means rerun with diminishing probability
    rerun = 2 means rerun always
    """
    values = hash_table.find(individual)

    if values is None or rerun == 2 or (rerun == 1 and random.random() < _rerun_probability(len(values))):
        fitness = environment.run_and_compute(individual)
        hash_table.insert(individual, fitness)

        if values is None:
            values = [fitness]

    print(values)
    #new_values = list(map(int, values))
    return mean(values)


def _crossover_parent_selection(population, fitness, gp_par):
    """
    Select parents for crossover. Returns indices of parents.
    """
    n_parents_crossover = int(round(gp_par.f_crossover * gp_par.n_population))
    if n_parents_crossover <= 0:
        return []
    return selection(gp_par.parent_selection,range(len(population)), fitness, n_parents_crossover)


def _mutation_parent_selection(population, fitness, crossover_parents, crossover_offspring, gp_par):
    """
    Select parents for crossover
    Input fitness contains fitness for crossover offspring after fitness for the rest of the population
    Input population does not contain crossover offspring
    Returns indices of parents.
    """
    mutable_population = population[:]
    mutable_fitness = fitness[:]

    if not gp_par.mutate_co_parents:
        crossover_parents.sort(reverse=True)
        for i in crossover_parents:
            mutable_population.pop(i)
            mutable_fitness.pop(i)
    if gp_par.mutate_co_offspring:
        mutable_population += crossover_offspring
    else:
        mutable_fitness = mutable_fitness[:len(population)]

    n_parents_mutation = int(round(gp_par.f_mutation * gp_par.n_population))
    if n_parents_mutation <= 0:
        return []
    return selection(gp_par.parent_selection, range(len(mutable_population)), fitness, n_parents_mutation)


def _survivor_selection(population, fitness, crossover_offspring, mutated_offspring, gp_par):
    """
    Select survivors for next generation
    """
    selectable = []
    selectable_fitness = []
    survivors = []
    survivor_fitness = []

    #Pick out selectable parents using elitism.
    n_parents = int(round(gp_par.f_parents * gp_par.n_population))
    if n_parents > 0:
        parents = selection(SelectionMethods.ELITISM, range(len(population)), fitness[:len(population)], n_parents)
        for i in parents:
            selectable.append(population[i])
            selectable_fitness.append(fitness[i])

    #Add offspring
    selectable += crossover_offspring + mutated_offspring
    selectable_fitness += fitness[len(population):]

    #Pick out elites
    n_elites = int(round(gp_par.f_elites * gp_par.n_population))
    if n_elites > 0:
        elites = selection(SelectionMethods.ELITISM, range(len(selectable)), selectable_fitness, n_elites)
        elites.sort(reverse=True)
        for i in elites:
            survivors.append(selectable[i])
            survivor_fitness.append(selectable_fitness[i])
            selectable.pop(i)
            selectable_fitness.pop(i)

    n_to_select = gp_par.n_population - len(survivors)
    selected = selection(gp_par.survivor_selection, range(len(selectable)), selectable_fitness, n_to_select)

    for i in selected:
        survivors.append(selectable[i])
        survivor_fitness.append(selectable_fitness[i])

    return survivors, survivor_fitness


def _print_population(population, fitness, generation):
    """
    Prints information about a population
    """
    print("Generation: ", generation)
    for i in range(len(population)):
        print(population[i])
        print("Fitness: ", fitness[i])
    best = np.argmax(fitness)
    print("Best individual: ", best)
    print(population[best])


def _save_state(gp_par, population, best_individual, best_fitness, n_episodes, baseline, generation, hash_table):
    # pylint: disable=too-many-arguments
    """ Saves state for later hotstart """
    logplot.log_last_population(gp_par.log_name, population)
    if best_individual is not None:
        logplot.log_best_individual(gp_par.log_name, best_individual)
    logplot.log_best_fitness(gp_par.log_name, best_fitness)
    logplot.log_n_episodes(gp_par.log_name, n_episodes)
    logplot.log_settings(gp_par.log_name, gp_par, baseline)
    logplot.log_state(gp_par.log_name, random.getstate(), np.random.get_state(), generation)
    hash_table.write_table()


def _load_state(log_name, hash_table):
    """ Loads state for hotstart """
    population = logplot.get_last_population(log_name)
    best_fitness = logplot.get_best_fitness(log_name)
    n_episodes = logplot.get_n_episodes(log_name)
    randomstate, np_randomstate, generation = logplot.get_state(log_name)
    random.setstate(randomstate)
    np.random.set_state(np_randomstate)
    logplot.clear_after_generation(log_name, generation)
    hash_table.load()
    return best_fitness, n_episodes, generation, population
