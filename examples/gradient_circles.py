#!/usr/bin/env python3
"""
Gradient Circles Example - ASCII Engine

Creates radial gradient patterns using concentric circles emanating from the center.
Demonstrates circle drawing with color gradients and animation effects.
"""

import os
import sys
import time
import math
from random import randint, choice

# Add parent directory to path to import ascii_engine
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ascii_engine.main import Canvas

def create_radial_gradient(canvas, center_x=None, center_y=None, max_radius=None, animate=False):
    """Create concentric circles with color gradient from center outward"""
    
    # Use canvas center if not specified
    if center_x is None:
        center_x = canvas.cols // 2
    if center_y is None:
        center_y = canvas.rows // 2
    
    # Calculate maximum radius to cover entire screen (allow overflow)
    if max_radius is None:
        max_radius = max(canvas.cols, canvas.rows)
    
    # Color gradient from center outward
    colors = ['white', 'yellow', 'red', 'magenta', 'blue', 'cyan', 'green']
    
    if not animate:
        # Static gradient
        for radius in range(max_radius, 0, -1):
            color_index = (max_radius - radius) % len(colors)
            color = colors[color_index]
            
            # Alternate between filled and outline for depth effect
            filled = (radius % 2 == 0)
            canvas.circle(center_x, center_y, radius, filled=filled, color=color)
    else:
        # Animated gradient with expanding rings
        frame = 0
        while True:
            canvas.clear()
            
            for radius in range(max_radius, 0, -1):
                # Shift colors based on frame for ripple effect
                color_index = (max_radius - radius + frame) % len(colors)
                color = colors[color_index]
                
                # Create pulsing effect
                pulse_radius = radius + int(2 * math.sin(frame * 0.2 + radius * 0.3))
                if pulse_radius > 0:
                    filled = (radius % 3 == 0)  # Less dense filling for animation
                    canvas.circle(center_x, center_y, pulse_radius, filled=filled, color=color)
            
            canvas.draw()
            time.sleep(0.15)
            frame += 1

def create_expanding_circles(canvas, center_x=None, center_y=None):
    """Create expanding circles animation from center"""
    
    if center_x is None:
        center_x = canvas.cols // 2
    if center_y is None:
        center_y = canvas.rows // 2
    
    max_radius = max(canvas.cols, canvas.rows)
    colors = ['white', 'yellow', 'red', 'magenta', 'blue', 'cyan', 'green']
    
    frame = 0
    while True:
        canvas.clear()
        
        # Create multiple expanding rings
        for ring in range(8):
            radius = (frame + ring * 10) % (max_radius + 30)
            if radius > 0:
                color = colors[ring % len(colors)]
                canvas.circle(center_x, center_y, radius, filled=False, color=color)
        
        canvas.draw()
        time.sleep(0.1)
        frame += 1

