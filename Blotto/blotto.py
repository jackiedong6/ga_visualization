from random import choice, uniform, randint, sample
from itertools import combinations
import numpy as np

MUTATE_PROB = 0.2

class Blotto:
    def __init__(self, units, score_distribution):
        self.units = units
        self.score_distribution = score_distribution
        self.battle_fields = len(score_distribution)
        self.num_individuals = 256
        self.possible_distributions = self.partition_battle_field_units()
        self.target_distributions = self.generate_targets()
        self.population = self.generate_individuals()
        self.fitness = []

    def partition_battle_field_units(self):
        """Generate all possible field partitionings using stars & bars strategy"""
        partitions = []
        for c in combinations(range(self.units + self.battle_fields - 1), self.battle_fields - 1):
            partitions.append([b - a - 1 for a, b in zip((-1,) + c, c + (self.units + self.battle_fields - 1,))])
        return partitions

    def generate_individuals(self):
        """Generate n individuals, each with a random distribution of units"""
        return [choice(self.possible_distributions) for _ in range(self.num_individuals)]

    def generate_targets(self):
        return[choice(self.possible_distributions) for _ in range(self.num_individuals)]


    def play(self, individual_one, individual_two):
        """Plays a distribution of units against each other and returns the value for player 1 """
        p1_score, p2_score = 0, 0
        for p1, p2, weight in zip(individual_one, individual_two, self.score_distribution):
            if p1 > p2:
                p1_score += weight
            elif p1 == p2:
                p1_score += weight / 2
                p2_score += weight / 2
            else:
                p2_score += weight

        if p1_score > p2_score:
            return 1
        else:
            return 0.5

    def evaluate_fitness(self):
        """Plays an individual against all strategies in the target distribution;
        returns the number of wins"""
        self.fitness = []
        for individual in self.population:
            curr_fitness = 0
            for target in self.target_distributions:
                if individual == target:
                    continue
                curr_fitness += self.play(individual, target)
            
            # curr_fitness /= len(self.target_distributions)
            self.fitness.append(curr_fitness)
        return self.fitness

    def mutate(self, individual):
        """Mutates an individual's strategy with probability = MUTATE_PROB"""
        if uniform(0,1) < MUTATE_PROB:
            index = randint(0, self.battle_fields - 1)
            individual[index] = randint(0, self.units)
            individual_sum = sum(individual)
            if individual_sum > self.units:
                diff = individual_sum - self.units
                test = np.array(individual) - diff
                index = choice(np.where(test >= 0)[0])
                individual[index] -= diff
            

    def crossover(self):
        fitness = self.evaluate_fitness()
        
        probs = np.array(fitness)
        probs = np.exp(probs) / np.sum(np.exp(probs))
        children = []
        for i in range(int(self.num_individuals / 2)):
            parent_one = self.population[np.random.choice(range(self.num_individuals), 1, p=probs)[0]]
            parent_two = self.population[np.random.choice(range(self.num_individuals), 1, p=probs)[0]]

            # perform the crossover:
            child_one = [0] * self.battle_fields
            child_two = [0] * self.battle_fields
            for i in range(self.battle_fields):
                if randint(0, 1) == 0:
                    child_one[i] = parent_one[i]
                    child_two[i] = parent_two[i]
                else:
                    child_one[i] = parent_two[i]
                    child_two[i] = parent_one[i]
                    
                    
            child_one_sum = sum(child_one)
            child_two_sum = sum(child_two)

            if child_one_sum > self.units:
                diff = child_one_sum - self.units
                test = np.array(child_one) - diff
                index = choice(np.where(test >= 0)[0])
                child_one[index] -= diff
                
            if child_two_sum > self.units:
                diff = child_two_sum - self.units
                test = np.array(child_two) - diff
                index = choice(np.where(test >= 0)[0])
                child_two[index] -= diff


            self.mutate(child_one)
            self.mutate(child_two)
            children.append(child_one)
            children.append(child_two)
        self.population = children
        return fitness

