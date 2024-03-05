import pygame
import numpy as np

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

class Hexagon:
    def __init__(self, x, y, biome):
        self.x = x
        self.y = y
        self.biome = biome

class Environment:
    def __init__(self, width, height, hex_size):
        self.width = width
        self.height = height
        self.hex_size = hex_size
        self.hex_grid = self.create_hex_grid()

    def create_hex_grid(self):
        grid = []
        vertical_distance = self.hex_size * 3**0.5
        horizontal_distance = self.hex_size * 1.5
        for row in range(self.height):
            for col in range(self.width):
                x = col * horizontal_distance + (row % 2) * (horizontal_distance / 2)
                y = row * vertical_distance * 0.75
                biome = self.determine_biome(x, y)
                grid.append(Hexagon(x, y, biome))
        return grid

    def determine_biome(self, x, y):
        if y < self.height / 3:
            return "desert" if x % 2 == 0 else "grassland"
        elif y < 2 * self.height / 3:
            return "forest" if x % 2 == 0 else "mountain"
        else:
            return "tundra" if x % 2 == 0 else "swamp"

    def get_biome_at(self, x, y):
        closest_hex = min(self.hex_grid, key=lambda hex: (hex.x - x)**2 + (hex.y - y)**2)
        return closest_hex.biome

def mutate(stats):
    mutation_rate = 1/3
    mutation_amplitude = 0.3

    for key in stats:
        if np.random.rand() < mutation_rate:
            change = np.random.uniform(-mutation_amplitude, mutation_amplitude)
            stats[key] *= (1 + change)

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.99, exploration_rate=0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = np.zeros((state_size, action_size))

    def choose_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return np.random.choice(self.action_size)
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        td_target = reward + self.discount_factor * np.max(self.q_table[next_state])
        td_error = td_target - self.q_table[state, action]
        self.q_table[state, action] += self.learning_rate * td_error

class Simulation:
    def __init__(self, screen):
        self.screen = screen
        self.population = self.initialize_population()
        self.environment = Environment(20, 20, 30)
        self.agent = QLearningAgent(state_size=4, action_size=2)

    def initialize_population(self):
        population = []
        for _ in range(100):
            diet = np.random.choice(['herbivore', 'carnivore', 'omnivore'])
            animal = Animal(diet, np.random.randint(0, 1000), np.random.randint(0, 1000))
            population.append(animal)
        return population

    def flee_if_attacked(self, animal):
        for other_animal in self.population:
            if other_animal.diet == 'carnivore' and animal.diet != 'carnivore':
                distance = ((other_animal.x - animal.x) ** 2 + (other_animal.y - animal.y) ** 2) ** 0.5
                if distance < 50:
                    if other_animal.x > animal.x:
                        animal.x -= animal.stats['speed']
                    else:
                        animal.x += animal.stats['speed']
                    if other_animal.y > animal.y:
                        animal.y -= animal.stats['speed']
                    else:
                        animal.y += animal.stats['speed']

    def take_action(self, animal, action):
        if action == 1:
            self.flee_if_attacked(animal)

    def get_state_representation(self, animal):
        return [animal.stats['hunger'], animal.stats['speed'], animal.x, animal.y]

    def calculate_reward(self, animal):
        return 1 if animal.stats['hunger'] > 0 else -1

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
                state = self.get_state_representation(animal)
                action = self.agent.choose_action(state)
                self.take_action(animal, action)
                reward = self.calculate_reward(animal)
                next_state = self.get_state_representation(animal)
                self.agent.update_q_table(state, action, reward, next_state)

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

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption('Life Simulation')

    simulation = Simulation
    simulation.run()
    pygame.quit()