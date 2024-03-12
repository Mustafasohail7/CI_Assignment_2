import pygame

class TextBox:
    def __init__(self, label, bg):
        self.label = label
        self.bg = bg
        self.font = pygame.font.SysFont(None, 20)
        self.text = "Initial Value"
        self.value = 0
        self.active = False
        self.color = (0, 0, 0)
        self.rect = pygame.Rect(bg)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.active_color = (0, 0, 0)

    def draw(self, screen):
        text_box_width = 110  # Adjust as needed
        text_box_height = 30  # Adjust as needed
        text_box_color = (200, 200, 200)  # Background color
        border_color = (0, 0, 0)  # Border color
        pygame.draw.rect(screen, text_box_color, self.rect.inflate(text_box_width, text_box_height))
        pygame.draw.rect(screen, border_color, self.rect.inflate(text_box_width, text_box_height), 2)

        # Render the text surface with a larger font size
        font_size = 16  # Adjust as needed
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(self.text, True, (0, 0, 0))
        # Position the text surface in the center of the text box
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.text = ""
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            self.color = self.active_color if self.active else (0, 0, 0)
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Update the text surface
                self.text_surface = self.font.render(self.text, True, self.color)
