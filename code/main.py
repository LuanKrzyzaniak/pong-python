import pygame
import sys
import random
import math

import config as c
from player import Player
from ball import Ball
from item import Item
from utils import *


# Instantiate objects
players = []
balls = []
items = []

players.append(Player(list(c.p1_pos), c.p1_color, list(c.p1_size), c.player_speed))
players.append(Player(list(c.p2_pos), c.p2_color, list(c.p2_size), c.player_speed))
balls.append(Ball(c.ball_pos, c.ball_vel, c.ball_size, c.ball_color))

# Game
pygame.init()
screen = pygame.display.set_mode((c.screen_length, c.screen_height))

while True:

    clock = pygame.time.Clock()
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    remaining_time = max(0, c.game_length - current_time)

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
                if c.game_paused and event.key == pygame.K_SPACE:
                    balls[0].vel = [random.choice([-1, 1]) * c.ball_speed, random.choice([-1, 1]) * c.ball_speed]
                    c.game_paused = False
                if event.key == pygame.K_r:
                    c.score = [0,0]
                    reset_game(balls, items)
                if event.key == pygame.K_QUOTE:
                    print(f"P1: {players[0].vel} P2: {players[0].vel} Ball: {balls[0].vel}\nPlayer Speed: {c.player_speed} Ball Speed: {c.ball_speed}\n")

    # Items
    if not c.game_paused and current_time - c.last_item_spawn_time > c.item_interval and random.random() < c.item_spawn_chance:
        i_temp = c.item_color
        if len(items) <= 10:
            items.append(Item(i_temp))
        c.last_item_spawn_time = current_time

    screen.fill(c.screen_color)

    # Rendering 
    for p in players:
        p.draw(screen)
    for b in balls:
        b.draw(screen)
    for i in items:
        i.draw(screen)

    show_ui(screen)
    
    # Movement 
    players[0].move(keys, pygame.K_w, pygame.K_s)
    players[1].move(keys, pygame.K_UP, pygame.K_DOWN) 

    for b in balls:
        b.move()
    
    # Ball collision
    ball_collision(balls, players, items)

    # Item collision
    item_collision(items, balls, c.item_size)

    clock.tick(60)
    pygame.display.update()