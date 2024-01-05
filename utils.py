import numpy as np

def mutate(stats):
    mutation_rate = 1/3
    mutation_amplitude = 0.3

    for key in stats:
        if np.random.rand() < mutation_rate:
            change = np.random.uniform(-mutation_amplitude, mutation_amplitude)
            stats[key] *= (1 + change)
