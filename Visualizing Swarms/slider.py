import pygame
from pygame.locals import *
from button import Button

class Slider:
    sliderCount = 0

    def __init__(self, label, low, high, default, bg):
        self.low = low
        self.high = high
        self.val = default
        self.label = label
        self.bg = bg
        self.x = bg[0] + (bg[2] - 120) / 2
        if Slider.sliderCount == 0:
            self.y = bg[1] + (Button.buttonCount + 1) * Button.buttonSpacing
            Slider.sliderCount = Button.buttonCount
        else:
            self.y = bg[1] + (Slider.sliderCount + 1) * Button.buttonSpacing
        self.rectx = self.x + (self.val - self.low) / (self.high - self.low) * 120
        self.recty = self.y - 10
        Slider.sliderCount += 1

    def draw(self, screen):
        pygame.draw.line(screen, (200, 200, 200), (self.x, self.y), (self.x + 120, self.y), 4)
        if pygame.mouse.get_pressed()[0] and pygame.Rect(self.rectx, self.recty, 15, 20).collidepoint(pygame.mouse.get_pos()):
            self.rectx = pygame.mouse.get_pos()[0]
        self.rectx = max(min(self.rectx, self.x + 120), self.x)
        pygame.draw.rect(screen, (255, 255, 255), (self.rectx, self.recty, 15, 20))
        font = pygame.font.SysFont(None, 12)
        val_text = font.render(str(int(self.val)), True, (0, 0, 0))
        label_text = font.render(self.label, True, (255, 255, 255))
        screen.blit(val_text, (self.rectx + 8, self.recty + 8))
        screen.blit(label_text, (self.x + 60, self.y + 20))
