from random import random
from math import cos, sin, radians, sqrt
from typing import List
from PVector import PVector
import pygame

class Boid:
    def __init__(self, x, y, speed, maxforce):
        self.position = PVector(x, y)
        self.velocity = PVector(cos(random() * 2 * 3.14), sin(random() * 2 * 3.14))
        self.acceleration = PVector(0, 0)
        self.r = 2.0
        self.maxspeed = speed
        self.maxforce = maxforce

    def applyForce(self, force):
        self.acceleration.add(force)

    def flock(self, boids: List['Boid']):
        sep = self.separate(boids)
        ali = self.align(boids)
        coh = self.cohesion(boids)
        sep.mult(1.5)
        ali.mult(1.0)
        coh.mult(1.0)
        self.applyForce(sep)
        self.applyForce(ali)
        self.applyForce(coh)

    def update(self):
        self.velocity.add(self.acceleration)
        self.velocity.x = min(max(self.velocity.x, -self.maxspeed), self.maxspeed)
        self.velocity.y = min(max(self.velocity.y, -self.maxspeed), self.maxspeed)
        self.position.add(self.velocity)
        self.acceleration.mult(0)

    def seek(self, target):
        desired = PVector(target.x - self.position.x, target.y - self.position.y)
        desired.normalize()
        desired.mult(self.maxspeed)
        steer = PVector(desired.x - self.velocity.x, desired.y - self.velocity.y)
        steer.limit(self.maxforce)
        return steer

    def render(self, canvas):
        theta = self.velocity.heading() + radians(90)
        fill_color = (0, 0, 0)  # Adjust color as needed
        triangle_points = [(-self.r, self.r), (self.r, self.r), (0, -self.r * 2)]
        
        rotated_triangle_points = []
        for point in triangle_points:
            rotated_x = point[0] * cos(theta) - point[1] * sin(theta)
            rotated_y = point[0] * sin(theta) + point[1] * cos(theta)
            rotated_triangle_points.append((rotated_x, rotated_y))

        # Adjust the rotated triangle position based on the boid's current position
        adjusted_triangle_points = [(x + self.position.x, y + self.position.y) for x, y in rotated_triangle_points]

        # Draw the rotated triangle on the canvas
        pygame.draw.polygon(canvas, fill_color, adjusted_triangle_points)

    def borders(self, width, height):
        if self.position.x < -self.r:
            self.position.x = width + self.r
        if self.position.y < -self.r:
            self.position.y = height + self.r
        if self.position.x > width + self.r:
            self.position.x = -self.r
        if self.position.y > height + self.r:
            self.position.y = -self.r

    def separate(self, boids: List['Boid']):
        desired_separation = 25.0
        steer = PVector(0, 0)
        count = 0
        for other in boids:
            d = sqrt((self.position.x - other.position.x) ** 2 + (self.position.y - other.position.y) ** 2)
            if 0 < d < desired_separation:
                diff = PVector(self.position.x - other.position.x, self.position.y - other.position.y)
                diff.normalize()
                diff.div(d)
                steer.add(diff)
                count += 1
        if count > 0:
            steer.div(count)
        if steer.mag() > 0:
            steer.normalize()
            steer.mult(self.maxspeed)
            steer.sub(self.velocity)
            steer.limit(self.maxforce)
        return steer

    def align(self, boids: List['Boid']):
        neighbordist = 50
        sum = PVector(0, 0)
        count = 0
        for other in boids:
            d = sqrt((self.position.x - other.position.x) ** 2 + (self.position.y - other.position.y) ** 2)
            if 0 < d < neighbordist:
                sum.add(other.velocity)
                count += 1
        if count > 0:
            sum.div(count)
            sum.normalize()
            sum.mult(self.maxspeed)
            steer = PVector(sum.x - self.velocity.x, sum.y - self.velocity.y)
            steer.limit(self.maxforce)
            return steer
        else:
            return PVector(0, 0)

    def cohesion(self, boids: List['Boid']):
        neighbordist = 50
        sum = PVector(0, 0)
        count = 0
        for other in boids:
            d = sqrt((self.position.x - other.position.x) ** 2 + (self.position.y - other.position.y) ** 2)
            if 0 < d < neighbordist:
                sum.add(other.position)
                count += 1
        if count > 0:
            sum.div(count)
            return self.seek(sum)
        else:
            return PVector(0, 0)
