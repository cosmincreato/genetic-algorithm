import random
import chromosome as chrm

def get_crossover_chromosomes_list(config : dict, population : list[chrm.Chromosome]) -> list[int]:
    crossover_list = []
    for i in range(len(population)):
        u = random.uniform(0, 1)
        if u < config["crossover_probability"]:
            crossover_list.append(i)

    return crossover_list


def crossover(config : dict, population : list[chrm.Chromosome], first_i : int, second_i : int) -> list[chrm.Chromosome]:

    new_population : list[chrm.Chromosome] = population.copy()

    first_parent : chrm.Chromosome = new_population[first_i]
    second_parent : chrm.Chromosome = new_population[second_i]
    point : int = random.randint(0, chrm.Chromosome.binary_length)

    # Perform crossover
    first_child_binary : str = first_parent.binary[:point]  + second_parent.binary[point:]
    second_child_binary : str = second_parent.binary[:point]  + first_parent.binary[point:]

    # Create new chromosomes
    first_child_decimal : float = chrm.get_decimal(first_child_binary, config)
    first_child_fitness : float = chrm.get_fitness(first_child_decimal, config)

    second_child_decimal : float = chrm.get_decimal(second_child_binary, config)
    second_child_fitness : float = chrm.get_fitness(second_child_decimal, config)

    first_child : chrm.Chromosome = chrm.Chromosome(first_child_binary, first_child_decimal, first_child_fitness)
    second_child : chrm.Chromosome = chrm.Chromosome(second_child_binary, second_child_decimal, second_child_fitness)

    # Replace parents with children in the new population
    new_population[first_i] : chrm.Chromosome = first_child
    new_population[second_i] : chrm.Chromosome = second_child

    return new_population