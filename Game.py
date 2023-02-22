import math

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
    def __init__(self, size, color, params):
        self.pos = FIELD.get_pos_border()
        self.color = color
        self.size = size
        self.rect = pg.Rect(100, 100, self.size, self.size)
        self.rect.center = self.pos
        self.params = params
        self.direction = None

    def set_size(self, size):
        self.size = size
        self.rect.update(100, 100, self.size, self.size)
        self.rect.center = self.pos


class Family:
    def __init__(self,
                 params_all=DEFAULT_PARAMS_ALL,
                 params_ch=DEFAULT_PARAMS_CH,
                 population=POPULATION,
                 params_family=next(DEFAULT_FAMILY_PARAMS),
                 ):

        self.population = population
        self.name = params_family[0]
        self.color = params_family[1]
        self.guys = [Guy(color=self.color,
                         size=DEFAULT_PARAMS_ALL["size"],
                         params=Params(params_all=dict(params_all),
                                       params_ch=params_ch)) for _ in range(population)]


class Drawing:
    def __init__(self, screen, families):
        self.screen = screen
        self.families = families

    def draw_stand(self):

        for family in self.families:
            for guy in family.guys:
                rect = guy.rect
                pg.draw.circle(self.screen, guy.color, rect.center, guy.size / 2)

    def draw_food(self, food):
        for food_item in food:
            if food_item.on_field:
                pg.draw.arc(self.screen, "red", food_item.rect, 0, 2 * pi)


class FoodItem:
    def __init__(self):
        self.pos = (random.randint(FIELD.x + 5, FIELD.x + FIELD.x_diff - 5),
                    random.randint(FIELD.y + 5, FIELD.y + FIELD.y_diff - 5))
        self.rect = pg.Rect(self.pos, (5, 5))
        self.on_field = True


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
        self.draw = Drawing(screen, families)
        self.day = None

    def new_day(self):
        self.day = Day(food_amount=self.world_vars['food_amount'],
                       )
        for family in self.families:
            for guy in family.guys:
                guy.params.params_all["satiety"] = 0

    def end_day(self):
        f = 0
        for family in self.families:
            f+=1
            new_family = []
            for num, guy in enumerate(family.guys):
                print(f, guy.params.params_all)
                eaten_food = guy.params.params_all["satiety"]

                if eaten_food == 1:
                    new_family.append(guy)
                elif eaten_food > 1:
                    new_family.append(guy)
                    new_guy = Guy(color=guy.color,
                                  size=guy.params.params_all["size"],
                                  params=Params(params_all=dict(guy.params.params_all), mutation=True))
                    new_guy.set_size(new_guy.params.params_all["size"])
                    new_guy.pos = FIELD.get_pos_border()
                    new_family.append(new_guy)
                guy.pos = FIELD.get_pos_border()
                guy.rect.center = guy.pos
            family.guys = new_family
        self.day = None

    def play_day(self, dt):
        for family in self.families:
            for guy in family.guys:
                if self.day.food_amount <= 0:
                    self.end_day()
                    return None
                speed = guy.params.params_all["speed"]

                closest_food = min(self.day.food,
                                   key=lambda x: abs(guy.pos[0] - x.pos[0]) + abs(guy.pos[1] - x.pos[1]))
                closest_prey = (None, float("+inf"))
                closest_predator = (None, float("+inf"))

                for family_c in self.families:
                    if family_c != family:
                        for guy_c in family_c.guys:
                            dist = (abs(guy.pos[0] - guy_c.pos[0]) + abs(guy_c.pos[1] - guy_c.pos[1]))
                            if guy_c.size > guy.size * DEFAULT_WORLD_VARS["predator_size"] and \
                                    dist < closest_predator[1]:
                                closest_predator = (guy_c, dist)
                            elif guy.size > guy_c.size * DEFAULT_WORLD_VARS["predator_size"] and \
                                    dist < closest_prey[1]:
                                closest_prey = (guy_c, dist)

                if guy.rect.colliderect(closest_food.rect):
                    closest_food.on_field = False
                    for food_num in range(self.day.food_amount):
                        if self.day.food[food_num] is closest_food:
                            self.day.food.pop(food_num)
                            self.day.food_amount -= 1
                            break

                    guy.params.params_all["satiety"] += 1

                elif closest_prey[0] and guy.rect.colliderect(closest_prey[0].rect):
                    for family_dead in self.families:
                        for idx, guy_dead in enumerate(family_dead.guys):
                            if guy_dead is closest_prey[0]:
                                family_dead.guys.pop(idx)
                                print("eaten")
                                break
                        else:
                            continue
                    guy.params.params_all["satiety"] += 1

                else:
                    food_dist = abs(guy.pos[1] - closest_food.pos[1]) + abs(guy.pos[0] - closest_food.pos[0])
                    if food_dist > closest_prey[1]:
                        closest_food = closest_prey[0]
                    food_dist = abs(guy.pos[1] - closest_food.pos[1]) + abs(guy.pos[0] - closest_food.pos[0])
                    destination = closest_food.pos
                    if food_dist > guy.params.params_all["reach"]:
                        if not guy.direction or \
                                (abs(guy.direction[0] - guy.pos[0]) < 1 and (abs(guy.direction[1] - guy.pos[1]) < 1)):
                            guy.direction = (random.randint(FIELD.x, FIELD.x + FIELD.x_diff),
                                             random.randint(FIELD.y, FIELD.y + FIELD.y_diff))
                        destination = guy.direction

                    direction = abs(guy.pos[0] - destination[0]) / \
                                (abs(guy.pos[1] - destination[1]) + abs(guy.pos[0] - destination[0]))

                    new_x = guy.pos[0] - dt * speed * sign(guy.pos[0] - destination[0]) * direction * 100
                    new_y = guy.pos[1] - dt * speed * sign(guy.pos[1] - destination[1]) * (1 - direction) * 100
                    guy.pos = (new_x, new_y)
                    guy.rect.center = guy.pos


