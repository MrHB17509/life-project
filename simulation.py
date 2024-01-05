import pygame
import numpy as np
from animal import Animal
from environment import Environment

class Simulation:
    def __init__(self, screen):
        self.screen = screen
        self.population = self.initialize_population()
        self.environment = Environment(20, 20, 30)  # Exemplo de parâmetros

    def initialize_population(self):
        population = []
        for _ in range(100):
            diet = np.random.choice(['herbivore', 'carnivore', 'omnivore'])
            animal = Animal(diet, np.random.randint(0, 1000), np.random.randint(0, 1000))
            population.append(animal)
        return population

    def run(self):
        clock = pygame.time.Clock()
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            self.screen.fill((255, 255, 255))
            new_animals = []

            for animal in self.population:
                self.update_animal(animal)
                if animal.stats['hunger'] <= 0 and animal.stats['reproduction_rate'] > 0:
                    offspring = animal.reproduce()
                    new_animals.append(offspring)
                    animal.stats['hunger'] = 20

            self.population.extend(new_animals)

            for animal in self.population:
                color = (0, 0, 0) if animal.diet == 'carnivore' else (0, 255, 0) if animal.diet == 'herbivore' else (0, 0, 255)
                pygame.draw.circle(self.screen, color, (int(animal.x), int(animal.y)), animal.stats['size'])

            pygame.display.flip()
            clock.tick(60)

    def update_animal(self, animal):
        animal.x += np.random.randint(-1, 2) * animal.stats['speed']
        animal.y += np.random.randint(-1, 2) * animal.stats['speed']
        animal.stats['hunger'] -= 1
        current_biome = self.environment.get_biome_at(animal.x, animal.y)
        animal.adjust_for_biome(current_biome)
