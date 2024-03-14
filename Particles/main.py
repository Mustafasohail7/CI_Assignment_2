import sys
import pygame
from pygame.locals import *
from raindrop import RainDrops
from cloud import Clouds
from GUI import GUI

pygame.init()

# Define screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
SCREEN_HEIGHT_forcells = 50
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
pygame.time.set_timer(PARTICLE_EVENT, 500)  # After how many milliseconds will each event be triggered.

snowbed = []

individualraindrops = RainDrops()
individualclouds = Clouds()

mean_raindrops = 2
var_raindrops = 1



def main():
    # gui = GUI(SCREEN_WIDTH, SCREEN_HEIGHT)  # Create an instance of the GUI class

    raindrops_intervals = []
    cloud_heights = []
    num_clouds = 0

    max = 1
    r = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == PARTICLE_EVENT:
                if num_clouds != 0:
                    # individualraindrops.add(raindrops_intervals, mean_raindrops, var_raindrops)
                    if r<max:
                        individualraindrops.add(raindrops_intervals, cloud_heights,  mean_raindrops, var_raindrops)
                    else:
                        r+=1
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    individualclouds.add(event.pos[0], event.pos[1])
                    raindrops_intervals.append([event.pos[0]-60, event.pos[0]+60])
                    cloud_heights.append(event.pos[1])
                    num_clouds += 1
                    
                    # if event.type == PARTICLE_EVENT:
                    # individualraindrops.add(SCREEN_WIDTH, mean_raindrops, var_raindrops)

            # Pass events to the GUI for handling
            # gui.handle_event(event)

        # Draw simulation area
        # screen.fill((200, 200, 255))
        screen.fill((35,35,35))

        individualclouds.emit(screen,raindrops_intervals)
        individualraindrops.emit(screen,snowbed)

        pygame.display.flip()

        # Draw control area (GUI)
        pygame.draw.rect(screen, (150, 150, 150), (SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # gui.draw(screen)  # Draw GUI elements

        # for position in snowbed:
            # pygame.draw.circle(screen, (255,0,0), position, 10)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
