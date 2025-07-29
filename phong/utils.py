import config as c
import math
import random
from ball import Ball

def player_ball_collision(ball_pos, radius, rect, velocity):
    closest_x = max(rect.left, min(ball_pos[0], rect.right))
    closest_y = max(rect.top, min(ball_pos[1], rect.bottom))

    distance_x = ball_pos[0] - closest_x
    distance_y = ball_pos[1] - closest_y

    if (distance_x**2 + distance_y**2) > (radius**2):
        return False, None

    overlap_x = min(abs(ball_pos[0] - rect.left), abs(ball_pos[0] - rect.right))
    overlap_y = min(abs(ball_pos[1] - rect.top), abs(ball_pos[1] - rect.bottom))

    if overlap_x < overlap_y:
        return True, 'left' if velocity[0] > 0 else 'right'
    else:
        return True, 'top' if velocity[1] > 0 else 'bottom'

def point_scored(balls, b, items):
    if b.x < c.screen_length / 2:
        c.score[1] += 1
    else:
        c.score[0] += 1

    reset_game(balls, items)
    return 

def reset_game(balls, items):
    for item in items[:]:
        items.remove(item)

    del balls[1:]
    balls[0].reset()
    c.game_paused = True

def item_collision(items, balls, item_size):
            for b in balls[:]:
                for item in items[:]:
                    item_center = item.center
                    dist_x = b.x - item_center[0]
                    dist_y = b.y - item_center[1]
                    distance = (dist_x**2 + dist_y**2)**0.5

                    if distance <= b.radius + item_size:
                        item.effect(balls, b)
                        items.remove(item)

def ball_collision(balls, players, items):
     for b in balls:
        ball_pos = b.pos
        ball_vel = b.vel

        p1_rect = players[0].get_rect()
        p2_rect = players[1].get_rect()

        p1_col, p1_side = player_ball_collision(ball_pos, b.radius, p1_rect, ball_vel)
        p2_col, p2_side = player_ball_collision(ball_pos, b.radius, p2_rect, ball_vel)

        x_collision = ball_pos[0] - b.radius <= 0 or ball_pos[0] + b.radius >= c.screen_length
        y_collision = ball_pos[1] - b.radius <= 0 or ball_pos[1] + b.radius >= c.screen_height

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
            point_scored(balls, b, items)
            return
            