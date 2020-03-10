# -*- coding: utf-8 -*-
"""
    pyeasyga module
"""

import random
import copy
from operator import attrgetter
import numpy as np
from time import gmtime, strftime
import matplotlib.pyplot as plt
from libs.get_random import get_rollet_wheel as rollet

from six.moves import range


class GeneticAlgorithm(object):
    """Genetic Algorithm class.
    This is the main class that controls the functionality of the Genetic
    Algorithm over 2 dim matrics.    
    """

    def __init__(self,
                 seed_data,
                 meta_data,
                 population_size=50,
                 generations=100,
                 crossover_probability=0.8,
                 mutation_probability=0.2,
                 elitism=True,
                 by_parent=False,
                 maximise_fitness=True,
                 initial_elit_prob=0.5,
                 initial_random_prob=0.5):       

        self.seed_data = seed_data
        self.meta_data = meta_data
        self.population_size = population_size
        self.generations = generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.elitism = elitism
        self.by_parent = by_parent
        self.maximise_fitness = maximise_fitness
        self.single_count = 0
        self.double_count = 0
        self.uniform_count = 0
        self.mutate_count = 0
        self.initial_elit_prob=initial_elit_prob,
        self.initial_random_prob = initial_random_prob

        self.current_generation = []
             
        
        def single_crossover(parent_1, parent_2):                       
            child_1, child_2 = parent_1, parent_2
            row, col = parent_1.shape
            for r in range(row):
                crossover_index = (random.randrange(1, col - 1))
                colt = crossover_index
                child_1.iloc[r] = np.append(parent_1.iloc[r, :colt],
                                            parent_2.iloc[r, colt:])    
                child_2.iloc[r] = np.append(parent_1.iloc[r , 
                                            colt:],parent_2.iloc[r, :colt])            
            return child_1, child_2
        
        def double_crossover(parent_1, parent_2):                       
            child_1, child_2 = parent_1, parent_2
            row, col = parent_1.shape
            for r in range(row):
                colt1 = (random.randrange(1, col - 1))
                colt2 = (random.randrange(colt1, col - 1))  
                 
                s1 = parent_2.iloc[r, :colt1]
                s1 = np.append(s1, parent_1.iloc[r, colt1:colt2])
                s1 = np.append(s1, parent_2.iloc[r, colt2:])
                child_1.iloc[r] = s1
                                            
                s2 = parent_1.iloc[r, :colt1]
                s2 = np.append(s2, parent_2.iloc[r, colt1:colt2])
                s2 = np.append(s2, parent_1.iloc[r, colt2:])
                child_2.iloc[r] = s1         
            return child_1, child_2
        
        def uniform_crossover(parent_1, parent_2):                       
            child_1, child_2 = parent_1, parent_2
            row, col = parent_1.shape
            for r in range(row):
                colt1 = (random.randrange(1, col - 1))   
                colt2 = (random.randrange(colt1, col - 1))
                colt3 = (random.randrange(colt2, col - 1))
                colt4 = (random.randrange(colt3, col - 1))
                colt5 = (random.randrange(colt4, col - 1))
                colt6 = (random.randrange(colt5, col - 1))
                colt7 = (random.randrange(colt6, col - 1))
                colt8 = (random.randrange(colt7, col - 1))
                colt9 = (random.randrange(colt8, col - 1))
                 
                s1= parent_2.iloc[r, :colt1]
                s1 = np.append(s1, parent_1.iloc[r, colt1:colt2])
                s1 = np.append(s1, parent_2.iloc[r, colt2:colt3])
                s1 = np.append(s1, parent_1.iloc[r, colt3:colt4])
                s1 = np.append(s1, parent_2.iloc[r, colt4:colt5])
                s1 = np.append(s1, parent_1.iloc[r, colt5:colt6])
                s1 = np.append(s1, parent_2.iloc[r, colt6:colt7])
                s1 = np.append(s1, parent_1.iloc[r, colt7:colt8])
                s1 = np.append(s1, parent_2.iloc[r, colt8:colt9])
                s1 = np.append(s1, parent_1.iloc[r, colt9:])
                child_1.iloc[r] = s1
                                               
                s2= parent_1.iloc[r, :colt1]
                s2 = np.append(s2, parent_2.iloc[r, colt1:colt2])
                s2 = np.append(s2, parent_1.iloc[r, colt2:colt3])
                s2 = np.append(s2, parent_2.iloc[r, colt3:colt4])
                s2 = np.append(s2, parent_1.iloc[r, colt4:colt5])
                s2 = np.append(s2, parent_2.iloc[r, colt5:colt6])
                s2 = np.append(s2, parent_1.iloc[r, colt6:colt7])
                s2 = np.append(s2, parent_2.iloc[r, colt7:colt8])
                s2 = np.append(s2, parent_1.iloc[r, colt8:colt9])
                s2 = np.append(s2, parent_2.iloc[r, colt9:])
                child_2.iloc[r] = s2
                
            return child_1, child_2

        def mutate(individual):
            parent = individual
            row , col = parent.shape
            shift_list = np.flip(meta_data.index.values.tolist())
            for r in range(row):
                mutate_index1 = random.randrange(1, col)
                mutate_index2 = random.randrange(1, col)                
                parent.iloc[r][mutate_index1] = np.random.choice(shift_list,
                                                 p=[0.0,0.0,0.0,
                                                    0.05,0.15,0.35,0.45],
                                                 size=1)
                parent.iloc[r][mutate_index2] = np.random.choice(shift_list,
                                                 p=[0.0,0.0,0.0,
                                                    0.05,0.15,0.35,0.45],
                                                 size=1)
        
        def create_individual(data,meta_data):  
            individual = data[:]
            shift_list = meta_data.index.values.tolist()
            for col in individual.columns :                  
                individual[col] = np.random.choice(shift_list,
                                                   size=len(individual))
            return individual
        
        def create_individual_local_search(data,meta_data):  
            individual = data[:]
            p = random.random()
            if p < 0.25:
                individual, _ = single_crossover(individual, individual)
            elif p < 0.5:
                individual, _ = double_crossover(individual, individual)
            elif p < 0.75:
                individual, _ = uniform_crossover(individual, individual)                
            else:
                mutate(individual)         
            return individual
        
        def random_selection(population):
            """Select and return a random member of the population."""
            return random.choice(population)
        
        def weighted_random_choice(population):
            max = sum(chromosome.fitness for chromosome in population)
            pick = random.uniform(0, max)
            current = 0
            for chromosome in population:
                current += chromosome.fitness
                if current > pick:
                    return chromosome

        def tournament_selection(population):
            """Select a random number of individuals from the population and
            return the fittest member of them all.
            """
            if self.tournament_size == 0:
                self.tournament_size = 2
            members = random.sample(population, self.tournament_size)
            members.sort(
                key=attrgetter('fitness'), reverse=self.maximise_fitness)
            return members[0]

        self.fitness_function = None
        self.tournament_selection = tournament_selection
        self.tournament_size = self.population_size // 10
        self.random_selection = random_selection
        self.create_individual = create_individual
        self.single_crossover_function = single_crossover
        self.double_crossover_function = double_crossover
        self.uniform_crossover_function = uniform_crossover
        self.mutate_function = mutate
        self.selection_function = self.tournament_selection        

    def create_initial_population(self):
        """Create members of the first population randomly.
        """
        initial_population = []
        individual = Chromosome(self.seed_data)
        parent = copy.deepcopy(individual)
               
        for i in range(self.population_size):
            genes = self.create_individual(self.seed_data,self.meta_data)                     
            individual = Chromosome(genes)                              
            individual.life_cycle = 1                                  
            self.single_count += 1
            initial_population.append(individual)
        
        if self.by_parent:
            initial_population[0] = parent
        self.current_generation = initial_population                  
        
        
    def calculate_population_fitness(self):
        """Calculate the fitness of every member of the given population using
        the supplied fitness_function.
        """
        for individual in self.current_generation:
            individual.set_fitness(self.fitness_function(individual.genes, 
                                                         self.meta_data)
                                  )

    def rank_population(self):
        """Sort the population by fitness according to the order defined by
        maximise_fitness.
        """
        self.current_generation.sort(
            key=attrgetter('fitness'), reverse=self.maximise_fitness)
        
        

    def create_new_population(self):
        """Create a new population using the genetic operators (selection,
        crossover, and mutation) supplied.
        """
        new_population = []
        elite = copy.deepcopy(self.current_generation[0])
        selection = self.selection_function

        while len(new_population) < self.population_size:
            parent_1 = copy.deepcopy(selection(self.current_generation))
            parent_2 = copy.deepcopy(selection(self.current_generation))

            child_1, child_2 = parent_1, parent_2
            child_1.parent_fitness, child_2.parent_fitness = (parent_1.fitness, 
                                                              parent_2.fitness)
            #-------------------- use tabu search ----------------------------#
            ''' if parent_1 or parent_2 use any opertator then these operators
                shoud not play for create child_1 and child_2.
                    << Tabu Search by last state of serach operation >>
            '''
            parent_single_cross_count = max(parent_1.single_cross_count,
                                            parent_2.single_cross_count)                
            parent_double_cross_count = max(parent_1.double_cross_count,
                                            parent_2.double_cross_count)
            parent_uniform_cross_count = max(parent_1.uniform_cross_count,
                                             parent_2.uniform_cross_count)
            parent_mutate_count = max(parent_1.mutate_count,
                                      parent_2.mutate_count)
            
            prob_single_cross  = int(parent_single_cross_count == 0)
            prob_double_cross  = int(parent_double_cross_count == 0)
            prob_uniform_cross = int(parent_uniform_cross_count == 0)
            prob_mutate        = int(parent_mutate_count == 0)
            sum_all_prob = (prob_single_cross+prob_double_cross+
                            prob_uniform_cross+prob_mutate)
