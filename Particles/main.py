import sys
import pygame
from pygame.locals import *
from raindrop import RainDrops
from cloud import Clouds

pygame.init()

# Define screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
SIMULATION_AREA_WIDTH = int(0.8 * SCREEN_WIDTH)
CONTROL_AREA_WIDTH = SCREEN_WIDTH - SIMULATION_AREA_WIDTH

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
flock = []

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 40)  # After how many milliseconds will each event be triggered.

individualraindrops = RainDrops(SCREEN_HEIGHT)
individualclouds = Clouds()

mean_raindrops = 10
var_raindrops = 5

def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == PARTICLE_EVENT:
                individualraindrops.add(SCREEN_WIDTH ,mean_raindrops, var_raindrops)
                # print("Adding raindrops")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    individualclouds.add(event.pos[0], event.pos[1])
                    # print("Adding clouds")

        screen.fill((200, 200, 255))

        individualclouds.emit(screen)
        individualraindrops.emit(screen)
        # print("Number of raindrops:", len(individualraindrops.raindrops))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
