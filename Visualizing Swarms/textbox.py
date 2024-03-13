import pygame

class Textbox:
    def __init__(self, label, initial_value, rect):
        self.label = label
        self.value = str(initial_value)
        self.rect = pygame.Rect(rect)
        self.font = pygame.font.Font(None, 16)
        self.active = False

    def draw(self, screen):
        color = (255, 255, 255) if self.active else (200, 200, 200)
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(f'{self.label}: {self.value}', True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.value = self.value[:-1]
                else:
                    self.value += event.unicode

    def get_value(self):
        try:
            return int(self.value)
        except ValueError:
            return 0
