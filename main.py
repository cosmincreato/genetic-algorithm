from __future__ import annotations
import utils
import population as pop
import selection
import crossover
import mutation
import visualizer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chromosome import Chromosome

config : dict = utils.read_input()
population : list[Chromosome] = pop.generate_population(config)
generations : list[list[Chromosome]] = [population]
current_generation : int = 1

while current_generation < config["generation_count"]:
    # Selection
    population = selection.elitist_selection(1, config, population)

    # Crossover
    crossover_list : list[int] = crossover.get_crossover_chromosomes_list(config, population)

    while len(crossover_list) > 1:
        first_i : int = crossover_list.pop(0)
        second_i : int = crossover_list.pop(0)
        population = crossover.crossover(config, population, first_i, second_i)

    # Mutation
    population = mutation.mutation(config, population)

    generations.append(population)
    current_generation += 1

delay : float = 0.2
visualizer.create_animated_plot(config, generations, delay)