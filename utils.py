from config import screen_length
import math
import random
from ball import Ball

def ball_collision(ball_pos, radius, rect, velocity):
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

def point_scored(score, balls, b, items):
    if b.x < screen_length / 2:
        score[1] += 1
    else:
        score[0] += 1

    for item in items[:]:
        items.remove(item)

    del balls[1:]
    balls[0].reset()

    return 

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