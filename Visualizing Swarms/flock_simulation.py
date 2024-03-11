import sys
import pygame
from pygame.locals import *
from boid import Boid

pygame.init()

WIDTH, HEIGHT = 640, 360
BG_COLOR = (50, 50, 50)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
flock = []

def setup():
    for i in range(150):
        flock.append(Boid(WIDTH / 2, HEIGHT / 2))


def draw():
    screen.fill(BG_COLOR)
    for boid in flock:
        boid.flock(flock)
        boid.update()
        boid.borders(WIDTH, HEIGHT)
        boid.render(screen)


def main():
    setup()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                flock.append(Boid(x, y))

        draw()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
