# Genetic Algorithm for Quadratic Function Optimization

A Python project that uses a genetic algorithm to search for the vertex of a quadratic function. The algorithm works by encoding possible solutions as binary strings ("chromosomes") and evolving a population of these solutions using operations such as selection, crossover, and mutation.

The algorithm tracks and displays:
- **Best Fitness**: Optimal solution found so far
- **Function Maximum**: Mathematical vertex of the quadratic
- **Delta**: Difference between found solution and theoretical optimum
## Demo

![Genetic Algorithm Evolution](https://i.imgur.com/pewntK9.gif)
*The genetic algorithm converging to find the optimal solution over multiple generations*

## Features

- Binary encoding with configurable precision
- Automatically detects whether to maximize or minimize based on quadratic function coefficients
- Live animated plots showing population evolution
- **Elite Selection**: Top performers survive to next generation
- **Roulette Wheel**: Fitness-proportionate selection
- **Crossover**: Single-point crossover with configurable rate
- **Mutation**: Bit-flip mutation with configurable rate

## How to use

Edit `input.txt` with your own parameters:

    
    20             # Population size
    -1 2           # Domain start and end
    -1 1 2         # Coefficients a, b, c
    6              # Precision (number of decimals)
    0.25           # Crossover probability
    0.05           # Mutation probability
    50             # Number of generations
