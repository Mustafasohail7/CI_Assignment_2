import sys
import pygame
from pygame.locals import *
from raindrop import RainDrops
from cloud import Clouds
from GUI import GUI

pygame.init()

# Define screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
SIMULATION_AREA_WIDTH = int(0.8 * SCREEN_WIDTH)
CONTROL_AREA_WIDTH = SCREEN_WIDTH - SIMULATION_AREA_WIDTH

# Define the number of rows and columns for the grid
NUM_ROWS = 100
NUM_COLS = 100

# Calculate the width and height of each cell
CELL_WIDTH = SCREEN_WIDTH // NUM_COLS
CELL_HEIGHT = SCREEN_HEIGHT // NUM_ROWS

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
flock = []

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 80)  # After how many milliseconds will each event be triggered.

individualraindrops = RainDrops()
individualclouds = Clouds()

mean_raindrops = 10
var_raindrops = 5

def main():
    # gui = GUI(SCREEN_WIDTH, SCREEN_HEIGHT)  # Create an instance of the GUI class

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == PARTICLE_EVENT:
                individualraindrops.add(SCREEN_WIDTH, mean_raindrops, var_raindrops)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    individualclouds.add(event.pos[0], event.pos[1])
                    # if event.type == PARTICLE_EVENT:
                    # individualraindrops.add(SCREEN_WIDTH, mean_raindrops, var_raindrops)

            # Pass events to the GUI for handling
            # gui.handle_event(event)

        # Draw simulation area
        # screen.fill((200, 200, 255))
        screen.fill((35,35,35))

        individualclouds.emit(screen)
        individualraindrops.emit(screen)

        # Draw grid lines
        for row in range(NUM_ROWS):
            pygame.draw.line(screen, (35,35,35), (0, row * CELL_HEIGHT), (SCREEN_WIDTH, row * CELL_HEIGHT))
        for col in range(NUM_COLS):
            pygame.draw.line(screen, (35,35,35), (col * CELL_WIDTH, 0), (col * CELL_WIDTH, SCREEN_HEIGHT))

        pygame.display.flip()

        # Draw control area (GUI)
        pygame.draw.rect(screen, (150, 150, 150), (SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # gui.draw(screen)  # Draw GUI elements

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
