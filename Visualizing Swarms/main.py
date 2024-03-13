import sys
import pygame
from pygame.locals import *
from boid import Boid
from GUI import GUI
from textbox import Textbox  # Import the Textbox class

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
        flock.append(Boid(SIMULATION_AREA_WIDTH, SCREEN_HEIGHT, 3, 0.03))  # Default values

def startSimulation():
    num_Birds = gui.get_textbox_values()['Number of Birds']
    for i in range(num_Birds): # slider parameter
        speed = gui.get_slider_values()['Speed']
        maxforce = gui.get_slider_values()['Max Force']
        flock.append(Boid(SIMULATION_AREA_WIDTH, SCREEN_HEIGHT, speed, maxforce))  # Default values

def stopSimulation():
    flock.clear()  # Clear existing birds

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

    # Create and add a Textbox to the GUI
    textbox_x = SCREEN_WIDTH - CONTROL_AREA_WIDTH + 50
    textbox_y = SCREEN_HEIGHT // 3
    # gui.textboxes.append(Textbox("Number of Birds", 150, (textbox_x, textbox_y, 140, 32)))

    setup()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                button_label = gui.mousepressed()
                if button_label == 'Add Bird':
                    x, y = SIMULATION_AREA_WIDTH // 2, SCREEN_HEIGHT // 2
                    flock.append(Boid(x, y, gui.get_slider_values()['Speed'], gui.get_slider_values()['Max Force']))
                elif button_label == 'Remove Bird':
                    if flock:
                        flock.pop()
                elif button_label == 'Stop Simulation':
                    stopSimulation()
                elif button_label == 'Start Simulation':
                    setup()

            # Pass events to the GUI
            gui.handle_event(event)

        draw()

if __name__ == "__main__":
    main()
