import pygame
import random
import math
from ball import Ball
from config import screen_length, score

class Font:
    def __init__(self, type, size, text, color, location):
        self.type = type
        self.size = size
        self.text = text
        self.color = color
        self.location = location

    def draw(self, screen):
        font = pygame.font.SysFont(self.type, self.size)
        surface = font.render(self.text, True, self.color)
        rect = surface.get_rect(center = self.location)
        screen.blit(surface, rect)