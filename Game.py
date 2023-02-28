import copy
import math
import numpy as np
from constants import *
import pygame as pg
from pygame.locals import *
from math import *
import time
from numpy import sign


class Params:
    """
    Class for manipulating with parameters of specific Family
    params_all - main dict with all parameters values
    params_ch - set with changeable parameters
    """

    def __init__(self,
                 params_all: dict,
                 params_ch=DEFAULT_PARAMS_CH,
                 mutation=False):
        if mutation:
            self.params_ch = params_ch
            self.params_all = self.change_auto(params_all)

        else:
            self.params_ch = params_ch
            self.params_all = params_all

    def change(self, param, value):
        self.params_all[param] = value

    def change_auto(self, params):
        change_parameter = random.choice(list(self.params_ch))
        change_sign = random.choice([-1, 1])
        mutation_percent = change_sign * random.random() * params["mutation_importance"] * 0.05
        if params["mutation_rate"] >= random.random():

            if change_parameter == "size":
                params["size"] = params["size"] + mutation_percent * DEFAULT_PARAMS_ALL["size"]
                params["speed"] = params["speed"] - mutation_percent * DEFAULT_PARAMS_ALL["speed"]

            elif change_parameter == "speed":
                params["speed"] = params["speed"] + mutation_percent * DEFAULT_PARAMS_ALL["speed"]
                params["reach"] = params["reach"] - mutation_percent * DEFAULT_PARAMS_ALL["reach"]

            elif change_parameter == "reach":
                params["reach"] = params["reach"] + mutation_percent * DEFAULT_PARAMS_ALL["reach"]
                params["size"] = params["size"] - mutation_percent * DEFAULT_PARAMS_ALL["size"]

            elif change_parameter == "mutation_importance":
                params["mutation_importance"] = params["mutation_importance"] \
                                                + mutation_percent * DEFAULT_PARAMS_ALL["mutation_importance"]
        return params


class Guy:
    def __init__(self, size, color, params, name):
        self.name = name
        self.pos = FIELD.get_pos_border()
        self.color = color
        self.size = size
        self.rect = pg.Rect(100, 100, self.size, self.size)
        self.rect.center = self.pos
        self.params = params
        self.goal = None
        self.direction = None
        self.closest_prey = (None, float("+inf"))

    def set_size(self, size):
        self.size = size
        self.rect.update(100, 100, self.size, self.size)
        self.rect.center = self.pos


class Family:
    def __init__(self,
                 params_family,
                 params_all=DEFAULT_PARAMS_ALL,
                 params_ch=DEFAULT_PARAMS_CH,
                 population=POPULATION
                 ):
        self.guy_number = iter(range(int(10e20)))
        self.population = population
        self.name = params_family[0]
        self.color = params_family[1]
        self.guys = [Guy(color=self.color,
                         size=DEFAULT_PARAMS_ALL["size"],
                         params=Params(params_all=dict(params_all),
                                       params_ch=params_ch
                                       ),
                         name=self.name + " " + str(next(self.guy_number))) for _ in range(population)]

    def add_guy(self, size, params):
        self.guys.append(Guy(color=self.color,
                             size=size,
                             params=params,
                             name=self.name + " " + str(next(self.guy_number))))


