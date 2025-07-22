import pygame
import sys
import random

def ball_collision(ball_pos, radius, rect, velocity):
    # Closest point from ball to rect
    closest_x = max(rect.left, min(ball_pos[0], rect.right))
    closest_y = max(rect.top, min(ball_pos[1], rect.bottom))

    # Distance to that point
    distance_x = ball_pos[0] - closest_x
    distance_y = ball_pos[1] - closest_y

    if (distance_x**2 + distance_y**2) > (radius**2):
        return False, None

    # Determine collision side more robustly
    overlap_x = min(abs(ball_pos[0] - rect.left), abs(ball_pos[0] - rect.right))
    overlap_y = min(abs(ball_pos[1] - rect.top), abs(ball_pos[1] - rect.bottom))

    if overlap_x < overlap_y:
        return True, 'left' if velocity[0] > 0 else 'right'
    else:
        return True, 'top' if velocity[1] > 0 else 'bottom'


def point_scored(ball_pos, items):
    if ball_pos[0] < screen_length / 2:
        score[1] += 1
    else:
        score[0] += 1
    ball_pos[0] = screen_length / 2
    ball_pos[1] = screen_height / 2

    for item in items[:]:
        items.remove(item)

    return [0,0]

# GAME DATA
player_speed = 1.5
ball_speed = 1
score = [0,0]
game_paused = True
last_item_spawn_time = 0
item_interval = 1000 
items = []  

# SCREEN DATA
screen_length = 1280
screen_height = 720
screen_color = (43, 44, 40)

# OBJECTS DATA
p1_data = [100, screen_height/3, 50, screen_height/4]
p1_color = (10, 147, 150)

p2_data = [screen_length-100, screen_height/3, 50, screen_height/4]
p2_color = (202,103,2)

ball_pos = [screen_length/2, screen_height/2]
ball_size = 15
ball_color = (233,216,166)
ball_vel = [0,0]

item_color = (166, 233, 183)
item_size = 30
item_spawn_chance = 0.1

# OVERLAY
font_color = 'white'
font_size = 60
font_type = None

# GAME
pygame.init()
screen = pygame.display.set_mode((screen_length, screen_height))

while True:
    # EVENTS & KEYS
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # RENDERING
    screen.fill(screen_color)

    p1 = pygame.draw.rect(screen, p1_color, p1_data)
    p2 = pygame.draw.rect(screen, p2_color, p2_data)
    ball = pygame.draw.circle(screen, ball_color, ball_pos, ball_size)

    font = pygame.font.SysFont(font_type, font_size)
    text_surface = font.render(f"{score[0]} - {score[1]}", True, font_color)
    text_ret = text_surface.get_rect(center = (screen_length/2, 50))
    screen.blit(text_surface, text_ret)

    # ITEMS
    current_time = pygame.time.get_ticks()

    if current_time - last_item_spawn_time > item_interval:
        if random.random() < item_spawn_chance:
            item_x = random.randint(item_size, screen_length - item_size)
            item_y = random.randint(item_size, screen_height - item_size)
            items.append(pygame.Rect(item_x - item_size, item_y - item_size, item_size*2, item_size*2))
        last_item_spawn_time = current_time

    # Draw all items
    #for item in items:
    #    pygame.draw.ellipse(screen, item_color, item)

    # GAME START
    if game_paused and keys[pygame.K_SPACE]:
        ball_vel = [random.choice([-1, 1]) * ball_speed, random.choice([-1, 1]) * ball_speed]
        game_paused = False

    # PLAYER MOVEMENT
    if keys[pygame.K_w] and p1_data[1] > 10:
        p1_data[1] -= player_speed
    if keys[pygame.K_s] and p1_data[1] <  screen_height - p1_data[3] - 10:
        p1_data[1] += player_speed
    if keys[pygame.K_UP] and p2_data[1] > 10:
        p2_data[1] -= player_speed
    if keys[pygame.K_DOWN] and p2_data[1] <  screen_height - p2_data[3] - 10:
        p2_data[1] += player_speed

    # BALL MOVEMENT
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # COLLISION
    p1_col, p1_side = ball_collision(ball_pos, ball_size, p1, ball_vel)
    p2_col, p2_side = ball_collision(ball_pos, ball_size, p2, ball_vel)
    
    x_collision = ball_pos[0] - ball_size <= 0 or ball_pos[0] + ball_size >= screen_length
    y_collision = ball_pos[1] - ball_size <= 0 or ball_pos[1] + ball_size >= screen_height
    
    x_player_collision = p1_col and p1_side in ['left', 'right'] or p2_col and p2_side in ['left', 'right']
    y_player_collision = p1_col and p1_side in ['top', 'bottom'] or p2_col and p2_side in ['top', 'bottom']

  
    if x_player_collision:
        ball_vel[0] *= -1.05
        if p1_col:
            ball_pos[0] = p1.right + ball_size
        elif p2_col:
            ball_pos[0] = p2.left - ball_size
    elif y_player_collision:
        ball_vel[1] *= -1  
        if p1_col:
            if ball_pos[1] < p1.centery:
                ball_pos[1] = p1.top - ball_size
            else:
                ball_pos[1] = p1.bottom + ball_size
        elif p2_col:
            if ball_pos[1] < p2.centery:
                ball_pos[1] = p2.top - ball_size
            else:
                ball_pos[1] = p2.bottom + ball_size
    elif y_collision:
        ball_vel[1] *= -1
    elif x_collision:
        ball_vel = point_scored(ball_pos, items)
        game_paused = True

    for item in items[:]:
        item_center = item.center
        dist_x = ball_pos[0] - item_center[0]
        dist_y = ball_pos[1] - item_center[1]
        distance = (dist_x**2 + dist_y**2)**0.5

        if distance <= ball_size + item_size:
            items.remove(item)
            ball_speed += 0.2


    pygame.display.update()