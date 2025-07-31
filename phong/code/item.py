import pygame
import random
import math
from ball import Ball
import config as c

class Item:
    def __init__(self, color):
        self.color = color
        x = random.randint(c.left_bound, c.right_bound)
        y = random.randint(c.item_size+ 200, c.screen_height - c.item_size - 200)
        self.rect = pygame.Rect(x - c.item_size, y - c.item_size, c.item_size*2, c.item_size*2)
        self.center = (x, y)
 

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
        font = pygame.font.SysFont(c.font_type, c.font_size-10)
        text_surface = font.render("x2", True, c.item_font_color)
        text_ret = text_surface.get_rect(center = (self.center[0], self.center[1]))
        screen.blit(text_surface, text_ret)

    def effect(self, balls, b):
        if b.color == (233,216,166):
            speed = math.hypot(b.vel[0], b.vel[1])
            current_angle = math.atan2(b.vel[1], b.vel[0])

            angle_offset = random.uniform(-0.3, 0.3)

            new_angle = current_angle + angle_offset

            new_vel = [speed * math.cos(new_angle), speed * math.sin(new_angle)]

            b_item = Ball(b.pos.copy(), new_vel, b.radius, b.color)
            balls.append(b_item)