class Drawing:
    def __init__(self, screen, families):
        self.screen = screen
        self.families = families
        self.info = []

    def draw_stand(self):
        self.screen.fill((220, 220, 220))
        pg.draw.rect(self.screen, (150, 150, 150), pg.Rect(FIELD_POSITION), 2)
        pg.draw.rect(self.screen, (150, 150, 150), pg.Rect(1150, 600, 180, 70))
        for family in self.families:
            for guy in family.guys:
                rect = guy.rect
                pg.draw.circle(self.screen, guy.color, rect.center, guy.size / 2)
        self.draw_info()

    def draw_food(self, food):
        for food_item in food:
            if food_item.on_field:
                pg.draw.arc(self.screen, "red", food_item.rect, 0, 2 * pi)

    def draw_info(self, update=False):
        if update or not self.info:
            self.info = []

            self.families.sort(key=lambda x: len(x.guys), reverse=True)
            params = {param: [] for param in DEFAULT_PARAMS_CH}
            for guy in self.families[0].guys:
                for param in DEFAULT_PARAMS_CH:
                    params[param].append(guy.params.params_all[param])
            for param in DEFAULT_PARAMS_CH:
                value = np.round(np.mean(params[param]), 2)
                percent = np.round(100 * value / DEFAULT_PARAMS_ALL[param] - 100, 2)
                color = [255, 255, 255]
                if percent > 0:
                    # color[0] = color[2] = color[0] - color[0]*percent/100
                    color = [0, 205, 0]
                elif percent < 0:
                    # color[1] = color[2] = color[1] + color[1]*percent/100
                    color = [205, 0, 0]
                self.info.append([str(value) + "  " + str(percent) + "% " + param, color])

        for idx, row in enumerate(self.info):
            text = row[0]
            color = row[1]
            self.draw_text(self.screen, text, color, (5, 630 + idx * 16), FONTS[16])

    @staticmethod
    def draw_text(screen, text, color, pos, font=FONTS[30]):
        text_screen = font.render(text, True, color)
        text_rect = text_screen.get_rect()
        text_rect.topleft = pos
        screen.blit(text_screen, text_rect)


class FoodItem:
    def __init__(self):
        self.pos = (random.randint(FIELD.x + 5, FIELD.x + FIELD.x_diff - 5),
                    random.randint(FIELD.y + 5, FIELD.y + FIELD.y_diff - 5))
        self.rect = pg.Rect(self.pos, (5, 5))
        self.on_field = True


class ShowFPS:
    def __init__(self):
        self.prev_time = time.time()
        self.text_screen = FONTS[30].render(str("fps"), True, (0, 0, 0))
        self.text_rect = self.text_screen.get_rect()
        self.text_rect.center = (20, 20)

    def show_fps(self, screen, dt):
        if time.time() - self.prev_time > 0.1 and dt != 0:
            self.prev_time = time.time()
            self.text_screen = FONTS[30].render(str(round(1 / dt)), True, (0, 0, 0))
        screen.blit(self.text_screen, self.text_rect)


class Day:
    def __init__(self, food_amount):
        self.food_amount = food_amount
        self.food = [FoodItem() for _ in range(food_amount)]


