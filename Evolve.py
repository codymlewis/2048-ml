#!/usr/bin/env python3

import random
import numpy as np
import sys

import Autoplay


'''
Functions to perform evolutionary learning of 2048
'''


BASES = ["u", "d", "l", "r"]


def pool_play(genomes):
    '''Get the population of genomes to play the game'''
    return [Autoplay.convert_and_play(g) for g in genomes]


def crossover(a, b):
    '''Crossover two genomes'''
    min_len = min(len(a), len(b))
    result = a[:min_len]
    for i, gene in enumerate(b[:min_len]):
        if random.randint(1, 100) <= 50:
            result[i] = gene
    return result


def mutate(genome):
    '''Mutate a genome'''
    for i, gene in enumerate(genome):
        if random.randint(1, 100) < 30:
            genome[i] = random.choice(BASES)
    if random.randint(1, 100) < 25:
        genome.extend(random.choices(BASES, k=random.randint(1, 5)))
    return genome


def evolve(epochs, verbose=True):
    '''Perform an evolutionary algorithm'''
    population = [
        random.choices(BASES, k=random.randint(4, 20)) for _ in range(100)
    ]
    the_best = str()
    for epoch in range(epochs):
        fitnesses = pool_play(population)
        med = np.median(fitnesses)
        new_pop = []
        for i, fitness in enumerate(fitnesses):
            if fitness >= med:
                new_pop.append(population[i])
        for _ in range(50):
            new_pop.append(
                mutate(
                    crossover(random.choice(new_pop), random.choice(new_pop))
                )
            )
        max_index = np.argmax(fitnesses)
        the_best = str().join(population[max_index])
        if verbose:
            sys.stdout.write("\033[K")
            print(
                f"Epoch {epoch + 1}: " +
                f"genome {the_best} " +
                f"scored {fitnesses[max_index]}",
                end="\r"
            )
        population = new_pop
    return the_best


if __name__ == "__main__":
    NUM_EPOCHS = 100
    print("Evolving a strategy for 2048...")
    RESULT = evolve(NUM_EPOCHS)
    SCORE = Autoplay.play(RESULT, verbose=True)
    print(f"The best strategy found was {RESULT}")
    print(f"It scored {SCORE}")
