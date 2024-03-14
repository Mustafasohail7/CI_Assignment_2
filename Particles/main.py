import sys
import pygame
from pygame.locals import *
from raindrop import RainDrops
from cloud import Clouds
from GUI import GUI

pygame.init()

# Define screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
# SCREEN_HEIGHT_forcells = 100
SIMULATION_AREA_WIDTH = int(0.8 * SCREEN_WIDTH)
CONTROL_AREA_WIDTH = SCREEN_WIDTH - SIMULATION_AREA_WIDTH

# Define the number of rows and columns for the grid
NUM_ROWS = 100
NUM_COLS = 100

# Calculate the width and height of each cell
CELL_WIDTH = SCREEN_WIDTH // NUM_COLS
CELL_HEIGHT = SCREEN_HEIGHT // NUM_ROWS

# Create a 2D array representing the grid
grid = [[0] * NUM_COLS for _ in range(NUM_ROWS)]

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

        screen.fill((35,35,35))

        individualclouds.emit(screen)
        individualraindrops.emit(screen)

        # Update the grid
        update_grid()

        pygame.display.flip()

        # Draw control area (GUI)
        pygame.draw.rect(screen, (150, 150, 150), (SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # gui.draw(screen)  # Draw GUI elements

        pygame.display.flip()
        clock.tick(60)

def update_grid():
    # Clear the grid
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            grid[row][col] = 0

    # Update the grid based on the position of raindrops
    for particle in individualraindrops.raindrops:
        col = int(particle[0][0] / CELL_WIDTH)
        row = int(particle[0][1] / CELL_HEIGHT)
        if 0 <= row < NUM_ROWS and 0 <= col < NUM_COLS:
            grid[row][col] = 1

if __name__ == "__main__":
    main()
