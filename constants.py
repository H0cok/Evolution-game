import pygame as pg
import random
import numpy
from widgets import Button, SliderButton, TextInput

pg.init()
DISPLAY_RES = (1420, 720)



DEFAULT_PARAMS_ALL = {"mutation_rate": 0.95,
                      "mutation_importance": 2,
                      "size": 20,
                      "speed": 8,
                      "reach": 40,
                      "satiety": 0}

UPDATE_AI_SPEED = 10

DEFAULT_PARAMS_CH = {"size",
                     "speed",
                     "reach",
                     }
FAMILY_NAMES_AND_COLORS = [['green foxes', (23, 152, 161)], ['green wolfs', (110, 22, 167)],
                           ['green cats', (202, 228, 97)], ['green dogs', (99, 86, 224)],
                           ['green sharks', (189, 171, 192)], ['yellow foxes', (67, 187, 34)],
                           ['yellow wolfs', (207, 9, 148)], ['yellow cats', (206, 167, 159)],
                           ['yellow dogs', (85, 60, 38)], ['yellow sharks', (80, 132, 216)],
                           ['orange foxes', (253, 236, 104)], ['orange wolfs', (47, 58, 170)],
                           ['orange cats', (178, 166, 111)], ['orange dogs', (139, 18, 29)],
                           ['orange sharks', (54, 77, 254)], ['blue foxes', (215, 28, 81)],
                           ['blue wolfs', (37, 167, 42)], ['blue cats', (179, 60, 86)],
                           ['blue dogs', (237, 241, 26)], ['blue sharks', (152, 28, 135)],
                           ['purple foxes', (252, 30, 19)], ['purple wolfs', (99, 184, 215)],
                           ['purple cats', (191, 2, 134)], ['purple dogs', (42, 130, 151)],
                           ['purple sharks', (91, 26, 170)], ['black foxes', (134, 253, 169)],
                           ['black wolfs', (232, 92, 75)], ['black cats', (151, 65, 84)],
                           ['black dogs', (119, 129, 85)], ['black sharks', (54, 46, 64)],
                           ['white foxes', (132, 8, 176)], ['white wolfs', (177, 54, 248)],
                           ['white cats', (177, 72, 30)], ['white dogs', (48, 23, 3)],
                           ['white sharks', (106, 24, 125)]]



POPULATION = 2
FIELD_POSITION = (110, 120, 900, 500)
FAMILY_NUM = 10

DEFAULT_WORLD_VARS = {"food_amount": 35,
                      "predator_size": 1.1}




FONTS = {num: pg.font.SysFont("calibri", num) for num in [14, 16, 30]}
WIDGETS_OBJECTS = {"Game":
                       [Button("New World", "New World", (1150, 600, 180, 70),
                               (150, 150, 150), (170, 170, 170), (255, 255, 255), False, True),

                        Button("New Day", "New Day", (1150, 500, 180, 70),
                               (150, 150, 150), (170, 170, 170), (255, 255, 255), False, True),

                        SliderButton("Slider", "Slider", (1150, 50, 180, 70),
                                     (150, 150, 150), (170, 170, 170), (255, 255, 255), False, True,
                                     [], (1150, 125, 180, 370), (150, 150, 150)),
                        TextInput("Day Input", "", (1350, 500, 50, 70),
                                  (200, 200, 200), (240, 240, 240), (0, 0, 0), False, True)],
                   "World_settings":
                       [SliderButton("Slider", "Edit Guys", (100, 150, 180, 70),
                                     (150, 150, 150), (170, 170, 170), (255, 255, 255), False, True,
                                     [], (100, 225, 180, 370), (150, 150, 150)),

                        SliderButton("Family Stats", "Family Stats", (1000, 150, 180, 70),
                                     (150, 150, 150), (170, 170, 170), (255, 255, 255), True, True,
                                     [], (1000, 225, 180, 370), (200, 200, 200)),


                        Button("Exit", "X", (1200, 50, 50, 50),
                               (150, 150, 150), (170, 170, 170), (255, 255, 255), False, True),
                        Button("Edit Family", "Edit Family", (100, 280, 180, 70),
                               (150, 150, 150), (170, 170, 170), (255, 255, 255), False, True),

                        # TextInput("speed", "", (550, 150 + 100 * 0, 50, 70),
                        #            (210, 210, 210), (240, 240, 240), (0, 0, 0), False, False),
                        #
                        # TextInput("reach", "", (550, 150 + 100 * 1, 50, 70),
                        #            (210, 210, 210), (240, 240, 240), (0, 0, 0), False, False),
                        #
                        # TextInput("size", "", (550, 150 + 100 * 2, 50, 70),
                        #            (210, 210, 210), (240, 240, 240), (0, 0, 0), False, False)


                       ]

                   }


WIDGETS_OBJECTS["World_settings"].extend([TextInput(name, "", (550, 150 + 100 * i, 50, 70),
                              (210, 210, 210), (240, 240, 240), (0, 0, 0), False, False)
                                          for i, name in enumerate(DEFAULT_PARAMS_CH)])


print(WIDGETS_OBJECTS["World_settings"])
class Field:
    def __init__(self):
        self.pos = FIELD_POSITION
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.x_diff = self.pos[2]
        self.y_diff = self.pos[3]

    def get_pos_border(self):
        random_pos = random.random() * (self.pos[2] * 2 + self.pos[3] * 2) + self.x
        if random_pos < self.x + self.x_diff:
            return random_pos, self.y
        random_pos -= self.x + self.x_diff
        if random_pos < self.y_diff:
            return self.x + self.x_diff, random_pos + self.y
        random_pos -= self.y_diff
        if random_pos < self.x_diff:
            return random_pos + self.x, self.y + self.y_diff
        random_pos -= self.x_diff
        return self.x, random_pos + self.y


FIELD = Field()
