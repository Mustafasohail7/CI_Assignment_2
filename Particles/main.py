import sys
import pygame
from pygame.locals import *
from raindrop import RainDrops
from cloud import Clouds
from button import Button
from slider import Slider

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
pygame.time.set_timer(PARTICLE_EVENT, 500)  # After how many milliseconds will each event be triggered.

snowbed = []

individualraindrops = RainDrops()
individualclouds = Clouds()

mean_raindrops = 3
var_raindrops = 2

# Create the button
button = Button("Stop Simulation", (30, 10, 130, 32))
button_pressed = False

def main():
    global button_pressed
    pygame.display.set_caption("Snowy evening")

    raindrops_intervals = []
    cloud_heights = []
    num_clouds = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == PARTICLE_EVENT:
                if num_clouds != 0 and not button_pressed:  # Check if the button is not pressed
                    individualraindrops.add(raindrops_intervals, cloud_heights,  mean_raindrops, var_raindrops)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not button_pressed:  # Check if the button is not pressed
                    individualclouds.add(event.pos[0], event.pos[1])
                    raindrops_intervals.append([event.pos[0]-60, event.pos[0]+60])
                    cloud_heights.append(event.pos[1])
                    num_clouds += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos):
                button_pressed = True  # Set the button_pressed variable to True when the button is pressed

        # Draw simulation area
        screen.fill((150, 150, 255))
        # screen.fill((200,200,200))
        image_path = 'images/snowytree.png'
        image = pygame.image.load(image_path)
        scaled_image = pygame.transform.scale(image, (350, 500))
        screen.blit(scaled_image, (0, SCREEN_HEIGHT - scaled_image.get_height()))

        scaled_image = pygame.transform.scale(image, (350, 500))
        screen.blit(scaled_image, (SCREEN_WIDTH - scaled_image.get_width(), SCREEN_HEIGHT - scaled_image.get_height()))

        individualclouds.emit(screen,raindrops_intervals)
        individualraindrops.emit(screen,snowbed)

        # Draw the button
        button.draw(screen)

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
