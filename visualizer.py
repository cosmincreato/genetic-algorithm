import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import chromosome as chrm

matplotlib.use('TkAgg')

def create_animated_plot(config: dict, generations: list[list[chrm.Chromosome]], delay: float) -> None:
    plt.ion()

    max_x = -config["b"] / (2 * config["a"])
    max_y = chrm.get_fitness(max_x, config)

    for generation, population in enumerate(generations, 1):
        plt.clf()

        x = np.linspace(config["domain_start"], config["domain_end"], 1000)
        y = chrm.get_fitness(x, config)
        x_values = [chromosome.decimal for chromosome in population]
        y_values = [chromosome.fitness for chromosome in population]

        if config["maximize"] is True:
            best_chromosome = max(population, key=lambda chrom: chrom.fitness)
        else:
            best_chromosome = min(population, key=lambda chrom: chrom.fitness)

        plt.plot(x, y, 'b-', linewidth=2,
                 label="f(x) = " + str(config["a"]) + "x² + " + str(config["b"]) + "x + " + str(config["c"]))
        plt.scatter(x_values, y_values,
                    c='crimson', s=25, zorder=2,
                    label="Generation " + str(generation) + " Chromosomes")

        plt.scatter(best_chromosome.decimal, best_chromosome.fitness,
                    c='gold', s=25, marker='*', zorder=3,
                    label=f"Best: {best_chromosome.fitness:0.7f}")

        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title("Quadratic Function Genetic Algorithm - Generation " + str(generation))
        plt.gcf().canvas.manager.set_window_title("Quadratic Function Genetic Algorithm")
        plt.legend()

        if generation == len(generations):
            delta = abs(max_y - best_chromosome.fitness)
            plt.plot([], [], color='none', label=f"Function Vertex: {max_y:.7f}")
            plt.plot([], [], color='none', label=f"Delta: {delta:.7f}")
            plt.legend()

        plt.pause(delay)

    plt.ioff()
    plt.show()