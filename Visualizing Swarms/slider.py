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
        self.clicked = False

    def draw(self, screen):
        pygame.draw.line(screen, (200, 200, 200), (self.x, self.y), (self.x + 120, self.y), 4)
        mouse_pressed = pygame.mouse.get_pressed()[0]  # Check if left mouse button is pressed
        if mouse_pressed and pygame.Rect(self.rectx, self.recty, 15, 20).collidepoint(pygame.mouse.get_pos()):
            self.rectx = pygame.mouse.get_pos()[0]
            self.clicked = True  # Set flag to True when slider is clicked
        elif not mouse_pressed:  # Check if left mouse button is released
            self.clicked = False  # Reset flag when mouse button is released outside slider area
        elif not self.clicked:  # Check if slider was not clicked
            self.rectx = self.x + (self.val - self.low) / (self.high - self.low) * 120
        self.rectx = max(min(self.rectx, self.x + 120), self.x)
        pygame.draw.rect(screen, (0, 0, 0), (self.rectx, self.recty, 15, 20))
        font = pygame.font.SysFont(None, 16)
        val_text = font.render(str(int(self.val)), True, (0, 0, 0))
        label_text = font.render(self.label, True, (0, 0, 0))
        screen.blit(val_text, (self.rectx, self.recty + 8))
        screen.blit(label_text, (self.x, self.y - 25))


