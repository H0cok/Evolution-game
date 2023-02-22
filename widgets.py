import pygame as pg



class Button:
    def __init__(self, name, text, coords, color, color_pressed, text_color, pressed, active):
        self.name = name
        self.text = text
        self.pos = coords
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
        self.buttons.sort(key=lambda x: sum(x.color))
        for idx, button in enumerate(self.buttons):
            button.pos = (self.pos[0], self.pos[1] + self.pos[3] * (1 + idx), self.pos[2], self.pos[3])
            button.rect.update(button.pos)
    def deactivate(self):
        for button in self.buttons:
            button.active = False







class TextInput:
    def __init__(self, name, text, coords, color, color_pressed, text_color, pressed, active):
        self.name = name
        self.text = text
        self.pos = coords
        self.color = color
        self.color_pressed = color_pressed
        self.text_color = text_color
        self.pressed = pressed
        self.active = active
        self.rect = pg.Rect(self.pos)
















