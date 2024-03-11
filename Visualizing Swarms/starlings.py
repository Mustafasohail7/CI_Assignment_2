import pygame
import random
import math

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Starlings:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.angle = random.randint(0, 360)  # Initial angle
        self.direction = random.randint(0, 360)  # Initial direction in degrees
        self.speed = 3  # Initial speed

    def move(self):
        # Update position based on direction and speed
        radian_angle = math.radians(self.angle)  # Convert degrees to radians for trigonometric functions
        self.x += self.speed * math.cos(radian_angle)
        self.y -= self.speed * math.sin(radian_angle)  # Minus because pygame's y-coordinate increases downwards

        # Limit the change in angle to avoid steep turns
        max_angle_change = 30  # Adjust this value to control the maximum change in angle
        angle_change = random.randint(-max_angle_change, max_angle_change)
        self.angle += angle_change

        # Wrap around the screen if the Starlings goes out of bounds
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0

    def draw(self, screen):
        Starlings_surface = pygame.Surface((40, 40), pygame.SRCALPHA)

        points = [(20, 0), (0, 40), (40, 40)]

        rotated_points = [(20 + (x - 20) * math.cos(math.radians(self.angle)) - (y - 20) * math.sin(math.radians(self.angle)),
                          20 + (x - 20) * math.sin(math.radians(self.angle)) + (y - 20) * math.cos(math.radians(self.angle))) 
                          for x, y in points]
        
        pygame.draw.polygon(Starlings_surface, WHITE, rotated_points)

        Starlings_rect = Starlings_surface.get_rect()

        Starlings_rect.center = (self.x, self.y)

        screen.blit(Starlings_surface, Starlings_rect)
