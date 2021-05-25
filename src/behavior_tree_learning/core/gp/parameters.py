from dataclasses import dataclass
from behavior_tree_learning.core.gp.selection import SelectionMethods


@dataclass
class GeneticParameters:
    """ Data class for parameters for the GP algorithm """

    ind_start_length: int = 5                              #Start length of initial genomes
    min_length: int = 2                                    #Minimum length of individual
    n_population: int = 8                                  #Number of individuals in population
    f_crossover: float = 0.5                               #Fraction of parent pool selected for crossover
    n_offspring_crossover: int = 1                         #Number of offspring from crossover per parent
    replace_crossover: bool = False                        #Crossover replaces subtree at receiving genome or inserts
    f_mutation: float = 0.5                                #Fraction of parent pool selected for mutation
    n_offspring_mutation: int = 1                          #Number of offspring from mutation per parent
    parent_selection: int = SelectionMethods.TOURNAMENT    #Selection method for parents
    survivor_selection: int = SelectionMethods.TOURNAMENT  #Selection method for survival
    f_elites: float = 0.1                                  #Fraction of population that survive as elites
    f_parents: float = 1                                   #Fraction of parents that may survive to next generation
    mutate_co_offspring: bool = False                      #Offspring from crossover may also be mutated
    mutate_co_parents: bool = False                        #Parents for crossover may also be mutated
    mutation_p_add: float = 0.4                            #Probability of mutation adding a gene
    mutation_p_delete: float = 0.3                         #Probability of mutation deleting a gene
    allow_identical: bool = False                          #Offspring may be identical to any parent in prev generation
    keep_baseline: bool = True                             #Baseline, if any, is always kept in population for breeding
    boost_baseline: bool = False                           #Baseline is boosted to have higher probability of breeding
    boost_baseline_only_co: bool = True                    #Baseline is boosted for crossover selection, not mutation
    plot: bool = True                                      #Plot fitness
    n_generations: int = 100                               #Number of generations
    hash_table_size: int = 100000                          #Size of hash table
    rerun_fitness: int = 0                                 #0-run only once, 1-according to prob, 2-always
    verbose: bool = False                                  #Extra prints
    log_name: str = '1'                                    #Name of log for folder and file handling
    fig_best: bool = True                                  #Save final best individual as figure
    fig_last_gen: bool = False                             #Save figures of entire last generation
