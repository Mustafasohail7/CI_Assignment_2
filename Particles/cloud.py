import pygame
import random

class Clouds:
    def __init__(self):
        self.cloud_particles = []

    def emit(self, screen):
        if self.cloud_particles:
            self.delete(SCREEN_HEIGHT=600)
            for particle in self.cloud_particles:
                # Update particle position or any other properties
                particle[0][0] += 0.5  # Move the particle in the x direction
                particle[0][1] += random.uniform(-0.2, 0.2)  # Move the particle in the y direction
                
                # Draw translucent circles to create a softer cloud-like appearance
                radius = particle[2]  # Get the radius of the particle
                alpha = int(255 * (radius / 50))  # Adjust alpha based on particle size
                color = particle[1]  # Get the color of the particle
                color.a = alpha  # Set alpha value for transparency
                pygame.draw.circle(screen, color, (int(particle[0][0]), int(particle[0][1])), int(radius))


    def add(self, pos_x, pos_y):
        # Add small cloud particles at the specified position
        hue = random.randint(210, 220)  # Random hue for clouds within the range of white to gray
        saturation = random.uniform(0, 3)  # Lower saturation for closer to white appearance
        value = random.uniform(90, 100)  # Higher value for closer to white appearance

        # Add shadow to the clouds
        shadow_hue = random.randint(210, 220)  # Random hue for shadow within the range of white to gray
        shadow_saturation = random.uniform(0, 10)  # Lower saturation for shadow closer to white appearance
        shadow_value = random.uniform(70, 80)  # Lower value for shadow closer to black appearance

        # Create color objects for cloud and shadow
        color = pygame.Color(0)
        color.hsva = (hue, saturation, value, 100)  # Set the color using HSV values with full alpha
        shadow_color = pygame.Color(0)
        shadow_color.hsva = (shadow_hue, shadow_saturation, shadow_value, 100)  # Set the shadow color using HSV values with full alpha

        num_particles = random.randint(3000, 5000)  # Number of particles for each cloud

        cloud_size = 50  # Adjust cloud size as needed
        spread_factor = 0.35  # Adjust spread factor to control particle spread

        for _ in range(num_particles):
            # Randomize position within the cloud area with reduced variation
            offset_x = random.gauss(0, cloud_size * spread_factor)  # Gaussian distribution for x offset
            offset_y = random.gauss(0, cloud_size * spread_factor / 2)  # Gaussian distribution for y offset
            particle_x = pos_x + offset_x
            particle_y = pos_y + offset_y
            radius = random.uniform(1, 5)  # Random radius for each particle

            # Randomly choose whether to draw a cloud particle or a shadow particle
            if random.random() < 0.99:  # 90% chance of drawing a cloud particle
                self.cloud_particles.append([[particle_x, particle_y], color, radius])
            else:  # 10% chance of drawing a shadow particle
                self.cloud_particles.append([[particle_x, particle_y], shadow_color, radius])
        
    def delete(self, SCREEN_HEIGHT):
        # Delete particles that have gone off-screen or expired
        self.cloud_particles = [particle for particle in self.cloud_particles if particle[0][1] < SCREEN_HEIGHT]