class World:
    def __init__(self,
                 screen,
                 families: list[Family],
                 world_vars=DEFAULT_WORLD_VARS,
                 ):
        self.families = families
        self.world_vars = world_vars
        self.screen = screen
        self.widgets = copy.deepcopy(WIDGETS_OBJECTS["Game"])
        self.draw = Drawing(screen, families)
        self.days_num = 0
        self.update_ai_speed = UPDATE_AI_SPEED + 1
        self.day = None

    def new_day(self):
        self.day = Day(food_amount=self.world_vars['food_amount'],
                       )
        for family in self.families:
            for guy in family.guys:
                guy.params.params_all["satiety"] = 0

    def end_day(self):
        for family in self.families:
            new_family = []
            for num, guy in enumerate(family.guys):
                eaten_food = guy.params.params_all["satiety"]

                if eaten_food == 1:
                    new_family.append(guy)
                elif eaten_food > 1:
                    new_family.append(guy)
                    new_guy = Guy(color=guy.color,
                                  size=guy.params.params_all["size"],
                                  params=Params(params_all=dict(guy.params.params_all), mutation=True),
                                  name=family.name + " " + str(next(family.guy_number)))
                    new_guy.set_size(new_guy.params.params_all["size"])
                    new_guy.pos = FIELD.get_pos_border()
                    new_family.append(new_guy)
                guy.pos = FIELD.get_pos_border()
                guy.rect.center = guy.pos
            family.guys = new_family
        self.day = None
        self.days_num -= 1

    def play_day(self, dt):
        for family in self.families:
            for guy in family.guys:
                if self.day.food_amount <= 0:
                    self.end_day()
                    return None
                if not guy.goal or guy.direction:
                    closest_food = min(self.day.food,
                                       key=lambda x: abs(guy.pos[0] - x.pos[0]) + abs(guy.pos[1] - x.pos[1]))
                    guy.goal = closest_food

                else:
                    closest_food = guy.goal
                closest_predator = (None, float("+inf"))
                if self.update_ai_speed:
                    for family_c in self.families:
                        if family_c != family:
                            for guy_c in family_c.guys:
                                dist = (abs(guy.pos[0] - guy_c.pos[0]) + abs(guy_c.pos[1] - guy_c.pos[1]))
                                if guy_c.size > guy.size * DEFAULT_WORLD_VARS["predator_size"] and \
                                        dist < closest_predator[1]:
                                    closest_predator = (guy_c, dist)
                                elif guy.size > guy_c.size * DEFAULT_WORLD_VARS["predator_size"] and \
                                        dist < guy.closest_prey[1]:
                                    guy.closest_prey = (guy_c, dist)

                if guy.rect.colliderect(closest_food.rect):
                    closest_food.on_field = False
                    for food_num in range(self.day.food_amount):
                        if self.day.food[food_num] is closest_food:
                            self.day.food.pop(food_num)
                            self.day.food_amount -= 1
                            break
                    guy.goal = None
                    guy.params.params_all["satiety"] += 1

                elif guy.closest_prey[0] and guy.rect.colliderect(guy.closest_prey[0].rect):
                    for family_dead in self.families:
                        for idx, guy_dead in enumerate(family_dead.guys):
                            if guy_dead is guy.closest_prey[0]:
                                family_dead.guys.pop(idx)
                                break
                        else:
                            continue
                    print("eaten")
                    guy.closest_prey = (None, float("+inf"))
                    guy.params.params_all["satiety"] += 1

                else:
                    food_dist = abs(guy.pos[1] - closest_food.pos[1]) + abs(guy.pos[0] - closest_food.pos[0])
                    if food_dist > guy.closest_prey[1]:
                        closest_food = guy.closest_prey[0]
                        food_dist = abs(guy.pos[1] - closest_food.pos[1]) + abs(guy.pos[0] - closest_food.pos[0])
                    destination = closest_food.pos
                    if food_dist > guy.params.params_all["reach"]:
                        if not guy.direction or \
                                (abs(guy.direction[0] - guy.pos[0]) < 7 and (abs(guy.direction[1] - guy.pos[1]) < 7)):
                            guy.direction = (random.randint(FIELD.x, FIELD.x + FIELD.x_diff),
                                             random.randint(FIELD.y, FIELD.y + FIELD.y_diff))
                        destination = guy.direction
                    else:
                        guy.direction = None

                    direction = abs(guy.pos[0] - destination[0]) / \
                                (abs(guy.pos[1] - destination[1]) + abs(guy.pos[0] - destination[0]))

                    new_x = guy.pos[0] - dt * guy.params.params_all["speed"] * sign(
                        guy.pos[0] - destination[0]) * direction * 100
                    new_y = guy.pos[1] - dt * guy.params.params_all["speed"] * sign(guy.pos[1] - destination[1]) * (
                            1 - direction) * 100
                    guy.pos = (new_x, new_y)
                    guy.rect.center = guy.pos


