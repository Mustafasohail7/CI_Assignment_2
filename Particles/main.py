import sys
import pygame
import pygame_widgets
from pygame.locals import *
from raindrop import RainDrops
from cloud import Clouds
from button import Button
from slider import Slider
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

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
pygame.time.set_timer(PARTICLE_EVENT, 300)  # After how many milliseconds will each event be triggered.

individualraindrops = RainDrops()
individualclouds = Clouds()
raindrops_intervals = []

def change_background():
    screen.fill((255, 0, 0))

def reset_sim():
    # print(individualraindrops.raindrops)
    global raindrops_intervals
    individualraindrops.raindrops = []
    individualclouds.cloud_particles = []
    raindrops_intervals = []

# Create the button
button = Button(screen,20,50,50,50,text="Reset Simulation",inactiveColour=(200, 50, 0),hoverColour=(150, 0, 0),pressedColour=(0, 200, 20),
                onClick=lambda: reset_sim())
background_btn = Button(screen, 20, 100, 50, 50, text="Background", inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0),
                pressedColour=(0, 200, 20), onClick=lambda: change_background())
button_pressed = False

speed_output = TextBox(screen, 35, 95, 0, 5, fontSize=15)
speed_slider = Slider(screen, 40, 100, 100, 5, min=0, max=10, step=1)
speed_output.disable()  # Act as label instead of textbox

windpressure_output = TextBox(screen, 35, 145, 0, 5, fontSize=15)
windpressure_slider = Slider(screen, 40, 150, 100, 5, min=-0.1, max=0.1, step=0.02)
windpressure_output.disable()  

dampen_output = TextBox(screen, 35, 195, 0, 5, fontSize=15)
dampen_slider = Slider(screen, 40, 200, 100, 5, min=0, max= 0.3, step=0.03)
dampen_output.disable()


def main():

    global raindrops_intervals

    speed = 5
    mean_raindrops = speed * 1.2
    var_raindrops = speed

    windpressure = 0

    global button_pressed
    pygame.display.set_caption("Snowy evening")

    
    cloud_heights = []
    num_clouds = 0

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == PARTICLE_EVENT:
                if num_clouds != 0 and not button_pressed:  # Check if the button is not pressed
                    individualraindrops.add(raindrops_intervals, cloud_heights,  mean_raindrops, var_raindrops)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not button_pressed and event.pos[0]>200:  # Check if the button is not pressed
                    individualclouds.add(event.pos[0], event.pos[1])
                    raindrops_intervals.append([event.pos[0]-60, event.pos[0]+60])
                    cloud_heights.append(event.pos[1])
                    num_clouds += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos):
                button_pressed = True  # Set the button_pressed variable to True when the button is pressed

        # Draw simulation area
        screen.fill((150, 150, 255))
        # screen.fill((200,200,200))
        image_path = '../images/snowytree.png'
        image = pygame.image.load(image_path)
        scaled_image = pygame.transform.scale(image, (350, 500))
        screen.blit(scaled_image, (0, SCREEN_HEIGHT - scaled_image.get_height()))

        scaled_image = pygame.transform.scale(image, (350, 500))
        screen.blit(scaled_image, (SCREEN_WIDTH - scaled_image.get_width(), SCREEN_HEIGHT - scaled_image.get_height()))

        speed = speed_slider.getValue()
        mean_raindrops = speed*2
        var_raindrops = speed

        windpressure = windpressure_slider.getValue()

        dampen = dampen_slider.getValue()

        individualclouds.emit(screen,raindrops_intervals)
        individualraindrops.emit(screen,speed,windpressure,dampen)

        speed_output.setText("Snowfall Speed: " + str(speed))  # Update the text of the textbox
        windpressure_output.setText("Wind Pressure")
        dampen_output.setText("Dampening Factor: " + str(dampen))

        pygame_widgets.update(events)
        pygame.display.update()

        pygame.display.flip()
        
        # Draw control area (GUI)
        pygame.draw.rect(screen, (150, 150, 150), (SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
