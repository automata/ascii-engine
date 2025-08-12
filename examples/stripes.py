#!/usr/bin/env python3
"""
Vertical Stripes Example - ASCII Engine

Creates animated colored vertical stripes using the ASCII engine.
Demonstrates basic rect() usage and color cycling.
"""

import os
import sys
import time
from random import randint

# Add parent directory to path to import ascii_engine
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ascii_engine.main import Canvas

def create_stripes(canvas, stripe_width=8, animate=True):
    """Create vertical stripes pattern"""
    
    # Define color sequence for stripes
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    
    # Static stripes
    if not animate:
        x = 0
        color_index = 0
        
        while x < canvas.cols:
            color = colors[color_index % len(colors)]
            
            # Draw vertical stripe
            canvas.rect(x, 0, stripe_width, canvas.rows, filled=True, color=color)
            
            x += stripe_width
            color_index += 1
    
    # Animated stripes with shifting colors
    else:
        frame = 0
        while True:
            canvas.clear()
            
            x = 0
            while x < canvas.cols:
                # Shift colors based on frame for animation effect
                color_index = (x // stripe_width + frame) % len(colors)
                color = colors[color_index]
                
                # Draw vertical stripe
                canvas.rect(x, 0, stripe_width, canvas.rows, filled=True, color=color)
                
                x += stripe_width
            
            canvas.draw()
            time.sleep(0.3)
            frame += 1

def create_rainbow_stripes(canvas, stripe_width=4):
    """Create animated rainbow stripes with gradient-like effect"""
    
    # Extended color palette for rainbow effect
    rainbow_colors = [
        'red', 'red', 'yellow', 'yellow', 
        'green', 'green', 'cyan', 'cyan',
        'blue', 'blue', 'magenta', 'magenta'
    ]
    
    frame = 0
    while True:
        canvas.clear()
        
        x = 0
        while x < canvas.cols:
            # Create flowing rainbow effect
            color_index = (x // stripe_width + frame) % len(rainbow_colors)
            color = rainbow_colors[color_index]
            
            # Draw vertical stripe
            canvas.rect(x, 0, stripe_width, canvas.rows, filled=True, color=color)
            
            x += stripe_width
        
        canvas.draw()
        time.sleep(0.2)
        frame += 1

def create_random_stripes(canvas, min_width=3, max_width=12):
    """Create stripes with random widths and colors"""
    
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'white']
    
    frame = 0
    while True:
        canvas.clear()
        
        x = 0
        while x < canvas.cols:
            # Random stripe width and color
            stripe_width = randint(min_width, max_width)
            color = colors[randint(0, len(colors) - 1)]
            
            # Draw vertical stripe
            canvas.rect(x, 0, stripe_width, canvas.rows, filled=True, color=color)
            
            x += stripe_width
        
        canvas.draw()
        time.sleep(0.5)
        frame += 1

def main():
    """Main function to demonstrate different stripe patterns"""
    
    # Create canvas
    rows = 30
    cols = 120
    canvas = Canvas(rows, cols)
    
    print("ASCII Engine - Vertical Stripes Examples")
    print("========================================")
    print("1. Animated Color Stripes")
    print("2. Rainbow Stripes")
    print("3. Random Width Stripes")
    print("4. Static Stripes")
    
    try:
        choice = input("\nSelect pattern (1-4): ").strip()
        
        if choice == '1':
            print("Creating animated color stripes... (Ctrl+C to stop)")
            create_stripes(canvas, stripe_width=6, animate=True)
        elif choice == '2':
            print("Creating rainbow stripes... (Ctrl+C to stop)")
            create_rainbow_stripes(canvas, stripe_width=4)
        elif choice == '3':
            print("Creating random width stripes... (Ctrl+C to stop)")
            create_random_stripes(canvas, min_width=2, max_width=15)
        elif choice == '4':
            print("Creating static stripes...")
            create_stripes(canvas, stripe_width=8, animate=False)
            canvas.draw()
        else:
            print("Invalid choice. Creating default animated stripes...")
            create_stripes(canvas, stripe_width=6, animate=True)
            
    except KeyboardInterrupt:
        print("\n\nStripes demo stopped.")
    except EOFError:
        print("No input provided. Creating default animated stripes...")
        create_stripes(canvas, stripe_width=6, animate=True)

if __name__ == "__main__":
    main()