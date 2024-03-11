from button import Button
from slider import Slider

class GUI:
    def __init__(self, screen_width, screen_height):
        self.buttons = []
        self.sliders = []
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Define the dimensions for the GUI area (20% of the screen width)
        gui_width = self.screen_width // 5
        gui_height = self.screen_height

        # Define the position and dimensions for the buttons and sliders
        button_width = 20
        button_height = 15
        slider_width = 20
        slider_height = 10

        # Position the buttons and sliders relative to the GUI area
        button_x = (self.screen_width - gui_width) + (gui_width - button_width) // 2
        slider_x = (self.screen_width - gui_width) + (gui_width - slider_width) // 2

        button_y = gui_height // 10
        button_spacing = button_height * 1.5
        slider_y = gui_height // 5

        # Create buttons
        self.buttons.append(Button('Add Bird', (button_x, button_y + button_spacing, button_width, button_height)))
        self.buttons.append(Button('Remove Bird', (button_x, button_y + button_spacing, button_width, button_height)))
        self.buttons.append(Button('Start Simulation', (button_x, button_y + button_spacing, button_width, button_height)))
        self.buttons.append(Button('Restart Simulation', (button_x, button_y + button_spacing, button_width, button_height)))

        # Create sliders
        self.sliders.append(Slider('Number of Birds', 1, 500, 1, (slider_x, slider_y + slider_height, slider_width, slider_height)))
        self.sliders.append(Slider('Speed', 1, 10, 1, (slider_x, slider_y + slider_height, slider_width, slider_height)))
        self.sliders.append(Slider('Max Force', 0.01, 0.5, 0.01, (slider_x, slider_y + slider_height, slider_width, slider_height)))

    def draw(self, screen):  
        for button in self.buttons:
            button.draw(screen)
        for slider in self.sliders:
            slider.draw(screen)

    def mouseHover(self):
        for button in self.buttons:
            if button.mouseHover():
                return button.label
        return None

    def mousepressed(self):
        for button in self.buttons:
            if button.mousepressed():
                return button.label
        return None

    def getSliderValues(self):
        values = {}
        for slider in self.sliders:
            values[slider.label] = slider.val
        return values

    def toggleButton(self, label):
        for button in self.buttons:
            if button.label == label:
                button.pressed = not button.pressed
