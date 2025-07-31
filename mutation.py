import random
import chromosome as chrm

def mutation(config : dict, population : list[chrm.Chromosome]) -> list[chrm.Chromosome]:
    new_population : list[chrm.Chromosome] = population.copy()

    for i in range(len(new_population)):
        u : float = random.uniform(0, 1)
        if u < config["mutation_probability"]:
            bit : int = random.randint(0, chrm.Chromosome.binary_length - 1)
            binary : str = new_population[i].binary
            new_bit : int = 1 - int(binary[bit])
            new_binary : str = binary[:bit] + str(new_bit) + binary[(bit+1):]
            new_decimal : float = chrm.get_decimal(new_binary, config)
            new_fitness : float = chrm.get_fitness(new_decimal, config)
            new_population[i] = chrm.Chromosome(new_binary, new_decimal, new_fitness)

    return new_population