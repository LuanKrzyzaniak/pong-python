import pygame
import sys
import random
import math



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

def point_scored(b, items):
    if b.x < screen_length / 2:
        score[1] += 1
    else:
        score[0] += 1

    for item in items[:]:
        items.remove(item)

    del balls[1:]
    balls[0].reset()

    return 



class ball:
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

class player:
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



# GAME DATA
score = [0,0]
game_paused = True

screen_color = (43, 44, 40)
screen_length = 1280
screen_height = 720

items = []  
item_color = (166, 233, 183)
item_size = 30
item_spawn_chance = 0.15
item_interval = 1000 
last_item_spawn_time = 0

font_color = 'white'
font_size = 60
font_type = None


# INSTANTIATE PLAYERS
players = []
player_speed = 1.5

player_color = (10, 147, 150)
player_pos = (100, screen_height/3)
player_size = (50, screen_height/4)
players.append(player(list(player_pos), player_color, list(player_size), player_speed))

player_color = (202,103,2)
player_pos = (screen_length-100, screen_height/3)
player_size = (50, screen_height/4)
players.append(player(list(player_pos), player_color, list(player_size), player_speed))

# INSTANTIATE BALL
balls = []
ball_speed = 1

ball_color = (233,216,166)
ball_size = 15
ball_vel = [0,0]
ball_pos = [screen_length/2, screen_height/2]
balls.append(ball(ball_pos, ball_vel, ball_size, ball_color))



# GAME
pygame.init()
screen = pygame.display.set_mode((screen_length, screen_height))

while True:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Items
    if current_time - last_item_spawn_time > item_interval and not game_paused:
        left_bound = players[0].x + players[0].size_x + item_size
        right_bound = players[1].x - item_size

        if random.random() < item_spawn_chance:
            item_x = random.randint(left_bound, right_bound)
            item_y = random.randint(item_size, screen_height - item_size)
            items.append(pygame.Rect(item_x - item_size, item_y - item_size, item_size*2, item_size*2))
        last_item_spawn_time = current_time



    # Rendering 
    screen.fill(screen_color)

    for p in players:
        p.draw(screen)
    for b in balls:
        b.draw(screen)

    font = pygame.font.SysFont(font_type, font_size)
    text_surface = font.render(f"{score[0]} - {score[1]}", True, font_color)
    text_ret = text_surface.get_rect(center = (screen_length/2, 50))
    screen.blit(text_surface, text_ret)

    for item in items:
        pygame.draw.ellipse(screen, item_color, item)

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
            point_scored(b, items)
            game_paused = True

        # Item collision

        for b in balls[:]:
            for item in items[:]:
                item_center = item.center
                dist_x = b.x - item_center[0]
                dist_y = b.y - item_center[1]
                distance = (dist_x**2 + dist_y**2)**0.5

                if distance <= b.radius + item_size:
                    items.remove(item)

                    speed = math.hypot(b.vel[0], b.vel[1])
                    current_angle = math.atan2(b.vel[1], b.vel[0])

                    angle_offset = random.uniform(-0.3, 0.3)  # ~ +/- 17 degrees

                    new_angle = current_angle + angle_offset

                    new_vel = [speed * math.cos(new_angle), speed * math.sin(new_angle)]

                    b_item = ball(b.pos.copy(), new_vel, b.radius, b.color)
                    balls.append(b_item)

    pygame.display.update()