#            sum_all_prob = 0.00001 if sum_all_prob==0 else sum_all_prob
            prob_single_cross  = prob_single_cross/sum_all_prob
            prob_double_cross  = prob_double_cross/sum_all_prob
            prob_uniform_cross = prob_uniform_cross/sum_all_prob
            prob_mutate        = prob_mutate/sum_all_prob
            #------------- rollet wheel -----------------#
            p = random.random()            
            cdf_prob_single_cross  =  prob_single_cross
            cdf_prob_double_cross  = (prob_single_cross + 
                                      prob_double_cross 
                                      if prob_double_cross else 0) 
            cdf_prob_uniform_cross = (prob_single_cross + 
                                      prob_double_cross + 
                                      prob_uniform_cross
                                      if prob_uniform_cross else 0) 
            cdf_prob_mutate        = (prob_single_cross + 
                                      prob_double_cross + 
                                      prob_uniform_cross+ 
                                      prob_mutate
                                      if prob_mutate else 0) 
            
            if p < cdf_prob_single_cross: 
                child_1.genes, child_2.genes = self.single_crossover_function(
                    parent_1.genes, parent_2.genes)
                child_1.set_init_count()
                child_2.set_init_count()
                child_1.single_cross_count, child_2.single_cross_count = 1, 1                           
                self.single_count += 1
