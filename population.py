import chromosome as chrm

def generate_population(config : dict) -> list[chrm.Chromosome]:
    population: list[chrm.Chromosome] = []

    # Set the chromosome length for the initial population
    chrm.set_chromosome_length(config)

    # Generate the population
    for i in range(config["population_size"]):
        chromosome : chrm.Chromosome = chrm.generate_chromosome(config)
        population.append(chromosome)

    return population


def get_population_fitness(pop : list[chrm.Chromosome]) -> float:
    total_fitness : float = 0
    for chromosome in pop:
        total_fitness += chromosome.fitness
    return total_fitness