class Mouse:
    def __init__(self, screen, button_pos=BUTTONS_POSITIONS):
        self.screen = screen
        self.button_pos = button_pos

    def press(self, press_pos):
        x_press, y_press = press_pos
        for x, y, x_diff, y_diff in self.button_pos:
            if not self.button_pos[(x, y, x_diff, y_diff)][2]:
                continue
            if x < x_press < x_diff + x and y < y_press < y_diff + y:
                pg.draw.rect(self.screen, (200, 200, 200), pg.Rect(x, y, x_diff, y_diff))
                pg.display.flip()
                return self.button_pos[(x, y, x_diff, y_diff)]
        return None


class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        pg.display.set_caption("Evolution")
        self.screen = pg.display.set_mode((1420, 720))
        self.draw_grid()
        self.mouse = Mouse(screen=self.screen)
        self.world = None

    def draw_grid(self):
        self.screen.fill((220, 220, 220))
        pg.draw.rect(self.screen, (150, 150, 150), pg.Rect(FIELD_POSITION), 2)
        pg.draw.rect(self.screen, (150, 150, 150), pg.Rect(1150, 600, 180, 70))
        for pos in BUTTONS_POSITIONS:
            text, color, active = BUTTONS_POSITIONS[pos]
            if active:
                rect = pg.Rect(pos)
                pg.draw.rect(self.screen, color, rect)
                text_screen = FONT.render(text, True, (255, 255, 255))
                text_rect = text_screen.get_rect()
                text_rect.center = rect.center
                self.screen.blit(text_screen, text_rect)

    def draw_main_menu(self):
        self.screen.fill((220, 220, 220))
        pass


    def update(self, dt):
        self.draw_grid()
        if self.world:
            self.world.draw.draw_stand()
            if self.world.day:
                self.world.draw.draw_food(self.world.day.food)
                self.world.play_day(dt)
        pg.display.update()

    def draw(self):
        pass

    def new_world(self, dt):
        self.families = []
        for family_num in range(FAMILY_NUM):
            self.families.append(Family())
        self.world = World(families=self.families, screen=self.screen)

    def check_event(self, button, dt):
        if button[0] == "New World":
            self.new_world(dt)
        if button[0] == "New Day":
            self.world.new_day()

    def run(self):
        running = True
        pause = False
        previous_time = time.time()
        while running:
            dt = (time.time() - previous_time)
            previous_time = time.time()
            for event in pg.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    button = self.mouse.press(press_pos=pg.mouse.get_pos())
                    if button and button[2]:
                        self.check_event(button, dt)

                if event.type == pg.MOUSEBUTTONUP:
                    self.draw_grid()
            self.update(dt)


if __name__ == '__main__':
    game = Game()
    game.run()
