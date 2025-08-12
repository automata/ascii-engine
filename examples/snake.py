#!/usr/bin/env python3
"""
Snake Game Animation Example - ASCII Engine

Creates an animated snake that moves randomly around the screen.
Demonstrates movement, collision detection, and trail effects.
"""

import os
import sys
import time
import math
from random import randint, choice

# Add parent directory to path to import ascii_engine
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ascii_engine.main import Canvas

class Snake:
    def __init__(self, canvas, length=8):
        self.canvas = canvas
        self.length = length
        self.body = []
        self.direction = choice(['up', 'down', 'left', 'right'])
        self.colors = ['green', 'yellow', 'red', 'cyan', 'magenta']
        self.trail_length = 3
        
        # Start snake in center of screen
        start_x = canvas.cols // 2
        start_y = canvas.rows // 2
        
        # Initialize body segments
        for i in range(length):
            self.body.append((start_x - i, start_y))
    
    def get_next_position(self):
        """Calculate next head position based on current direction"""
        head_x, head_y = self.body[0]
        
        if self.direction == 'up':
            return (head_x, head_y - 1)
        elif self.direction == 'down':
            return (head_x, head_y + 1)
        elif self.direction == 'left':
            return (head_x - 1, head_y)
        elif self.direction == 'right':
            return (head_x + 1, head_y)
    
    def change_direction_randomly(self):
        """Randomly change direction (with some probability to continue straight)"""
        # 70% chance to continue, 30% chance to turn
        if randint(1, 10) <= 7:
            return
        
        # Don't reverse direction
        opposite = {
            'up': 'down', 'down': 'up',
            'left': 'right', 'right': 'left'
        }
        
        directions = ['up', 'down', 'left', 'right']
        directions.remove(opposite[self.direction])
        self.direction = choice(directions)
    
    def wrap_position(self, x, y):
        """Wrap position around screen boundaries"""
        wrapped_x = x % self.canvas.cols
        wrapped_y = y % self.canvas.rows
        return (wrapped_x, wrapped_y)
    
    def move(self):
        """Move snake one step forward"""
        # Get next head position
        next_x, next_y = self.get_next_position()
        
        # Wrap around screen edges
        next_x, next_y = self.wrap_position(next_x, next_y)
        
        # Add new head
        self.body.insert(0, (next_x, next_y))
        
        # Remove tail to maintain length
        if len(self.body) > self.length:
            self.body.pop()
        
        # Randomly change direction
        self.change_direction_randomly()
    
    def draw(self):
        """Draw snake with gradient colors and trail effect"""
        for i, (x, y) in enumerate(self.body):
            if i == 0:
                # Head - use special character and bright color
                self.canvas.set_pixel(y, x, '●', 'white')
            elif i < len(self.body) // 2:
                # Front body - bright colors
                color_index = i % len(self.colors)
                self.canvas.set_pixel(y, x, '█', self.colors[color_index])
            else:
                # Back body - dimmer effect
                color_index = i % len(self.colors)
                self.canvas.set_pixel(y, x, '▓', self.colors[color_index])

def create_single_snake(canvas):
    """Create animation with a single snake moving randomly"""
    snake = Snake(canvas, length=12)
    
    frame = 0
    while True:
        canvas.clear()
        
        # Move and draw snake
        snake.move()
        snake.draw()
        
        canvas.draw()
        time.sleep(0.15)
        frame += 1

