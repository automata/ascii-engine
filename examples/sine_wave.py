# Animated Sine Wave
import math

frame = 0

def setup():
    pass

def draw():
    global frame
    
    # Draw sine wave
    for x in range(1, canvas.cols - 1):
        y = int(canvas.rows // 2 + 10 * math.sin((x + frame) * 0.1))
        if 0 <= y < canvas.rows:
            canvas.set_pixel(y, x, '●', 'cyan')
    
    # Draw additional waves with phase offset
    for x in range(1, canvas.cols - 1):
        y = int(canvas.rows // 2 + 5 * math.sin((x + frame) * 0.15 + 1))
        if 0 <= y < canvas.rows:
            canvas.set_pixel(y, x, '○', 'magenta')
    
    frame += 1