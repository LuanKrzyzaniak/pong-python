# Game data
score = [0,0]
game_paused = True
game_length = 2 * 1000

# Screen
screen_color = (43, 44, 40)
screen_length = 1280
screen_height = 720

# Font
font_color = 'white'
font_size = 60
font_type = None

score_location = (screen_length/2, 50)
timer_location = (screen_length/2, 100)

# Ball
ball_color = (233,216,166)
ball_size = 15
ball_vel = [0,0]
ball_pos = [screen_length/2, screen_height/2]
ball_speed = 1

# Players
player_speed = 1.5

p1_color = (10, 147, 150)
p1_pos = (100, screen_height/3)
p1_size = (50, screen_height/4)

p2_color = (202,103,2)
p2_pos = (screen_length-100, screen_height/3)
p2_size = (50, screen_height/4)

# Items
item_color = (166, 233, 183)
item_size = 30
item_spawn_chance = 0.15
item_interval = 1000 
last_item_spawn_time = 0
left_bound = p1_pos[0] + p1_size[0] + item_size
right_bound = p2_pos[0] - p2_size[0] - item_size