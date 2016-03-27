# Implementation of classic arcade game Pong
# http://www.codeskulptor.org/#user41_tTvefkLXhd39pqr.py

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
SCORE1_POSITION = [WIDTH / 4, HEIGHT / 2]
SCORE2_POSITION = [(WIDTH / 4) * 3, HEIGHT / 2]
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
LEFT = False
RIGHT = True
BALL_RADIUS = 20
v = 1.1
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = 0
paddle2_pos = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    acc = 4
    ball_vel[0] = 0
    ball_vel[1] = 0
    if direction:
        ball_vel[0] += acc
        ball_vel[1] = random.randrange(1, 2)
    else:
        ball_vel[0] -= acc
        ball_vel[1] = -random.randrange(1, 2)    	

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = 0
    paddle2_pos = 0
    score1 = 0
    score2 = 0
    paddle1_vel = 0
    paddle2_vel = 0	
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, v, score1, score2
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += v * ball_vel[0]
    ball_pos[1] += v * ball_vel[1]
    
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if (ball_pos[1] <= paddle1_pos + PAD_HEIGHT) and (ball_pos[1] >= paddle1_pos):
            ball_vel[0] = -v * ball_vel[0]
        else:
            score2 += 1
            spawn_ball(RIGHT)
            
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -v * ball_vel[1]
    
    if ball_pos[0] >= WIDTH - BALL_RADIUS:
        if (ball_pos[1] <= paddle2_pos + PAD_HEIGHT) and (ball_pos[1] >= paddle2_pos):
            ball_vel[0] = -v * ball_vel[0]
        else:
            score1 += 1
            spawn_ball(LEFT)
        
    if ball_pos[1] > HEIGHT - BALL_RADIUS:
        ball_vel[1] = -v * ball_vel[1]
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 12, "White", 'White')
    # update paddle's vertical position, keep paddle on the screen
    
    if paddle1_pos <= 0 and paddle1_vel < 0:
        pass
    elif paddle1_pos + PAD_HEIGHT >= HEIGHT and paddle1_vel > 0:
        pass
    else:
        paddle1_pos += paddle1_vel
        
        
    if paddle2_pos <= 0 and paddle2_vel < 0:
        pass
    elif paddle2_pos + PAD_HEIGHT >= HEIGHT and paddle2_vel > 0:
        pass
    else:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos], [PAD_WIDTH, paddle1_pos], [PAD_WIDTH, paddle1_pos + PAD_HEIGHT], [0, paddle1_pos + PAD_HEIGHT]], 12,"WHITE", "WHITE")
    
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos], [WIDTH, paddle2_pos], [WIDTH, paddle2_pos + PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT]], 12,"WHITE", "WHITE")
    
    # determine whether paddle and ball collide    
    
    # draw scores
    canvas.draw_text(str(score1), SCORE1_POSITION, 40, 'White')
    canvas.draw_text(str(score2), SCORE2_POSITION, 40, 'White') 
    
def keydown(key):
    global paddle1_vel, paddle2_vel, ball_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle1_vel = 4
    elif key==simplegui.KEY_MAP["up"]:
        paddle1_vel = -4
    
    if key == simplegui.KEY_MAP["s"]:
        paddle2_vel = 4
    elif key == simplegui.KEY_MAP["w"]:
        paddle2_vel = -4
        
    acc = 1
    if key == simplegui.KEY_MAP["left"]:
        spawn_ball(LEFT)
    elif key == simplegui.KEY_MAP["right"]:
        spawn_ball(RIGHT)
        

def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
