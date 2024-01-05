import pygame
from simulation import Simulation

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption('Life Simulation')

    simulation = Simulation(screen)
    simulation.run()

    pygame.quit()

if __name__ == "__main__":
    main()
