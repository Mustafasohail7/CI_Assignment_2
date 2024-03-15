import pygame
import random

class RainDrops:
    def __init__(self):
        self.raindrops = []

    def emit(self, screen,speed,windpressure,dampen):
        if self.raindrops:
            self.delete()
            for i in range(len(self.raindrops)):
                particle = self.raindrops[i]
                if particle[0][1] >= screen.get_height() - particle[1]:
                        particle[0][1] = screen.get_height() - (particle[1])
                        particle[1] = 0
                else:
                    particle[0][0] += particle[2][1] # Move the particle in the y direction
                    particle[0][1] += particle[2][0] + speed # Move the particle in the x direction
                particle[2][1] += windpressure  # Acceleration factor to the particle, this will be used to simulate the wind pressure
                particle[1] -= dampen # Dampen the particle size, that is how fast the particle will shrink/die off
              
                for j in range(i+1, len(self.raindrops)):
                    other_particle = self.raindrops[j]
                    distance = ((particle[0][0] - other_particle[0][0])**2 + (particle[0][1] - other_particle[0][1])**2)**0.5
                    if distance < particle[1] + other_particle[1]:
                        particle[2][0], other_particle[2][0] = other_particle[2][0], particle[2][0]
                        particle[2][1], other_particle[2][1] = other_particle[2][1], particle[2][1]
                            
                pygame.draw.circle(screen, (200, 230, 255), particle[0], int(particle[1]))

    def add(self, intervals, height, mean_raindrops, var_raindrops):
        num_raindrops = max(0, int(random.gauss(mean_raindrops, var_raindrops)))
        if intervals:
            for _ in range(num_raindrops):
                selected_cloud = random.choice(intervals)
                pos_x = random.randint(int(selected_cloud[0]), int(selected_cloud[1]))
                index = intervals.index(selected_cloud)
                pos_y = height[index]+10
                radius = random.uniform(5, 7.5)
                direction_x = random.randint(1, 5)
                direction_y = 0  # Ensure raindrops move downwards
                particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
                self.raindrops.append(particle_circle)


    def delete(self):
        particle_copy = [particle for particle in self.raindrops if particle[1] > 0]
        self.raindrops = particle_copy
