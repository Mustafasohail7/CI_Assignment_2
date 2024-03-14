import pygame
import random

class Clouds:
    def __init__(self):
        self.cloud_particles = []


    def emit(self, screen, raindrops_intervals):
        if self.cloud_particles:
            self.delete(SCREEN_HEIGHT=600)
            for particle in self.cloud_particles:
                # Update particle position or any other properties
                particle[0][0] += 0.5  # Move the particle in the x direction
                particle[0][1] += random.uniform(-0.2, 0.2)  # Move the particle in the y direction
                
                radius = particle[2]  # Get the radius of the particle
                alpha = int(255 * (radius / 5))  # Adjust alpha based on particle size
                color = particle[1]  # Get the color of the particle
                color.a = alpha  # Set alpha value for transparency
                pygame.draw.circle(screen, color, (int(particle[0][0]), int(particle[0][1])), int(radius))
            
            for i in raindrops_intervals:
                i[0] += 0.5
                i[1] += 0.5



    def add(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        # Add small cloud particles at the specified position
        hue = random.randint(250, 255)  # Random hue for clouds within the range of white to gray
        saturation = random.uniform(0, 3)  # Lower saturation for closer to white appearance
        value = random.uniform(90, 100)  # Higher value for closer to white appearance

        # Create color objects for cloud and shadow
        color = pygame.Color(0)
        color.hsva = (hue, saturation, value, 100)  # Set the color using HSV values with full alpha

        self.num_particles = random.randint(500, 1000)  # Number of particles for each cloud

        self.cloud_size = 80  # What is the size of the cloud
        self.spread_factor = 0.3  # How spread are the particles that make up the cloud

        for _ in range(self.num_particles):
            # Randomize position within the cloud area with reduced variation
            offset_x = random.gauss(0, self.cloud_size * self.spread_factor)  # Gaussian distribution for x offset
            offset_y = random.gauss(0, self.cloud_size * self.spread_factor / 2)  # Gaussian distribution for y offset
            particle_x = pos_x + offset_x
            particle_y = pos_y + offset_y
            radius = random.uniform(1, 5)  # Random radius for each particle
            self.cloud_particles.append([[particle_x, particle_y], color, radius])
        
    def delete(self, SCREEN_HEIGHT):
        self.cloud_particles = [particle for particle in self.cloud_particles if particle[0][1] < SCREEN_HEIGHT]
