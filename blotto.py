import sys
from random import choice, uniform, randint
from itertools import combinations
import numpy as np

class Blotto:

    NUM_STRATS = 3
    MUTATION_PROB = 0.1

    def __init__(self, units, score_distribution, n):
        self.units = units
        self.score_distribution = score_distribution
        self.n = n
        self.battle_fields = len(score_distribution)

        self.possible_distributions = self.partition_battle_field_units()

        # generate population of size n
        self.population = self.generate_individuals(self.n)

    def partition_battle_field_units(self):
        """Generate all possible field partitionings using stars & bars strategy"""
        partitions = []
        for c in combinations(range(self.units+self.battle_fields-1), self.battle_fields-1):
            partitions.append([b-a-1 for a, b in zip((-1,)+c, c+(self.units+self.battle_fields-1,))])
        return partitions

    def generate_individuals(self, n):
        """Generate n individuals, each with a mixed strategy made up of
        3 pure strategies, and return the individuals in an array"""
        
        indivs = []
        for i in range(n):
            individual = {}
            for j in range(Blotto.NUM_STRATS):
                weight = round(uniform(0, 1), 4)
                individual[weight] = choice(self.possible_distributions)
            indivs.append(individual)
        return indivs

    def print_population(self):
        # DELETE THIS LATER, just for debugging
        print(self.population)

    def play(self, individual_one, individual_two):
        p1_score, p2_score = 0, 0
        for p1, p2, weight in zip(individual_one, individual_two, self.score_distribution):
            if p1 > p2: #p1 wins
                p1_score += weight
            if p1 == p2: #draw
                p1_score += weight / 2
                p2_score += weight / 2
            else: #p2 wins
                p2_score += weight

        return p1_score, p2_score
    
    def eval_fitness(self):
        wins = [0]*self.n
        for p1 in range(self.n):
            for p2 in range(self.n):
                if self.population[p1] == self.population[p2]:
                    continue

                score1, score2 = self.play(self.population[p1], self.population[p2])
                wins[p1] += score1
                wins[p2] += score2

        for i in range(len(wins)):
            wins[i] /= self.n
        return wins

    def reproduce(self):
        fitness = self.eval_fitness()

        # convert to probabilities via softmax
        fitness = np.array(fitness)
        probs = np.exp(fitness) / np.sum(np.exp(fitness))

        new_population = []

        for i in range(self.n): # [question] does the parent survive?
            child = {}

            # get two parents
            p1 = np.random.choice(range(20), 1, p=probs)
            p2 = np.random.choice(range(20), 1, p=probs)
            while p2 == p1:
                p2 = np.random.choice(range(20), 1, p=probs)

            # CROSSOVER + MUTATION
            # for each strategy, randomly determine whether gene from parent 1 or parent 2
            for j in range(self.NUM_STRATS):
                # mutate with probability MUTATION_PROB
                if uniform(0, 1) <= self.MUTATION_PROB:
                    weight = round(uniform(0, 1), 4) # refactor ... ??? b/c copied from above
                    child[weight] = choice(self.possible_distributions)
                else:
                    if randint(1, 2) == 1:
                        # copy from player 1
                        child[p1.keys()[j]] = p1[p1.keys()[j]]
                    else:
                        # copy from player 2
                        child[p2.keys()[j]] = p2[p2.keys()[j]]
                
                # add child to new population


    def simulate(fields, points, units, n, time):
        """n = number of individuals in population, time =
        number of generations"""

        # randomly generate initial population
            # this involves generating random pure strategies and then mixing them randomly (probability) for mixed
        # population = new_population(n)

        # evaluate fitness scores
        fitness_scores = []
        # for i in population:
        #     fitness.append(fitness(i))

        # convert fitness scores to probabilities via softmax

        # crossover and mutate
        # crossover : already have the probabilities that each parent gets chosen; 
        # generate children (same number as parent)
        # for mutation, replace one of their pure strats (with some probability) with one picked from the pool of random ones

    def new_population(n):
        pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit()

    fields = int(sys.argv[1])
    score_distribution = []
    pos = 1
    for i in range(fields):
        pos += 1
        score_distribution.append(int(sys.argv[pos]))
    
    units = int(sys.argv[pos + 1])
    n = int(sys.argv[pos + 2])
    time = int(sys.argv[pos + 3])

    blotto = Blotto(units, score_distribution, n)
    # blotto.print_population()
    blotto.reproduce()