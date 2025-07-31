def read_input() -> dict:
    with open("input.txt", "r") as f:
        population_size = int(f.readline())
        domain = [int(v) for v in f.readline().split()]
        abc = [int(v) for v in f.readline().split()]
        precision = int(f.readline())
        crossover_probability = float(f.readline())
        mutation_probability = float(f.readline())
        generation_count = int(f.readline())
    config = {
        'population_size': population_size,
        'domain_start': domain[0],
        'domain_end': domain[1],
        'a': abc[0],
        'b': abc[1],
        'c': abc[2],
        'precision': precision,
        'crossover_probability': crossover_probability,
        'mutation_probability': mutation_probability,
        'generation_count': generation_count,
        "maximize": True
    }

    if config["a"] > 0:
        config["maximize"] = False

    return config