import pygame
from pygame.locals import *

class Button:
    buttonCount = 0
    buttonSpacing = 48

    def __init__(self, label, bg):
        self.label = label
        self.id = Button.buttonCount + 1
        self.w = 130
        self.h = 32
        self.bg = bg
        self.x = bg[0] + (bg[2] - self.w) / 2
        self.y = bg[1] + (Button.buttonCount + 0.5) * Button.buttonSpacing
        Button.buttonCount += 1
        self.pressed = False
        self.color = (50, 95, 149)
        self.font = pygame.font.SysFont(None, 20)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 2)
        if self.mouseHover() or self.pressed:
            pygame.draw.rect(screen, (27, 52, 82), (self.x + 2, self.y + 2, self.w - 4, self.h - 4))
        else:
            pygame.draw.rect(screen, self.color, (self.x + 2, self.y + 2, self.w - 4, self.h - 4))
        label_surface = self.font.render(self.label, True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(self.x + self.w / 2, self.y + self.h / 2))
        screen.blit(label_surface, label_rect)

    def mousepressed(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.x < mouse_pos[0] < self.x + self.w and self.y < mouse_pos[1] < self.y + self.h

    def mouseHover(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.x < mouse_pos[0] < self.x + self.w and self.y < mouse_pos[1] < self.y + self.h