#                print('single_crossover_function')
            elif p < cdf_prob_double_cross: 
                child_1.genes, child_2.genes = self.double_crossover_function(
                    parent_1.genes, parent_2.genes)          
                child_1.set_init_count()
                child_2.set_init_count()                
                child_1.double_cross_count, child_2.double_cross_count = 1, 1                
                self.double_count += 1
#                print('double_crossover_function')
            elif p < cdf_prob_uniform_cross:
                child_1.genes, child_2.genes = self.uniform_crossover_function(
                    parent_1.genes, parent_2.genes) 
                child_1.set_init_count()
                child_2.set_init_count()
                child_1.uniform_cross_count, child_2.uniform_cross_count = 1, 1                
                self.uniform_count += 1
#                print('uniform_crossover_function')
            else:
                self.mutate_function(child_1.genes)
                self.mutate_function(child_2.genes)
                child_1.set_init_count()
                child_2.set_init_count()
                child_1.mutate_count, child_2.mutate_count = 1, 1
                self.mutate_count += 1
#                print('mutate_function')
            #------------- ------------- -----------------#
            

            new_population.append(child_1)
            if len(new_population) < self.population_size:
                new_population.append(child_2)

        if self.elitism:
            new_population[0] = elite

        self.current_generation = new_population

    def create_first_generation(self):
        """Create the first population, calculate the population's fitness and
        rank the population by fitness according to the order specified.
        """
        self.create_initial_population()
        self.calculate_population_fitness()
        self.rank_population()

    def create_next_generation(self):
        """Create subsequent populations, calculate the population fitness and
        rank the population by fitness in the order specified.
        """
        self.create_new_population()
        self.calculate_population_fitness()
        self.rank_population()

    def run(self):
        """Run (solve) the Genetic Algorithm."""
        print('start: '+ strftime("%Y-%m-%d %H:%M:%S:%SS", gmtime()))
        self.create_first_generation()       
        for g in range(1, self.generations):
            print('---------- Start ---------------')            
            print('generation-' +str(g) + ' -> start: ')                        
            self.create_next_generation()  
            print('best cost: ' + str(self.current_generation[0].fitness))
            print('single_count:' +str(self.single_count))
            print('double_count:' +str(self.double_count))
            print('uniform_count:' +str(self.uniform_count))
            print('mutate_count:' +str(self.mutate_count))
        print('----------- End ----------------')
        print('end: '+ strftime("%Y-%m-%d %H:%M:%S:%SS", gmtime()))
    def best_individual(self):
        """Return the individual with the best fitness in the current
        generation.
        """
        best = self.current_generation[0]        
        return (best.fitness, best.genes)

    def last_generation(self):
        """Return members of the last generation as a generator function."""
        return ((member.fitness, member.genes) for member
                in self.current_generation)


class Chromosome(object):
    """ Chromosome class that encapsulates an individual's fitness and solution
    representation.
    """
    def __init__(self, genes):
        """Initialise the Chromosome."""
        self.genes = genes
        self.fitness = 0
        self.parent_fitness = 0
        self.life_cycle = 0
        self.fitness_const_count = 0
        self.single_cross_count = 0
        self.double_cross_count = 0
        self.uniform_cross_count = 0
        self.mutate_count = 0
        self.elit = 0

    def __repr__(self):
        """Return initialised Chromosome representation in human readable form.
        """
        return repr((self.fitness, self.genes))
    def set_fitness(self, fitness):
        self.life_cycle += 1
        #print('life_cycle:' + str(self.life_cycle))
        self.fitness = fitness
        if self.parent_fitness == self.fitness :
            self.fitness_const_count += 1
            #print('fitness_const_count:' + str(self.fitness_const_count))
    def set_init_count(self):
        self.single_cross_count = 0
        self.double_cross_count = 0
        self.uniform_cross_count = 0
        self.mutate_count = 0