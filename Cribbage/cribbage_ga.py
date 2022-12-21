#!/usr/bin/env pypy3
from .policy import CompositePolicy, RandomThrower, RandomPegger, GreedyThrower, GreedyPegger
from .cribbage import Game, evaluate_policies
from .my_policy import MyPolicy
from random import choice, uniform, randint, sample
import itertools
import numpy as np

MUTATE_PROB = 0.2
class Cribbage_GA:
    def __init__(self):
        self.game = game = Game()
        self.benchmark = CompositePolicy(game, GreedyThrower(game), GreedyPegger(game))
        self.games = 1000
        self.num_individuals = 16
        self.num_parameters = 3
        self.population = self.generate_individuals()


    def evaluate_fitness(self):
        self.fitness = []
        for individual in self.population:
            # print(individual)
            individual_policy = MyPolicy(self.game, individual)
            results = evaluate_policies(self.game, individual_policy,self.benchmark, self.games)
            # print(results)
            self.fitness.append(results[0])
            
    
        return self.fitness



    def generate_individuals(self):
        return [[round(uniform(0,4), 1), round(uniform(0,4), 1), round(uniform(0,4), 1)] for _ in range(self.num_individuals)]




    def mutate(self, individual):


        if uniform(0,1) < MUTATE_PROB:
            index = randint(0, self.num_parameters - 1)
            if randint(0,1):
                individual[index] -= 0.1

            else:
                individual[index] += 0.1



    def crossover(self):
        fitness = self.evaluate_fitness()

        probs = np.array(fitness)
        probs = np.exp(probs) / np.sum(np.exp(probs))

        children = []


        for i in range(int(self.num_individuals / 2)):
            parent_one = self.population[np.random.choice(range(self.num_individuals), 1, p=probs)[0]]
            parent_two = self.population[np.random.choice(range(self.num_individuals), 1, p=probs)[0]]

            child_one = [0] * self.num_parameters
            child_two = [0] * self.num_parameters



            for i in range(self.num_parameters):
                if randint(0, 1) == 0:
                    child_one[i] = parent_one[i]
                    child_two[i] = parent_two[i]
                else:
                    child_one[i] = parent_two[i]
                    child_two[i] = parent_one[i]


            self.mutate(child_one)
            self.mutate(child_two)

            children.append(child_one)
            children.append(child_two)

        self.population = children

        return fitness