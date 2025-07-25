import pygame
import sys
import random
import math

from config import *
from player import Player
from ball import Ball
from item import Item
from utils import *



# GAME DATA
score = [0,0]
game_paused = True

# INSTANTIATE PLAYERS
players = []
players.append(Player(list(p1_pos), p1_color, list(p1_size), player_speed))
players.append(Player(list(p2_pos), p2_color, list(p2_size), player_speed))

# INSTANTIATE BALL
balls = []
balls.append(Ball(ball_pos, ball_vel, ball_size, ball_color))

# ITEMS
items = []  

# GAME
pygame.init()
screen = pygame.display.set_mode((screen_length, screen_height))
screen.fill(screen_color)

while True:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Items
    if not game_paused and current_time - last_item_spawn_time > item_interval and random.random() < item_spawn_chance:
        i_temp = item_color
        items.append(Item(i_temp))
        last_item_spawn_time = current_time

    # Rendering 
    for p in players:
        p.draw(screen)
    for b in balls:
        b.draw(screen)
    for i in items:
        i.draw(screen, item_color)

    font = pygame.font.SysFont(font_type, font_size)
    text_surface = font.render(f"{score[0]} - {score[1]}", True, font_color)
    text_ret = text_surface.get_rect(center = (screen_length/2, 50))
    screen.blit(text_surface, text_ret)


    # Gane start
    if game_paused and keys[pygame.K_SPACE]:
        balls[0].vel = [random.choice([-1, 1]) * ball_speed, random.choice([-1, 1]) * ball_speed]
        game_paused = False

    # Movement 
    players[0].move(keys, pygame.K_w, pygame.K_s)
    players[1].move(keys, pygame.K_UP, pygame.K_DOWN) 

    for b in balls:
        b.move()

    # COLLISION
    for b in balls:
        ball_pos = b.pos
        ball_vel = b.vel

        p1_rect = players[0].get_rect()
        p2_rect = players[1].get_rect()

        p1_col, p1_side = ball_collision(ball_pos, b.radius, p1_rect, ball_vel)
        p2_col, p2_side = ball_collision(ball_pos, b.radius, p2_rect, ball_vel)

        x_collision = ball_pos[0] - b.radius <= 0 or ball_pos[0] + b.radius >= screen_length
        y_collision = ball_pos[1] - b.radius <= 0 or ball_pos[1] + b.radius >= screen_height

        x_player_collision = (p1_col and p1_side in ['left', 'right']) or (p2_col and p2_side in ['left', 'right'])
        y_player_collision = (p1_col and p1_side in ['top', 'bottom']) or (p2_col and p2_side in ['top', 'bottom'])

        if x_player_collision:
            ball_vel[0] *= -1.05
            if p1_col:
                ball_pos[0] = p1_rect.right + b.radius
            elif p2_col:
                ball_pos[0] = p2_rect.left - b.radius
        elif y_player_collision:
            ball_vel[1] *= -1  
            if p1_col:
                if ball_pos[1] < p1_rect.centery:
                    ball_pos[1] = p1_rect.top - b.radius
                else:
                    ball_pos[1] = p1_rect.bottom + b.radius
            elif p2_col:
                if ball_pos[1] < p2_rect.centery:
                    ball_pos[1] = p2_rect.top - b.radius
                else:
                    ball_pos[1] = p2_rect.bottom + b.radius
        elif y_collision:
            ball_vel[1] *= -1
        elif x_collision:
            point_scored(score, balls, b, items)
            game_paused = True

        # Item collision
            item_collision(items, balls, item_size)

    pygame.display.update()