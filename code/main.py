import os
import sys
import pygame
import random

import config as c
from player import Player
from ball import Ball
from item import Item
from utils import *

def resource_path(relative_path):
    try:
        # Get default pyinstaller path (.exe)
        base_path = sys._MEIPASS 
    except Exception:
        # Get current path (dev)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    # Instantiate objects
    players = []
    balls = []
    items = []

    players.append(Player(list(c.p1_pos), c.p1_color, list(c.p1_size), c.player_speed))
    players.append(Player(list(c.p2_pos), c.p2_color, list(c.p2_size), c.player_speed))
    balls.append(Ball(c.ball_pos, c.ball_vel, c.ball_size, c.ball_color))

    # Load icon
    icon_path = resource_path(os.path.join("assets", "icon.png"))
    icon = pygame.image.load(icon_path)
    
    # Setup screen and clock (for FPS limiting)
    screen = pygame.display.set_mode((c.screen_length, c.screen_height))
    clock = pygame.time.Clock()
    
    # Setup game
    pygame.init()
    pygame.display.set_caption("CoolPongGame")
    pygame.display.set_icon(icon)

    # Game loop
    while True:
        # Collect events, keys and ticks
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Treat events and key presses
        for event in events:
            # Window closing
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN: 
                # Start logic
                if c.game_paused and event.key == pygame.K_SPACE:
                    balls[0].vel = [random.choice([-1, 1]) * c.ball_speed,
                                    random.choice([-1, 1]) * c.ball_speed]
                    c.game_paused = False
                # Reset logic
                elif event.key == pygame.K_r:
                    c.score = [0, 0]
                    reset_game(balls, items)
                # Debug button
                elif event.key == pygame.K_QUOTE:
                    print(f"P1: {players[0].vel} P2: {players[1].vel} Ball: {balls[0].vel}\n"
                          f"Player Speed: {c.player_speed} Ball Speed: {c.ball_speed}\n")
                # Exit game logic
                elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        # Items spawning
        if (not c.game_paused and
            current_time - c.last_item_spawn_time > c.item_interval and
            random.random() < c.item_spawn_chance):
            if len(items) <= c.item_limit:
                items.append(Item(c.item_color))
            c.last_item_spawn_time = current_time

        # Screen and objects rendering
        screen.fill(c.screen_color)
        for p in players:
            p.draw(screen)
        for b in balls:
            b.draw(screen)
        for i in items:
            i.draw(screen)

        # Load UI texts
        show_ui(screen)

        # Player movement
        players[0].move(keys, pygame.K_w, pygame.K_s)
        players[1].move(keys, pygame.K_UP, pygame.K_DOWN)

        # Balls movement
        for b in balls:
            b.move()

        # Ball and item collisions
        ball_collision(balls, players, items)
        item_collision(items, balls, c.item_size)

        # FPS limiting
        clock.tick(60)
        
        # Game update
        pygame.display.update()

if __name__ == "__main__":
    main()
