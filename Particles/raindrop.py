import pygame
import random

class RainDrops:
    def __init__(self):
        self.raindrops = []
        self.surface = pygame.image.load('images/raindrop.png').convert_alpha()
        self.width = self.surface.get_rect().width
        self.height = self.surface.get_rect().height

    def emit(self, screen):
        if self.raindrops:
            self.delete()
            for particle in self.raindrops:
                particle[0][1] += particle[2][0]  # Move the particle in the x direction
                particle[0][0] += particle[2][1]  # Move the particle in the y direction
                # particle[2][1] += 0.1  # Acceleration factor to the particle, this will be used to simulate the wind pressure
                particle[1] -= 0.08  # Dampen the particle size, that is how fast the particle will shrink/die off
                pygame.draw.circle(screen, pygame.Color('White'), particle[0], int(particle[1]))

    def add(self, SCREEN_WIDTH, mean_raindrops, var_raindrops):
        num_raindrops = max(0, int(random.gauss(mean_raindrops, var_raindrops)))
        for _ in range(num_raindrops):
            pos_x = random.randint(0, SCREEN_WIDTH)
            pos_y = 0 
            radius = 7.5
            direction_x = random.randint(1, 5)
            direction_y = 0  # Ensure raindrops move downwards
            particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
            self.raindrops.append(particle_circle)


    def delete(self):
        particle_copy = [particle for particle in self.raindrops if particle[1] > 0]
        self.raindrops = particle_copy
