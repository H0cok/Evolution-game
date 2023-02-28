import pygame as pg
pg.init()

class Button:
    def __init__(self, name, text, coords, color, color_pressed, text_color, pressed, active, font=30):
        self.name = name
        self.text = text
        self.pos = coords
        self.color = color
        self.color_pressed = color_pressed
        self.text_color = text_color
        self.pressed = pressed
        self.active = active
        self.rect = pg.Rect(self.pos)
        self.font = font


class SliderButton(Button):
    def __init__(self, name, text, coords, color, color_pressed, text_color, pressed, active, buttons, field_coords,
                 field_color):
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

    def scroll(self, pos, event):
        if self.field_rect.collidepoint(pos) and event.button in {4, 5}:
            if event.button == 4:
                move_sign = 1
            else:
                move_sign = -1
            for button in self.buttons:
                button.pos = (button.pos[0], button.pos[1] + 30 * move_sign, button.pos[2], button.pos[3])
                button.rect.update(button.pos)
            return True
        else:
            return False


class TextInput:
    def __init__(self, name, text, coords, color, color_pressed, text_color, pressed, active, font=30):
        self.name = name
        self.text = text
        self.pos = coords
        self.color = color
        self.color_pressed = color_pressed
        self.text_color = text_color
        self.pressed = pressed
        self.active = active
        self.rect = pg.Rect(self.pos)
        self.font = font

    def change_text(self, event, numeric=False):
        if event.key == pg.K_BACKSPACE:
            self.text = self.text[:-1]

        elif event.key == pg.K_RETURN and (self.text.isnumeric() or not numeric):
            self.pressed = False
            return self.text
        else:
            self.text += event.unicode
