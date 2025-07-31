import pygame
from config import screen_height

class Player:
    def __init__(self, pos, color, size, vel):
        self.pos = pos
        self.color = color
        self.size = size
        self.vel = vel

        self.x = self.pos[0]
        self.y = self.pos[1]
        self.size_x = self.size[0]
        self.size_y = self.size[1]

    def move(self, keys, up_key, down_key):
        if keys[up_key] and self.pos[1] > 10:
            self.pos[1] -= self.vel
        if keys[down_key] and self.pos[1] < screen_height - self.size[1] - 10:
            self.pos[1] += self.vel
        self.y = self.pos[1]


    def draw(self, screen):
        rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        pygame.draw.rect(screen, self.color, rect)

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])