# Animated Spiral
import math

angle = 0

def setup():
    pass

def draw():
    global angle
    
    center_x = canvas.cols // 2
    center_y = canvas.rows // 2
    
    # Draw expanding spiral
    for i in range(100):
        spiral_angle = angle + i * 0.2
        radius = i * 0.3
        
        x = int(center_x + radius * math.cos(spiral_angle))
        y = int(center_y + radius * math.sin(spiral_angle))
        
        if 0 <= x < canvas.cols and 0 <= y < canvas.rows:
            colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
            color = colors[i % len(colors)]
            canvas.set_pixel(y, x, '●', color)
    
    angle += 0.05