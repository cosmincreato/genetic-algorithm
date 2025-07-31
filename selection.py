from __future__ import annotations
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chromosome import Chromosome


def roulette_wheel(population: list[Chromosome], config: dict) -> Chromosome:
    fitness_values = [chrom.fitness for chrom in population]

    if config["maximize"] is True:
        min_fitness = min(fitness_values)
        if min_fitness < 0:
            shifted_fitness = [f - min_fitness + 0.001 for f in fitness_values]
        else:
            shifted_fitness = fitness_values
    else:
        max_fitness = max(fitness_values)
        shifted_fitness = [max_fitness - f + 0.001 for f in fitness_values]

    total_fitness = sum(shifted_fitness)

    val = random.uniform(0, 1)
    cumulative_prob = 0

    for i, chromosome in enumerate(population):
        cumulative_prob += shifted_fitness[i] / total_fitness
        if cumulative_prob >= val:
            return chromosome

    return population[-1]


def elitist_selection(elitist_count : int, config : dict, population : list[Chromosome]) -> list[Chromosome]:
    new_population : list[Chromosome] = []

    elitist_chromosomes : list[Chromosome] = sorted(population, key=lambda x: x.fitness, reverse=config["maximize"])[:elitist_count]
    new_population.extend(elitist_chromosomes)

    for i in range(config["population_size"] - elitist_count):
        new_population.append(roulette_wheel(population, config))

    return new_population