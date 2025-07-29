import pygame
import random
import math
from ball import Ball
from config import left_bound, right_bound, item_size, screen_height

class Item:
    def __init__(self, color):
        self.color = color
        x = random.randint(left_bound, right_bound)
        y = random.randint(item_size, screen_height - item_size)
        self.rect = pygame.Rect(x - item_size, y - item_size, item_size*2, item_size*2)
        self.center = (x, y)
 

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def effect(self, balls, b):
        if b.color == (233,216,166):
            speed = math.hypot(b.vel[0], b.vel[1])
            current_angle = math.atan2(b.vel[1], b.vel[0])

            angle_offset = random.uniform(-0.3, 0.3)  # ~ +/- 17 degrees

            new_angle = current_angle + angle_offset

            new_vel = [speed * math.cos(new_angle), speed * math.sin(new_angle)]

            b_item = Ball(b.pos.copy(), new_vel, b.radius, b.color)
            balls.append(b_item)
