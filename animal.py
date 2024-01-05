import numpy as np
from utils import mutate

class Animal:
    def __init__(self, diet, x, y):
        self.diet = diet
        self.x = x
        self.y = y
        self.stats = self.initialize_stats()

    def initialize_stats(self):
        return {'size': np.random.randint(5, 15),
                'speed': np.random.randint(1, 5),
                'reproduction_rate': np.random.randint(1, 5),
                'hunger': np.random.randint(1, 5)}

    def reproduce(self):
        offspring = Animal(self.diet, self.x, self.y)
        offspring.stats = self.stats.copy()
        mutate(offspring.stats)
        return offspring

    def adjust_for_biome(self, biome):
        if biome == "forest":
            self.stats['speed'] *= 0.9
        elif biome == "desert":
            self.stats['hunger'] += 1
        elif biome == "grassland":
            self.stats['reproduction_rate'] += 0.1
        # Mais lógicas de biomas podem ser adicionadas aqui
