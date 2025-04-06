import math
import random

class Chromosome():
    binary_length = 0

    def __init__(self, binary, decimal, fitness):
        self.binary = binary
        self.decimal = decimal
        self.fitness = fitness

    def __str__(self):
        return f"Binary: {self.binary} Decimal: {self.decimal} Fitness: {self.fitness}\n"

    def __repr__(self):
        return f"{self.fitness}"


def read_input():
    global population_size, domain_start, domain_end, a, b, c, precision
    global crossover_probabilty, mutation_probabilty, generation_count
    with open("input.txt", "r") as f:
        population_size = int(f.readline())
        domain_start, domain_end = [int(value) for value in f.readline().split()]
        a, b, c = [int(coeff) for coeff in f.readline().split()]
        precision = int(f.readline())
        crossover_probabilty = float(f.readline())
        mutation_probabilty = float(f.readline())
        generation_count = int(f.readline())


def set_chromosome_length():
    # lungimea unui cromozom va fi log2[(b - a) * 10^p]
    Chromosome.binary_length = math.ceil(math.log((domain_end - domain_start) * 10 ** precision, 2))


def get_binary(value):
    # umplem cu zero bitii de la stanga ca sa avem lungimea binarului egala cu lungimea crom
    return bin(value)[2:].zfill(Chromosome.binary_length)


def get_decimal(binary):
    # decodificarea X(2) in zecimal este (b - a) / (2^l - 1) * X(10) + a
    return round(int(binary, 2) * (domain_end - domain_start) / (2 ** Chromosome.binary_length - 1) + a, precision)


def get_fitness(decimal):
    return a * decimal * decimal + b * decimal + c


def generate_chromosome():
    # generam un numar random care poate sa incapa intr-un binar de lungime chr_length
    value = random.randint(0, 2 ** Chromosome.binary_length - 1)
    binary = get_binary(value)
    decimal = get_decimal(binary)
    fitness = get_fitness(decimal)
    return Chromosome(binary, decimal, fitness)


def generate_population():
    # generam count cromozomi si ii adaugam la populatie
    for i in range(population_size):
        chromosome = generate_chromosome()
        population.append(chromosome)


def population_fitness(pop):
    ans = 0
    for chromosome in pop:
        ans += chromosome.fitness
    return ans


def display_population(pop):
    with open("output.txt", "a") as f:
        for i in range(len(pop)):
            f.write("[" + str(i + 1) + "] " + str(pop[i]))
        f.write('\n')


def display_probabilities():
    total_fitness = population_fitness(population)
    with open("output.txt", "a") as f:
        f.write("Probabilitati selectia ruleta\n")
        for i in range(len(population)):
            f.write(f"Cromozom {i + 1} Probabilitate {population[i].fitness / total_fitness}\n")
        f.write("\nIntervale probabilitati selectie\n")
        u = 0
        per_row = 5
        for i in range(len(population)):
            f.write(str(u) + ' ')
            per_row -= 1
            if per_row == 0:
                per_row = 5
                f.write('\n')
            u += (population[i].fitness / total_fitness)
        f.write("1\n\n")



def roulette_wheel():
    total_fitness = population_fitness(population)
    val = random.uniform(0, 1)
    u = 0
    for i in range(len(population)):
        u += (population[i].fitness / total_fitness)
        if u >= val:
            # detaliem alegerea din prima generatie
            if current_generation == 1:
                with open("output.txt", "a") as f:
                    f.write(f"u={u} Selectam cromozomul {i+1}\n")
            return population[i]


def selection(elitist_count):
    new_population = []
    # selectia elitista
    # sortam cromozomii descrescator, primii vor fi cei elitisti
    elitist_chromosomes = sorted(population, key=lambda x: x.fitness, reverse=True)[:elitist_count]
    new_population.extend(elitist_chromosomes)

    # selectia ruleta
    for i in range(population_size - elitist_count):
        new_population.append(roulette_wheel())

    return new_population


