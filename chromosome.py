import math
import random

class Chromosome:
    binary_length = 0

    def __init__(self, binary : str, decimal : float, fitness : float):
        self.binary = binary
        self.decimal = decimal
        self.fitness = fitness

    def __str__(self):
        return f"Binary: {self.binary} Decimal: {self.decimal} Fitness: {self.fitness}\n"

    def __repr__(self):
        return f"{self.fitness}"


def set_chromosome_length(config : dict) -> None:
    # log2[(b - a) * 10^p]
    Chromosome.binary_length = math.ceil(math.log((config["domain_end"] - config["domain_start"]) * 10 ** config["precision"], 2))


def generate_chromosome(config : dict) -> Chromosome:
    # We generate a random number that can fit in a binary number of length chr_length
    value : int = random.randint(0, 2 ** Chromosome.binary_length - 1)
    binary : str = get_binary(value)
    decimal : float = get_decimal(binary, config)
    fitness : float = get_fitness(decimal, config)
    return Chromosome(binary, decimal, fitness)


def get_binary(value : int) -> str:
    # We fill with zeroes on the left so that the length of the binary is equal to the length of the chromosome
    return bin(value)[2:].zfill(Chromosome.binary_length)


def get_decimal(binary : str, config : dict) -> float:
    # bin(X) -> (b - a) / (2^l - 1) * dec(X) + a
    return round(int(binary, 2) * (config["domain_end"] - config["domain_start"]) / (2 ** Chromosome.binary_length - 1) + config["domain_start"], config["precision"])


def get_fitness(decimal : float, config : dict) -> float:
    # Quadratic function
    return config["a"] * decimal * decimal + config["b"] * decimal + config["c"]