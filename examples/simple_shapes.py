# Simple Shapes Demo
from random import randint

def setup():
    pass

def draw():
    # Draw some random shapes each frame
    
    # Random circles
    for i in range(3):
        x = randint(10, canvas.cols - 10)
        y = randint(5, canvas.rows - 5)
        radius = randint(2, 6)
        colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']
        color = colors[randint(0, len(colors) - 1)]
        canvas.circle(x, y, radius, filled=True, color=color)
    
    # Random rectangles
    for i in range(2):
        x = randint(5, canvas.cols - 20)
        y = randint(3, canvas.rows - 10)
        width = randint(8, 15)
        height = randint(4, 8)
        colors = ['white', 'yellow', 'cyan']
        color = colors[randint(0, len(colors) - 1)]
        canvas.rect(x, y, width, height, filled=False, color=color)
    
    # Random lines
    for i in range(5):
        x1 = randint(0, canvas.cols - 1)
        y1 = randint(0, canvas.rows - 1)
        x2 = randint(0, canvas.cols - 1)
        y2 = randint(0, canvas.rows - 1)
        colors = ['white', 'red', 'green', 'blue']
        color = colors[randint(0, len(colors) - 1)]
        canvas.line(x1, y1, x2, y2, color=color)