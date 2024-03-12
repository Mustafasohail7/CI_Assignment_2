from button import Button
from slider import Slider
from textbox import TextBox

class GUI:
    def __init__(self, screen_width, screen_height):
        self.buttons = []
        self.sliders = []
        self.text_boxes = []
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

        # Position the buttons, sliders, and text boxes relative to the GUI area
        button_x = (self.screen_width - gui_width) + (gui_width - button_width) // 2
        slider_x = (self.screen_width - gui_width) + (gui_width - slider_width) // 2

        button_y = gui_height // 10
        button_spacing = button_height * 1.5
        slider_y = gui_height // 5

        # Create buttons
        self.buttons.append(Button('Add Bird', (button_x, button_y + button_spacing, button_width, button_height)))
        self.buttons.append(Button('Remove Bird', (button_x, button_y + button_spacing, button_width, button_height)))
        self.buttons.append(Button('Start Simulation', (button_x, button_y + button_spacing, button_width, button_height)))
        self.buttons.append(Button('Stop Simulation', (button_x, button_y + button_spacing, button_width, button_height)))

        # Create text box for Number of Birds
        self.text_box = TextBox('Number of Birds', (slider_x, slider_y + slider_height + 200, slider_width, slider_height))
        self.text_boxes.append(self.text_box)  # Add the text box to the list

        # Create sliders
        self.sliders.append(Slider('Speed', 1, 10, 1, (slider_x, slider_y + slider_height + 25, slider_width, slider_height)))
        self.sliders.append(Slider('Max Force', 0.01, 0.5, 0.01, (slider_x, slider_y + slider_height + 25, slider_width, slider_height)))

    def draw(self, screen):  
        for button in self.buttons:
            button.draw(screen)
        for slider in self.sliders:
            slider.draw(screen)
        for text_box in self.text_boxes:
            text_box.draw(screen)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
        for slider in self.sliders:
            slider.handle_event(event)
        self.text_box.handle_event(event)

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

    def getTextBoxValues(self):
        values = {}
        for text_box in self.text_boxes:
            values[text_box.label] = int(text_box.value)
        return values
