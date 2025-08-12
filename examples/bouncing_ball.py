# Bouncing Ball Example
import math

# Global variables
ball_x = 25
ball_y = 15
vel_x = 2
vel_y = 1
radius = 3

def setup():
    global ball_x, ball_y, vel_x, vel_y
    ball_x = canvas.cols // 2
    ball_y = canvas.rows // 2

def draw():
    global ball_x, ball_y, vel_x, vel_y
    
    # Update position
    ball_x += vel_x
    ball_y += vel_y
    
    # Bounce off walls
    if ball_x <= radius or ball_x >= canvas.cols - radius:
        vel_x *= -1
    if ball_y <= radius or ball_y >= canvas.rows - radius:
        vel_y *= -1
        
    # Keep ball in bounds
    ball_x = max(radius, min(canvas.cols - radius, ball_x))
    ball_y = max(radius, min(canvas.rows - radius, ball_y))
    
    # Draw ball
    canvas.circle(ball_x, ball_y, radius, filled=True, color='yellow')