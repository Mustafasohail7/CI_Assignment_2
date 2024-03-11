import pygame
import os
from starlings import Starlings

# Set the working directory to the directory of the script
os.chdir(os.path.dirname(__file__))

# Initialize Pygame
pygame.init()

WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving starlings")

# Load the background image
background_image = pygame.image.load("images/skyBG.jpeg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize the image to match screen size

# Create a list to store starlings
starlings = [Starlings() for _ in range(10)]  # Adjust the number of starlings here

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background_image, (0, 0))  # Blit the background image onto the screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and draw starlings
    for starling in starlings:
        starling.move()
        starling.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