class WorldSettings:
    def __init__(self, screen, family_name, family):
        self.widgets = copy.deepcopy(WIDGETS_OBJECTS["World_settings"])
        self.family_name = family_name
        self.family = family
        self.screen = screen
        self.draw()
        self.update_stats()


    def draw(self):
        pg.draw.rect(self.screen, (230, 230, 230, 100), Rect(0, 0, DISPLAY_RES[0], DISPLAY_RES[1]))
        gap = 40
        pg.draw.rect(self.screen, (200, 200, 200), Rect(gap, gap, DISPLAY_RES[0] - gap * 5, DISPLAY_RES[1] - gap * 2))
        Drawing.draw_text(self.screen, self.family_name, (40, 40, 40), (gap + 5, gap + 5))

    def update_stats(self):
        for widget in self.widgets:
            if widget.name == "Family Stats":
                widget.buttons = []
                break
        params = {param: [] for param in DEFAULT_PARAMS_ALL}
        for guy in self.family.guys:
            for param in DEFAULT_PARAMS_ALL:
                params[param].append(guy.params.params_all[param])

        for idx, param in enumerate(DEFAULT_PARAMS_ALL):
            value = np.round(np.mean(params[param]), 2)
            percent = np.round(100 * value / DEFAULT_PARAMS_ALL[param] - 100, 2)
            color = [200, 200, 200]
            if percent > 0:
                # color[0] = color[2] = color[0] - color[0]*percent/100
                color = [0, 205, 0]
            elif percent < 0:
                # color[1] = color[2] = color[1] + color[1]*percent/100
                color = [205, 0, 0]
            text = param + "  " + str(value) + "  " + str(percent) + "% "
            widget.buttons.append(Button(param, text, (1000, 150 + idx * 70, 180, 70),
                                         color, color, (0, 0, 0), True, True, font = 14))

            # Drawing.draw_text(self.screen, text, color, (5, 630 + idx * 16), FONT)


