import pygame
from config import screen_length, screen_height

class Ball:
    def __init__(self, pos, vel, radius, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.color = color
    
        self.x = self.pos[0]
        self.y = self.pos[1]

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.x = self.pos[0]
        self.y = self.pos[1]

    def reset(self):
        self.pos = [screen_length/2, screen_height/2]
        self.vel = [0,0]
        self.x = self.pos[0]
        self.x = self.pos[0]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)