def create_spiral_gradient(canvas, center_x=None, center_y=None):
    """Create spiral gradient using circles of varying sizes and positions"""
    
    if center_x is None:
        center_x = canvas.cols // 2
    if center_y is None:
        center_y = canvas.rows // 2
    
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'white']
    
    frame = 0
    while True:
        canvas.clear()
        
        # Create spiraling circles covering full screen
        for i in range(40):
            angle = (frame * 0.1 + i * 0.6) % (2 * math.pi)
            distance = i * 3
            
            # Calculate spiral position
            x = center_x + int(distance * math.cos(angle))
            y = center_y + int(distance * 0.5 * math.sin(angle))  # Compress vertically for ASCII
            
            radius = max(1, 8 - i // 6)
            color = colors[i % len(colors)]
            
            # Fade effect by alternating filled/outline
            filled = (i + frame // 5) % 3 == 0
            canvas.circle(x, y, radius, filled=filled, color=color)
        
        canvas.draw()
        time.sleep(0.12)
        frame += 1

def create_multi_center_gradient(canvas):
    """Create gradient patterns from multiple centers"""
    
    # Define multiple centers
    centers = [
        (canvas.cols // 4, canvas.rows // 3),
        (3 * canvas.cols // 4, canvas.rows // 3),
        (canvas.cols // 2, 2 * canvas.rows // 3)
    ]
    
    colors = ['red', 'green', 'blue']
    
    frame = 0
    while True:
        canvas.clear()
        
        for i, (cx, cy) in enumerate(centers):
            color_set = ['white', colors[i], 'yellow', colors[i]]
            max_radius = max(canvas.cols, canvas.rows) // 2
            
            for radius in range(max_radius, 0, -3):
                # Phase offset for each center
                phase = frame * 0.3 + i * 2
                actual_radius = radius + int(3 * math.sin(phase + radius * 0.2))
                
                if actual_radius > 0:
                    color_index = (radius // 3) % len(color_set)
                    color = color_set[color_index]
                    filled = (radius % 4 == 0)
                    canvas.circle(cx, cy, actual_radius, filled=filled, color=color)
        
        canvas.draw()
        time.sleep(0.16)
        frame += 1

def create_breathing_gradient(canvas, center_x=None, center_y=None):
    """Create a breathing/pulsing gradient effect"""
    
    if center_x is None:
        center_x = canvas.cols // 2
    if center_y is None:
        center_y = canvas.rows // 2
    
    colors = ['white', 'yellow', 'red', 'magenta', 'blue', 'cyan']
    base_radius = max(canvas.cols, canvas.rows) // 2
    
    frame = 0
    while True:
        canvas.clear()
        
        # Breathing effect - expand and contract
        breath_factor = 0.3 + 0.7 * (math.sin(frame * 0.15) + 1) / 2
        
        for i in range(len(colors) * 3):  # More rings for full coverage
            radius = int((base_radius - i * 5) * breath_factor)
            if radius > 0:
                color = colors[i % len(colors)]  # Use modulo to cycle through colors
                # Alternate filling based on breath cycle
                filled = (frame // 10 + i) % 2 == 0
                canvas.circle(center_x, center_y, radius, filled=filled, color=color)
        
        canvas.draw()
        time.sleep(0.08)
        frame += 1

def main():
    """Main function to demonstrate different gradient circle patterns"""
    
    # Create canvas
    rows = 35
    cols = 120
    canvas = Canvas(rows, cols)
    
    print("ASCII Engine - Gradient Circles Examples")
    print("========================================")
    print("1. Static Radial Gradient")
    print("2. Animated Radial Gradient")
    print("3. Expanding Circles")
    print("4. Spiral Gradient")
    print("5. Multi-Center Gradient")
    print("6. Breathing Gradient")
    
    try:
        choice = input("\nSelect pattern (1-6): ").strip()
        
        if choice == '1':
            print("Creating static radial gradient...")
            create_radial_gradient(canvas, animate=False)
            canvas.draw()
        elif choice == '2':
            print("Creating animated radial gradient... (Ctrl+C to stop)")
            create_radial_gradient(canvas, animate=True)
        elif choice == '3':
            print("Creating expanding circles... (Ctrl+C to stop)")
            create_expanding_circles(canvas)
        elif choice == '4':
            print("Creating spiral gradient... (Ctrl+C to stop)")
            create_spiral_gradient(canvas)
        elif choice == '5':
            print("Creating multi-center gradient... (Ctrl+C to stop)")
            create_multi_center_gradient(canvas)
        elif choice == '6':
            print("Creating breathing gradient... (Ctrl+C to stop)")
            create_breathing_gradient(canvas)
        else:
            print("Invalid choice. Creating default animated radial gradient...")
            create_radial_gradient(canvas, animate=True)
            
    except KeyboardInterrupt:
        print("\n\nGradient circles demo stopped.")
    except EOFError:
        print("No input provided. Creating default animated radial gradient...")
        create_radial_gradient(canvas, animate=True)

if __name__ == "__main__":
    main()