class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        pg.display.set_caption("Evolution")
        self.screen = pg.display.set_mode(DISPLAY_RES)
        self.scene = "Game"
        self.world = None
        self.worlds = {world_name: None for world_name in WIDGETS_OBJECTS.keys()}
        self.new_world()
        self.widgets = self.world.widgets
        self.fps = None

    def screen_game(self, dt, widgets, pos, event):
        if event:
            for widget in widgets:
                if widget.name == "Slider":
                    if not widget.buttons:
                        for family in self.world.families:
                            name = family.name
                            widget.add_button(Button(name, name, (1150, 500, 180, 70),
                                                     family.color, (170, 170, 170), (255, 255, 255), False,
                                                     False))
                    for button in widget.buttons:
                        if button.active and button.rect.collidepoint(pos):
                            if event.button == 1:

                                for family in self.world.families:
                                    if family.name == button.name:
                                        self.worlds["World_settings"] = WorldSettings(family_name=button.name,
                                                                                      family=family,
                                                                                      screen=self.screen)
                                        break
                                self.update_world("World_settings")

                                return None
                    widget.scroll(pos, event)
                if event.type == pg.MOUSEBUTTONDOWN:
                    if widget.rect.collidepoint(pos):
                        if widget.name == "New World":
                            widget.pressed = True
                            self.new_world()
                        if widget.name == "New Day" and self.world:
                            widget.pressed = True
                            self.world.days_num = 1
                        if widget.name == "Slider":
                            widget.pressed = not widget.pressed
                            widget.deactivate()
                        if widget.name == "Day Input":
                            widget.pressed = not widget.pressed

                elif event.type == pg.MOUSEBUTTONUP and \
                        widget.name in {"New World", "New Day"}:
                    widget.pressed = False

                elif event.type == pg.KEYDOWN and \
                        widget.pressed and isinstance(widget, TextInput):
                    text = widget.change_text(event, True)
                    if text:
                        self.world.days_num = int(widget.text)

        if self.world:
            self.world.draw.draw_stand()
            if not self.world.day:
                self.world.draw.draw_info(update=True)
                if self.world.days_num > 0 and not self.world.day:
                    self.world.new_day()

        if self.world.day:
            self.world.draw.draw_food(self.world.day.food)
            self.world.play_day(dt)

    def update_world(self, world_name):
        self.scene = world_name
        self.world = self.worlds[world_name]
        self.widgets = self.world.widgets

    def screen_world_settings(self, widgets, pos, event):
        if event:
            for widget in widgets:
                if type(widget) == Button:
                    if event.type == pg.MOUSEBUTTONDOWN and widget.rect.collidepoint(pos):
                        widget.pressed = True
                        if widget.name == "Exit":
                            self.update_world("Game")
                            return None

                elif type(widget) == SliderButton:
                    if widget.scroll(pos, event):
                        return None
                    if event.type == pg.MOUSEBUTTONDOWN and widget.rect.collidepoint(pos):
                        widget.pressed = not widget.pressed
                        if widget.name == "Slider" and not widget.buttons:
                            for guy in self.world.family.guys:
                                widget.add_button(Button(guy.name, guy.name, (1150, 500, 180, 70),
                                                         (200, 200, 200), (170, 170, 170), (255, 255, 255), False,
                                                         False))

                # elif event.type == pg.MOUSEBUTTONUP and widget.rect.collidepoint(pos):
                #     widget.pressed = False

    def update(self, dt, pos=None, event=None):
        if self.scene == "Game":
            self.world.update_ai_speed -= 1
            self.screen_game(dt, self.widgets, pos, event)
            if self.scene == "Game":
                if self.world.update_ai_speed == 0:
                    self.world.update_ai_speed = UPDATE_AI_SPEED
        if self.scene == "World_settings":
            self.world.draw()
            self.screen_world_settings(self.widgets, pos, event)

        self.draw_widgets(self.widgets)
        self.fps.show_fps(self.screen, dt)
        pg.display.update()

    def draw_widgets(self, widgets):
        for widget in widgets:
            font = FONTS[widget.font]
            if isinstance(widget, Button):
                button = widget
                if button.active:
                    if button.pressed:
                        pg.draw.rect(self.screen, button.color_pressed, button.rect)
                    else:
                        pg.draw.rect(self.screen, button.color, button.rect)
                    text_screen = font.render(button.text, True, button.text_color)
                    text_rect = text_screen.get_rect()
                    text_rect.center = button.rect.center
                    self.screen.blit(text_screen, text_rect)
            if isinstance(widget, SliderButton):
                slider = widget
                if slider.active:
                    pg.draw.rect(self.screen, slider.color, slider.rect)
                    text_screen = font.render(slider.text, True, slider.text_color)
                    text_rect = text_screen.get_rect()
                    text_rect.center = slider.rect.center
                    self.screen.blit(text_screen, text_rect)
                    if slider.pressed:
                        pg.draw.rect(self.screen, slider.field_color, slider.field_rect)
                        for button in slider.buttons:
                            button_font = FONTS[button.font]
                            if button.pos[1] >= slider.pos[1] + slider.pos[3] and \
                                    button.pos[1] + button.pos[3] <= slider.field_coords[1] + slider.field_coords[3]:
                                button.active = True
                            else:
                                button.active = False
                            if button.active:
                                if button.pressed:
                                    pg.draw.rect(self.screen, button.color_pressed, button.rect)
                                else:
                                    pg.draw.rect(self.screen, button.color, button.rect)
                                text_screen = button_font.render(button.text, True, button.text_color)
                                text_rect = text_screen.get_rect()
                                text_rect.center = button.rect.center
                                self.screen.blit(text_screen, text_rect)
            if isinstance(widget, TextInput):
                if widget.active:
                    pg.draw.rect(self.screen, widget.color, widget.rect)
                    if widget.pressed:
                        pg.draw.rect(self.screen, widget.color_pressed, widget.rect)
                    text = widget.text
                    text_screen = font.render(text, True, widget.text_color)
                    text_rect = text_screen.get_rect()
                    text_rect.center = widget.rect.center
                    self.screen.blit(text_screen, text_rect)

    def new_world(self):
        np.random.shuffle(FAMILY_NAMES_AND_COLORS)
        families_iterator = iter(FAMILY_NAMES_AND_COLORS)
        families = [Family(params_family=next(families_iterator))
                    for _ in range(FAMILY_NUM)]
        self.worlds["Game"] = World(families=families, screen=self.screen)
        self.update_world("Game")

    def run(self):
        running = True
        previous_time = time.time()
        self.fps = ShowFPS()
        while running:

            dt = (time.time() - previous_time)
            previous_time = time.time()
            for event in pg.event.get():
                if event.type == QUIT:
                    running = False
                if event.type in {pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEWHEEL, pg.KEYDOWN}:
                    self.update(dt, pg.mouse.get_pos(), event)
                    break
            self.update(dt)


if __name__ == '__main__':
    game = Game()
    game.run()
