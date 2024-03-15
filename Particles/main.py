import sys
import pygame
import pygame_widgets
from pygame.locals import *
from raindrop import RainDrops
from cloud import Clouds
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
SIMULATION_AREA_WIDTH = int(0.8 * SCREEN_WIDTH)
CONTROL_AREA_WIDTH = SCREEN_WIDTH - SIMULATION_AREA_WIDTH

NUM_ROWS = 100
NUM_COLS = 100

CELL_WIDTH = SCREEN_WIDTH // NUM_COLS
CELL_HEIGHT = SCREEN_HEIGHT // NUM_ROWS

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
flock = []

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 300) 

individualraindrops = RainDrops()
individualclouds = Clouds()
raindrops_intervals = []
nighttimebg = pygame.image.load('./images/nightbg.png')

background = 0
backgrounds = [(150, 150, 255), (200,200,200)]

def change_background():
    global background
    if background == 0:
        background = 1
    else:
        background = 0

def reset_sim():
    global raindrops_intervals
    individualraindrops.raindrops = []
    individualclouds.cloud_particles = []
    raindrops_intervals = []

button = Button(screen, 40, 20, 100, 20, text="Reset Simulation", inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(200, 50, 0), fontSize=12, onClick=lambda: reset_sim(), textColour=(255, 255, 255))
button2 = Button(screen, 40, 50, 100, 20, text="Change Background", inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(200, 50, 0), fontSize=12, onClick=lambda: change_background(), textColour=(255, 255, 255))

speed_output = TextBox(screen, 35, 95, 0, 5, fontSize=15, textColour=(255, 255, 255))
speed_slider = Slider(screen, 40, 100, 100, 5, min=0, max=10, step=1)
speed_output.disable()  

windpressure_output = TextBox(screen, 35, 135, 0, 5, fontSize=15, textColour=(255, 255, 255))
windpressure_slider = Slider(screen, 40, 140, 100, 5, min=-0.1, max=0.1, step=0.02)
windpressure_output.disable()  

dampen_output = TextBox(screen, 35, 185, 0, 5, fontSize=15, textColour=(255, 255, 255))
dampen_slider = Slider(screen, 40, 190, 100, 5, min=0, max= 0.2, step=0.03)
dampen_output.disable()

def main():
    global raindrops_intervals
    global background
    global button_pressed

    speed = 5
    mean_raindrops = speed * 1.1
    var_raindrops = speed
    windpressure = 0

    pygame.display.set_caption("Snowy evening")
    
    cloud_heights = []
    num_clouds = 0

    button_pressed = False

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == PARTICLE_EVENT:
                if num_clouds != 0 and not button_pressed:
                    individualraindrops.add(raindrops_intervals, cloud_heights,  mean_raindrops, var_raindrops)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not button_pressed and event.pos[0]>200:
                    individualclouds.add(event.pos[0], event.pos[1])
                    raindrops_intervals.append([event.pos[0]-60, event.pos[0]+60])
                    cloud_heights.append(event.pos[1])
                    num_clouds += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos):
                button_pressed = True
                change_background()  # Call the change_background function when the button is pressed

        screen.fill(backgrounds[background])

        # Draw the night background only if the night background is selected
        if background == len(backgrounds) - 1:
            screen.blit(nighttimebg, (0, 0))

        # Draw simulation area
        image_path = './images/snowytree.png'
        image = pygame.image.load(image_path)
        scaled_image = pygame.transform.scale(image, (350, 500))
        screen.blit(scaled_image, (0, SCREEN_HEIGHT - scaled_image.get_height()))
        screen.blit(scaled_image, (SCREEN_WIDTH - scaled_image.get_width(), SCREEN_HEIGHT - scaled_image.get_height()))

        speed = speed_slider.getValue()
        mean_raindrops = speed * 2
        var_raindrops = speed
        windpressure = windpressure_slider.getValue()
        dampen = dampen_slider.getValue()

        individualclouds.emit(screen, raindrops_intervals)
        individualraindrops.emit(screen, speed, windpressure, dampen)

        speed_output.setText("Snowfall Speed: " + str(speed))
        windpressure_output.setText("Wind Pressure")
        dampen_output.setText("Dampening Factor: " + str(dampen))

        pygame_widgets.update(events)
        pygame.display.update()
        clock.tick(60)
        
if __name__ == "__main__":
    main()
