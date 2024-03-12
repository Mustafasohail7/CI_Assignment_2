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

def setup():
    for i in range(150): # slider parameter
        flock.append(Boid(SIMULATION_AREA_WIDTH, SCREEN_HEIGHT, 3, 0.03))  # Default values (position x, position y, speed, maxforce)

def startSimulation():
    setup()

def stopSimulation():
    flock.clear()  # Clear existing birds

def setnumbirds(num):
    flock.clear()
    for i in range(num):
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

    # Draw control area background
    control_area_bg = pygame.Surface((CONTROL_AREA_WIDTH, SCREEN_HEIGHT))
    control_area_bg.fill((128, 128, 128))  # Fill with gray color
    screen.blit(control_area_bg, (SIMULATION_AREA_WIDTH, 0))

    # Draw GUI elements in the control area
    gui.draw(screen)

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
                elif button_label == 'Stop Simulation':
                    stopSimulation()
                elif button_label == 'Start Simulation':
                    startSimulation()
                elif textbox_value := gui.getTextBoxValues().get('Number of Birds'):
                    setnumbirds(textbox_value)

        draw()


if __name__ == "__main__":
    main()
