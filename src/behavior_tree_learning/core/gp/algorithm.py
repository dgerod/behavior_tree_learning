import logging
import os
import random
from statistics import mean
import numpy as np

from behavior_tree_learning.core.logger import logplot
from behavior_tree_learning.core.gp.hash_table import HashTable
from behavior_tree_learning.core.gp.parameters import GeneticParameters
from behavior_tree_learning.core.gp.environment import GeneticEnvironment
from behavior_tree_learning.core.gp.selection import SelectionMethods, selection
from behavior_tree_learning.core.gp.operators import GeneticOperators


class GeneticProgramming:

    def __init__(self, operators: GeneticOperators):

        self._operators = operators
        self._verbose = False
        self._logger = logging.getLogger("gp")

    def run(self, environment: GeneticEnvironment, parameters: GeneticParameters,
            seed=None, hot_start=False, base_line=None, verbose=False):

        self._initialize_random_generator(seed)
        self._verbose = verbose
        return self._run(environment, parameters, hot_start, base_line)

    @staticmethod
    def _initialize_random_generator(seed):

        if seed:
            random.seed(seed)
            np.random.seed(seed)

    def _run(self, environment: GeneticEnvironment, parameters: GeneticParameters, hot_start=False, base_line=None):

        self._logger.debug('[run] BEGIN')

        hash_table = HashTable(parameters.hash_table_size,
                               os.path.join(logplot.get_log_folder(parameters.log_name)))

        # Original population
        # --------------------------------------------------

        if hot_start:
            best_fitness, num_episodes, last_generation, population = self._load_state(parameters.log_name, hash_table)
        else:
            population = self._create_random_population(parameters.n_population, parameters.ind_start_length)
            logplot.clear_logs(parameters.log_name)
            best_fitness = []
            num_episodes = [hash_table.num_values()]
            last_generation = 0

            if base_line is not None:
                population[0] = base_line
                baseline_index = 0

        # Select best candidate
        # --------------------------------------------------

        fitness = []
        for individual in population:
            fitness.append(self._calculate_fitness(individual, hash_table, environment, rerun=0))

        if not hot_start:
            best_fitness.append(max(fitness))
            logplot.log_fitness(parameters.log_name, fitness)
            logplot.log_population(parameters.log_name, population)

        self._print_message("=== Generation: %d ===" % last_generation)
        self._print_population("Population", population, fitness)
        self._print_best_individual(population, fitness)

        # Produce next generations
        # --------------------------------------------------

        generation = parameters.n_generations - 1  # In case loop is skipped due to hot-start
        for generation in range(last_generation + 1, parameters.n_generations):

            self._print_message("=== Generation: %d/%d ===" % (generation, parameters.n_generations))
            self._print_population("Population", population, fitness)
            self._print_best_individual(population, fitness)

            if parameters.keep_baseline:
                if base_line is not None and base_line not in population:
                    # Make sure we are always able to source from baseline
                    population.append(base_line)

            if generation > 1:
                fitness = []
                for index, individual in enumerate(population):
                    fitness.append(self._calculate_fitness(individual, hash_table, environment, parameters.rerun_fitness))
                    if base_line is not None and individual == base_line:
                        baseline_index = index

            if parameters.keep_baseline and parameters.boost_baseline and base_line is not None:
                baseline_fitness = fitness[baseline_index]
                fitness[baseline_index] = max(fitness)

            crossover_parents = self._crossover_parent_selection(population, fitness, parameters)
            crossover_offspring = self._crossover(population, crossover_parents, parameters)
            for offspring in crossover_offspring:
                fitness.append(self._calculate_fitness(offspring, hash_table, environment,
                                                       parameters.rerun_fitness))
            self._print_offspring("Crossover", crossover_parents, crossover_offspring)

            if parameters.boost_baseline and parameters.boost_baseline_only_co and base_line is not None:
                # Restore original fitness for survivor selection
                fitness[baseline_index] = baseline_fitness

            mutation_parents = self._mutation_parent_selection(population, fitness,
                                                               crossover_parents, crossover_offspring, parameters)
            mutated_offspring = self._mutation(population + crossover_offspring, mutation_parents,
                                               parameters)
            for offspring in mutated_offspring:
                fitness.append(self._calculate_fitness(offspring, hash_table, environment,
                                                       parameters.rerun_fitness))
            self._print_offspring("Mutation", mutation_parents, mutated_offspring)

            if parameters.boost_baseline and base_line is not None:
                # Restore original fitness for survivor selection
                fitness[baseline_index] = baseline_fitness

            population, fitness = self._survivor_selection(population, fitness,
                                                           crossover_offspring, mutated_offspring, parameters)
            best_fitness.append(max(fitness))
            num_episodes.append(hash_table.num_values())

            self._print_population("Survivors", population, fitness)
            self._print_message("Best fitness: %f" % best_fitness[-1])
            self._print_message("Num episodes: %s" % num_episodes[-1])
            self._print_best_individual(population, fitness)

            logplot.log_fitness(parameters.log_name, fitness)
            logplot.log_population(parameters.log_name, population)

            if (generation + 1) % 25 == 0 and generation < parameters.n_generations - 1:
                # Save state every 25 generations but not the last one as it is saved later
                self._save_state(parameters, population, None, best_fitness, num_episodes, base_line, generation,
                                 hash_table)

        # Prepare results
        # --------------------------------------------------

        best_individual = selection(SelectionMethods.ELITISM, population, fitness, 1, self._verbose)[0]
        self._save_state(parameters, population, best_individual, best_fitness, num_episodes, base_line, generation,
                         hash_table)

        self._print_population("Final population", population, fitness)
        self._print_best_individual(population, fitness)
        self._print_verbose_message("Best individual: %s" % best_individual)

        self._plot_results(parameters, environment, population, num_episodes, best_fitness, best_individual)

        self._logger.debug('[run] END')
        return population, fitness, best_fitness, best_individual

    def _create_random_population(self, population_size, genome_length):

        self._print_verbose_message("Create random population")
        self._print_verbose_message("   Requested population: %d" % population_size)
        self._print_verbose_message("   Genome length: %d" % genome_length)

        new_population = []
        max_attempts = 100

        for _ in range(population_size):
            attempts = 0
            while attempts < max_attempts:
                individual = self._operators.random_genome(genome_length)
                if individual != [] and individual not in new_population:
                    new_population.append(individual)
                    break
                attempts += 1

        return new_population

    def _mutation(self, population, parents, parameters):
        """
        Generate offspring by mutating a gene
        """

        mutated_population = []
        max_attempts = 100

        for parent in parents:
            for _ in range(parameters.n_offspring_mutation):

                attempts = 0
                while attempts < max_attempts:

                    mutated_individual = self._operators.mutate_gene(population[parent],
                                                                     parameters.mutation_p_add,
                                                                     parameters.mutation_p_delete)

                    if (len(mutated_individual) >= parameters.min_length
                            and (parameters.allow_identical
                                 or (mutated_individual not in population + mutated_population))):
                        mutated_population.append(mutated_individual)
                        break
                    attempts += 1

        return mutated_population

    def _crossover(self, population, parents, parameters):
        """
        Generates offspring by crossovers two genes
        """

        if len(parents) % 2 != 0:
            raise ValueError("Number of parents for crossover must be even number")

        crossover_offspring = []
        max_attempts = 100

        for _ in range(parameters.n_offspring_crossover):
            unused_parents = list(parents)
            attempts = 0

            while len(unused_parents) >= 2 and attempts < max_attempts:

                crossover_parents = random.sample(range(len(unused_parents)), 2)
                parent1 = unused_parents[int(crossover_parents[0])]
                parent2 = unused_parents[int(crossover_parents[1])]

                offspring1, offspring2 = self._operators.crossover_genome(population[parent1],
                                                                          population[parent2],
                                                                          parameters.replace_crossover)

                if (len(offspring1) >= parameters.min_length and len(offspring2) >= parameters.min_length
                        and (parameters.allow_identical
                             or (offspring1 not in population + crossover_offspring and
                                 offspring2 not in population + crossover_offspring))):
                    crossover_offspring.append(offspring1)
                    crossover_offspring.append(offspring2)
                    unused_parents.pop(crossover_parents[0])
                    if crossover_parents[0] < crossover_parents[1]:
                        crossover_parents[1] -= 1
                    unused_parents.pop(crossover_parents[1])
                    attempts = 0
                else:
                    attempts += 1

            if (attempts == max_attempts and len(unused_parents) > 0
                    and parameters.n_offspring_mutation <= 1 and parameters.n_offspring_crossover <= 1):
                # Fill up with mutation in case we can't find enough good crossovers
                crossover_offspring += self._mutation(population + crossover_offspring, unused_parents, parameters)

        return crossover_offspring

    def _rerun_probability(self, num_runs):
        """
        Calculates a probability for running another episode with the same
        genome.
        """

        if num_runs <= 0:
            return 1
        return 1 / num_runs ** 2

    def _calculate_fitness(self, individual, hash_table, environment: GeneticEnvironment, rerun=0):
        """
        Gets fitness from hash table if possible, otherwise gets it from simulation
        rerun = 0 means never rerun
        rerun = 1 means rerun with diminishing probability
        rerun = 2 means rerun always
        """

        values = hash_table.find(individual)

        if values is None or rerun == 2 or (rerun == 1 and random.random() < self._rerun_probability(len(values))):
            fitness = environment.run_and_compute(individual, self._verbose)
            hash_table.insert(individual, fitness)

            if values is None:
                values = [fitness]

        if self._verbose:
            print('Calculated fitness: ', values)

        return mean(values)

    def _crossover_parent_selection(self, population, fitness, parameters):
        """
        Select parents for crossover. Returns indices of parents.
        """

        num_parents_crossover = int(round(parameters.f_crossover * parameters.n_population))
        if num_parents_crossover <= 0:
            return []
        return selection(parameters.parent_selection, range(len(population)), fitness, num_parents_crossover,
                         self._verbose)

    def _mutation_parent_selection(self, population, fitness, crossover_parents, crossover_offspring, parameters):
        """
        Select parents for crossover
        Input fitness contains fitness for crossover offspring after fitness for the rest of the population
        Input population does not contain crossover offspring
        Returns indices of parents.
        """

        mutable_population = population[:]
        mutable_fitness = fitness[:]

        if not parameters.mutate_co_parents:
            crossover_parents.sort(reverse=True)
            for i in crossover_parents:
                mutable_population.pop(i)
                mutable_fitness.pop(i)

        if parameters.mutate_co_offspring:
            mutable_population += crossover_offspring
        else:
            mutable_fitness = mutable_fitness[:len(population)]

        num_parents_mutation = int(round(parameters.f_mutation * parameters.n_population))
        if num_parents_mutation <= 0:
            return []
        return selection(parameters.parent_selection, range(len(mutable_population)), fitness, num_parents_mutation,
                         self._verbose)

    def _survivor_selection(self, population, fitness, crossover_offspring, mutated_offspring, parameters):

        selectable = []
        selectable_fitness = []
        survivors = []
        survivor_fitness = []

        # Pick out selectable parents using elitism.
        num_parents = int(round(parameters.f_parents * parameters.n_population))
        if num_parents > 0:
            parents = selection(SelectionMethods.ELITISM, range(len(population)), fitness[:len(population)], num_parents,
                                self._verbose)
            for i in parents:
                selectable.append(population[i])
                selectable_fitness.append(fitness[i])

        # Add offspring
        selectable += crossover_offspring + mutated_offspring
        selectable_fitness += fitness[len(population):]

        # Pick out elites
        num_elites = int(round(parameters.f_elites * parameters.n_population))
        if num_elites > 0:
            elites = selection(SelectionMethods.ELITISM, range(len(selectable)), selectable_fitness, num_elites,
                               self._verbose)
            elites.sort(reverse=True)
            for i in elites:
                survivors.append(selectable[i])
                survivor_fitness.append(selectable_fitness[i])
                selectable.pop(i)
                selectable_fitness.pop(i)

        num_to_select = parameters.n_population - len(survivors)
        selected = selection(parameters.survivor_selection, range(len(selectable)), selectable_fitness, num_to_select,
                             self._verbose)

        for i in selected:
            survivors.append(selectable[i])
            survivor_fitness.append(selectable_fitness[i])

        return survivors, survivor_fitness

    def _save_state(self, parameters, population, best_individual, best_fitness, n_episodes, base_line, generation,
                    hash_table):
        """
        Saves state for later hot-start
        """

        logplot.log_last_population(parameters.log_name, population)
        if best_individual is not None:
            logplot.log_best_individual(parameters.log_name, best_individual)
        logplot.log_best_fitness(parameters.log_name, best_fitness)
        logplot.log_n_episodes(parameters.log_name, n_episodes)
        logplot.log_settings(parameters.log_name, parameters, base_line)
        logplot.log_state(parameters.log_name, random.getstate(), np.random.get_state(), generation)
        hash_table.write()

    def _load_state(self, log_name, hash_table):
        """
        Loads state for hot-start
        """

        population = logplot.get_last_population(log_name)
        best_fitness = logplot.get_best_fitness(log_name)
        n_episodes = logplot.get_n_episodes(log_name)
        randomstate, np_randomstate, generation = logplot.get_state(log_name)
        random.setstate(randomstate)
        np.random.set_state(np_randomstate)
        logplot.clear_after_generation(log_name, generation)
        hash_table.load()
        return best_fitness, n_episodes, generation, population

    def _plot_results(self, parameters, environment, population, num_episodes, best_fitness, best_individual):

        if parameters.plot_fitness:
            logplot.plot_fitness(parameters.log_name, best_fitness, num_episodes)
        if parameters.plot_best_individual:
            environment.plot_individual(logplot.get_log_folder(parameters.log_name), 'best individual', best_individual)
        if parameters.plot_last_generation:
            for i in range(parameters.n_population):
                environment.plot_individual(logplot.get_log_folder(parameters.log_name), 'individual_' + str(i),
                                            population[i])

    def _print_verbose_message(self, message, *args):

        if self._verbose:
            print(message % args)
        self._logger.debug(message % args)

    def _print_message(self, message, *args):

        print(message % args)
        self._logger.info(message % args)

    def _print_population(self, title, population, fitness):

        self._print_verbose_message(title)
        for i in range(len(population)):
            self._print_verbose_message("   (%d) Genome: %s" % (i, population[i]))
            self._print_verbose_message("        Fitness: %f" % fitness[i])

    def _print_best_individual(self, population, fitness):

        best = np.argmax(fitness)
        self._print_verbose_message("Best individual: %d" % best)
        self._print_verbose_message("   Genome: %s" % population[best])
        self._print_verbose_message("   Fitness: %f" % fitness[best])
        self._print_verbose_message("Fitness average: %f, std dev: %f" % (np.average(fitness), np.std(fitness)))

    def _print_offspring(self, title, parents, offspring):

        self._logger.debug(title)
        self._logger.debug("   Parents: %s", parents)
        for i in range(len(offspring)):
            self._logger.debug("   (%d) Offspring: %s" % (i, offspring[i]))
