import pygame as pg



class Button:
    def __init__(self, name, text, coords, color, color_pressed, text_color, pressed, active):
        self.name = name
        self.text = text
        self.pos = coords
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.x_diff = self.pos[2]
        self.y_diff = self.pos[3]
        self.color = color
        self.color_pressed = color_pressed
        self.text_color = text_color
        self.pressed = pressed
        self.active = active
        self.rect = pg.Rect(self.pos)



class SliderButton(Button):
    def __init__(self, name, text, coords, color, color_pressed, text_color, pressed, active, buttons, field_coords, field_color):
        super().__init__(name, text, coords, color, color_pressed, text_color, pressed, active)
        self.buttons = buttons
        self.field_coords = field_coords
        self.field_color = field_color
        self.field_rect = pg.Rect(self.field_coords)

    def add_button(self, button):
        self.buttons.append(button)
        for idx, button in enumerate(self.buttons):
            button.pos = (self.x, self.y + self.y_diff*(1 + idx), self.x_diff, self.y_diff)
            button.rect.update(button.pos)
    def deactivate(self):
        for button in self.buttons:
            button.active = False















