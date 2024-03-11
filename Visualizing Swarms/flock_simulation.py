import sys
import pygame
from pygame.locals import *
from boid import Boid
from GUI import GUI

pygame.init()

# Define screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
SIMULATION_AREA_WIDTH = int(0.8 * SCREEN_WIDTH)
CONTROL_AREA_WIDTH = SCREEN_WIDTH - SIMULATION_AREA_WIDTH

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
flock = []

background_image = pygame.image.load('Visualizing Swarms/images/skyBG2.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def restartSimulation():
    flock.clear()  # Clear existing birds
    num_birds = int(gui.getSliderValues()['Number of Birds'])
    speed = gui.getSliderValues()['Speed']
    maxforce = gui.getSliderValues()['Max Force']
    for _ in range(num_birds):
        flock.append(Boid(SIMULATION_AREA_WIDTH / 2, SCREEN_HEIGHT / 2, speed, maxforce))

def setup():
    for i in range(150): # slider parameter
        flock.append(Boid(SIMULATION_AREA_WIDTH / 2, SCREEN_HEIGHT / 2, 2, 0.03))  # Default values

def draw():
    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw simulation area
    for boid in flock:
        boid.flock(flock)
        boid.update()
        boid.borders(SIMULATION_AREA_WIDTH, SCREEN_HEIGHT) 
        boid.render(screen)

    # Draw control area
    control_area = screen.subsurface((SIMULATION_AREA_WIDTH, 0, CONTROL_AREA_WIDTH, SCREEN_HEIGHT))
    control_area.fill((200, 200, 200))  # Fill control area with a background color

    gui.draw(control_area)  # Draw GUI elements in the control area

    # Update the display
    pygame.display.flip()
    clock.tick(60)


def main():
    global gui  
    gui = GUI(SCREEN_WIDTH, SCREEN_HEIGHT)  
    setup()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                button_label = gui.mousepressed()
                if button_label == 'Add Bird':
                    x, y = pygame.mouse.get_pos()
                    flock.append(Boid(x, y, gui.getSliderValues()['Speed'], gui.getSliderValues()['Max Force']))
                elif button_label == 'Remove Bird':
                    # Remove the last bird
                    if flock:
                        flock.pop()
                elif button_label == 'Restart Simulation':
                    restartSimulation()

        draw()


if __name__ == "__main__":
    main()