def get_crossover_list():
    crossover_list = []
    if current_generation == 1:
        f = open("output.txt", "a")
        f.write(f"\nProbabilitatea de incurcisare {crossover_probabilty}\n")
    for i in range(len(new_population)):
        u = random.uniform(0, 1)
        if current_generation == 1:
            f.write(f"[{i + 1}] {new_population[i].binary} u={u}")
        ##
        if u < crossover_probabilty:
            crossover_list.append(i)
            if current_generation == 1:
                f.write(f" < {crossover_probabilty} participa")

        if current_generation == 1:
            f.write('\n')

    if current_generation == 1:
        f.close()

    return crossover_list


def crossover():
    first_i = crossover_list.pop(0)
    second_i = crossover_list.pop(0)

    if current_generation == 1:
        f = open("output.txt", "a")
        f.write(f"\nRecombinare dintre cromozomul {first_i + 1} cu cromozomul {second_i + 1}:\n")

    first_parent = new_population[first_i]
    second_parent = new_population[second_i]
    point = random.randint(0, Chromosome.binary_length)

    if current_generation == 1:
        f.write(f"{first_parent.binary} {second_parent.binary} Punct: {point}\n")

    first_child_binary = first_parent.binary[:point]  + second_parent.binary[point:]
    second_child_binary = second_parent.binary[:point]  + first_parent.binary[point:]

    first_child_decimal = get_decimal(first_child_binary)
    first_child_fitness = get_fitness(first_child_decimal)

    second_child_decimal = get_decimal(second_child_binary)
    second_child_fitness = get_fitness(second_child_decimal)

    first_child = Chromosome(first_child_binary, first_child_decimal, first_child_fitness)
    second_child = Chromosome(second_child_binary, second_child_decimal, second_child_fitness)

    new_population[first_i] = first_child
    new_population[second_i] = second_child

    if current_generation == 1:
        f.write(f"Rezultat: {first_child.binary} {second_child.binary}\n")
        f.close()


def mutation():
    if current_generation == 1:
        f = open("output.txt", "a")
        f.write(f"\nProbabilitatea de mutatie pentru fiecare gena {mutation_probabilty}\n")

    for i in range(len(new_population)):
        u = random.uniform(0, 1)
        if u < mutation_probabilty:
            bit = random.randint(0, Chromosome.binary_length - 1)
            binary = new_population[i].binary
            new_bit = 1 - int(binary[bit])
            new_binary = binary[:bit] + str(new_bit) + binary[(bit+1):]
            new_decimal = get_decimal(new_binary)
            new_fitness = get_fitness(new_decimal)
            new_population[i] = Chromosome(new_binary, new_decimal, new_fitness)
            if current_generation == 1:
                f.write(f"Cromozomul {i + 1} modificat\n")

    if current_generation == 1:
        f.close()

read_input()
set_chromosome_length()

population = []
current_generation = 1

generate_population()

# populatia initiala
with open("output.txt", "w") as f:
    f.write("Populatia initiala\n")
display_population(population)

while current_generation < generation_count:
    if current_generation == 1:
        # probabilitatile de selectie pt ruleta
        display_probabilities()

    new_population = selection(1)
    if current_generation == 1:
        # populatia dupa selectia elitista si cea ruleta
        with open("output.txt", "a") as f:
            f.write("\nDupa selectie\n")
        display_population(new_population)

    crossover_list = get_crossover_list()
    while len(crossover_list) > 1:
        crossover()
    if current_generation == 1:
        # populatia dupa crossover
        with open("output.txt", "a") as f:
            f.write("\nDupa recombinare:\n")
        display_population(new_population)

    mutation()
    population = new_population

    if current_generation == 1:
        # populatia dupa mutatie
        with open("output.txt", "a") as f:
            f.write("\nDupa mutatie:\n")
        display_population(population)

    if current_generation == 2:
        with open("output.txt", "a") as f:
            f.write("\nEvolutia maximului:\n")
    if current_generation != 1:
        max_fitness = float('-inf')
        for chromosome in population:
            max_fitness = max(max_fitness, chromosome.fitness)
        with open("output.txt", "a") as f:
            f.write(str(max_fitness) + '\n')

    current_generation += 1