from random import random
from math import cos, sin, radians, sqrt, atan2
import pygame

class Boid:
    def __init__(self, x, y, speed, maxforce):
        self.position = (x, y)
        self.velocity = (cos(random() * 2 * 3.14), sin(random() * 2 * 3.14))
        self.acceleration = (0, 0)
        self.r = 2.0
        self.maxspeed = speed
        self.maxforce = maxforce

    def apply_force(self, force):
        self.acceleration = (self.acceleration[0] + force[0], self.acceleration[1] + force[1])

    def flock(self, boids):
        sep = self.separate(boids)
        ali = self.align(boids)
        coh = self.cohesion(boids)
        sep = (sep[0] * 1.5, sep[1] * 1.5)
        ali = (ali[0] * 1.0, ali[1] * 1.0)
        coh = (coh[0] * 1.0, coh[1] * 1.0)
        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)

    def update(self):
        self.velocity = (self.velocity[0] + self.acceleration[0], self.velocity[1] + self.acceleration[1])
        mag = sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
        if mag > self.maxspeed:
            self.velocity = (self.velocity[0] / mag * self.maxspeed, self.velocity[1] / mag * self.maxspeed)
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.acceleration = (0, 0)

    def seek(self, target):
        desired = (target[0] - self.position[0], target[1] - self.position[1])
        desired_mag = sqrt(desired[0] ** 2 + desired[1] ** 2)
        desired = (desired[0] / desired_mag * self.maxspeed, desired[1] / desired_mag * self.maxspeed)
        steer = (desired[0] - self.velocity[0], desired[1] - self.velocity[1])
        steer_mag = sqrt(steer[0] ** 2 + steer[1] ** 2)
        steer = (steer[0] / steer_mag * self.maxforce, steer[1] / steer_mag * self.maxforce)
        return steer

    def render(self, canvas):
        # Add comments explaining the logic here
        theta = atan2(self.velocity[1], self.velocity[0]) + radians(90)
        fill_color = (0, 0, 0)  
        triangle_points = [(-self.r, self.r), (self.r, self.r), (0, -self.r * 2)]
        
        rotated_triangle_points = []
        for point in triangle_points:
            rotated_x = point[0] * cos(theta) - point[1] * sin(theta)
            rotated_y = point[0] * sin(theta) + point[1] * cos(theta)
            rotated_triangle_points.append((rotated_x, rotated_y))

        adjusted_triangle_points = [(x + self.position[0], y + self.position[1]) for x, y in rotated_triangle_points]

        pygame.draw.polygon(canvas, fill_color, adjusted_triangle_points)

    def borders(self, width, height):
        if self.position[0] < -self.r:
            self.position = (width + self.r, self.position[1])
        if self.position[1] < -self.r:
            self.position = (self.position[0], height + self.r)
        if self.position[0] > width + self.r:
            self.position = (-self.r, self.position[1])
        if self.position[1] > height + self.r:
            self.position = (self.position[0], -self.r)

    def separate(self, boids):
        desired_separation = 25.0
        steer = (0, 0)
        count = 0
        for other in boids:
            d = sqrt((self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2)
            if 0 < d < desired_separation:
                diff = ((self.position[0] - other.position[0]) / d, (self.position[1] - other.position[1]) / d)
                steer = (steer[0] + diff[0], steer[1] + diff[1])
                count += 1
        if count > 0:
            steer = (steer[0] / count, steer[1] / count)
        if sqrt(steer[0] ** 2 + steer[1] ** 2) > 0:
            steer_mag = sqrt(steer[0] ** 2 + steer[1] ** 2)
            steer = (steer[0] / steer_mag * self.maxspeed, steer[1] / steer_mag * self.maxspeed)
            steer = (steer[0] - self.velocity[0], steer[1] - self.velocity[1])
            steer_mag = sqrt(steer[0] ** 2 + steer[1] ** 2)
            steer = (steer[0] / steer_mag * self.maxforce, steer[1] / steer_mag * self.maxforce)
        return steer

    def align(self, boids):
        neighbordist = 50
        sum = (0, 0)
        count = 0
        for other in boids:
            d = sqrt((self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2)
            if 0 < d < neighbordist:
                sum = (sum[0] + other.velocity[0], sum[1] + other.velocity[1])
                count += 1
        if count > 0:
            sum = (sum[0] / count, sum[1] / count)
            sum_mag = sqrt(sum[0] ** 2 + sum[1] ** 2)
            sum = (sum[0] / sum_mag * self.maxspeed, sum[1] / sum_mag * self.maxspeed)
            steer = (sum[0] - self.velocity[0], sum[1] - self.velocity[1])
            steer_mag = sqrt(steer[0] ** 2 + steer[1] ** 2)
            steer = (steer[0] / steer_mag * self.maxforce, steer[1] / steer_mag * self.maxforce)
            return steer
        else:
            return (0, 0)

    def cohesion(self, boids):
        neighbordist = 50
        sum = (0, 0)
        count = 0
        for other in boids:
            d = sqrt((self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2)
            if 0 < d < neighbordist:
                sum = (sum[0] + other.position[0], sum[1] + other.position[1])
                count += 1
        if count > 0:
            sum = (sum[0] / count, sum[1] / count)
            return self.seek(sum)
        else:
            return (0, 0)