def create_multiple_snakes(canvas, num_snakes=3):
    """Create animation with multiple snakes moving independently"""
    snakes = []
    colors_per_snake = [
        ['green', 'cyan'],
        ['red', 'yellow'], 
        ['blue', 'magenta'],
        ['white', 'cyan'],
        ['yellow', 'green']
    ]
    
    for i in range(num_snakes):
        snake = Snake(canvas, length=8)
        snake.colors = colors_per_snake[i % len(colors_per_snake)]
        # Start snakes in different positions
        start_x = (canvas.cols // (num_snakes + 1)) * (i + 1)
        start_y = (canvas.rows // (num_snakes + 1)) * (i + 1)
        snake.body = [(start_x + j, start_y) for j in range(snake.length)]
        snakes.append(snake)
    
    frame = 0
    while True:
        canvas.clear()
        
        # Move and draw all snakes
        for snake in snakes:
            snake.move()
            snake.draw()
        
        canvas.draw()
        time.sleep(0.12)
        frame += 1

def create_growing_snake(canvas):
    """Create a snake that grows over time"""
    snake = Snake(canvas, length=5)
    
    frame = 0
    while True:
        canvas.clear()
        
        # Grow snake every 50 frames
        if frame % 50 == 0 and frame > 0:
            snake.length = min(snake.length + 1, 25)  # Max length 25
        
        snake.move()
        snake.draw()
        
        # Add some visual effects
        if frame % 20 == 0:
            # Occasional sparkle effect around head
            head_x, head_y = snake.body[0]
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    spark_x, spark_y = snake.wrap_position(head_x + dx, head_y + dy)
                    canvas.set_pixel(spark_y, spark_x, '*', 'yellow')
        
        canvas.draw()
        time.sleep(0.13)
        frame += 1

def create_snake_maze(canvas):
    """Create snakes that interact with obstacles"""
    snake = Snake(canvas, length=10)
    
    # Create some obstacles
    obstacles = []
    for _ in range(15):
        obs_x = randint(0, canvas.cols - 1)
        obs_y = randint(0, canvas.rows - 1)
        obstacles.append((obs_x, obs_y))
    
    frame = 0
    while True:
        canvas.clear()
        
        # Draw obstacles
        for obs_x, obs_y in obstacles:
            canvas.set_pixel(obs_y, obs_x, '■', 'red')
        
        # Check if snake would hit obstacle
        next_x, next_y = snake.get_next_position()
        next_x, next_y = snake.wrap_position(next_x, next_y)
        
        # If next position is obstacle, turn randomly
        if (next_x, next_y) in obstacles:
            directions = ['up', 'down', 'left', 'right']
            opposite = {
                'up': 'down', 'down': 'up',
                'left': 'right', 'right': 'left'
            }
            directions.remove(opposite[snake.direction])
            snake.direction = choice(directions)
        
        snake.move()
        snake.draw()
        
        canvas.draw()
        time.sleep(0.14)
        frame += 1

def create_rainbow_snake(canvas):
    """Create a snake with rainbow trail effect"""
    snake = Snake(canvas, length=15)
    snake.colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    
    frame = 0
    while True:
        canvas.clear()
        
        snake.move()
        
        # Draw with shifting rainbow colors
        for i, (x, y) in enumerate(snake.body):
            if i == 0:
                # Head
                canvas.set_pixel(y, x, '◆', 'white')
            else:
                # Body with rainbow effect
                color_index = (i + frame // 5) % len(snake.colors)
                char = '█' if i < 5 else ('▓' if i < 10 else '▒')
                canvas.set_pixel(y, x, char, snake.colors[color_index])
        
        canvas.draw()
        time.sleep(0.1)
        frame += 1

def main():
    """Main function to demonstrate different snake animations"""
    
    # Create canvas
    rows = 30
    cols = 100
    canvas = Canvas(rows, cols)
    
    print("ASCII Engine - Snake Game Animation Examples")
    print("===========================================")
    print("1. Single Snake")
    print("2. Multiple Snakes")
    print("3. Growing Snake")
    print("4. Snake Maze")
    print("5. Rainbow Snake")
    
    try:
        choice = input("\nSelect animation (1-5): ").strip()
        
        if choice == '1':
            print("Creating single snake animation... (Ctrl+C to stop)")
            create_single_snake(canvas)
        elif choice == '2':
            print("Creating multiple snakes animation... (Ctrl+C to stop)")
            create_multiple_snakes(canvas, num_snakes=3)
        elif choice == '3':
            print("Creating growing snake animation... (Ctrl+C to stop)")
            create_growing_snake(canvas)
        elif choice == '4':
            print("Creating snake maze animation... (Ctrl+C to stop)")
            create_snake_maze(canvas)
        elif choice == '5':
            print("Creating rainbow snake animation... (Ctrl+C to stop)")
            create_rainbow_snake(canvas)
        else:
            print("Invalid choice. Creating default single snake...")
            create_single_snake(canvas)
            
    except KeyboardInterrupt:
        print("\n\nSnake animation stopped.")
    except EOFError:
        print("No input provided. Creating default single snake...")
        create_single_snake(canvas)

if __name__ == "__main__":
    main()