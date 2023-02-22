import pygame as pg
import random
import numpy
from widgets import *
pg.init()
DEFAULT_PARAMS_ALL = {"mutation_rate": 0.95,
                       "mutation_importance": 1.5,
                       "size": 20,
                       "speed": 4.5,
                       "reach": 40,
                       "satiety": 0}

DEFAULT_PARAMS_CH = {  "size",
                        "speed",
                        "reach",
                        "mutationimportance"}
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
random.shuffle(FAMILY_NAMES_AND_COLORS)
DEFAULT_FAMILY_PARAMS = iter(FAMILY_NAMES_AND_COLORS)

POPULATION = 1
FIELD_POSITION = (110, 120, 900, 500)
FAMILY_NUM = 6


DEFAULT_WORLD_VARS = {"food_amount": 20,
                       "predator_size": 1.1}


FONT = pg.font.SysFont("calibri", 30)

BUTTONS_POSITIONS = {(1150, 600, 180, 70): ("New World", (150, 150, 150), True),
                     (1150, 500, 180, 70): ("New Day", (150, 150, 150), True)}

class Field:
    def __init__(self):
        self.pos = (110, 120, 900, 500)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.x_diff = self.pos[2]
        self.y_diff = self.pos[3]

    def get_pos_border(self):
        random_pos = random.random() * (self.pos[2]*2+self.pos[3]*2) + self.x
        if random_pos < self.x + self.x_diff:
            return (random_pos, self.y)
        random_pos -= self.x + self.x_diff
        if random_pos < self.y_diff:
            return (self.x+self.x_diff,random_pos+self.y)
        random_pos -= self.y_diff
        if random_pos < self.x_diff:
            return (random_pos+self.x, self.y+self.y_diff)
        random_pos -= self.x_diff
        return (self.x,random_pos+self.y)
FIELD = Field()


